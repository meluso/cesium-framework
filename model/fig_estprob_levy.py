# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:31:16 2021

@author: John Meluso
"""

import fig_estprob_load as fel
import matplotlib.pyplot as plt
import fig_settings as fs


fs.set_fonts()

fn_name = 'levy'

# Load data
df2obj2desc = fel.load_data()

# Plot absolute-sum
fig = plt.figure(dpi=300,figsize=fs.fig_size(0.48,0.3))
ax = fig.gca()
ax.set_xlabel('Future Estimate Probability')
ax.set_ylabel('System Performance')
ax.errorbar(x=df2obj2desc[fn_name]['x_est_prob']['y_sys_perf']['group'],
                 y=df2obj2desc[fn_name]['x_est_prob']['y_sys_perf']['mean'],
                 yerr=df2obj2desc[fn_name]['x_est_prob']['y_sys_perf']['ci'],
                 ls='',lw=1,marker='o',ms=5,capsize=5)
fig.tight_layout()

for ff in fs.get_formats():
    fig.savefig('../figures/est_prob_' + fn_name,
                format=ff,
                bbox_inches='tight')