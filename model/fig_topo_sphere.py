# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:31:16 2021

@author: John Meluso
"""

import fig_topo_load as ftl
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource
import fig_settings as fs
import numpy as np
import pandas as pd


#%% Get data
fs.set_fonts()

fn_name = 'sphere'

# Load data
df2obj2topo = ftl.load_data()

topo_list = [
    [np.round(df2obj2topo[fn_name]['x_prob_triangle'][xx],decimals=1),
     np.round(df2obj2topo[fn_name]['x_est_prob'][xx],decimals=1),
     df2obj2topo[fn_name]['mean'][xx]
     ]
    for xx in np.arange(
            len(df2obj2topo[fn_name]['x_prob_triangle'])
            )
    ]


# Combine data into pivot of results
topo_df = pd.DataFrame(
    topo_list,
    columns = ['x_prob_triangle','x_est_prob','mean']
    )
topo_pivot = topo_df.pivot(
    index='x_prob_triangle',
    columns='x_est_prob',
    values='mean'
    )

# Create meshes
x_range = topo_pivot.index.to_numpy()
y_range = topo_pivot.columns.to_numpy()
x_mesh, y_mesh = np.meshgrid(x_range,y_range)
z_mesh = np.array(topo_pivot)


#%% Plot data

# Plot absolute-sum
fig = plt.figure(dpi=300)
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=25,azim=-115)
ls = LightSource(270, 45)
rgb = ls.shade(
    z_mesh,
    cmap=plt.cm.viridis,
    vert_exag=0.25,
    )
surf = ax.plot_surface(
    x_mesh, y_mesh, z_mesh,
    facecolors=rgb,
    linewidth=0,
    antialiased=False,
    shade=False
    )

# Labels
ax.set_xlabel('Triangle Probability')
ax.set_ylabel('Future Estimate Probability')
ax.set_zlabel('Mean System Performance')

fig.tight_layout()
fig.show()
#fig.savefig('../figures/est_prob_' + fn_name + '.eps',
#            format='eps', bbox_inches='tight')
