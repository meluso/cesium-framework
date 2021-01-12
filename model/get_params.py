# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:27:28 2020

@author: John Meluso
"""

import numpy as np
import pickle

def get_params(exec_num=2):
    """Creates parameters for a simulation."""

    if exec_num == 2:

        # Create array for each input parameter.
        nod = [100]
        obj = ["absolute-sum","sphere","levy","ackley"]
        edg = [2]
        tri = np.round(np.arange(0,1.1,0.1),decimals=1)
        con = np.array([0.01,0.05,0.1,0.5,1,5,10])
        cyc = [100]
        tmp = [0.1]
        itr = [1]
        mth = ["future"]
        prb = np.round(np.arange(0,1.1,0.1),decimals=1)
        crt = [2.62]

        # Iterate through parameters
        params = iterate_pararms(exec_num,nod,obj,edg,tri,con,
                                 cyc,tmp,itr,mth,prb,crt)

    elif exec_num == 3:

        # Create array for each input parameter.
        nod = [500]
        obj = ["absolute-sum","sphere","levy","ackley"]
        edg = [2]
        tri = np.round(np.arange(0,1.1,0.1),decimals=1)
        con = np.array([0.01,0.05,0.1,0.5,1,5,10])
        cyc = [100]
        tmp = [0.1]
        itr = [1]
        mth = ["future"]
        prb = np.round(np.arange(0,1.1,0.1),decimals=1)
        crt = [2.62]

        # Iterate through parameters
        params = iterate_pararms(exec_num,nod,obj,edg,tri,con,
                                 cyc,tmp,itr,mth,prb,crt)

    elif exec_num == 4:

        # Create array for each input parameter.
        nod = [1000]
        obj = ["absolute-sum","sphere","levy","ackley"]
        edg = [2]
        tri = np.round(np.arange(0,1.1,0.1),decimals=1)
        con = np.array([0.01,0.05,0.1,0.5,1,5,10])
        cyc = [100]
        tmp = [0.1]
        itr = [1]
        mth = ["future"]
        prb = np.round(np.arange(0,1.1,0.1),decimals=1)
        crt = [2.62]

        # Iterate through parameters
        params = iterate_pararms(exec_num,nod,obj,edg,tri,con,
                                 cyc,tmp,itr,mth,prb,crt)

    elif exec_num == 5:

        # Load parameter list from pickle
        # 0 Leftover from initial run
        params = pickle.load(open("leftovers_exec001.pickle","rb"))

    elif exec_num == 6:

        # Load parameter list from pickle
        # 3407 leftover from initial run
        params = pickle.load(open("leftovers_exec002.pickle","rb"))

    elif exec_num == 7:

        # Load parameter list from pickle
        # 6679 leftover from initial run
        params = pickle.load(open("leftovers_exec003.pickle","rb"))

    elif exec_num == 8:

        # Load parameter list from pickle
        # 10190 leftover from initial run
        params = pickle.load(open("leftovers_exec004.pickle","rb"))

    elif exec_num == 9:

        # Load parameter list from pickle
        # 274 leftover from execution 274
        params = pickle.load(open("leftovers_exec008.pickle","rb"))

    else: # exec_num == 1:

        # Create array for each input parameter.
        nod = [50]
        obj = ["absolute-sum","sphere","levy","ackley"]
        edg = [2]
        tri = np.round(np.arange(0,1.1,0.1),decimals=1)
        con = np.array([0.01,0.05,0.1,0.5,1,5,10])
        cyc = [100]
        tmp = [0.1]
        itr = [1]
        mth = ["future"]
        prb = np.round(np.arange(0,1.1,0.1),decimals=1)
        crt = [2.62]

        # Iterate through parameters
        params = iterate_pararms(exec_num,nod,obj,edg,tri,con,
                                 cyc,tmp,itr,mth,prb,crt)

    # Return parameters
    return params


def iterate_pararms(exec_num,nod,obj,edg,tri,con,cyc,tmp,itr,mth,prb,crt):
    """Iterates through a set of parameter ranges to construct a full list of
    cases to run."""

    # Count of new, unique cases created for each execution for unique indexing
    case_count = [3388,3388,3388,3388,0,0,0,0,0]

    # Index counter initialization for simulation runs
    index = sum(case_count[0:exec_num-1])-1

    # Empty parameter array for simulation
    params = []

    # Iteratively construct dictionaries and populate the parameter list.
    for nn in np.arange(len(nod)):
        for oo in np.arange(len(obj)):
            for ee in np.arange(len(edg)):
                for tr in np.arange(len(tri)):
                    for co in np.arange(len(con)):
                        for cy in np.arange(len(cyc)):
                            for tm in np.arange(len(tmp)):
                                for ii in np.arange(len(itr)):
                                    for mm in np.arange(len(mth)):
                                        for pp in np.arange(len(prb)):
                                            for cr in np.arange(len(crt)):
                                                index += 1
                                                new_params \
                                                    = {'ind': index,
                                                       'run': -1,
                                                       'nod': nod[nn],
                                                       'obj': obj[oo],
                                                       'edg': edg[ee],
                                                       'tri': tri[tr,],
                                                       'con': con[co,],
                                                       'cyc': cyc[cy],
                                                       'tmp': tmp[tm],
                                                       'itr': itr[ii],
                                                       'mth': mth[mm],
                                                       'prb': prb[pp],
                                                       'crt': crt[cr]
                                                       }
                                                params.append(new_params)

    # Return parameters
    return params


if __name__ == '__main__':
    params = get_params(8)