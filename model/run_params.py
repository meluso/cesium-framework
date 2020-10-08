# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:27:28 2020

@author: John Meluso
"""

import pickle
import numpy as np

if __name__ == '__main__':

    index = 0  # Index counter for simulation runs
    params = []  # Empty parameter array for simulation

    n = np.array([10,100,1000])
    obj = ["ackley","langermann","levy",""]
    edg = 2
    tri = 0.1
    con = 0.01
    cyc = 100
    tmp = 0.1
    itr = 1
    mthd = "future"
    p = 0.5
    crt = 2.62



