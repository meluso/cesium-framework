# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:42:36 2021

@author: John Meluso
"""

import get_params as gp
import numpy as np
import matplotlib.pyplot as plt
from model_agent import Objective
import run_model as rm


if __name__ == '__main__':

    params_run = {'ind': 999999,
                  'run': 999999,
                  'nod': 2,
                  'obj': "levy",
                  'edg': 1,
                  'tri': 0.0,
                  'con': 0.1,
                  'cyc': 10,
                  'tmp': 10,
                  'itr': 1,
                  'mth': "future",
                  'prb': 0.5,
                  'crt': 2.62
                  }

    summary, history, system = rm.run_model(params_run)

#history = [9.730880338936295, 9.730880338936295, 9.730880338936295, 0.16826342605191372, 0.0476644561474772, 0.0476644561474772, 0.0476644561474772, 0.0476644561474772]