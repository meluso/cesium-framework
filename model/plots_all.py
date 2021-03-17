# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 15:00:03 2021

@author: John Meluso
"""

#import math
#import statistics
import numpy as np
import scipy.stats
import pandas as pd
import data_import as di
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def mean_ci(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h

# Import data from file
df = di.import_execset()
params = di.import_params()

#%% Slicing ####################

# Create frames for objective functions
df2obj = {'absolute-sum': df[df['x_objective_fn'] == 'absolute-sum'],
          'sphere': df[df['x_objective_fn'] == 'sphere'],
          'ackley': df[df['x_objective_fn'] == 'ackley'],
          'levy': df[df['x_objective_fn'] == 'levy']}

obj = ['absolute-sum','sphere','ackley','levy']
xvar = ['x_num_nodes','x_prob_triangle','x_conv_threshold','x_est_prob']
yvar = ['y_num_cycles','y_sys_perf']

# Create PDF to save data
pp1 = PdfPages('plots_all_split.pdf')
pp2 = PdfPages('plots_all_pareto.pdf')

# Create dictionary for slice descriptors
df2obj2desc = {}

# Loop through objectives
for jj in np.arange(len(obj)):

    # Create dictionary for x variables and loop through
    df2obj2desc[obj[jj]] = {}
    for xx in np.arange(len(xvar)):

        # Create Figure to plot yvars
        fig1, axs1 = plt.subplots(2,len(yvar))
        fig2, axs2 = plt.subplots()
        fig1.suptitle(obj[jj])
        fig2.suptitle(obj[jj] + ' + ' + xvar[xx])

        # Create dictionary for y variables and loop through
        df2obj2desc[obj[jj]][xvar[xx]] = {}
        for yy in np.arange(len(yvar)):

            # Create dictionary for descriptors
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]] = {}

            # Get group for x-y pairing
            curr_slice = df2obj[obj[jj]].groupby(xvar[xx])[[yvar[yy]]]
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['data'] = curr_slice

            # Create arrays for groups and their descriptors
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'] = []
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['mean'] = []
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['ci'] = []
            df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['std'] = []

            # Iterate through groups
            for name, df_group in curr_slice:

                # Calculate mean and confidence interval for x-y pairing
                mn, ci  = mean_ci(df_group[yvar[yy]].to_numpy())
                std = df_group[yvar[yy]].std()

                # Append values to lists
                df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'].append(name)
                df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['mean'].append(mn)
                df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['ci'].append(ci)
                df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['std'].append(std)

            # Plot data for yvar
            axs1[0,yy].set_xlabel(xvar[xx])
            axs1[0,yy].set_ylabel(yvar[yy])
            axs1[0,yy].errorbar(x=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'],
                                y=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['mean'],
                                yerr=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['ci'],
                                ls='',lw=1,marker='o',ms=5)
            axs1[1,yy].set_xlabel(xvar[xx])
            axs1[1,yy].set_ylabel('log(' + str(yvar[yy]) + ')')
            axs1[1,yy].errorbar(x=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'],
                                y=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['mean'],
                                yerr=df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['ci'],
                                ls='',lw=1,marker='o',ms=5)
            axs1[1,yy].set_yscale('log')

        # Plot Pareto fronts
        axs2.set_xlabel('y_num_cycles')
        axs2.set_ylabel('y_sys_perf')
        for gg in np.arange(len(df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'])):
            axs2.errorbar(x=df2obj2desc[obj[jj]][xvar[xx]][yvar[0]]['mean'][gg],
                          y=df2obj2desc[obj[jj]][xvar[xx]][yvar[1]]['mean'][gg],
                          xerr=df2obj2desc[obj[jj]][xvar[xx]][yvar[0]]['ci'][gg],
                          yerr=df2obj2desc[obj[jj]][xvar[xx]][yvar[1]]['ci'][gg],
                          ls='',lw=1,marker='o',ms=5,
                          label=str(df2obj2desc[obj[jj]][xvar[xx]][yvar[yy]]['group'][gg]))

        handles, labels = axs2.get_legend_handles_labels()
        fig2.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.025),
                    borderaxespad=0.,ncol=5)

        # Save plot to pdf
        fig1.tight_layout()
        fig2.tight_layout(rect=(0,0.15,1,1))
        pp1.savefig(fig1)
        pp2.savefig(fig2)

# Close PDFs
pp1.close()
pp2.close()






#%% Variable Description

# Independent variables to try
# - Nodes (x_num_nodes) (4 options)
# - Objective Functions (x_objective_fn) (4 options)
# - Triangle Formation Probability (x_prob_triangle) (11 options)
# - System Convergence Threshold (x_conv_threshold) (7 options)
# - Future Estimate Probability (x_est_prob) (11 options)

# Create array for each input parameter.
# nod = [50, 100, 500, 1000]
# obj = ["absolute-sum","sphere","levy","ackley"]
# edg = [2]
# tri = np.round(np.arange(0,1.1,0.1),decimals=1)
# con = np.array([0.01,0.05,0.1,0.5,1,5,10])
# cyc = [100]
# tmp = [0.1]
# itr = [1]
# mth = ["future"]
# prb = np.round(np.arange(0,1.1,0.1),decimals=1)
# crt = [2.62]

# Dependent variables to try
# - Number of Cycles to Convergence or Timeout (y_num_cycles)
# - Ending System Performance (y_sys_perf)
