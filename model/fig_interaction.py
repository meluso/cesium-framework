# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 11:45:13 2021

@author: John Meluso
"""

import fig_settings as fs
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt



if __name__ == '__main__':

    # Load fonts
    fs.set_fonts()
    
    # Set page space occupancy
    frac_width = 0.5
    frac_height = 0.25
    num_cols = 2
    
    # Create figure
    fig = plt.figure(
        dpi=300,
        figsize=fs.fig_size(
            frac_width,
            frac_height,
            num_cols)
        )
    ax = fig.add_axes([0, 0, 1, 1], frameon=False, aspect=1.)
    
    # Create figure limits
    xmin = -1
    xmax = 9
    ymin = 1
    ymax = 8
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(ymin,ymax)
    
    color = {
        'blue': '#1f77b4',
        'orange': '#ff7f0e',
        'green': '#2ca02c',
        'red': '#d62728',
        'black': 'k',
        'white': 'w',
        'none': 'none'
            }
    size = {
        'no': 0,
        'md': 0.25,
        'lg': 0.75
        }
    
    # List of Nodes as Tuples
    node_tuple = [
        ( 1, (  -1,1.75), 'no',  False,   'none',   'none',  '-'), # 0
        ( 1, (  -1, 5.5), 'no',  False,   'none',   'none',  '-'), # 1
        ( 1, (  -1, 7.5), 'no',  False,   'none',   'none',  '-'), # 2
        ( 1, ( 1.5,   3), 'md',   True, 'orange', 'orange',  '-'), # 3
        ( 1, (   1, 6.5), 'md',   True, 'orange', 'orange',  '-'), # 4
        ( 1, ( 5.5, 2.5), 'md',   True, 'orange', 'orange',  '-'), # 5
        ( 1, (   5,   6), 'md',   True, 'orange', 'orange',  '-'), # 6
        ( 1, ( 1.5,   3), 'lg',   True,   'blue',   'none', '-.'), # 7
        ( 1, ( 5.5, 2.5), 'lg',   True,  'green',   'none', '--'), # 8
        ( 1, (   5,   6), 'lg',   True,   'blue',   'none', '-.'), # 9
        ( 2, (   7, 1.5), 'no',  False,   'none',   'none',  '-'), #10
        ( 2, (7.65, 1.5), 'no',  False,   'none',   'none',  '-'), #11
        ( 2, ( 8.3, 1.5), 'no',  False,   'none',   'none',  '-')  #12
        ]
    
    # List of Nodes as Patches
    node_patch = []
    
    # List of Annotations
    annotation = [
        ( 1, ( 4.5,   8),  'black', '$S=[x_1,x_2,x_3,x_4,...,x_n]$'),
        ( 1, (3.25,7.35),  'green', '$x_i=x_1$'),
        ( 1, ( 5.5,7.35),   'blue', '$x_j=[x_2,x_4]$'),
        ( 1, (   1,   7),  'black', '$x_3$'),
        ( 1, (   5, 6.5),  'black', '$x_4$'),
        ( 1, ( 1.5, 2.5),  'black', '$x_2$'),
        ( 1, ( 5.5,   2),  'black', '$x_1$'),
        ( 1, ( 7.5,1.35),  'black', '$f_1(x_1,x_2,x_4)$')
        ]
    
    # List of Edges
    edge = [
        ( 1,  0,  3,  'black',  '-',  '-',  'none'),
        ( 1,  1,  4,  'black',  '-',  '-',  'none'),
        ( 1,  2,  4,  'black',  '-',  '-',  'none'),
        ( 1,  3,  4,  'black',  '-',  '-',  'none'),
        ( 1,  3,  5,  'black',  '-',  '-',  'none'),
        ( 1,  3,  6,  'black',  '-',  '-',  'none'),
        ( 1,  4,  6,  'black',  '-',  '-',  'none'),
        ( 1,  5,  6,  'black',  '-',  '-',  'none'),
        ( 2,  7, 11,   'blue', '<-', '-.',  'opt1'),
        ( 2,  8, 10,  'green', '<-', '--',  'opt2'),
        ( 2,  9, 12,   'blue', '<-', '-.',  'opt3')
        ]
    
    curve = {
        'none': None,
        'opt1': 'angle3, angleA=100, angleB=20',
        'opt2': 'angle3, angleA=100, angleB=0',
        'opt3': 'angle3, angleA=90, angleB=-30'
        }
    
    # Iterate through plotting groups
    groups = [1,2]
    for gg in groups:
    
        # Plot circles
        for group, xy, sz, fill, ec, fc, ls in node_tuple:
            
            # If in this group
            if gg == group:
                
                # If need a patch
                if size[sz] > 0:
                    
                    # Generate Patch
                    patch = mpatches.Circle(
                        xy,
                        radius = size[sz],
                        ec = color[ec],
                        fc = color[fc],
                        fill = fill,
                        linestyle = ls
                        )
                    
                    # Add patch to list
                    node_patch.append(patch)
                    
                    # Place patch on axes
                    ax.add_patch(patch)
                    
                # Otherwise, add none
                else:
                    node_patch.append(None)
                    
        # Plot annotations
        for group, xy, tc, text in annotation:
            
            # If in this group
            if gg == group:
                
                # Place the annotation
                ax.annotate(
                    text,
                    xy,
                    ha="center",
                    va="center",
                    color=color[tc]
                    )
        
        # Plot lines
        for group, n1, n2, lc, arrow, ls, arc in edge:
            
            # If in this group
            if gg == group:
            
                # Place the edge
                ax.annotate("",
                    node_tuple[n1][1],
                    node_tuple[n2][1],
                    ha="center", va="center",
                    arrowprops=dict(
                        arrowstyle=arrow,
                        color=color[lc],
                        patchA=node_patch[n2],
                        patchB=node_patch[n1],
                        shrinkA=1,
                        shrinkB=1,
                        linestyle=ls,
                        connectionstyle=curve[arc]
                        )
                    )
    
    # Create a colormap
    cdict = {
        'red': (
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0)
            ),
        'green': (
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0)
            ),
        'blue': (
            (0.0, 1.0, 1.0),
            (1.0, 1.0, 1.0)
            ),
        'alpha': (
            (0.0, 1.0, 1.0),
            (0.5, 1.0, 1.0),
            (1.0, 0.0, 0.0)
            )}
    cmap_name = 'vary_transparency'
    cm = LinearSegmentedColormap(cmap_name, cdict)
                
    # Set rectangle specs
    olwidth = 1.5
    extent = (xmin,xmin+olwidth,ymin,ymax)
    ax.imshow(
        [[0.,1.], [0.,1.]], 
        cmap = cm,
        interpolation = 'bicubic',
        extent = extent,
        zorder = 10
        )            
            
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)        
    
    fig.savefig('../figures/interaction.tif', bbox_inches='tight')
    fig.show()
            
            