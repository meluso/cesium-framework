# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:02:17 2020

@author: John Meluso
"""

from model_system import System
import datetime as dt
import pickle

def run_system(self, x):
    '''
    Function which loads the table of simulation

    Parameters
    ----------
    x : INT
        DESCRIPTION.

    Returns
    -------
    None.

    '''



    # Start timer
    t_start = dt.datetime.now()

    # Generate a system with n nodes, obj objective function, edg random edges,
    # tri probability of triange, con convergence threshold, tmp for cooling rate,
    # and itr iterations for basin-hopping
    n = 1000
    obj = "ackley"
    edg = 2
    tri = 0.1
    con = 0.01
    cyc = 100
    tmp = 0.1
    itr = 1
    mthd = "future"
    p = 0.5
    crt = 2.62
    s1 = System(n,obj,edg,tri,con,cyc,tmp,itr,mthd,p,crt)

    # Run the system
    results = s1.run()

    # Stop timer
    t_stop = dt.datetime.now()
    print((t_stop - t_start))

    #Save system & results
    pickle.dump(s1, open("test_system.pickle","wb"))
    pickle.dump(results, open("test_results.pickle","wb"))
