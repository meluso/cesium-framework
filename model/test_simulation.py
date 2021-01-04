# -*- coding: utf-8 -*-

"""
@author: John Meluso
@date: 2020-10-06
@name: test_simulation.py

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
import test_plot as tp
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()


def test_simulation():

    # Get start time
    t_start = dt.datetime.now()

    '''Set running conditions based on platform.'''

    if sys.platform.startswith('linux'):

        # get the number of this job and the total number of jobs from the
        # queue system. These arguments are given by the VACC to this script
        # via submit_job.sh. If there are n jobs to be run total (numruns = n),
        # then casenum should run from 0 to n-1. In notation: [0,n) or [0,n-1].
        try:
            outputdir = str(sys.argv[1])
            execnum = int(sys.argv[2])
            runnum = int(sys.argv[3])
        except IndexError:
            sys.exit("Usage: %s outputdir execnum runnum" % sys.argv[0] )

    else:

        outputdir = '../data/test'
        execnum = 2
        runnum = 999999

    '''Run simulation.'''

    # Get parameter values
    params = gp.get_params(execnum)

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
    print('Case Time Elapsed: ' + str(t_stop - t_start))
    print('[' + str(params[casenum]['nod']) + ', ' \
          + str(params[casenum]['obj'])  + ', 2000mb] >>> ' \
          + str(t_stop - t_start))

    return filename


if __name__ == '__main__':

    # Run the simulation test
    filename = test_simulation()

    # Use filename base to plot test results
    if not(sys.platform.startswith('linux')):
        tp.plot_data(filename)