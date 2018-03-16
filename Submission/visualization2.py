#######################################################################
#   Displaying Line Graphs of Female to Male Ratio per year
#   For Academic Alliance and Extension Services
#   Considering the Attributes -> Graduated, New Enrollments and Left Institution
#   Also, I've been horrible at variable naming - so please bear with that
#   I hope the comments make up for that

#   Special Thanks to
#   https://bokeh.pydata.org/en/latest/docs/user_guide.html
#   and stackoverflow
#######################################################################

import pandas as pd
import numpy as np
import bokeh
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Legend
from bokeh.palettes import Spectral6
from bokeh.models.widgets import Panel, Tabs, Paragraph, Div
from bokeh.layouts import layout, column, row

ncwit = pd.read_csv('NCWIT_DataV2_RawData.csv', low_memory=False)

#   Delete all the records which don't have an Associated ID -> all values are NaN
ncwit = ncwit[np.isfinite(ncwit['Record#'])]

#   Changing the NCWIT Participant Column to only have Academic Alliance and Extension Services
ncwit['NCWIT Participant'] = ncwit['NCWIT Participant'].map({'Extension Services, Academic Alliance':'Extension Services', 'Academic Alliance':'Academic Alliance','Academic Alliance, Academic Alliance':'Academic Alliance','Academic Alliance, IPEDS':'Academic Alliance'})

#   Create an array of School Years for laying out X axis
years = ncwit['School Year'].unique()
years.sort()

#   Handling Missing Data -> Fill all the empty columns with 0's
ncwit['Totals, Female: Graduated (Tot. F)'] = ncwit['Totals, Female: Graduated (Tot. F)'].fillna(0)

#   Now repeating the lines 43 - 56 but for Males
ncwit['Totals, Male: Graduated (Tot. M)'] = ncwit['Totals, Male: Graduated (Tot. M)'].fillna(0)

