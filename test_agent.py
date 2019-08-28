# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-18
@name: test_agent.py

-------------------------------------------------------------------------------
Description:

This file tests the agent class.

The file creantes an agent using its location, the amount of neighbors that it 
has, and the objective funtion that is being used ("ackley", "rosenbrock", 
"styblinski-tang", and "sphere").
The file prints out results for three sets of estimates.  
 
-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.

-------------------------------------------------------------------------------
"""

import model_agent as ag
from numpy.random import random_sample as rand
import matplotlib.pylab as plt

# Create an instance of an agent
a1 = ag.Agent(2,[0,3],"ackley",10,1) 
print(("Location = " + str(a1.location)))
print(("Neighbors = " + str(a1.neighbors)))
print(("Bound = " + str(a1.obj_bounds.xmax)))
print(("Objective function type = " + a1.fn))

# Create a history vector for a set of 4 agents
sys_vect = [ag.Obj_Eval() for i in range(4)]

# Create output vectors for the main agent
x_vals = []
fx_vals = []

# Set initial estimates for the agent
print("--Initial estimate--")
a1.initialize_estimates()
print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx)))

# Create an estimate
print("--1st updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx)))
x_vals.append(a1.curr_est.x)
fx_vals.append(a1.curr_est.fx)

# Create an estimate
print("--2nd updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx)))
x_vals.append(a1.curr_est.x)
fx_vals.append(a1.curr_est.fx)

# Create an estimate
print("--3rd updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx)))
x_vals.append(a1.curr_est.x)
fx_vals.append(a1.curr_est.fx)

plt.scatter(x_vals,fx_vals)
plt.xlabel("Historical x value")
plt.ylabel("Historical f(x) value")
plt.show()