import pandas as pd
import numpy as np
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.models.widgets import Panel, Tabs

ncwit = pd.read_csv('NCWIT_DataV2_RawData.csv')
ncwit = ncwit[np.isfinite(ncwit['Record#'])]
ncwit['NCWIT Participant'] = ncwit['NCWIT Participant'].map({'Extension Services, Academic Alliance':'Extension Services', 'Academic Alliance':'Academic Alliance','Academic Alliance, Academic Alliance':'Academic Alliance','Academic Alliance, IPEDS':'Academic Alliance'})

years = ncwit['School Year'].unique()
years.sort()

ncwit['Totals, Female: Graduated (Tot. F)'] = ncwit['Totals, Female: Graduated (Tot. F)'].fillna(0)

totgradf = ncwit['Totals, Female: Graduated (Tot. F)']
ncwit['Enroll, Female: New Enrollments (Enrl F)'] = ncwit['Enroll, Female: New Enrollments (Enrl F)'].fillna(0)

yearctfgrad = {}
for y in years:
    yearctfgrad[y] = float(0)

for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctfgrad[row['School Year']] += row['Totals, Female: Graduated (Tot. F)']
        
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        if row['School Year'] == '2016-2017':
            print (row['Totals, Female: Graduated (Tot. F)'])

femalegradext = []
for key,value in sorted(yearctfgrad.items()):
    femalegradext.append(value)
    
yr = []
for val in years:
    yr.append(val)
    
yearctfgrad_aa = {}
for y in years:
    yearctfgrad_aa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctfgrad_aa[row['School Year']] += row['Totals, Female: Graduated (Tot. F)']

femalegradaa = []
for key,value in sorted(yearctfgrad_aa.items()):
    femalegradaa.append(value)
    
yearctmgrad = {}
for y in years:
    yearctmgrad[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctmgrad[row['School Year']] += row['Totals, Male: Graduated (Tot. M)']

malegradex = []
for key,value in sorted(yearctmgrad.items()):
    malegradex.append(value)
    
ncwit['Totals, Male: Graduated (Tot. M)'] = ncwit['Totals, Male: Graduated (Tot. M)'].fillna(0)

yearctmgrad_aa = {}
for y in years:
    yearctmgrad_aa[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Academic Alliance':
        yearctmgrad_aa[row['School Year']] += row['Totals, Male: Graduated (Tot. M)']

malegradaa = []
for key,value in sorted(yearctmgrad_aa.items()):
    malegradaa.append(value)
    
yrex = []
for key, value in sorted(yearctfgrad.items()):
    if value != float(0):
        yrex.append(key)
        
yraa = []
for key, value in sorted(yearctmgrad_aa.items()):
    if value != float(0):
        yraa.append(key)

yearctmgrad = {}
for y in years:
    yearctmgrad[y] = float(0)
for index,row in ncwit.iterrows():
    if row['NCWIT Participant'] == 'Extension Services':
        yearctmgrad[row['School Year']] += row['Totals, Male: Graduated (Tot. M)']

malegradex = []
for key,value in sorted(yearctmgrad.items()):
    if key in yrex:
        malegradex.append(value)
        
femalegradext = []
for key,value in sorted(yearctfgrad.items()):
    if key in yrex:
        femalegradext.append(value)
        
ratiogradex = []
for i in range(0, len(femalegradext)):
    ratiogradex.append(float(femalegradext[i]/malegradex[i]))
    
femalegradaa = []
for key,value in sorted(yearctfgrad_aa.items()):
    if key in yraa:
        femalegradaa.append(value)
        
malegradaa = []
for key,value in sorted(yearctmgrad_aa.items()):
    if key in yraa:
        malegradaa.append(value)
        
ratiogradaa = []
for i in range(0, len(femalegradaa)):
    ratiogradaa.append(float(femalegradaa[i]/malegradaa[i]))
    
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
    
topyval = max(max(ratiogradex),max(ratiogradaa),max(ratioenrollex),max(ratioenrollaa),max(ratioleftex),max(ratioleftaa))

topyval = topyval + float(topyval/10)

# output to static HTML file
output_file("lines.html")

p1 = figure(x_range=yrex, y_range=(0,topyval), plot_height=500, plot_width = 1000, title="Visualization 2", x_axis_label='School Year', y_axis_label='Females to Male Ratio')
p1.line(yrex, ratiogradex, legend="Extension Services", line_width=2, color = 'red', line_dash="4 4")
p1.line(yraa, ratiogradaa, legend="Academic Alliance", line_width=2, color = 'blue')
p1.circle(yrex, ratiogradex, legend="Extension Services", size=7, color = 'red')
p1.circle(yraa, ratiogradaa, legend="Academic Alliance", size=7, color = 'blue')
p1.legend.orientation = "horizontal"
p1.legend.location = "top_center"
p1.legend.click_policy="hide"
tab1 = Panel(child=p1,title="Graduated")

p2 = figure(x_range=yrex_en, y_range=(0,topyval), plot_height=500, plot_width = 1000, title="Visualization 2", x_axis_label='School Year', y_axis_label='Females to Male Ratio')
p2.line(yrex_en, ratioenrollex, legend="Extension Services", line_width=2, color = 'red', line_dash="4 4")
p2.line(yraa_en, ratioenrollaa, legend="Academic Alliance", line_width=2, color = 'blue')
p2.circle(yrex_en, ratioenrollex, legend="Extension Services", size=7, color = 'red')
p2.circle(yraa_en, ratioenrollaa, legend="Academic Alliance", size=7, color = 'blue')
p2.legend.orientation = "horizontal"
p2.legend.location = "top_center"
p2.legend.click_policy="hide"
tab2 = Panel(child=p2,title="Enrolled")

p3 = figure(x_range=yrex_le, y_range=(0,topyval), plot_height=500, plot_width = 1000, title="Visualization 2", x_axis_label='School Year', y_axis_label='Females to Male Ratio')
p3.line(yrex_le, ratioleftex, legend="Extension Services", line_width=2, color = 'red', line_dash="4 4")
p3.line(yraa_le, ratioleftaa, legend="Academic Alliance", line_width=2, color = 'blue')
p3.circle(yrex_le, ratioleftex, legend="Extension Services", size=7, color = 'red')
p3.circle(yraa_le, ratioleftaa, legend="Academic Alliance", size=7, color = 'blue')
p3.legend.orientation = "horizontal"
p3.legend.location = "top_center"
p3.legend.click_policy="hide"
tab3 = Panel(child=p3, title="Left Institution")

tabs = Tabs(tabs=[ tab1, tab2, tab3 ])

# show the results
show(tabs)
