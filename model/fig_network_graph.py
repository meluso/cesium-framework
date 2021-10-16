# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 13:42:59 2019

@author: Juango the Blue
"""

import networkx as nx
import matplotlib.pyplot as plt
import model_system as sy
import pickle
import fig_settings as fs


fs.set_fonts()


# Generate a system
n=1000
gen_sys = False
if gen_sys:
    s1 = sy.System(n=n,tri=0.9)
    with open('../figures/network_1000.pickle', 'wb') as f:
        pickle.dump(s1, f)
else:
    with open('../figures/network_1000.pickle', 'rb') as f:
        s1 = pickle.load(f)

#%% Plot Network Graph

# Sort the system graph
fig_net = plt.figure()
options = {
    'node_color': '#ff7f0e',
    'node_size': 15,
    'width': 1
    }
nx.draw_kamada_kawai(s1.graph, **options)

# Save and show the figure
for ff in fs.get_formats():
    plt.savefig("../figures/network_graph",
                format=ff,
                dpi=300,
                bbox_inches='tight')
plt.show()