#   Create a dictionary to have the total sum of males graduated per year
#   In extension services
yearctmgrad = {}
for y in years:
    yearctmgrad[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctmgrad[row['School Year']] += row['Totals, Male: Graduated (Tot. M)']

#   Plot only for those years which have a certain value of males
#   Otherwise we get a divide by 0 situation -> we don't want that
#   For laying out the X axis of the plot
yrex = []
for key, value in sorted(yearctmgrad.items()):
    if value != float(0):
        yrex.append(key)

#   Creating a new array that will store only the counts for every year
malegradex = []
for key,value in sorted(yearctmgrad.items()):
    if key in yrex:
        malegradex.append(value)

#   Create a dictionary to have the total sum of females graduated per year
#   In extension services
yearctfgrad = {}
for y in years:
    yearctfgrad[y] = float(0)

#   Here is where we do the sum and fill our dictionary
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctfgrad[row['School Year']] += row['Totals, Female: Graduated (Tot. F)']

#   Creating a new array that will store only the counts for every year
femalegradext = []
for key,value in sorted(yearctfgrad.items()):
    if key in yrex:
        femalegradext.append(value)

#   Creating a new array that will store only the Years
#   This is different from years in the sense that it is a normal array wheras years was a numpy array
yr = []
for val in years:
    yr.append(val)

#   Repeating 42-61 for Academic Alliance
yearctmgrad_aa = {}
for y in years:
    yearctmgrad_aa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctmgrad_aa[row['School Year']] += row['Totals, Male: Graduated (Tot. M)']

#   Same thing but for Academic Alliance
yraa = []
for key, value in sorted(yearctmgrad_aa.items()):
    if value != float(0):
        yraa.append(key)

malegradaa = []
for key,value in sorted(yearctmgrad_aa.items()):
    if key in yraa:
        malegradaa.append(value)

#   Now do the exact same thing but for Academic Alliance
yearctfgrad_aa = {}
for y in years:
    yearctfgrad_aa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctfgrad_aa[row['School Year']] += row['Totals, Female: Graduated (Tot. F)']

femalegradaa = []
for key,value in sorted(yearctfgrad_aa.items()):
    if key in yraa:
        femalegradaa.append(value)

#    We have eveything now so just get the ratio
#    For Extension Services
ratiogradex = []
for i in range(0, len(femalegradext)):
    ratiogradex.append(float(femalegradext[i]/malegradex[i]))

#    For Academic Alliance
ratiogradaa = []
for i in range(0, len(femalegradaa)):
    ratiogradaa.append(float(femalegradaa[i]/malegradaa[i]))

############### Done With Total Graduated Stuff #############################
#   Now we need to repeat the same for New Enrollments and Left Institution
#   Not putting comments here because its just the same thing with variables changed

ncwit['Enroll, Female: New Enrollments (Enrl F)'] = ncwit['Enroll, Female: New Enrollments (Enrl F)'].fillna(0)
ncwit['Enroll, Male: New Enrollments (Enrl M)'] = ncwit['Enroll, Male: New Enrollments (Enrl M)'].fillna(0)
ncwit['Totals, Female: Left Institution (not graduated) (Tot. F)'] = ncwit['Totals, Female: Left Institution (not graduated) (Tot. F)'].fillna(0)
ncwit['Totals, Male: Left Institution (not graduated) (Tot. M)'] = ncwit['Totals, Male: Left Institution (not graduated) (Tot. M)'].fillna(0)

yearctmenrollex = {}
for y in years:
    yearctmenrollex[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctmenrollex[row['School Year']] += row['Enroll, Male: New Enrollments (Enrl M)']

yearctfenrollex = {}
for y in years:
    yearctfenrollex[y] = float(0)

for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctfenrollex[row['School Year']] += row['Enroll, Female: New Enrollments (Enrl F)']

yrex_en = []
for key, value in sorted(yearctmenrollex.items()):
    if value != float(0):
        yrex_en.append(key)

maleenrollex = []
for key,value in sorted(yearctmenrollex.items()):
    if key in yrex_en:
        maleenrollex.append(value)

femaleenrollex = []
for key,value in sorted(yearctfenrollex.items()):
    if key in yrex_en:
        femaleenrollex.append(value)

ratioenrollex = []
for i in range(0, len(femaleenrollex)):
    ratioenrollex.append(float(femaleenrollex[i]/maleenrollex[i]))

yearctmenrollaa = {}
for y in years:
    yearctmenrollaa[y] = float(0)

for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctmenrollaa[row['School Year']] += row['Enroll, Male: New Enrollments (Enrl M)']

yearctfenrollaa = {}
for y in years:
    yearctfenrollaa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctfenrollaa[row['School Year']] += row['Enroll, Female: New Enrollments (Enrl F)']

yraa_en = []
for key, value in sorted(yearctmenrollaa.items()):
    if value != float(0):
        yraa_en.append(key)

maleenrollaa = []
for key,value in sorted(yearctmenrollaa.items()):
    if key in yraa_en:
        maleenrollaa.append(value)

femaleenrollaa = []
for key,value in sorted(yearctfenrollaa.items()):
    if key in yraa_en:
        femaleenrollaa.append(value)

ratioenrollaa = []
for i in range(0, len(femaleenrollaa)):
    ratioenrollaa.append(float(femaleenrollaa[i]/maleenrollaa[i]))

############### Done With New Enrollments #############################
#   Here is the Left Instituion Code

yearctmleftex = {}
for y in years:
    yearctmleftex[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctmleftex[row['School Year']] += row['Totals, Male: Left Institution (not graduated) (Tot. M)']

yearctfleftex = {}
for y in years:
    yearctfleftex[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctfleftex[row['School Year']] += row['Totals, Female: Left Institution (not graduated) (Tot. F)']

yrex_le = []
for key, value in sorted(yearctmleftex.items()):
    if value != float(0):
        yrex_le.append(key)

maleleftex = []
for key,value in sorted(yearctmleftex.items()):
    if key in yrex_le:
        maleleftex.append(value)

femaleleftex = []
for key,value in sorted(yearctfleftex.items()):
    if key in yrex_le:
        femaleleftex.append(value)

ratioleftex = []
for i in range(0, len(femaleleftex)):
    ratioleftex.append(float(femaleleftex[i]/maleleftex[i]))

yearctmleftaa = {}
for y in years:
    yearctmleftaa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctmleftaa[row['School Year']] += row['Totals, Male: Left Institution (not graduated) (Tot. M)']

yearctfleftaa = {}
for y in years:
    yearctfleftaa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctfleftaa[row['School Year']] += row['Totals, Female: Left Institution (not graduated) (Tot. F)']

yraa_le = []
for key, value in sorted(yearctmleftaa.items()):
    if value != float(0):
        yraa_le.append(key)
maleleftaa = []
for key,value in sorted(yearctmleftaa.items()):
    if key in yraa_le:
        maleleftaa.append(value)
femaleleftaa = []
for key,value in sorted(yearctfleftaa.items()):
    if key in yraa_le:
        femaleleftaa.append(value)

ratioleftaa = []
for i in range(0, len(femaleleftaa)):
    ratioleftaa.append(float(femaleleftaa[i]/maleleftaa[i]))

############### Done With Left Instituion #############################

#   Now for the Y axis, calculate the maximum ratio for all three attributes
#   and for both academic alliance and extension services
#   Now get the y axis max scale by adding 10% of the top value to the top value
topyval = max(max(ratiogradex),max(ratiogradaa),max(ratioenrollex),max(ratioenrollaa),max(ratioleftex),max(ratioleftaa))
topyval = topyval + float(topyval/10)

# Make title
div_title_filler = Div(text="""ahhhhhhhhhhhhhhhhhhhhh""", #&nbsp &nbsp &nbsp
                       style={"font-size": "30px", "text-align": "center"}, width=600, height=80)
div_title = Div(text="""&nbsp &nbsp &nbsp &nbsp &nbsp Ratio of Female to Male Students for 
	                    &nbsp &nbsp &nbsp &nbsp &nbsp Extension Services vs. Academic Alliance""",
                style={"font-size": "30px", "text-align": "center"}, width=750, height=80)

#   Plotting the first visualization -> for the Graduated Attribute
p1 = figure(x_range=yrex, y_range=(0,topyval), plot_height=500, plot_width=1000,
            x_axis_label='School Year', y_axis_label='Female to Male Ratio', tools="pan,wheel_zoom,box_zoom,reset")
l1_ES = p1.line(yrex_en, ratioenrollex, line_width=2, color='red', line_dash="4 4", muted_alpha=0.2)
l1_AA = p1.line(yraa_en, ratioenrollaa, line_width=2, color='blue', muted_alpha=0.2)
c1_ES = p1.circle(yrex_en, ratioenrollex, radius=0.1, color='red', muted_alpha=0.2)
c1_AA = p1.circle(yraa_en, ratioenrollaa, radius=0.1, color='blue', muted_alpha=0.2)
leg1 = Legend(items=[
    ("Extension Services", [l1_ES, c1_ES]),
    ("Academic Alliance", [l1_AA, c1_AA])],
    location=(250, 5))
p1.add_layout(leg1, 'above')
p1.legend.border_line_width = 1
p1.legend.border_line_color = "black"
p1.legend.orientation = "horizontal"
p1.legend.label_text_font_size = "18px"
p1.legend.click_policy = "mute"
p1.xaxis.major_label_orientation = np.pi/4
p1.xaxis.axis_label_text_font_size = "18px"
p1.xaxis.major_label_text_font_size = "18px"
p1.yaxis.axis_label_text_font_size = "18px"
p1.yaxis.major_label_text_font_size = "18px"
p1.toolbar.logo = None
tab1 = Panel(child=p1, title="New Enrollments")

#   Plotting the first visualization -> for the New Enrollments Attribute
p2 = figure(x_range=yrex_en, y_range=(0,topyval), plot_height=500, plot_width = 1000,
            x_axis_label='School Year', y_axis_label='Female to Male Ratio', tools="pan,wheel_zoom,box_zoom,reset")
l2_ES = p2.line(yrex, ratiogradex, line_width=2, color='red', line_dash="4 4", muted_alpha=0.2)
l2_AA = p2.line(yraa, ratiogradaa, line_width=2, color='blue', muted_alpha=0.2)
c2_ES = p2.circle(yrex, ratiogradex, radius=0.1, color='red', muted_alpha=0.2)
c2_AA = p2.circle(yraa, ratiogradaa, radius=0.1, color='blue', muted_alpha=0.2)
leg2 = Legend(items=[
    ("Extension Services", [l2_ES, c2_ES]),
    ("Academic Alliance", [l2_AA, c2_AA])],
    location=(250, 5))
p2.add_layout(leg2, 'above')
p2.legend.border_line_width = 1
p2.legend.border_line_color = "black"
p2.legend.orientation = "horizontal"
p2.legend.label_text_font_size = "18px"
p2.legend.click_policy = "mute"
p2.xaxis.major_label_orientation = np.pi/4
p1.xaxis.axis_label_text_font_size = "18px"
p2.xaxis.major_label_text_font_size = "18px"
p2.yaxis.axis_label_text_font_size = "18px"
p2.yaxis.major_label_text_font_size = "18px"
p2.toolbar.logo = None
tab2 = Panel(child=p2, title="Graduated")

#   Plotting the first visualization -> for the Left Institution Attribute
p3 = figure(x_range=yrex_le, y_range=(0,topyval), plot_height=500, plot_width = 1000,
            x_axis_label='School Year', y_axis_label='Female to Male Ratio', tools="pan,wheel_zoom,box_zoom,reset")
l3_ES = p3.line(yrex_le, ratioleftex, line_width=2, color='red', line_dash="4 4", muted_alpha=0.2)
l3_AA = p3.line(yraa_le, ratioleftaa, line_width=3, color='blue', muted_alpha=0.2)
c3_ES = p3.circle(yrex_le, ratioleftex, radius=0.1, color='red', muted_alpha=0.2)
c3_AA = p3.circle(yraa_le, ratioleftaa, radius=0.1, color='blue', muted_alpha=0.2)
leg3 = Legend(items=[
    ("Extension Services", [l3_ES, c3_ES]),
    ("Academic Alliance", [l3_AA, c3_AA])],
    location=(250, 5))
p3.add_layout(leg3, 'above')
p3.legend.border_line_width = 1
p3.legend.border_line_color = "black"
p3.legend.orientation = "horizontal"
p3.legend.label_text_font_size = "18px"
p3.legend.click_policy = "mute"
p3.xaxis.major_label_orientation = np.pi/4
p3.xaxis.axis_label_text_font_size = "18px"
p3.xaxis.major_label_text_font_size = "18px"
p3.yaxis.axis_label_text_font_size = "18px"
p3.yaxis.major_label_text_font_size = "18px"
p3.toolbar.logo = None
tab3 = Panel(child=p3, title="Left Institution")


# Make paragraph sections for discussion
par1 = Paragraph(text=
    """This visualization shows the ratio of the number of female students to the number of male studnets
       each year who have (i) newly enrolled, (ii) graduated, or (iii) left their institution without graduating.
       We separated the totals by the type of NCWIT involvement (Academic Alliance vs. Extension Services).
       Data for programs in the Academic Alliance is only available for more recent years while data for
       programs using Extension Services is available as far back as the 2003-2004 school year. Across all
       three attributes, we notice that the ratio of females to males for programs using Extension Services
       is more constant from year to year compared to Academic Alliance.""",
     style={"font-size": "18px"}, width=1000, height=100)


tabs = Tabs(tabs=[tab1, tab2, tab3], width=400)
layout = column(div_title, tabs, par1)
curdoc().add_root(layout)
curdoc().title = "Visualization 2"
