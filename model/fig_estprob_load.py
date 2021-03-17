# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:31:16 2021

@author: John Meluso
"""

#import math
#import statistics
import numpy as np
import scipy.stats
import data_import as di


def mean_ci(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, h


def load_data():

    # Import data from file
    df = di.import_execset()

    # Create frames for objective functions
    df2obj = {'absolute-sum': df[df['x_objective_fn'] == 'absolute-sum'],
              'sphere': df[df['x_objective_fn'] == 'sphere'],
              'ackley': df[df['x_objective_fn'] == 'ackley'],
              'levy': df[df['x_objective_fn'] == 'levy']}

    obj = ['absolute-sum','sphere','ackley','levy']
    xvar = ['x_num_nodes','x_prob_triangle','x_conv_threshold','x_est_prob']
    yvar = ['y_num_cycles','y_sys_perf']

    # Create dictionary for slice descriptors
    df2obj2desc = {}

    # Loop through objectives
    for jj in np.arange(len(obj)):

        # Create dictionary for x variables and loop through
        df2obj2desc[obj[jj]] = {}
        for xx in np.arange(len(xvar)):

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

    return df2obj2desc