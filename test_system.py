# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-21
@name: test_system.py

-------------------------------------------------------------------------------
Description:

This file tests the system class.

The file takes in the amount of nodes that are present in the system and the 
objective function to show how many connections occur between the nodes through
a network diagram.

The plot that follows shows the amount of nodes that have the same amount of 
connections. 

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.
2019-07-09  jmeluso    Updated to new inputs System(n,obj,edg,tri,con,div,itr).
2019-11-04  jmeluso    Updated to new inputs System(n,obj,edg,tri,con,tmp,crt).

-------------------------------------------------------------------------------
"""

import model_system as sy
import matplotlib.pyplot as plt
import networkx as nx
import datetime as dt

if __name__ == '__main__':

    # Start timer
    t_start = dt.datetime.now()
    
    # Generate a system with n nodes, obj objective function, edg random edges,
    # tri probability of triange, con convergence threshold, tmp for cooling rate,
    # and itr iterations for basin-hopping
    n = 100
    obj = "langermann"
    edg = 2
    tri = 0.5
    con = 0.01
    tmp = 0.1
    crt = 1.1
    s1 = sy.System(n,obj,edg,tri,con,tmp,crt)
    
    # Save figures? True or False
    save_figs = False
    
    # Plot the system
    options = {
            'node_color': 'red',
            'node_size': 15,
            'width': 1
            }
    
    # Create new figure for network graph
    fig_network = plt.figure()
    
    # Build network graph in figure
    nx.draw_kamada_kawai(s1.graph, **options)
    if save_figs:
        plt.savefig("network_graph.tif", format='tif', dpi=250)
        plt.savefig("network_graph.eps", format='eps', dpi=250)
    plt.show()
    
    #degree histogram
    hist = [float(x)/n for x in nx.degree_histogram(s1.graph)]        
    
    # Create a linear plot of the degree distribution
    #plt.plot(hist, color='b',marker=".",ls="none")
    #plt.show()
    
    # Create a logarithmic plot of the degree distribution
    fig_log = plt.figure()
    
    # Build logarithmic plot of the degree distribution
    plt.loglog(hist, color='b',marker=".",ls="none")
    plt.ylabel("Fraction of Nodes")
    plt.xlabel("Artifact Degree")
    if save_figs:    
        plt.savefig("degree_distribution.tif", format='tif', dpi=250)
        plt.savefig("degree_distribution.eps", format='eps', dpi=250)
    plt.show()
    
    # 
    
    # Run the system
    results = s1.run()
    
    # Create figure for system performance
    fig_system = plt.figure()
    
    # Plot the system performance
    plt.plot(results.perf_system)
    plt.xlabel("Design Cycle")
    plt.ylabel("System Performance")
    #plt.semilogy(results.perf_system)
    plt.show()
    
    # Stop timer
    t_stop = dt.datetime.now()
    print((t_stop - t_start))
