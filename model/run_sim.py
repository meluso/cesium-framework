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

import sys, os
import numpy as np
import cPickle as pickle

if __name__ == '__main__':

    # get the number of this job and the total number of jobs from the PBS
    # queue system. These arguments are given by the VACC to this script via
    # submit_job.sh. If there are n jobs to be run total (NUMJOBS = n), then
    # JOBNUM should run from 0 to n-1. In notation: [0,n) or [0,n-1].
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

    # build a big list of all combinations of parameters and runs, for the
    # simulations for ALL jobs:
    list_parameter1 = np.arange(0,1.0,10)
    list_parameter2 = np.arange(-1,1,100)
    num_runs = 100 # perform, in this case, 100 identical runs for each pair of parameters (to average over)
    params = []
    for p in list_parameter1:
        for q in list_parameter2:
            for r in range(num_runs):
                params.append((p,q,r))

    # now keep only the parameters for THIS job:
    params = [p for i,p in enumerate(params) if i % NUMJOBS == JOBNUM]
    # (this will spread the parameters evenly over the parallel jobs)


    # prep output directory
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # run the simulations for THIS job:
    for p,q,r in params:

        var1,var2 = SIMULATION(p1,p2) # replace with actual simulation code
        # (This example assumes each sim creates two output variables. this
        # depends on what you are specifically doing.)

        # save any files for this simulation:
        parameter_slug = "p%0.2f_q%0.2f_run%04d" % (p1,p2,r)
        pickle.dump(simulation_var1, open('%s/simVar1__%s.pkl' % (output_dir,parameter_slug), 'wb'), protocol=-1)
        pickle.dump(simulation_var2, open('%s/simVar2__%s.pkl' % (output_dir,parameter_slug), 'wb'), protocol=-1)
        # (This is saving the variables as python pickles, but it may be better
        # for your actual simulation to save csv files or some other format.)


