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
    xvar = ['x_prob_triangle','x_est_prob']
    #yvar = ['y_sys_perf']

    # Create dictionary for getting topology descriptors by objective fns
    df2obj2topo = {}

    # Loop through objectives
    for jj in np.arange(len(obj)):
        
        # Create dictionary for group descriptors
        df2obj2topo[obj[jj]] = {}
        
        # Create arrays for groups and their descriptors
        df2obj2topo[obj[jj]]['x_prob_triangle'] = []
        df2obj2topo[obj[jj]]['x_est_prob'] = []
        df2obj2topo[obj[jj]]['mean'] = []
        df2obj2topo[obj[jj]]['ci'] = []
        df2obj2topo[obj[jj]]['std'] = []

        # Get grouped data for this objective function
        curr_slice = df2obj[obj[jj]].groupby(xvar)[['y_sys_perf']]
        
        # Iterate through groups to get means
        for name, df_group in curr_slice:
            
            # Calculate mean and confidence interval for x-y pairing
            mn, ci  = mean_ci(df_group['y_sys_perf'].to_numpy())
            std = df_group['y_sys_perf'].std()
            
            # Append values to lists
            df2obj2topo[obj[jj]]['x_prob_triangle'].append(name[0])
            df2obj2topo[obj[jj]]['x_est_prob'].append(name[1])
            df2obj2topo[obj[jj]]['mean'].append(mn)
            df2obj2topo[obj[jj]]['ci'].append(ci)
            df2obj2topo[obj[jj]]['std'].append(std)
            
    return df2obj2topo


if __name__ == '__main__':
    
    df = load_data()