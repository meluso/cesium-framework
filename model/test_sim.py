# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:55:11 2020

@author: John Meluso
"""

import run_sim as rs
import test_plot as tp

# Run test simulation
filename = rs.run_simulation(True)

# Use filename base to plot test results
tp.plot_data(filename)