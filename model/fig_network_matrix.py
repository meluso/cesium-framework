# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 13:42:59 2019

@author: Juango the Blue
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import model_system as sy
import pickle
import fig_settings as fs


fs.set_fonts()


# Generate a system
n=100
gen_sys = False
if gen_sys:
    s1 = sy.System(n=n,tri=0.9)
    with open('../figures/network_100.pickle', 'wb') as f:
        pickle.dump(s1, f)
else:
    with open('../figures/network_100.pickle', 'rb') as f:
        s1 = pickle.load(f)

#%% Create adjacency matrix

# Sort the system graph
Q = nx.algorithms.community.greedy_modularity_communities(s1.graph)

# Compile sorted order into a single 'order' vector
order = [] # Initialize the order vector
for i in range(len(Q)): # Sort through the communities of Q

    # Extract the current community i from Q
    community = sorted(Q[i])

    # Sort through the members of the selected community
    for j in range(len(community)):

        # Append the entry to the end of the order vector
        order.append(community[j])

# Convert to numpy matrix
adjacency_matrix = nx.to_numpy_matrix(s1.graph, dtype=np.bool, nodelist=order)

# Create figure for adjacency matrix with axes
fig, ax = plt.subplots(figsize=fs.fig_size(0.38,0.25))
im = ax.imshow(adjacency_matrix,cmap="Greys")
plt.axis("on")
plt.xlabel("node $i$")
plt.ylabel("node $j$")
plt.xticks([0,20,40,60,80])


# Save and show the figure
for ff in fs.get_formats():
    plt.savefig("../figures/network_matrix",
                format=ff,
                dpi=300,
                bbox_inches='tight')
plt.show()