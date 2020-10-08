# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2020-10-06
@name: plot_test.py

-------------------------------------------------------------------------------
Description:

This file plots results saved by directly running model_system.py.

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2020-10-06  jmeluso    Initial version.

-------------------------------------------------------------------------------
"""

from model_system import Results, System
import matplotlib.pyplot as plt
import networkx as nx
import pickle
import datetime as dt

if __name__ == '__main__':


    # Start timer
    t_start = dt.datetime.now()

    # Load restults from test
    s1 = pickle.load(open("test_system.pickle","rb"))
    results = pickle.load(open("test_results.pickle","rb"))

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
    hist = [float(x)/(s1.n) for x in nx.degree_histogram(s1.graph)]

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
