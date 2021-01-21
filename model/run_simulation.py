# -*- coding: utf-8 -*-

"""
@author: John Meluso
@date: 2020-10-06
@name: run_simulation.py

-------------------------------------------------------------------------------
Description:

This file plots runs the simulation for CESIUM over a range of specified
parameters.

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2020-10-07  jmeluso    Initial version.

-------------------------------------------------------------------------------
"""

import sys
import datetime as dt
import data_manager as dm
import get_params as gp
import numpy as np
import run_model as rm
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()


def run_simulation(mode="test"):

    # Get start time
    t_start = dt.datetime.now()

    '''Set running conditions based on platform.'''

    if sys.platform.startswith('linux'):

        # get the number of this job and the total number of jobs from the
        # queue system. These arguments are given by the VACC to this script
        # via submit_job.sh. If there are n jobs to be run total (numruns = n),
        # then casenum should run from 0 to n-1. In notation: [0,n) or [0,n-1].
        try:

            # Get directory and execution number
            outputdir = str(sys.argv[1])
            execnum = int(sys.argv[2])

            # Get parameters for execution number
            params = gp.get_params(execnum)

            # Get specific case-run combo if mode is single, else get run input
            if mode == "single":
                caseruncombo = int(sys.argv[3])
            elif mode == "subset":
                subset = int(sys.argv[3])
                numsets = int(sys.argv[4])
            else:
                runnum = int(sys.argv[3])

        except IndexError:
            sys.exit("Usage: %s outputdir execnum runnum" % sys.argv[0] )

    else:

        # Get directory and execution number
        outputdir = '../data/test'
        execnum = 10

        # Get parameters for execution number
        params = gp.get_params(execnum)

        # Get specific case-run combo if mode is single, else set top runnum
        if mode == "single":
            caseruncombo = rng.integers(len(params))
        elif mode == "subset":
            numsets = 1000
            subset = rng.integers(numsets)
        else:
            runnum = 999999

    '''Run simulation.'''

    if mode == "test":

        # Select random case for testing
        casenum = rng.integers(len(params))
        case = params[casenum]

        # Add run number to case info
        case['run'] = runnum

        # Run simulation for specified set of parameters
        summary, history, system = rm.run_model(case)

        # Build name for specific test
        case_str = f'case{casenum:06}'
        run_str = f'run{runnum:06}'
        filename = outputdir + '/' + case_str + '_' + run_str

        # Save results to location specified by platform
        dm.save_data(filename,summary,history,system)

        # Print filename
        print('Output Filename Base: ' + filename)

        # Print end time
        t_stop = dt.datetime.now()
        print('Simulation Time Elapsed: ' + str(t_stop - t_start))

        return filename

    elif mode == "single":

        # Run a single case with a specified run number
        case = params[caseruncombo]

        # Get case and run for testing
        casenum = case['ind']
        runnum = case['run']

        # Run simulation for specified set of parameters
        summary, history, system = rm.run_model(case)

        # Build name for specific test
        case_str = f'case{casenum:06}'
        run_str = f'run{runnum:06}'
        filename = outputdir + '/' + case_str + '_' + run_str

        # Save results to location specified by platform
        dm.save_data(filename,summary,history)

        # Print filename
        print('Output Filename Base: ' + filename + '\n')

        # Print end time
        t_stop = dt.datetime.now()

        print('Simulation Time Elapsed: ' + str(t_stop - t_start))

    elif mode == "subset":

        # Get number of parameter combinations in subset
        par_per_sub = int(np.ceil(len(params)/numsets))

        # Get subset of parameters
        sub_params = params[par_per_sub*(subset-1):par_per_sub*subset]

        # Loop through all cases
        for case in sub_params:

            # Get case and run for testing
            casenum = case['ind']
            runnum = case['run']

            # Run simulation for specified set of parameters
            summary, history, system = rm.run_model(case)

            # Build name for specific test
            case_str = f'case{casenum:06}'
            run_str = f'run{runnum:06}'
            filename = outputdir + '/' + case_str + '_' + run_str

            # Save results to location specified by platform
            dm.save_data(filename,summary,history)

            # Print filename
            print('Output Filename Base: ' + filename + '\n')

        # Print end time
        t_stop = dt.datetime.now()

        print('Simulation Time Elapsed: ' + str(t_stop - t_start))

    elif mode == "all":

        # Loop through all cases
        for case in params:

            # Get case for testing
            casenum = case['ind']

            # Add run number to case info
            case['run'] = runnum

            # Run simulation for specified set of parameters
            summary, history, system = rm.run_model(case)

            # Build name for specific test
            case_str = f'case{casenum:06}'
            run_str = f'run{runnum:06}'
            filename = outputdir + '/' + case_str + '_' + run_str

            # Save results to location specified by platform
            dm.save_data(filename,summary,history)

            # Print filename
            print('Output Filename Base: ' + filename + '\n')

        # Print end time
        t_stop = dt.datetime.now()

        print('Simulation Time Elapsed: ' + str(t_stop - t_start))

    else:

        print("Not a valid input. No simulation run.")


if __name__ == '__main__':
    run_simulation("single")