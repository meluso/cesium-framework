# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 13:42:59 2019

@author: Juango the Blue
"""

import numpy as np
import scipy as sc
import networkx as nx
import matplotlib.pyplot as plt
import model_system as sy


# Generate a system
n=1000
s1 = sy.System(n=n,tri=0.9)

#%% Plot Network Graph

# Sort the system graph
fig_net = plt.figure()
options = {
    'node_color': '#F47D20',
    'node_size': 15,
    'width': 1
    }
nx.draw_kamada_kawai(s1.graph, **options)

# Save and show the figure
plt.savefig("network_graph.eps",dpi=250)
plt.savefig("network_graph.tif",dpi=250)
plt.show()

#%% Plot Histograph

# degree histogram
hist = [float(x)/n for x in nx.degree_histogram(s1.graph)]
start = 2
hist = hist[start:]

def fn_log(t,m,b): return m*np.log(t) + b
def fn_exp(t,a,b): return b*np.exp(a*t)

# Calculate line of best fit
x = []
y = []
for ii in np.arange(start,len(hist)):
    if hist[ii] > 0:
        x.append(np.float(ii))
        y.append(hist[ii])
x = np.array(x)
y = np.array(y)
w = np.sqrt(y)
coeffs, pcov = sc.optimize.curve_fit(fn_log,x,y)
fitline = fn_exp(x,coeffs[0],coeffs[1])

# Create a logarithmic plot of the degree distribution
fig_log = plt.figure()

# Build logarithmic plot of the degree distribution
plt.loglog(hist, color='b',marker=".",ls="none")
#plt.log(x,fitline)
plt.ylabel("Fraction of Nodes")
plt.xlabel("Artifact Degree")
plt.savefig("degree_distribution.tif", format='tif', dpi=250)
plt.savefig("degree_distribution.eps", format='eps', dpi=250)
plt.show()