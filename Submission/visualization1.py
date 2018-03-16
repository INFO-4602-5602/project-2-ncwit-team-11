from __future__ import division

from os.path import join, dirname
from math import pi
import pandas as pd
import numpy as np
from bokeh.io import show, export_png, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool,LinearColorMapper, ColorBar
from bokeh.models.widgets import CheckboxGroup, Paragraph, Div
from bokeh.layouts import row, widgetbox, layout, column
from bokeh.palettes import Spectral6
from bokeh.transform import factor_cmap
import pdb
import logging
from operator import add, truediv

def find(lst,val):
    return [x==val for x in lst]

def findind(lst,val):
    return [i for i, x in enumerate(lst) if x==val]

#Read in data file
def basicInfo(filename):
    ''' Filename should be .csv'''

    dat = pd.read_csv(filename,dtype={'CIP# Only':'unicode'})
    d = dat['Record#']
    null_idx = d.isnull()
    val_idx = np.invert(null_idx.as_matrix())
    dat = dat.iloc[val_idx]
    rows_tot = dat.shape[0]
    dat['NCWIT Participant'] = dat['NCWIT Participant'].map({'Extension Services, Academic Alliance':'Extension Services',
                            'Academic Alliance':'Academic Alliance','Academic Alliance, Academic Alliance':'Academic Alliance',
                            'Academic Alliance, IPEDS':'Academic Alliance'})
    return dat


# Round up CIP #  to two decimal places
def roundupCIPvals(CIP_mat,decl_sums, grad_sums, left_inst_sums, prop_ES):

    CIP_int = []
    for i in range(len(CIP_mat)):
        if CIP_mat[i] != '?':
            CIP_int.append(np.around(float(CIP_mat[i]),2))
        else:
            CIP_int.append(0)

    CIP_int_unique = list(np.unique(np.array(CIP_int)))

    dec_sums_arr = np.array(decl_sums)
    grad_sums_arr= np.array(grad_sums)
    left_inst_sums_arr= np.array(left_inst_sums)
    prop_ES = np.array(prop_ES)
    dec_sums_aug = []
    grad_sums_aug=[]
    left_sums_aug=[]
    prop_ES_aug = []
    for cip_no in CIP_int_unique:
        dec_sums_aug.append(np.sum(dec_sums_arr[find(CIP_int,cip_no)]))
        grad_sums_aug.append(np.sum(grad_sums_arr[find(CIP_int,cip_no)]))
        left_sums_aug.append(np.sum(left_inst_sums_arr[find(CIP_int,cip_no)]))
        prop_ES_aug.append( np.nansum(prop_ES[find(CIP_int,cip_no)]) )


    CIP_int_unique = [str(c) for c in CIP_int_unique]

    return CIP_int_unique, dec_sums_aug, grad_sums_aug, left_sums_aug, prop_ES

def retDictionaryMajors(CIP,decl_sums, grad_sums, left_inst_sums, prop_ES):

# Consolidate CIP # with 2 decimal points and assign majors correpsondingly
    keys = ['Computer Science',
             'Computer and Information Sciences',
             'Management Information Systems',
             'Computer Engineering',
             'Electrical,Electronics and Computer Engineering',
             'Mechanical Engineering',
             'Systems Engineering',
             'Information Studies',
             'Computer Programming',
             'Computer Systems Analysis',
             'CS and Media',
             'Telecom',
             'Computer Administration']


    vals = [11.07, 11.01, 52.12, 14.09, 14.10, 14.19, 14.27, 11.04, 11.02, 11.05, 11.08, 11.09, 11.10]

    hash = {k:v for k, v in zip(keys, vals)}

    majs  = [keys[findind(vals,CIP[i])[0]] for i in range(len(CIP)) if findind(vals,CIP[i]) ]
    decl_sums = [decl_sums[i] for i in range(len(CIP)) if findind(vals,CIP[i]) ]
    grad_sums = [grad_sums[i] for i in range(len(CIP)) if findind(vals,CIP[i]) ]
    left_inst_sums = [left_inst_sums[i] for i in range(len(CIP)) if findind(vals,CIP[i]) ]
    prop_ES = [prop_ES[i] for i in range(len(CIP)) if findind(vals,CIP[i]) ]
    return majs, decl_sums, grad_sums, left_inst_sums, prop_ES

