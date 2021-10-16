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


#%% Plot Histogram

# degree histogram
hist = [float(x)/n for x in nx.degree_histogram(s1.graph)]
start = 2
hist = hist[start:]

# Create a logarithmic plot of the degree distribution
fig_log = plt.figure(figsize=fs.fig_size(0.4,0.25))

# Build logarithmic plot of the degree distribution
plt.loglog(hist, marker=".",ls="none")
plt.ylabel("Fraction of Artifacts")
plt.xlabel("Artifact Degree $k_i$")
for ff in fs.get_formats():
    plt.savefig("../figures/network_dist", format=ff,
                dpi=300,
                bbox_inches='tight')
plt.show()