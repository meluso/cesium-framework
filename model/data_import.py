# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 13:40:40 2021

@author: John Meluso
"""

import get_data as gd
import get_params as gp
import math
import statistics
import numpy as np
import scipy.stats
import pandas as pd

def import_execset(execset=1):
    """Imports data from a specified execution set and returns a dataframe
    sorted by case number and run number."""

    # Specify dataframe inputs
    names = ['index_case',
             'index_run',
             'x_num_nodes',
             'x_objective_fn',
             'x_num_edges',
             'x_prob_triangle',
             'x_conv_threshold',
             'x_max_cycles',
             'x_init_temp',
             'x_anneal_iter',
             'x_est_method',
             'x_est_prob',
             'x_anneal_coolrate',
             'y_num_cycles',
             'y_sys_perf']
    types = {'index_case': np.int32,
             'index_run': np.int32,
             'x_num_nodes': np.int32,
             'x_objective_fn': 'category',
             'x_num_edges': np.int32,
             'x_prob_triangle': np.float64,
             'x_conv_threshold': np.float64,
             'x_max_cycles': np.int32,
             'x_init_temp': np.float64,
             'x_anneal_iter': np.int32,
             'x_est_method': 'category',
             'x_est_prob': np.float64,
             'x_anneal_coolrate': np.float64,
             'y_num_cycles': np.int32,
             'y_sys_perf': np.float64}

    # Read from CSV file
    df = pd.read_csv(f'../data/sets/execset{execset:03}_summary.csv',
                     names=names, dtype=types)

    # Sort the new dataframe by case and run
    df.sort_values(by=['index_case','index_run'],axis=0, inplace=True)
    df.reset_index(drop=True,inplace=True)

    # Return the dataframe
    return df


def import_params(exec_list=[1,2,3,4],run_list=np.arange(100)):

    params_all = []

    # Iterate through executions
    for execnum in exec_list:

        # Get parameters for each execution number
        params_subset = gp.get_params(execnum)

        for ps in params_subset:
            params_all.append(ps.copy())

    return params_all


if __name__ == '__main__':

    # Import data
    params = import_params()

