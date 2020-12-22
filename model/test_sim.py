# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:55:11 2020

@author: John Meluso
"""

import sys
import run_sim as rs
import test_plot as tp

# Run test simulation
filename = rs.run_simulation()

# Use filename base to plot test results
if not(sys.platform.startswith('linux')):
    tp.plot_data(filename)