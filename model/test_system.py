# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-21
@name: test_system.py

-------------------------------------------------------------------------------
Description:

This file tests the system class.

The file takes in the amount of nodes that are present in the system and the
objective function to show how many connections occur between the nodes through
a network diagram.

The plot that follows shows the amount of nodes that have the same amount of
connections.

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.
2019-07-09  jmeluso    Updated to new inputs System(n,obj,edg,tri,con,div,itr).
2019-11-04  jmeluso    Updated to new inputs System(n,obj,edg,tri,con,tmp,crt).

-------------------------------------------------------------------------------
"""

import sys
import data_manager as dm
import run_params as rp
import run_model as rm
import test_plot as tp
from numpy.random import default_rng

# Create the random number generator
rng = default_rng()

if __name__ == '__main__':

    # Specify run mode
    #run_mode = "random"
    run_mode = ""

    if run_mode == "random":

        params_all = rp.run_params()
        case = rng.integers(len(params_all))
        params_run = params_all[case]

    else:

        params_run = {'ind': 999999,
                      'nod': 100,
                      'obj': "griewank",
                      'edg': 2,
                      'tri': 0.4,
                      'con': 0.1,
                      'cyc': 100,
                      'tmp': 0.1,
                      'itr': 1,
                      'mth': "future",
                      'prb': 0.5,
                      'crt': 2.62
                      }

    print(params_run)
    summary, history, system = rm.run_system(params_run)
    dm.save_test(summary, history, system)
    if not(sys.platform.startswith('linux')):
        tp.test_plot()
