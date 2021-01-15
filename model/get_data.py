# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:55:38 2021

@author: John Meluso
"""

import csv
import data_manager as dm
import get_params as gp
import numpy as np
import os
import pickle
import sys


def os_setup():
    """Configures the function for the current operating system."""

    # Get variables from platform
    if sys.platform.startswith('linux'):

        try:
            outputdir = str(sys.argv[1])
            execnum = int(sys.argv[2])

        except IndexError:
            sys.exit("Usage: %s outputdir" % sys.argv[0] )

    else:

        outputdir = '../data/test'
        execnum = 8

    # Specify outputs based on execution number
    if execnum <= 4:

        # Executions 1-4
        if sys.platform.startswith('linux'):
            run_list = np.arange(100)
        else:
            run_list = [999999]
        return outputdir, execnum, run_list

    else:

        # Executions >= 5
        return outputdir, execnum


def get_exec_set(set_num=0):
    """Defines execution sets and returns specified set."""
    if set_num == 0: # Test set
        exec_set = [1,2]
    elif set_num == 1:
        exec_set = [1,2,3,4,6,7,8,9]
    else:
        print('Not a set. Please check input.')
    return exec_set


def change_filenames_exec001_004(outputdir, execnum, run_list):
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


def run_change_filenames_exec001_004():
    outputdir, execnum, run_list = os_setup()
    change_filenames_exec001_004(outputdir, execnum, run_list)


def get_incompletes(outputdir, execnum, run_list=[]):
    """Identifies runs that didn't save data for the specified execution,
    directory, and list of runs."""

    # Get parameters for specified execution
    params = gp.get_params(execnum)

    # Create empty list for parameter combos that didn't run
    leftovers = []
    counts = np.zeros((len(params),2))
    index_case = 0
    index_count = 1
    case_num = -1

    # Cycle through parameters and runs for this execution number
    for case in params:

        case_num += 1

        # Get case for testing
        casenum = case['ind']
        counts[case_num,index_case] = casenum

        if execnum <= 4:

            for runnum in run_list:

                # Add run number to case info
                case['run'] = runnum

                # Build name for specific test
                case_str = f'case{casenum:06}'
                run_str = f'run{runnum:06}'
                file_prefix = outputdir + '/' + case_str + '_' + run_str

                # Check if the file exists
                try:
                    summary, history = dm.load_data(file_prefix)
                    counts[case_num,index_count] += 1
                except IOError:
                    leftovers.append(case.copy())

        else:

            # Get run number from case info
            runnum = case['run']

            # Build name for specific test
            case_str = f'case{casenum:06}'
            run_str = f'run{runnum:06}'
            file_prefix = outputdir + '/' + case_str + '_' + run_str

            # Check if the file exists
            try:
                summary, history = dm.load_data(file_prefix)
            except IOError:
                leftovers.append(case.copy())

    return leftovers, counts


def run_get_incompletes_exec001_004():
    outputdir, execnum, run_list = os_setup()
    leftovers, counts \
        = get_incompletes(outputdir, execnum, run_list)
    pickle.dump(leftovers, open(f'leftovers_exec{execnum:03}.pickle',"wb"))
    np.save(f'counts_exec{execnum:03}.npy',counts)


def run_get_incompletes_exec005_008():
    outputdir, execnum = os_setup()
    leftovers, counts = get_incompletes(outputdir, execnum)
    pickle.dump(leftovers, open(f'leftovers_exec{execnum:03}.pickle',"wb"))
    np.save(f'counts_exec{execnum:03}.npy',counts)


def load_incompletes(execnum):
    """Loads the incompletes from file."""

    if sys.platform.startswith('linux'):
        save_dir = ''
    else:
        save_dir = '../data/leftovers/'

    return pickle.load(open(save_dir + f'leftovers_exec{execnum:03}.pickle',
                            "rb"))


def run_load_incompletes():
    """Loads incomplete runs for the first four executions and saves them in a
    single structure for use with get_params."""

    exec_list = [1,2,3,4]
    leftovers_all = []

    for execnum in exec_list:
        leftovers = load_incompletes(execnum)

        for ll in leftovers:
            leftovers_all.append(ll.copy())

    pickle.dump(leftovers_all, open("leftovers.pickle","wb"))
    return leftovers_all


def combine_data(outputdir, exec_list):
    """Combines _summary.csv files for the executions specified as input."""

    # Create empty list for storing data
    all_summaries = []
    all_histories = []

    # Iterate over executions provided
    for execnum in exec_list:

        # Set current search directory
        curr_dir = outputdir + f'/exec{execnum:03}'

        # Iterate over files in directory
        for file in os.listdir(curr_dir):

            # Get contents if the file has the summary.csv ending
            if file.endswith('summary.csv'):

                # Open csv file
                with open(curr_dir + '/' + file,"r") as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    all_summaries.append(next(reader))

            elif file.endswith('history.csv'):

                # Open csv file
                with open(curr_dir + '/' + file,"r") as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    line = next(reader)
                    all_histories.append([float(xx) for xx in line])

    return all_summaries, all_histories


def run_combine_data(exec_set):
    """Combines specified executions and saves the summary and history data to
    a single csv for each."""

    # Get variables from platform
    if sys.platform.startswith('linux'):
        try:
            outputdir = str(sys.argv[1])

        except IndexError:
            sys.exit("Usage: %s outputdir" % sys.argv[0] )
    else:
        outputdir = '../data'

    # Get data for specified executions
    exec_list = get_exec_set(exec_set)
    all_summaries, all_histories = combine_data(outputdir, exec_list)

    # Write summary results to file
    filename = outputdir + f'/sets/execset{exec_set:03}_summary.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for caserun in all_summaries:
            writer.writerow(caserun)

    # Write history results to file
    filename = outputdir + f'/sets/execset{exec_set:03}_history.csv'
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for caserun in all_histories:
            writer.writerow(caserun)


if __name__ == '__main__':
    run_combine_data(1)













