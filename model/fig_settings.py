# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:11:05 2021

@author: John Meluso
"""

import matplotlib.pylab as pylab

def set_fonts():
    params = {
        'font.family': 'Times New Roman',
        'mathtext.fontset': 'cm',
        'legend.fontsize': 10,
        'axes.labelsize': 10,
        'axes.titlesize': 12,
        'xtick.labelsize':10,
        'ytick.labelsize':10
        }
    pylab.rcParams.update(params)
    
def fig_size(frac_width,frac_height,n_cols=1,n_rows=1):
    
    # Set default sizes
    page_width = 8.5
    page_height = 11
    side_margins = 1
    tb_margins = 1
    middle_margin = 0.25
    mid_marg_width = middle_margin*(n_cols-1)
    mid_marg_height = middle_margin*(n_rows-1)
    
    # Width logic
    if frac_width == 1:
        width = page_width - side_margins
    else:
        width = (page_width - side_margins - mid_marg_width)*frac_width
        
    # Height logic
    if frac_height == 1:
        height = page_height - tb_margins
    else:
        height = (page_height - tb_margins - mid_marg_height)*frac_height
        
    return (width,height)

def get_formats():
    return ['eps','jpg','pdf','tif']