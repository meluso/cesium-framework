# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:55:38 2021

@author: John Meluso
"""

import data_manager as dm
import get_params as gp
import numpy as np
import os
import sys


def change_filenames(execnum,outputdir, run_list):
    """Renames file case numbers to match their respective indeces."""

    # Get parameters for specified execution
    params = gp.get_params(execnum)

    # Cycle through parameters and runs for this execution number
    for casenum in np.arange(len(params)):
        for runnum in run_list:

            # Build name for specific test
            case_str = f'case{casenum:06}'
            run_str = f'run{runnum:06}'
            file_prefix = outputdir + '/' + case_str + '_' + run_str

            # Check if the file exists
            try:

                # Get file contents
                summary, history = dm.load_data(file_prefix)

                # Get case number from summary
                summary_case = int(summary[0])
                summary_str = f'case{summary_case:06}'

                # Check if case string matches case number
                if not(summary_str == case_str):
                    new_prefix = outputdir + '/' + summary_str + '_' + run_str
                    os.rename(file_prefix + '_summary.csv',
                              new_prefix + '_summary.csv')
                    os.rename(file_prefix + '_history.csv',
                              new_prefix + '_history.csv')
            except IOError:
                print('No ' + file_prefix)




def get_incompletes(execnum, outputdir, run_list):
    """Identifies runs that didn't save data for the specified execution,
    directory, and list of runs."""

    # Get parameters for specified execution
    params = gp.get_params(execnum)

    # Create empty list for parameter combos that didn't run
    leftovers = []

    # Cycle through parameters and runs for this execution number
    for case in params:
        for runnum in run_list:

            # Get case for testing
            casenum = case['ind']

            # Add run number to case info
            case['run'] = runnum

            # Build name for specific test
            case_str = f'case{casenum:06}'
            run_str = f'run{runnum:06}'
            file_prefix = outputdir + '/' + case_str + '_' + run_str

            # Check if the file exists
            try:
                summary, history = dm.load_data(file_prefix)
            except IOError:
                leftovers.append(case)

    return leftovers


if __name__ == '__main__':

    if sys.platform.startswith('linux'):

        try:
            outputdir = str(sys.argv[1])
            execnum = int(sys.argv[2])
            runlist = np.arange(100)
        except IndexError:
            sys.exit("Usage: %s outputdir" % sys.argv[0] )

    else:

        outputdir = '../data/test'
        execnum = 2
        runlist = [999999]

    change_filenames(execnum, outputdir, runlist)