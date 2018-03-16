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
div_title = Div(text="""Number of Female Students per Institution by Degrees Offered""",
                style={"font-size": "30px", "text-align": "center"}, width=1000, height=60)

# Make plot
plt = figure(plot_width=1000, plot_height=600, x_range=yrs, tools="pan,wheel_zoom,box_zoom,reset")

# Make paragraph section for discussion
div_RadGroup = Div(text="""Select Data Source: &nbsp""",
	               style={"font-size": "18px", "text-align": "right"}, width=400, height=40)

# Make drop-down menu
radio_button_group = RadioButtonGroup(labels=["New Enrollments", "Graduated", "Left Institution"],
	                                  active=0, width=600)

# Make paragraph sections for discussion
p1 = Paragraph(text=
	"""This visualization shows the total numbers of female students each year who have (i) newly enrolled,
	   (ii) graduated, or (iii) left their institution without graduating. These totals are normalized by
	   the number of institutions included in the sum. Note that the normalizing number of institutions for
	   each data point is displayed in the tooltip. Additionally, we separated the totals by the types of
	   degrees offered by the institution. This allows us to compare data for various types of institutions
	   directly.""",
	 style={"font-size": "18px"}, width=1000, height=100)
p2 = Paragraph(text=
	"""The first thing we notice is that there is very limited data for institutions only offering a
	   Bachelor's degree. This makes it difficult to make any inferences for this data. In comparing
	   institutions that offer Ph.D.'s versus those that don't, we notice that the Ph.D. institutions
	   have larger numbers of female students enrolling and graduating while having relatively comparable
	   numbers of female students leaving the institution. Perhaps there is some aspect of research-based
	   institutions that help attract and retain female students through graduation.""",
	 style={"font-size": "18px"}, width=1000, height=125)
p3 = Paragraph(text=
	"""Next, we examine trends over the years. First, we notice that Ph.D. institutions have large numbers
	   of female students per institution across all three categories in 2003-2004. By using the tooltip,
	   we notice that these data points contain relatively few institutions. In later years, the number of
	   Ph.D institutions grows significantly, which likely accounts for the initial decline in these
	   normalized numbers. In more recent years, we see strong growth in the numbers of newly enrolled and
	   graduated female students from Ph.D institutions. Bachelor's and Master's insitutions display some
	   growth in new female enrollments as well as a temporary bump in graduated female students. However,
	   both categories of institutions see similar trends in the number of female students leaving without
	   graduating. This again suggests that institutions offering Ph.D. programs are performing better in
	   terms of recruitment and retention of female students.""",
	 style={"font-size": "18px"}, width=1000, height=125)

# Initialize data sources
source_B = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))
source_BM = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))
source_BMP = ColumnDataSource(data=dict(x=[], y=[], num_insts=[]))

# Function that parses the data and updates the data sources
def gather_data(data_flag):

	# Get appropriate data column based on drop-down menu
	if (data_flag == 0):
		col_header = "Enroll, Female: New Enrollments (Enrl F)"
	elif (data_flag == 1):
		col_header = "Totals, Female: Graduated (Tot. F)"
	elif (data_flag == 2):
		col_header = "Totals, Female: Left Institution (not graduated) (Tot. F)"

	# Remove data that doesn't have "What degrees does your institution offer?" data
	d = dat["What degrees does your institution offer?"]
	null_idx = d.isnull()
	val_idx = np.invert(null_idx.as_matrix())
	dat2 = dat.iloc[val_idx]

	# Get types of degrees offered
	deg_offered = sorted(dat2["What degrees does your institution offer?"].unique())

	for deg in deg_offered:

		# Remove data for institutions offering different degrees
		dat_deg = dat2[dat2["What degrees does your institution offer?"] == deg]

		x_dat, y_dat, num_insts = [], [], []
		for yr in yrs:

			# Remove data that isn't for the given year
			dat_deg_yr = dat_deg[dat_deg["School Year"] == yr]

			# Remove data with NaNs
			dat_deg_yr = dat_deg_yr[np.logical_not(np.isnan(dat_deg_yr[col_header]))]

			# Get number of institutions included in calculation
			N_schls = len(dat_deg_yr["Institution"].unique())
			num_insts.append(N_schls)

			# Append data
			x_dat.append(yr)
			if (N_schls > 0):
				y_dat.append(np.nansum(dat_deg_yr[col_header])/N_schls)
			else:
				y_dat.append(np.nan)

		# Update appropriate source data
		if (deg == "Bachelor's degrees only"):
			source_B.data = dict(x=x_dat, y=y_dat, num_insts=num_insts)
		elif (deg == "Bachelor's and master's degrees only"):
			source_BM.data = dict(x=x_dat, y=y_dat, num_insts=num_insts)
		elif (deg == "Bachelor's, master's, and Ph.D. degrees"):
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

# Format axes and labels
plt.xaxis.major_label_orientation = np.pi/4
plt.xaxis.axis_label_text_font_size = "18px"
plt.xaxis.major_label_text_font_size = "18px"

plt.yaxis.axis_label = "Number of Female Students / Institution"
plt.yaxis.axis_label_text_font_size = "18px"
plt.yaxis.major_label_text_font_size = "18px"

# Get rid of stupid Bokeh logo
plt.toolbar.logo = None

# Set callback function for the radio button group
radio_button_group.on_click(gather_data)

# Define layout of glyphs on the page
layout = column(div_title, row(div_RadGroup, radio_button_group), plt, p1, p2, p3)
curdoc().add_root(layout)

# Set title
curdoc().title = "Visualization 3"
