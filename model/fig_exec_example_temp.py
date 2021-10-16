# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 13:42:36 2021

@author: John Meluso
"""

import numpy as np
import matplotlib.pyplot as plt
from model_agent import Objective
import run_model as rm
import fig_settings as fs


fs.set_fonts()

def con_style(ax, x, y, arrstyles, constyles):
    x1, y1 = 0.3, 0.2
    x2, y2 = 0.8, 0.6
    
    for xx in np.arange(len(x)-1):
        x1, x2 = x[xx], x[xx+1]
        y1, y2 = y[xx], y[xx+1]
        if constyles[xx] == 1:
            connectionstyle = "arc3,rad=0.3"
        elif constyles[xx] == -1:
            connectionstyle = "arc3,rad=-0.3"
        else:
            connectionstyle = "arc3,rad=0."
        
        ax.plot([x1, x2], [y1, y2], ".",ms=5,
                color="white",
                )
        
        if arrstyles[xx] == 1:
            ax.annotate("",
                        xy=(x1, y1), xycoords='data',
                        xytext=(x2, y2), textcoords='data',
                        arrowprops=dict(arrowstyle="<|-", lw=0.75,
                                        color="white",
                                        patchA=None,
                                        connectionstyle=connectionstyle,
                                        mutation_scale=8
                                        ),
                        )
        else:
            ax.annotate("",
                        xy=(x1, y1), xycoords='data',
                        xytext=(x2, y2), textcoords='data',
                        arrowprops=dict(arrowstyle="-", lw=0.75,
                                        color="white",
                                        patchA=None,
                                        connectionstyle=connectionstyle
                                        ),
                    )

        

#%% Generate data
gen_dat = False
if gen_dat:

    found_run = False
    fn = "levy"
    x_min = -10
    x_max = 10

    while not(found_run):

        params_run = {'ind': 999999,
                      'run': 999999,
                      'nod': 2,
                      'obj': fn,
                      'edg': 1,
                      'tri': 0.0,
                      'con': 0.1,
                      'cyc': 25,
                      'tmp': 10000,
                      'itr': 1,
                      'mth': "future",
                      'prb': 0.5,
                      'crt': 2.62
                      }

        summary, history, system = rm.run_model(params_run)

        changed_sys = [(abs(history[ii] - history[ii+1]) > 0.1) for ii in np.arange(len(history)-1)]
        changed_a1 = [(abs(system.archive[ii][0] - system.archive[ii+1][0]) > 0.2) for ii in np.arange(len(history)-1)]
        changed_a2 = [(abs(system.archive[ii][1] - system.archive[ii+1][1]) > 0.2) for ii in np.arange(len(history)-1)]
        count_sys = np.count_nonzero(changed_sys)
        count_a1 = np.count_nonzero(changed_a1)
        count_a2 = np.count_nonzero(changed_a2)
        count_delta = np.count_nonzero(changed_a1 and changed_a2)
        print(str(count_sys) + ", " + str(count_a1) + ", " + str(count_a2) + ", " + str(count_delta))

        if (count_sys > 5) and (count_a1 > 2) and (count_a2 > 2) and (count_delta > 0):
            found_run = True

    agents_x = [[xx[0] for xx in system.archive],[xx[1] for xx in system.archive]]
    arrstyles = []
    for xx in np.arange(len(agents_x[0])-1):
        if np.abs(np.sqrt((agents_x[0][xx]-agents_x[0][xx+1])**2 + (agents_x[1][xx]-agents_x[1][xx+1])**2)) > 0.1:
            arrstyles.append(1)
        else:
            arrstyles.append(0)
    constyles = np.zeros((len(arrstyles),))

#%% Plot functions

data = 1

# Other variables
neighbors = [[1],[0]]
ndivs = 100
n_agents = 2

# # Define Function Inputs
if not(gen_dat) and data == 1:
    fn = "levy"
    obj = Objective(fn,neighbors[0])
    x_min = -1
    x_max = 4
    agents_x = [[2.466977257108084, 2.466977257108084, 2.466977257108084, 2.466977257108084, 2.466977257108084, 2.466977257108084, -0.35209921002388, 0.42892447113990784, 0.42892447113990784, 0.42892447113990784, 0.5907500237226486, 0.5907500237226486, 0.5907500237226486, 0.8617645762860775, 0.8617645762860775, 0.8617645762860775, 0.8617645762860775, 0.8617645762860775], [3.6305058125865735, 3.6305058125865735, -0.20002388954162598, -0.20002388954162598, -0.20002388954162598, -0.20002388954162598, -0.20002388954162598, -0.20002388954162598, 1.633800322189927, 1.633800322189927, 1.633800322189927, 1.633800322189927, 1.633800322189927, 0.4960061013698578, 0.4960061013698578, 0.4960061013698578, 0.4960061013698578, 0.4960061013698578]]
    agents_fx = [[obj(agents_x[0][ii],[agents_x[1][ii]]) for ii in np.arange(len(agents_x[0]))],
                 [obj(agents_x[1][ii],[agents_x[0][ii]]) for ii in np.arange(len(agents_x[1]))]]
    history = [agents_fx[0][ii] + agents_fx[1][ii] for ii in np.arange(len(agents_fx[0]))]
    arrstyles = [0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    constyles = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
elif not(gen_dat) and data == 2:
    fn = "levy"
    obj = Objective(fn,neighbors[0])
    x_min = -5.5
    x_max = 2
    history = [25.825286175296455, 25.825286175296455, 25.162502712193838, 12.407125905775171, 3.2372578623084967, 0.45582824803941935, 0.45582824803941935, 0.34499267926135935, 0.15101752336878946, 0.15101752336878946, 0.15101752336878946]
    agents_x = [[-5.18771521649162, -5.18771521649162, 0.36042213812470436, 0.36042213812470436, 1.2893157750368118, 1.2893157750368118, 1.2893157750368118, 1.2893157750368118, 1.2893157750368118, 1.2893157750368118, 1.2893157750368118], [-3.791741436183445, -3.791741436183445, -3.791741436183445, -3.791741436183445, 1.5074383355677128, 1.5074383355677128, 1.5074383355677128, 0.8029612749814987, 0.8029612749814987, 0.8029612749814987, 0.8029612749814987]]
elif not(gen_dat) and data == 3:
    fn = "sphere"
    obj = Objective(fn,neighbors[0])
    x_min = -5.12
    x_max = 5.12
    history = [21.663083184197113, 13.177079176392242, 7.213953571945536, 0.8991763813875486, 0.810423332537276, 0.6674534139092987, 0.5672497025098704, 0.37839183396046117, 0.055342300612341716, 0.055342300612341716, 0.055342300612341716]
    agents_x = [[1.7372827844059016, 1.7372827844059016, 1.7372827844059016, -0.5324741423820383, -0.5324741423820383, -0.5324741423820383, -0.5324741423820383, 0.4348560428817594, -0.16605725324936227, -0.16605725324936227, -0.16605725324936227], [-3.825987782449223, 2.4803585433654254, 0.4348021379882452, -0.3782407402401615, 0.31670151617710385, 0.009805047141550283, 0.009805047141550283, 0.009805047141550283, 0.009805047141550283, 0.009805047141550283, 0.009805047141550283]]
elif not(gen_dat) and data == 4:
    fn = "sphere"
    obj = Objective(fn,neighbors[0])
    x_min = -10
    x_max = 3
    history = [14.714562700955105, 18.361173644128083, 14.714562700955105, 5.959000187891365, 5.1822979210563584, 5.072224626464571, 5.072224626464571, 5.072224626464571, 4.306229314645855, 0.20159731337305492, 0.20159731337305492, 0.20159731337305492, 0.20159731337305492]
    agents_x = [[8.130406476702323, 10.519148606675133, 8.130406476702323, 2.5209589678953988, 1.813455346673408, 1.813455346673408, 1.813455346673408, 1.813455346673408, 1.1454650412529401, 1.1454650412529401, 1.1454650412529401, 1.1454650412529401, 1.1454650412529401], [6.374734185213724, 17.390700116714548, 6.374734185213724, 5.4380412199959665, 5.258769279791163, 5.258769279791163, 5.258769279791163, 5.258769279791163, 1.0561322721201147, 1.0561322721201147, 1.0561322721201147, 1.0561322721201147, 1.0561322721201147]]
else:
    obj = Objective(fn,neighbors[0])

# Create meshgrid
x_range = np.linspace(x_min,x_max,ndivs)
y_range = np.linspace(x_min,x_max,ndivs)
x_mesh, y_mesh = np.meshgrid(x_range,y_range)
z_mesh = np.round(np.zeros((n_agents,ndivs,ndivs)),decimals=0)

# Create z meshes for agents
for x_ind in np.arange(len(x_range)):
    for y_ind in np.arange(len(y_range)):
        z_mesh[0,x_ind,y_ind] = obj(x_range[x_ind],[y_range[y_ind]])
        z_mesh[1,x_ind,y_ind] = obj(x_range[x_ind],[y_range[y_ind]])

# Create objective evaluations for agents
agents_fx = [[obj(agents_x[0][ii],[agents_x[1][ii]])+1 for ii in np.arange(len(agents_x[0]))],
             [obj(agents_x[1][jj],[agents_x[0][jj]])+1 for jj in np.arange(len(agents_x[1]))]]

d1=0.5
d2=0.3

# Create figure
fig1 = plt.figure(dpi=300,figsize=fs.fig_size(d1,d2))
ax1 = fig1.gca()
con_style(ax1, agents_x[0], agents_x[1], arrstyles, constyles)
surf1 = ax1.contourf(x_mesh,y_mesh,z_mesh[0],cmap=plt.cm.viridis,levels=25)
ax1.set_xlabel('$x_1$')
ax1.set_ylabel('$x_2$')
ax1.set_xticks([-1,0,1,2,3,4])
ax1.set_yticks([-1,0,1,2,3,4])
fig1.colorbar(surf1, ticks=[0, 1.5, 3])
fig1.tight_layout()
for ff in fs.get_formats():
    fig1.savefig('../figures/example_f1', format=ff, bbox_inches='tight')
fig1.show()

# Create figure
constyles = [-cc for cc in constyles]
fig2 = plt.figure(dpi=300,figsize=fs.fig_size(d1,d2))
ax2 = fig2.gca()
con_style(ax2, agents_x[1], agents_x[0], arrstyles, constyles)
surf2 = ax2.contourf(x_mesh,y_mesh,z_mesh[1],cmap=plt.cm.viridis,levels=25)
ax2.set_xlabel('$x_2$')
ax2.set_ylabel('$x_1$')
ax2.set_xticks([-1,0,1,2,3,4])
ax2.set_yticks([-1,0,1,2,3,4])
fig2.colorbar(surf2, ticks=[0, 1.5, 3])
fig2.tight_layout()
for ff in fs.get_formats():
    fig2.savefig('../figures/example_f2', format=ff, bbox_inches='tight')
fig2.show()

# Create figure
fig3 = plt.figure(dpi=300,figsize=fs.fig_size(d1,d2))
ax3 = fig3.gca()
ax3.plot(history,'-o',ms=3,lw=1)
ax3.set_xlabel('$t$')
ax3.set_ylabel('$F(t,f_1,f_2)$')
fig3.tight_layout()
for ff in fs.get_formats():
    fig3.savefig('../figures/example_hist', format=ff, bbox_inches='tight')
fig3.show()