def retrieveEnroll(mf):

    dat = basicInfo("NCWIT_DataV2.csv");
    rows = dat.shape[0]

    CIP_col = dat['CIP# Only']
    CIP_mat = CIP_col.as_matrix()
    CIP_mat = np.unique( np.unique(CIP_mat))
    graduated_sum = []
    left_inst_sum = []
    declared_sum = []
    declared_ES = []

    for i in range(len(CIP_mat)):
        dd= dat[dat['CIP# Only']==CIP_mat[i]]
        ddE = dd[dd['NCWIT Participant'] == 'Extension Services']
        if mf == 'F':
            declared_sum.append(np.nansum(dd['Totals, Female: Total Declared Majors (Tot. F)'].as_matrix()))
            declared_ES.append(np.nansum(ddE['Totals, Female: Total Declared Majors (Tot. F)'].as_matrix()) )
            graduated_sum.append(np.nansum(dd['Totals, Female: Graduated (Tot. F)'].as_matrix()))
            left_inst_sum.append(np.nansum(dd['Totals, Female: Left Institution (not graduated) (Tot. F)'].as_matrix()))
        else:
            declared_sum.append(np.nansum(dd['Totals, Male: Total Declared Majors (Tot. M)'].as_matrix()))
            declared_ES.append(np.nansum(ddE['Totals, Male: Total Declared Majors (Tot. M)'].as_matrix()))
            graduated_sum.append(np.nansum(dd['Totals, Male: Graduated (Tot. M)'].as_matrix()))
            left_inst_sum.append(np.nansum(dd['Totals, Male: Left Institution (not graduated) (Tot. M)'].as_matrix()))

    CIP_mat, declared_sum, graduated_sum, left_inst_sum, declared_ES = roundupCIPvals(CIP_mat,declared_sum,graduated_sum, left_inst_sum, declared_ES)
    CIP_mat = np.array(CIP_mat)
    declared_array = np.array(declared_sum)
    declared_idx = np.argsort(declared_array)
    declared_sum = declared_array[declared_idx].tolist()
    declared_ES_array = np.array(declared_ES)
    declared_ES = declared_ES_array[declared_idx].tolist()
    graduated_sum = np.array(graduated_sum)
    left_inst_sum = np.array(left_inst_sum)
    CIP_mat = CIP_mat[declared_idx]
    CIP_mat = CIP_mat.tolist()
    graduated_sum = graduated_sum[declared_idx]
    graduated_sum = graduated_sum.tolist()
    left_inst_sum =left_inst_sum[declared_idx]
    left_inst_sum = left_inst_sum.tolist()

    declared_sum = declared_sum[::-1]
    CIP_mat = CIP_mat[::-1]
    graduated_sum = graduated_sum[::-1]
    left_inst_sum = left_inst_sum[::-1]
    declared_ES = declared_ES[::-1]

    return CIP_mat, declared_sum, graduated_sum, left_inst_sum, declared_ES

# Make paragraph section for discussion
div_title = Div(text="""Distribution of total number of majors declared for males and females""",
                style={"font-size": "30px", "text-align": "center"}, width=1000, height=60)

# Make paragraph section for discussion
div_RadGroup = Div(text="""Select Data Source: &nbsp""",
                   style={"font-size": "18px", "text-align": "right"}, width=400, height=40)

