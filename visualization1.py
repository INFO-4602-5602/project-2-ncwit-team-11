from __future__ import division

from os.path import join, dirname
from math import pi
import pandas as pd
import numpy as np 
from bokeh.io import show, export_png, output_file, curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, NumeralTickFormatter
from bokeh.models.widgets import CheckboxGroup
from bokeh.layouts import row, widgetbox, layout, column
from bokeh.palettes import Spectral6
import pdb
import logging
from operator import add

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
    
    return dat


# Round up CIP #  to two decimal places
def roundupCIPvals(CIP_mat,decl_sums):
    
    CIP_int = []
    for i in range(len(CIP_mat)):
        if CIP_mat[i] != '?':
            CIP_int.append(np.around(float(CIP_mat[i]),2))
        else:
            CIP_int.append(0)
    
    CIP_int_unique = list(np.unique(np.array(CIP_int)))
    
    dec_sums_arr = np.array(decl_sums)
    dec_sums_aug = []
    for cip_no in CIP_int_unique:
        dec_sums_aug.append(np.sum(dec_sums_arr[find(CIP_int,cip_no)]))
        
    CIP_int_unique = [str(c) for c in CIP_int_unique]

    return CIP_int_unique, dec_sums_aug

def retDictionaryMajors(CIP,decl_sums):
    
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
    return majs, decl_sums
    
def retrieveEnroll(mf):

    dat = basicInfo("NCWIT_DataV2.csv");    
    rows = dat.shape[0]
    output_file("bars.html")
    
    CIP_col = dat['CIP# Only']
    CIP_mat = CIP_col.as_matrix()
    CIP_mat = np.unique( np.unique(CIP_mat))
    
    declared_sum = []
    
    for i in range(len(CIP_mat)): 
        dd= dat[dat['CIP# Only']==CIP_mat[i]]
        if mf == 'F':
            declared_sum.append(np.nansum(dd['Totals, Female: Total Declared Majors (Tot. F)'].as_matrix()))
        else:
            declared_sum.append(np.nansum(dd['Totals, Male: Total Declared Majors (Tot. M)'].as_matrix()))
    
    CIP_mat, declared_sum = roundupCIPvals(CIP_mat,declared_sum)
    CIP_mat = np.array(CIP_mat)
    declared_array = np.array(declared_sum)
    declared_idx = np.argsort(declared_array)
    declared_sum = declared_array[declared_idx].tolist()
    CIP_mat = CIP_mat[declared_idx]
    CIP_mat = CIP_mat.tolist()
    
    declared_sum = declared_sum[::-1]
    CIP_mat = CIP_mat[::-1]
    
    return CIP_mat, declared_sum
    

CIP_mat_f, declared_sum_f = retrieveEnroll('F')
CIP_mat_m, declared_sum_m = retrieveEnroll('M')
declared_sum_tot = list(map(add,declared_sum_m,declared_sum_f))

CIP_mat = [float(c) for c in CIP_mat_f ]
Maj_mat, declared_sums_f = retDictionaryMajors(CIP_mat, declared_sum_f)
Maj_mat, declared_sums_m = retDictionaryMajors(CIP_mat, declared_sum_m)
Maj_mat, declared_sums_tot = retDictionaryMajors(CIP_mat, declared_sum_tot)

# define data source for bokeh
sourcef = ColumnDataSource(data=dict(CIP_matf =Maj_mat,dec_sumf=declared_sums_f))
sourcem = ColumnDataSource(data=dict(CIP_matm =Maj_mat ,dec_summ=declared_sums_m))
sourcetot= ColumnDataSource(data=dict(CIP_matm =Maj_mat ,dec_sumtot=declared_sums_tot))

# create figure for bar chart
p = figure(x_range=Maj_mat,plot_width=800, plot_height=500, title="Graduation to enrollment ratio Female",toolbar_location=None, tools="")
p.y_range.start = 0
p.xaxis.major_label_orientation = pi/4
ff = p.vbar(x='CIP_matf', top='dec_sumf', width=0.9, source=sourcef)
mm = p.vbar(x='CIP_matm', top='dec_summ', width=0.9, source=sourcem)
tot =  p.vbar(x='CIP_matm', top='dec_sumtot', width=0.9, source=sourcetot)

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
        elif 1 in checkbox_group.active:
            mm.visible = True
            ff.visible = False
            p.y_range.end = max(declared_sums_m) +.1* max(declared_sums_m)
        else:
            ff.visible = False
            mm.visible = False
        
    else:
        tot.visible = 1 in checkbox_group.active
        ff.visible = False
        mm.visible = False
        p.y_range.end = max(declared_sums_tot)+ .1* max(declared_sums_tot)

for w in [checkbox_group]:
    w.on_change('active',respond_toggle)
p.left[0].formatter.use_scientific = False
p.yaxis[0].formatter = NumeralTickFormatter(format='0,0')
options = widgetbox(checkbox_group)
doc_layout = layout(column(options))
curdoc().clear()
curdoc().add_root(row(p, doc_layout))
curdoc().title = "checkbox"

