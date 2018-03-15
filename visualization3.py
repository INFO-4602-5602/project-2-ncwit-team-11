import numpy as np
import pandas as pd
from bokeh.io import curdoc, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Legend, HoverTool
from bokeh.models.widgets import Paragraph, Div, RadioButtonGroup
from bokeh.layouts import layout, column, row

# Load data
dat = pd.read_csv("NCWIT_DataV2.csv", low_memory=False)
d = dat['Record#']
null_idx = d.isnull()
val_idx = np.invert(null_idx.as_matrix())
dat = dat.iloc[val_idx]

rows_tot = dat.shape[0]

# Get sorted list of school years
yrs = sorted(dat["School Year"].unique())

# Make paragraph section for discussion
div_title = Div(text="""Number of Female Students per Institution by Degrees Offered""", style={"font-size": "30px"}, width=1000, height=60)

# Make plot
plt = figure(plot_width=1000, plot_height=600, x_range=yrs, tools="pan,wheel_zoom,box_zoom,reset")
#plt_Grd = figure(plot_width=800, plot_height=400, x_range=yrs, tools="pan,wheel_zoom,box_zoom,reset")
#lt_Lft = figure(plot_width=800, plot_height=400, x_range=yrs, tools="pan,wheel_zoom,box_zoom,reset")

# Make paragraph section for discussion
div_RadGroup = Div(text="""Select Data Source:    """,
	               style={"font-size": "18px", "text-align": "right"}, width=300, height=40)

# Make drop-down menu
radio_button_group = RadioButtonGroup(labels=["New Enrollments", "Graduated", "Left Institution"], 
	                                  active=0, width=600)

# Make paragraph section for discussion
p = Paragraph(text="""Discussion here of this visualization....""", style={"font-size": "18px"}, width=1000, height=400)

# Initializae data sources
source_B = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))
source_BM = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))
source_BMP = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))

# Function that parses the data and updates the data sources
def gather_data(data_flag):

	# Remove data that doesn't have "What degrees does your institution offer?" data
	d = dat["What degrees does your institution offer?"]
	null_idx = d.isnull()
	val_idx = np.invert(null_idx.as_matrix())
	dat_sch_type = dat.iloc[val_idx]

	# Get types of degrees offered
	schl_type = sorted(dat_sch_type["What degrees does your institution offer?"].unique())

	for item in schl_type:
		schl_type_ind = schl_type.index(item)
		
		tf_type = (dat_sch_type["What degrees does your institution offer?"] == item)
		
		x_dat, y_dat, num_insts = [], [], []
		for yr in yrs:
			tf_yr = (dat_sch_type["School Year"] == yr)

			tf_both = [a and b for a, b in zip(tf_type, tf_yr)]

			# Get appropriate data column based on drop-down menu
			if (data_flag == 0):
				col_header = "Enroll, Female: New Enrollments (Enrl F)"
			elif (data_flag == 1):
				col_header = "Totals, Female: Graduated (Tot. F)"
			elif (data_flag == 2):
				col_header = "Totals, Female: Left Institution (not graduated) (Tot. F)"

			# Check that not all of the data is NaN
			any_data = (not all(np.isnan(dat_sch_type[col_header][tf_both])))

			# Get number of institutions with data this year
			### NOTE: this has a bug, it should not include institutions with NaN
			N_schls = len(dat_sch_type["Institution"][tf_both].unique())
			num_insts.append(N_schls)

			# Append data
			x_dat.append(yr)
			if (N_schls > 0) and (any_data):
				y_dat.append(np.nansum(dat_sch_type[col_header][tf_both])/N_schls)
			else:
				y_dat.append(np.nan)

		if (item == "Bachelor's degrees only"):
			source_B.data = dict(x=x_dat, y=y_dat, num_insts=num_insts)
		elif (item == "Bachelor's and master's degrees only"):
			source_BM.data = dict(x=x_dat, y=y_dat, num_insts=num_insts)
		elif (item == "Bachelor's, master's, and Ph.D. degrees"):
			source_BMP.data = dict(x=x_dat, y=y_dat, num_insts=num_insts)

# Initalize data sources
gather_data(0)

# Make line plots with circles at datapoints
l_B   = plt.line(x="x", y="y", color="blue", line_width=2, muted_alpha=0.2, source=source_B)
c_B   = plt.circle(x="x", y="y", color="blue", radius=0.1, muted_alpha=0.2, source=source_B)
l_BM  = plt.line(x="x", y="y", color="red", line_width=2, muted_alpha=0.2, source=source_BM)
c_BM  = plt.circle(x="x", y="y", color="red", radius=0.1, muted_alpha=0.2, source=source_BM)
l_BMP = plt.line(x="x", y="y", color="green", line_width=2, muted_alpha=0.2,source=source_BMP)
c_BMP = plt.circle(x="x", y="y", color="green", radius=0.1, muted_alpha=0.2, source=source_BMP)

# Make and format legend
legend = Legend(items=[
    ("Bachelor's, Master's, and Ph.D. degrees", [l_BMP, c_BMP]),
    ("Bachelor's and Master's degrees only", [l_BM, c_BM]),
    ("Bachelor's degrees only", [l_B, c_B])],
    location=(0, 5))

plt.add_layout(legend, 'above')
plt.legend.border_line_width = 1
plt.legend.border_line_color = "black"
plt.legend.orientation = "horizontal"
plt.legend.label_text_font_size = "18px"
plt.legend.click_policy="mute"

# Make and format tooltip
hover = HoverTool(tooltips=[
			("# of Institutions", '@num_insts')
        ])
plt.add_tools(hover)

# Other plot formatting
plt.xaxis.major_label_orientation = np.pi/4
plt.xaxis.axis_label_text_font_size = "18px"
plt.xaxis.major_label_text_font_size = "18px"

plt.yaxis.axis_label = "Number of Female Students / Institution"
plt.yaxis.axis_label_text_font_size = "18px"
plt.yaxis.major_label_text_font_size = "18px"

plt.toolbar.logo = None

#select.on_change('value', update_plot)
radio_button_group.on_click(gather_data)
layout = column(div_title, row(div_RadGroup, radio_button_group), plt, p)
curdoc().add_root(layout)

curdoc().title = "Visualization 3"