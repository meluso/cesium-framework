# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:02:17 2020

@author: John Meluso
"""

import sys
import datetime as dt
import data_manager as dm
import model_system as sy
import get_params as gp
import test_plot as tp
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()


def run_model(params):
    """Function which runs one instance of the system model for a given set of
    input parameters and saves the resulting data."""

    # Print input parameters
    print('Run parameters: ' + str(params) + '\n')

    # Start timer
    t_start = dt.datetime.now()

    # Generate a system with nod nodes, obj objective function, edg random
    # edges, tri probability of triange, con convergence threshold, cyc for
    # number of the max number of design cycles, tmp for the initial temp of
    # the dual annealing algorithm, itr iterations per call of the dual
    # annealing algorithm, mth the estimate methods agents are allowed to use,
    # prb probability that an agent will use a future estimate, and crt the
    # cooling rate of the dual annealing algorithm.
    system = sy.System(params['nod'],params['obj'],params['edg'],params['tri'],
                       params['con'],params['cyc'],params['tmp'],params['itr'],
                       params['mth'],params['prb'],params['crt'])

    # Run the system
    results = system.run()

    # Stop timer
    t_stop = dt.datetime.now()
    print('Run Time Elapsed: ' + str(t_stop - t_start) + '\n')

    # Build data to return
    summary = [params['ind'], params['run'],
               params['nod'], params['obj'], params['edg'],
               params['tri'], params['con'], params['cyc'],
               params['tmp'], params['itr'], params['mth'],
               params['prb'], params['crt'],
               results.design_cycles, results.perf_system[-1]]

    history = results.perf_system

    # Return results
    return summary, history, system


if __name__ == '__main__':
    params = gp.get_params()
    case = rng.integers(len(params))
    summary, history, system = run_model(params[case])
    dm.save_test(summary, history, system)
    if not(sys.platform.startswith('linux')):
        tp.plot_test()