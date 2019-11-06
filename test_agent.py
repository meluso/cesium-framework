# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-18
@name: test_agent.py

-------------------------------------------------------------------------------
Description:

This file tests the agent class.

The file creantes an agent using its location, the amount of neighbors that it 
has, and the objective funtion that is being used. The file prints out results
for a specified (iterations) number of estimates.
 
-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.
2019-10-28  jmeluso    Updated to allow for a specified number of iterations
                       and added clearer comments.

-------------------------------------------------------------------------------
"""

import model_agent as ag
from numpy.random import random_sample as rand
import matplotlib.pylab as plt

# Number of iterations to run the agent test
iterations = 25

# Create an instance of an agent
index = 2
a1 = ag.Agent(loc=index,nbr=[0,3],obj="levy",tmp=1000,crt=2.62) 
print(("Location = " + str(a1.location)))
print(("Neighbors = " + str(a1.neighbors)))
print(("Min Bound = " + str(a1.obj_bounds.xmin)))
print(("Max Bound = " + str(a1.obj_bounds.xmax)))
print(("Objective function type = " + a1.fn))

# Create output vectors for the main agent
x_vals = []
fx_vals = []

# Set initial estimates for the agent
print("--Initial estimate--")
a1.initialize_estimates()

# Create initialization vector for system
init_vect = [(a1.obj_bounds.xmax-a1.obj_bounds.xmin)*rand()+a1.obj_bounds.xmin,
             (a1.obj_bounds.xmax-a1.obj_bounds.xmin)*rand()+a1.obj_bounds.xmin,
             (a1.obj_bounds.xmax-a1.obj_bounds.xmin)*rand()+a1.obj_bounds.xmin,
             (a1.obj_bounds.xmax-a1.obj_bounds.xmin)*rand()+a1.obj_bounds.xmin]
init_vect[index] = a1.curr_est.x

# Populate f(x) values based on initial values
a1.initialize_evaluations(init_vect)

# Save the initial estimate to the archival vectors
x_vals.append(a1.curr_est.x)
fx_vals.append(a1.curr_est.fx)

print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " \
       + str(a1.curr_est.fx)))

# Create an estimate
for ind in range(0,iterations):
    
    # Print title for this iteration of the test
    print("--Update " + str(ind+1) + "--")
    
    # Populate the system vector with random data
    sys_vect = [ag.Obj_Eval((a1.obj_bounds.xmax-a1.obj_bounds.xmin)*\
                            rand()+a1.obj_bounds.xmin,0),
                ag.Obj_Eval((a1.obj_bounds.xmax-a1.obj_bounds.xmin)*\
                            rand()+a1.obj_bounds.xmin,0),
                ag.Obj_Eval((a1.obj_bounds.xmax-a1.obj_bounds.xmin)*\
                            rand()+a1.obj_bounds.xmin,0),
                ag.Obj_Eval((a1.obj_bounds.xmax-a1.obj_bounds.xmin)*\
                            rand()+a1.obj_bounds.xmin,0)]
                
    # Fill the estimate into the appropriate system vector slots (at index)
    sys_vect[index].x = a1.curr_est.x
    sys_vect[index].fx = a1.curr_est.fx

    # Generate a new estiamte from the system vector
    received_est = a1.generate_estimate(sys_vect)
    
    # Save the updated estimate to the archival vectors
    x_vals.append(a1.curr_est.x)
    fx_vals.append(a1.curr_est.fx)
    
    # Print the updated estimate
    print(("Current estimate = f(" + str(a1.curr_est.x) + ") = " \
           + str(a1.curr_est.fx)))

# Plot x values vs f(x) values
plt.scatter(x_vals,fx_vals)
plt.xlabel("Historical x value")
plt.ylabel("Historical f(x) value")
plt.show()

# Plot historical trend
plt.plot(fx_vals)
plt.xlabel("Iteration")
plt.ylabel("f(x) value")
plt.show()
