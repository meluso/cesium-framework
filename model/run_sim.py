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
import run_params as rp
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()


def run_simulation(test_mode=False):

    # Get start time
    t_start = dt.datetime.now()

    '''Set running conditions based on platform.'''
    if sys.platform.startswith('linux'):

        # get the number of this job and the total number of jobs from the
        # queue system. These arguments are given by the VACC to this script
        # via submit_job.sh. If there are n jobs to be run total (numruns = n),
        # then runnum should run from 0 to n-1. In notation: [0,n) or [0,n-1].
        try:
            runnum = int(sys.argv[1])
            output_dir = str(sys.argv[2])
        except IndexError:
            sys.exit("Usage: %s runnum numruns" % sys.argv[0] )

    else:

        runnum = 999999
        output_dir = '../data/test'

    '''Main body of simulation.'''

    # Get parameter values
    params = rp.run_params()

    if test_mode == True:

        # Select random case for testing
        case = rng.integers(len(params))

        # Run simulation for specified set of parameters
        summary, history, system = rm.run_system(params[case])

        # Build name for specific test
        case_str = f'case{case:06}'
        job_str = f'run{runnum:06}'
        filename = output_dir + '/' + case_str + '_' + job_str

        # Save results to location specified by platform
        dm.save_data(filename,summary,history,system)

        # Print end time
        t_stop = dt.datetime.now()
        print(t_stop - t_start)
        print(filename)

        return filename

    else:

        # Loop through all cases
        for case in np.arange(len(params)):

            # Run simulation for specified set of parameters
            summary, history, system = rm.run_system(params[case])

            # Build name for specific test
            case_str = f'case{case:06}'
            job_str = f'run{runnum:06}'
            filename = output_dir + '/' + case_str + '_' + job_str

            # Save results to location specified by platform
            dm.save_data(filename,summary,history)

        # Print end time
        t_stop = dt.datetime.now()
        print(t_stop - t_start)


if __name__ == '__main__':
    run_simulation()