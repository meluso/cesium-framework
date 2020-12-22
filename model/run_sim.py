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


def run_simulation():

    # Get start time
    t_start = dt.datetime.now()

    # Get parameter values
    params = gp.get_params()

    '''Set running conditions based on platform.'''
    if sys.platform.startswith('linux'):

        # get the number of this job and the total number of jobs from the
        # queue system. These arguments are given by the VACC to this script
        # via submit_job.sh. If there are n jobs to be run total (numruns = n),
        # then callnum should run from 0 to n-1. In notation: [0,n) or [0,n-1].
        try:
            callnum = int(sys.argv[1])
            output_dir = str(sys.argv[2])
        except IndexError:
            sys.exit("Usage: %s callnum numruns" % sys.argv[0] )

    else:

        callnum = rng.integers(len(params))
        output_dir = '../data/test'

    '''Main body of simulation.'''

    # Run simulation for specified set of parameters
    summary, history, system = rm.run_model(params[callnum])

    # Build name for specific test
    call_str = f'call{callnum:09}'
    filename = output_dir + '/' + call_str

    # Save results to location specified by platform
    dm.save_data(filename,summary,history,system)

    # Print end time
    t_stop = dt.datetime.now()
    print('Output Filename Base: ' + filename + '\n')

    return filename

    print('Simulation Time Elapsed: ' + str(t_stop - t_start) + '\n')


if __name__ == '__main__':
    run_simulation()