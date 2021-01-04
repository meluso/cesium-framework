# -*- coding: utf-8 -*-

"""
@author: John Meluso
@date: 2020-10-06
@name: run_sim.py

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
import numpy as np
import datetime as dt
import data_manager as dm
import run_model as rm
import get_params as gp
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()


def run_simulation(test_mode=True):

    # Get start time
    t_start = dt.datetime.now()

    # Get parameter values
    params = gp.get_params()

    '''Set running conditions based on platform.'''
    if sys.platform.startswith('linux'):

        # get the number of this job and the total number of jobs from the
        # queue system. These arguments are given by the VACC to this script
        # via submit_job.sh. If there are n jobs to be run total (numruns = n),
        # then casenum should run from 0 to n-1. In notation: [0,n) or [0,n-1].
        try:
            casenum = int(sys.argv[1])
            output_dir = str(sys.argv[2])
        except IndexError:
            sys.exit("Usage: %s casenum numruns" % sys.argv[0] )

    else:

        casenum = rng.integers(len(params))
        output_dir = '../data/test'

    '''Main body of simulation.'''

    # Run simulation for specified set of parameters
    summary, history, system = rm.run_model(params[casenum])

    # Build name for specific test
    case_str = f'case{casenum:06}'
    filename = output_dir + '/' + case_str

    # Save results to location specified by platform
    if test_mode:
        dm.save_data(filename,summary,history,system)
    else:
        dm.save_data(filename,summary,history)

    # Print end time
    t_stop = dt.datetime.now()
    print('Output Filename Base: ' + filename)
    print('Simulation Time Elapsed: ' + str(t_stop - t_start))
    print('[' + str(params[casenum]['nod']) + ', ' \
          + str(params[casenum]['obj'])  + ', 4000mb] >>> ' \
          + str(t_stop - t_start))

    return filename


if __name__ == '__main__':

    # Run the simulation test
    filename = run_simulation()

    # Use filename base to plot test results
    if not(sys.platform.startswith('linux')):
        tp.plot_data(filename)