# Make paragraph sections for discussion
p1 = Paragraph(text=
    """The goal of the visualization is to display the distribution by majors of the total number of students who declared
        their majors. The data was summed across years to get a sense of the distribution for the entire time frame. The checkbox group on the right
        can be used to toggle between Male and Female data. When both are selected, the graph displays the total number of students (male and female).
        NOTE: When toggling from Male to Female and vice versa, the y axis range changes. This is because number of females declaring their majors
        was far lower than the number of males. When the axis was kept constant, the female data wasn't quite as salient. Based on Dr. Lecia Barker's comments,
        it seemed that NCWIT was interested especially in the data pertaining to females, so we chose salience over consistency.""",
     style={"font-size": "18px"}, width=1000, height=155)
p2 = Paragraph(text=
    """We see that for both males and females, the most dominant major is Computer Science. Hoevering over the bars in the bar chart reveals a tooltip
        that shows the total number of students who graduated and also those who left the institution for the corresponding majors. The colors of the bars
        indicate the proportion of NCWIT participants who were part of the Extension Services program - lighter bar color indicates a greater proportion of
        NCWIT participants who were part of the Extension Services program.""",
     style={"font-size": "18px"}, width=1000, height=125)
p3 = Paragraph(text=
    """ """,
     style={"font-size": "18px"}, width=1000, height=125)

CIP_mat_f, declared_sum_f, graduated_sum_f, left_inst_sum_f,declared_ESf = retrieveEnroll('F')
CIP_mat_m, declared_sum_m, graduated_sum_m, left_inst_sum_m, declared_ESm = retrieveEnroll('M')
declared_sum_tot = list(map(add,declared_sum_m,declared_sum_f))
graduated_sum_tot = list(map(add,graduated_sum_m,graduated_sum_f))
left_inst_sum_tot =list(map(add,left_inst_sum_m,left_inst_sum_f))
declared_ES_tot = list(map(add,declared_ESf, declared_ESm))
CIP_mat = [float(c) for c in CIP_mat_f ]
Maj_mat, declared_sums_f,graduated_sum_f, left_inst_sum_f, declared_ESf = retDictionaryMajors(CIP_mat, declared_sum_f,graduated_sum_f, left_inst_sum_f, declared_ESf)
Maj_mat, declared_sums_m, graduated_sum_m, left_inst_sum_m, declared_ESm = retDictionaryMajors(CIP_mat, declared_sum_m, graduated_sum_m, left_inst_sum_m, declared_ESm)
Maj_mat, declared_sums_tot, graduated_sum_tot, left_inst_sum_tot, declared_EStot = retDictionaryMajors(CIP_mat, declared_sum_tot, graduated_sum_tot, left_inst_sum_tot, declared_ES_tot)

propESf = list(map(truediv,declared_ESf, declared_sums_f))
propESm = list(map(truediv,declared_ESm, declared_sums_m))
propEStot = list(map(truediv,declared_EStot, declared_sum_tot))


palettef = []
palettem =[]
palettetot= []
i =0
for p in propESf:
    if p>1:
        p= 0
        propESf[i] = 0

    r = int(np.around(p*255,0))
    g = int(np.around(p*255,0))
    b = 255
    code = '#%02x%02x%02x' % (r,g,b)
    if(p== max(propESf)):
        code_maxf = code
    palettef.append(code)
    i=i+1

i=0
for p in propESm:

    if p>1:
        p= 0
        propESm[i]=0
    r = int(np.around(p*255,0))
    g = int(np.around(p*255,0))
    b = 255
    code = '#%02x%02x%02x' % (r,g,b)
    if(p== max(propESm)):
        code_maxm = code
    palettem.append(code)
    i=i+1

i=0
for p in propEStot:
    if p>1:
        p= 0
        propEStot[i]=0
    r = int(np.around(p*255,0))
    g = int(np.around(p*255,0))
    b = 255
    code = '#%02x%02x%02x' % (r,g,b)
    palettetot.append(code)
    i=i+1


code_maxtot = palettetot[propEStot.index(max(propEStot))]

linsptot = np.linspace(0,1,100)*255
linsptot = linsptot.tolist()


