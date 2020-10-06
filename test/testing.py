#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: rojanov

_______________________________________________________________________________
Description:
    
    This script aims to test all of the functions that are present in the 
    script model_agent. The script contains a total of 5 agents with different
    properties. The agents all obtain an initial estimate. The estimate is then 
    optimized usiing dual annealing and based in the objective function given 
    to that agent. The user is given the option to see every estimate that was 
    generated at the start. /


_______________________________________________________________________________

"""
import model_agent as ag
from numpy.random import random_sample as rand 
import matplotlib.pyplot as plt

#Gives the user the option to see that plots for all 5 agents
figure = input("Would you like to see the plots for all 5 agents? (y/n):\n")

# Gives the user the option to view all of the estimates that were generated 
# during the optimization - the anount of estimates generated is equal to the
# number of iterations that the agent has
estimates = input("Would you like to see all of the estimates generated during optimization? (y/n):\n")

print("____________________________________________________________")
'''Agent 1'''
#Test the function agent by creating an instance of an agent and give it a 
#location, neighbors, an objective function, iterations and domain divisions.
print ("First Agent") 

agent1 =  ag.Agent(2,[0,4],"sphere", 1000,2.62,35)
print ("Agent One Location: " + str(agent1.location)) 
print ("Agent One Neighbors: " + str(agent1.neighbors))
print ("Agent One Objective Function: " + str(agent1.fn))
print ("Max Bound: " + str(agent1.obj_bounds.xmax))
print ("Min Bound: " + str(agent1.obj_bounds.xmin))
print ("Agent One Iterations: " + str(agent1.iterations))
print ("   ")
x_val1 = []
fx_val1 = [] 
#Create the estimate for the agent
agent1.initialize_estimates()

itr1=agent1.iterations

obj_vect1 = [rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,
             rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,
             rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,
             rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,
             rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin]
    
agent1.initialize_evaluations(obj_vect1)
x_val1.append(agent1.curr_est.x) ###adding the agent's estimate to sys_vect1
fx_val1.append(agent1.curr_est.fx)

for i in range(0,itr1):     

    sys_vect1 =[ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent1.obj_bounds.xmax-agent1.obj_bounds.xmin)+agent1.obj_bounds.xmin,0)]
    
    agent1.initialize_estimates()

    x_val1.append(agent1.curr_est.x) ###adding the agent's estimate to sys_vect1

##use initialize_evaluations to create an fx value for the agent's current x value
    fx_val1.append(agent1.curr_est.fx)

    received_est1 = agent1.generate_estimate(sys_vect1)

#prints out every estimate that was created for the agent during optimization
    if estimates == "y":
        print ("Agent One Estimate Input (x): " + str(agent1.curr_est.x)) 
        print ("Agent One Estimate Output (fx): " + str(agent1.curr_est.fx))
        print ("    ")

print ("Minimum value obtained of fx for Agent 1: " + str(min(fx_val1)))
minfx = min(fx_val1)
fxmindex = fx_val1.index(min(fx_val1)) 
#xmindex = x_val1.index(fxmindex) #currently looks for the value in the vector and gives the index that corresponds to that values

for i in x_val1:
    if  agent1.curr_est.x < agent1.obj_bounds.xmin and agent1.curr_est.x > agent1.obj_bounds.xmax:
        print (x_val1.index()) 
   
            #can this be printed out once - or make it only print for errors?

if figure == "y":
#How f_x changes over time 
    plt.plot(fx_val1) 
    plt.show()
    plt.scatter(x_val1,fx_val1)
    plt.show()

print ("   ") ##Provides a break between the agents that are being printed

print("____________________________________________________________")
'''Agent 2'''
#Creating A Second Agent
print("Second Agent")
agent2 =  ag.Agent(7,[1,8,3,6],"ackley", 1000,2.62,50)  #problem with ackley
print ("Agent Two Location: " + str(agent2.location)) 
print ("Agent Two Neighbors: " + str(agent2.neighbors))
print ("Agent Two Objective Function: " + str(agent2.fn))
print ("Max Bound: " + str(agent2.obj_bounds.xmax))
print ("Min Bound: " + str(agent2.obj_bounds.xmin))
print ("Agent Two Iterations: " + str(agent2.iterations))
print (" ")
x_val2 = []
fx_val2 = [] 

agent2.initialize_estimates()

itr2=agent2.iterations

obj_vect2 = [rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,
             rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin]
    
agent2.initialize_evaluations(obj_vect2)
x_val2.append(agent2.curr_est.x) ###adding the agent's estimate to sys_vect2
fx_val2.append(agent2.curr_est.fx)

for i in range(0,itr2): 
    
    sys_vect2 =[ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent2.obj_bounds.xmax-agent2.obj_bounds.xmin)+agent2.obj_bounds.xmin,0)]
    
    x_val2.append(agent2.curr_est.x)
    fx_val2.append(agent2.curr_est.fx)
    received_est2 = agent2.generate_estimate(sys_vect2)

    if estimates == "y":    
  #prints every estimate created for agent 2
        print ("Agent Two Estimate Input (x): " + str(agent2.curr_est.x)) 
        print ("Agent Two Estimate Output (fx): " + str(agent2.curr_est.fx))
        print ("    ")
    
print ("Minimum value obtained of fx for Agent 2: " + str(min(fx_val2)))
minfx2 = min(fx_val2)
fxmindex2 = fx_val2.index(min(fx_val2)) 

if figure == "y":
    plt.plot(fx_val2) 
    plt.show()

    plt.scatter(x_val2,fx_val2)
    plt.show()

print("    ")

print("____________________________________________________________")

'''Agent 3'''
#Creating A Third Agent
print("Third Agent")
agent3 =  ag.Agent(11,[7,12,2,5,8,11],"rosenbrock", 1000,2.62,24)
print ("Agent Three Location: " + str(agent3.location)) 
print ("Agent Three Neighbors: " + str(agent3.neighbors))
print ("Agent Three Objective Function: " + str(agent3.fn))
print ("Max Bound: " + str(agent3.obj_bounds.xmax))
print ("Min Bound: " + str(agent3.obj_bounds.xmin))
print ("Agent Three Iterations: " + str(agent3.iterations))
print (" ")

x_val3 = []
fx_val3 = [] 
agent3.initialize_estimates()

itr3 = agent3.iterations

obj_vect3 = [rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,
             rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin]

agent3.initialize_evaluations(obj_vect3)
x_val3.append(agent3.curr_est.x)
fx_val3.append(agent3.curr_est.fx) 

for i in range(0,itr3):

    sys_vect3 =[ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent3.obj_bounds.xmax-agent3.obj_bounds.xmin)+agent3.obj_bounds.xmin,0)]
    
    agent3.initialize_estimates()
    x_val3.append(agent3.curr_est.x)
    fx_val3.append(agent3.curr_est.fx) 
    received_est3 = agent3.generate_estimate(sys_vect3)
    
    if estimates == "y":    
  
        print ("Agent Three Estimate Input (x): " + str(agent2.curr_est.x)) 
        print ("Agent Three Estimate Output (fx): " + str(agent2.curr_est.fx))
        print ("    ")


print ("Minimum value obtained of fx for Agent 3: " + str(min(fx_val3)))
minfx3 = min(fx_val3)
fxmindex3 = fx_val3.index(min(fx_val3)) 

if figure == "y":
    plt.plot(fx_val3) 
    plt.show()

    plt.scatter(x_val3,fx_val3)
    plt.show()

print("    ")

print("____________________________________________________________")
'''Agent 4'''
#Creating A Fourth Agent
print("Fourth Agent")
agent4 =  ag.Agent(9,[1,4,6,7,9],"ackley",1000,2.62,26)
print ("Agent Four Location: " + str(agent4.location)) 
print ("Agent Four Neighbors: " + str(agent4.neighbors))
print ("Agent Four Objective Function: " + str(agent4.fn))
print ("Max Bound: " + str(agent4.obj_bounds.xmax))
print ("Min Bound: " + str(agent4.obj_bounds.xmin))
print ("Agent Four Iterations: " + str(agent4.iterations))
print (" ")

x_val4 = []
fx_val4 = [] 
agent4.initialize_estimates()

itr4 = agent4.iterations 

obj_vect4 = [rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,
             rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin]

agent4.initialize_evaluations(obj_vect4)
x_val4.append(agent4.curr_est.x)
fx_val4.append(agent4.curr_est.fx)

for i in range(0, itr4): 

    sys_vect4 =[ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent4.obj_bounds.xmax-agent4.obj_bounds.xmin)+agent4.obj_bounds.xmin,0)]

    agent4.initialize_estimates()
    x_val4.append(agent4.curr_est.x)
    fx_val4.append(agent4.curr_est.fx)
    received_est4 = agent4.generate_estimate(sys_vect4)
        
    if estimates == "y":
        print ("Initial Agent Four Estimate Input (x): " + str(agent4.curr_est.x))
        print ("Agent Four Estimate Output (fx): " + str(agent4.curr_est.fx))

print ("Minimum value obtained of fx for Agent 4: " + str(min(fx_val4)))
minfx4 = min(fx_val4)
fxmindex4 = fx_val4.index(min(fx_val4))

if figure == "y":
    plt.plot(fx_val4) 
    plt.show()

    plt.scatter(x_val4,fx_val4)
    plt.show()

print("    ")

print("____________________________________________________________")
'''Agent 5'''
#Creating A Fifth Agent
print("Fifth Agent")
agent5 =  ag.Agent(18,[19,23,4,7,2,15,18,22,10,2],"styblinski-tang", 1000,2.62,18)
print ("Agent Five Location: " + str(agent5.location)) 
print ("Agent Five Neighbors: " + str(agent5.neighbors))
print ("Agent Five Objective Function: " + str(agent4.fn))
print ("Max Bound: " + str(agent5.obj_bounds.xmax))
print ("Min Bound: " + str(agent5.obj_bounds.xmin))
print ("Agent Five Iterations: " + str(agent5.iterations))
print (" ")

x_val5 = []
fx_val5 = [] 
agent5.initialize_estimates()

itr5 = agent5.iterations

obj_vect5 = [rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,
             rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin]

agent5.initialize_evaluations(obj_vect5)
x_val1.append(agent5.curr_est.x) ###adding the agent's estimate to sys_vect1
fx_val1.append(agent5.curr_est.fx)


for i in range(0,itr5):

    sys_vect5 =[ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0),
                ag.Obj_Eval(rand()*(agent5.obj_bounds.xmax-agent5.obj_bounds.xmin)+agent5.obj_bounds.xmin,0)]
    
    agent5.initialize_estimates()
    x_val5.append(agent5.curr_est.x)
    fx_val5.append(agent5.curr_est.fx) 
    received_est5 = agent5.generate_estimate(sys_vect5)
    
    if estimates == "y":
        print ("Initial Agent Five Estimate Input (x): " + str(agent5.curr_est.x))
        print ("Agent Five Estimate Output (fx): " + str(agent5.curr_est.fx))
        print("    ")
    
print("     ")

print ("Minimum value obtained of fx for Agent 5: " + str(min(fx_val5)))
minfx5 = min(fx_val5)
fxmindex5 = fx_val5.index(min(fx_val5))

if figure == "y":
    plt.plot(fx_val5) 
    plt.show()

    plt.scatter(x_val5,fx_val5)
    plt.show()

print("____________________________________________________________")

    
print ("    ")
## Has the agent failed or passed the test? - How many have they failed?
#### Starting with a counter -- How mant passed how many fail

#objective funtions bounds
ackley_min = -32.768
ackley_max = 32.768
griewank_min = -600.00
griewank_max = 600.00
langermann_min = 0.00
langermann_max = 10.00
levy_min = -10.00
levy_max = 10.00
rosenbrock_min = -5.00
rosenbrock_max = 10.00
schwefel_min = -500.00
schwefel_max = 500.00
sphere_min = -5.12
sphere_max = 5.12
styblinskitang_min = -5
styblinskitang_max = 5

pass_count1 = 0 
fail_count1 = 0

if agent1.obj_bounds.xmin == sphere_min and agent1.obj_bounds.xmax == sphere_max:
    pass_count1 += 1
else:
    fail_count1 += 1
    print ("The agent is not using the correct function bounds")

if  fx_val1[0] > minfx:
    pass_count1 +=1
else:
    fail_count1 += 1
    print ("Agent 1 was not optimzed")
    
for i in x_val1:
    if all(x_val1) < agent1.obj_bounds.xmax and all(x_val1) > agent1.obj_bounds.xmin: 
             bounds_check1 = 'true' 
    else:
        bounds_check1 ='false'
        print ("The estimation inputs are not within the objective function bound")
if bounds_check1 == 'true':
    pass_count1 +=1
else:
    fail_count1 +=1
    
if len(x_val1) == len(fx_val1): #checks if the number out inputs and outputs match
    pass_count1 +=1
else:
    fail_count1 +=1
    print ("The number of outputs does not match the number of outputs")

    
print ("Amount of Tests Agent 1 has passed = " + str(pass_count1))
print ("Amount of Tests Agent 1 has failed = " + str(fail_count1))
 ##
print (" ")
pass_count2 = 0 
fail_count2 = 0

if agent2.obj_bounds.xmin == ackley_min and agent2.obj_bounds.xmax == ackley_max:
    pass_count2 += 1
else:
    fail_count2 += 1
    print ("The agent is not using the correct function bounds")

if  fx_val2[0] > minfx2:
    pass_count2 +=1
else:
    fail_count2 += 1
    print ("Agent 2 was not optimzed")
    
for i in x_val2:
    if all(x_val2) < agent2.obj_bounds.xmax and all(x_val2) > agent2.obj_bounds.xmin: 
             bounds_check2 = 'true' 
    else:
        bounds_check2 ='false'
        print ("The estimation inputs are not within the objective function bound")
if bounds_check2 == 'true':
    pass_count2 +=1
else:
    fail_count2 +=1

if len(x_val2) == len(fx_val2): #checks if the number out inputs and outputs match
    pass_count2 +=1
else:
    fail_count2 +=1
    print ("The number of outputs does not match the number of outputs")

    
print ("Amount of Tests Agent 2 has passed = " + str(pass_count2))
print ("Amount of Tests Agent 2 has failed = " + str(fail_count2))

print(" ")
pass_count3 = 0 
fail_count3 = 0

if agent3.obj_bounds.xmin == rosenbrock_min and agent3.obj_bounds.xmax == rosenbrock_max:
    pass_count3 += 1
else:
    fail_count3 += 1
    print ("The agent is not using the correct function bounds")

if  fx_val3[0] > minfx3:
    pass_count3 +=1
else:
    fail_count3 += 1
    print ("The Agent was not optimzed")
    
for i in x_val3:
    if all(x_val3) < agent3.obj_bounds.xmax and all(x_val3) > agent3.obj_bounds.xmin: 
             bounds_check3 = 'true' 
    else:
        bounds_check3 ='false'
        print ("The estimation inputs are not within the objective function bound")
if bounds_check3 == 'true':
    pass_count3 +=1
else:
    fail_count3 +=1

if len(x_val3) == len(fx_val3): #checks if the number out inputs and outputs match
    pass_count3 +=1
else:
    fail_count3 +=1
    print ("The number of outputs does not match the number of outputs")
    
print ("Amount of Tests Agent 3 has passed = " + str(pass_count3))
print ("Amount of Tests Agent 3 has failed = " + str(fail_count3))
print(" ")


pass_count4 = 0 
fail_count4 = 0

if agent4.obj_bounds.xmin == ackley_min and agent4.obj_bounds.xmax == ackley_max:
    pass_count4 += 1
else:
    fail_count4 += 1
    print ("The agent is not using the correct function bounds")

if  fx_val4[0] > minfx4:
    pass_count4 +=1
else:
    fail_count4 += 1
    print ("Agent 4 was not optimzed")
    
for i in x_val4:
    if all(x_val4) < agent4.obj_bounds.xmax and all(x_val4) > agent4.obj_bounds.xmin: 
             bounds_check4 = 'true' 
    else:
        bounds_check4 ='false'
        print ("The estimation inputs are not within the objective function bound")
if bounds_check4 == 'true':
    pass_count4 +=1
else:
    fail_count4 +=1

if len(x_val4) == len(fx_val4): #checks if the number out inputs and outputs match
    pass_count4 +=1
else:
    fail_count4 +=1
    print ("The number of outputs does not match the number of outputs")
    
print ("Amount of Tests Agent 4 has passed = " + str(pass_count4))
print ("Amount of Tests Agent 4 has failed = " + str(fail_count4))
print(" ")
 
pass_count5 = 0 
fail_count5 = 0

if agent5.obj_bounds.xmin == styblinskitang_min and agent5.obj_bounds.xmax == styblinskitang_max:
    pass_count5 += 1
else:
    fail_count5 += 1
    print ("The agent is not using the correct function bounds")

if  fx_val5[0] > minfx5:
    pass_count5 +=1
else:
    fail_count5 += 1
    print ("Agent 5 was not optimzed")
    
for i in x_val5:
    if all(x_val5) < agent5.obj_bounds.xmax and all(x_val5) > agent5.obj_bounds.xmin: 
             bounds_check5 = 'true' 
    else:
        bounds_check5 ='false'
        print ("The estimation inputs are not within the objective function bound")
if bounds_check5 == 'true':
    pass_count5 +=1
else:
    fail_count5 +=1
    
if len(x_val5) == len(fx_val5): #checks if the number out inputs and outputs match
    pass_count5 +=1
else:
    fail_count5 +=1
    print ("The number of outputs does not match the number of outputs")

    
print ("Amount of Tests Agent 5 has passed = " + str(pass_count5))
print ("Amount of Tests Agent 5 has failed = " + str(fail_count5))
 
 


 
 