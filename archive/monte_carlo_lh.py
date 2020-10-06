# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-10
@name: monte_carlo_mp.py

-------------------------------------------------------------------------------
Description:

Performs a Monte Carlo simulation on a network of engineer agents. This
model initializes and runs an instance of the system model...

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.
2019-10-30  jmeluso    Second version for CESIUM.

-------------------------------------------------------------------------------
"""
import model_system as sy
from doe_lhs import lhs
from multiprocessing import Process, Queue
import datetime as dt
import csv

###############################################################################
# Execution & Logging Functions
###############################################################################                

def execute_trial(x):
    '''Executes a single trial of the Monte Carlo simulation. Function creates
     an instances of a system, runs the model for that system, and saves the
     results of the trial.'''
         
    # Convert x to model input values
    run_ID = x[0]
    num_agents = x[1]
    obj_fn = x[2]
    est_prob = x[3]
    est_meth = x[4]
    
    # Initialize the system
    model = sy.System(num_agents, obj_fn, est_prob, est_meth)
    
    # Run the simulation
    output = model.run()
    
    # Store the results in the array
    results_summary = [
            run_ID,
            est_meth,
            obj_fn,
            est_prob,
            output.design_cycles,
            output.perf_system[-1],
            output.k_mean
            ]
    
    results_system = output.perf_system
    
    results_agents = [output.perf_agents,output.k_agents]
    
    # Return results
    return [results_summary, results_system, results_agents]

    
###############################################################################
# Initialize simulation parameters
###############################################################################
    
if __name__ == '__main__':
    
    # Start timer
    t_start = dt.datetime.now()
    
    # Number of agents in the model
    list_agents = [50,100,500,1000,5000]
    num_agents = len(list_agents)
    
    # A list of the different objective functions available to the agents.
    list_obj = ["ackley","langermann","levy","rosenbrock","schwefel"]
    num_obj = len(list_obj)
    
    # A list of the number of edges to create for each new node
    list_edges = [1,2,3,4,5]
    num_edges = len(list_edges) 
    
    # A list of the different triangle creation probabilities
    list_tri = [0.1, 0.3, 0.5, 0.7, 0.9]
    num_tri = len(list_tri)
    
    # A list of the convergence limits
    list_conv = [0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    num_conv = len(list_conv)
    
    # A list of the initial temperatures
    list_temp = [1,5,10,50,100,500,1000,5000,10000,50000]
    num_temp = len(list_temp)
    
    # Set number of latin hypercube samples
    samples = 10  # Functionality test
    #samples = (num_tri*num_conv*num_temp)  # 350 base LHS
    #samples = (num_tri*num_conv*num_temp) * 14  # 350*14 = 4900 full LHS
    
    # Set number of workers (nodes? cores?)
    workers = 2


###############################################################################
# Simulation Storage & Logistics
###############################################################################

    # Array corresponding to all of the variables of the trial
    sim_inputs = Queue()
    sim_outputs = Queue()
    results_summary = []
    results_system = []
    results_agents = []


###############################################################################
# Create Simulation Input Array
###############################################################################

    # Loop through each of the parameters to create an input matrix
    for ag in range(num_agents):
        for ob in range(num_obj):
            for ed in range(num_edges):
                    
                # Construct latin hypercube sample for remaining variables
                hypercube = lhs(3,samples=samples)
                
                # Construct the simulation input values from hypercube
                for i in range(len(hypercube)):
                    
                    # Iterate through triangle options to find value
                    found = False
                    j = 0
                    while found is False:
                        if hypercube[i][0] < float((j + 1)/num_tri):
                            curr_tri = list_tri[j]
                            found = True
                        else:
                            j += 1
                    
                    # Iterate through convergence options to find value
                    found = False
                    j = 0
                    while found is False:
                        if hypercube[i][0] < float((j + 1)/num_conv):
                            curr_conv = list_conv[j]
                            found = True
                        else:
                            j += 1
                    
                    # Iterate through temperature options to find value
                    found = False
                    j = 0
                    while found is False:
                        if hypercube[i][0] < float((j + 1)/num_temp):
                            curr_temp = list_temp[j]
                            found = True
                        else:
                            j += 1
                
                    # Populate the simulation inputs array
                    sim_inputs.put([list_agents[ag],
                                    list_obj[ob],
                                    list_edges[ed],
                                    curr_tri,
                                    curr_conv,
                                    curr_temp])


###############################################################################
# Run the Simulation in Parallel via Multiprocessing Module
###############################################################################
    
    # Start worker processes
    for wk in range()
        
        
        
    # Run simulation through pool of workers with sim_inputs
    pool = mp.Pool()
    sim_outputs = pool.map_async(execute_trial,sim_inputs).get()
    pool.close()
    pool.join()


###############################################################################
# Save Results to File
###############################################################################
    
    # Parse the results into matrices
    for i in range(len(sim_outputs)):
        results_summary.append(sim_outputs[i][0])
        results_system.append(sim_outputs[i][1])
        results_agents.append(sim_outputs[i][2])

    # Write the results to a CSV file stamped with the time
    filename = dt.datetime.now().isoformat()[0:20].replace("T","_").\
        replace(":","-").replace(".","_")
    
    # Construct a file for the summary
    with open("../results/"+filename+"MCResultsSummary.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_summary:
            writer.writerow(line)
            
    # Construct a file for the system results
    with open("../results/"+filename+"MCResultsSystem.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_system:
            writer.writerow(line)
            
    # Construct a file for the 
    with open("../results/"+filename+"MCResultsAgents.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_agents:
            writer.writerow(line)

    # Stop timer
    t_stop = dt.datetime.now()
    print(t_stop - t_start)

                
                
                
                