p_colorbartot = ['#%02x%02x%02x' %  (int(np.around(r,0)),int(np.around(g,0)),int(b) ) for (r,g,b) in zip(linsptot, linsptot, [255]*100) ]
# define data source for bokeh
sourcef = ColumnDataSource(data=dict(CIP_matf =Maj_mat,dec_sumf=declared_sums_f,tooltip1= graduated_sum_f,tooltip2= left_inst_sum_f ))
sourcem = ColumnDataSource(data=dict(CIP_matm =Maj_mat ,dec_summ=declared_sums_m,tooltip1= graduated_sum_m,tooltip2=left_inst_sum_m ))
sourcetot= ColumnDataSource(data=dict(CIP_matm =Maj_mat ,dec_sumtot=declared_sums_tot,tooltip1=graduated_sum_tot,tooltip2=left_inst_sum_tot))

# create figure for bar chart
p = figure(x_range=Maj_mat,plot_width=1000, plot_height=600,toolbar_location=None)
p.y_range.start = 0
p.xaxis.major_label_orientation = pi/4

hover = HoverTool(tooltips=[
                    ('# Graduated', '@tooltip1'),
                    ('# Left Institution','@tooltip2')
                    ])


mapper = LinearColorMapper(palette=p_colorbartot , low=0, high=1)

mapper.low_color=  '#0000ff'
mapper.high_color = code_maxtot

ff = p.vbar(x='CIP_matf', top='dec_sumf', width=0.9, source=sourcef, fill_color=factor_cmap('CIP_matf', palette=palettef, factors=Maj_mat ) )
mm = p.vbar(x='CIP_matm', top='dec_summ', width=0.9, source=sourcem, fill_color=factor_cmap('CIP_matm', palette=palettem, factors=Maj_mat) )
ff.visible = False
mm.visible = False
tot =  p.vbar(x='CIP_matm', top='dec_sumtot', width=0.9, source=sourcetot, fill_color=factor_cmap('CIP_matm', palette=palettetot, factors=Maj_mat) )

# Create colorbar object 
color_bar = ColorBar(color_mapper=mapper, location=(0,0))

# Create checkbox
checkbox_group = CheckboxGroup(labels=["Female", "Male"], active=[0, 1])

# Callback function for toggling
def respond_toggle(attr, old, new):

    if len(checkbox_group.active)<2:
        tot.visible= False
        if 0 in checkbox_group.active:
            ff.visible = True
            mm.visible = False
            p.y_range.end = max(declared_sums_f) + .1* max(declared_sums_f)
            div_title.text ="""Distribution of total number of majors declared for females"""
#             color_bar.color_mapper = mapperf

        elif 1 in checkbox_group.active:
            mm.visible = True
            ff.visible = False
            p.y_range.end = max(declared_sums_m) +.1* max(declared_sums_m)
            div_title.text="""Distribution of total number of majors declared for males"""
#             color_bar.color_mapper = mapperm

        else:
            ff.visible = False
            mm.visible = False
            div_title.text=""" """

    else:
        tot.visible = 1 in checkbox_group.active
        ff.visible = False
        mm.visible = False
        p.y_range.end = max(declared_sums_tot)+ .1* max(declared_sums_tot)
        div_title.text="""Distribution of total number of majors declared for males and females"""
#         color_bar.color_mapper = mappertot

p.add_tools(hover)
p.add_layout(color_bar, 'right')
for w in [checkbox_group]:
    w.on_change('active',respond_toggle)
p.left[0].formatter.use_scientific = False

p.xaxis.axis_label_text_font_size = "15px"
p.xaxis.major_label_text_font_size = "15px"

p.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
p.yaxis.axis_label_text_font_size = "18px"
p.yaxis.major_label_text_font_size = "18px"

options = widgetbox(checkbox_group)

layout = column(div_title, row(p, checkbox_group), p1, p2, p3)
curdoc().clear()
curdoc().add_root(layout)
curdoc().title = "checkbox"
