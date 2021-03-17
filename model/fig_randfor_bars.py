# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:24:47 2021

@author: Juango the Blue
"""

import matplotlib.pyplot as plt
import pandas as pd
import pickle
import fig_settings as fs


fs.set_fonts()

with open('../figures/random_forest.pickle', 'rb') as f:
    ser = pickle.load(f)

# Organize dataframe
df = pd.DataFrame(ser)
fig_opt = 3

if fig_opt == 1:
    
    df = df[['x_est_prob','x_conv_threshold','x_prob_triangle','x_num_nodes']].transpose()

    # Create figure
    fig = plt.figure(dpi=300, figsize=fs.fig_size(1,0.15))
    ax_big = fig.add_subplot(111, frameon=False)
    
    # Turn off axis lines and ticks of the big subplot
    ax_big.spines['top'].set_color('none')
    ax_big.spines['bottom'].set_color('none')
    ax_big.spines['left'].set_color('none')
    ax_big.spines['right'].set_color('none')
    ax_big.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)
    
    # Absolute-Sum
    fig.add_subplot(221)
    ax1 = fig.gca()
    loc = ['absolute-sum_y_sys_perf','absolute-sum_y_num_cycles']
    df[loc].plot(kind='barh',ax=ax1,legend=False)
    
    # Sphere
    fig.add_subplot(222)
    ax2 = fig.gca()
    loc = ['sphere_y_sys_perf','sphere_y_num_cycles']
    df[loc].plot(kind='barh',ax=ax2,legend=False)
    
    # Ackley
    fig.add_subplot(223)
    ax3 = fig.gca()
    loc = ['ackley_y_sys_perf','ackley_y_num_cycles']
    df[loc].plot(kind='barh',ax=ax3,legend=False)
    
    # Levy
    fig.add_subplot(224)
    ax4 = fig.gca()
    loc = ['levy_y_sys_perf','levy_y_num_cycles']
    df[loc].plot(kind='barh',ax=ax4,legend=False)
    
    # Legend
    handles, labels = ax4.get_legend_handles_labels()
    fig.legend(handles, ['Sys. Perf.','Num. Cycles'], loc='lower center', ncol=4)
    
    # Titles
    ax1.set_title('Absolute-Sum')
    ax2.set_title('Sphere')
    ax3.set_title('Ackley')
    ax4.set_title('Levy')
    
    # Axis Labels
    # ax_big.set_xlabel('Features')
    # ax_big.set_ylabel('Feature Importance')
    
    fig.tight_layout(rect=[0,0.03,1,1])
    fig.show()
    
elif fig_opt == 2:
    
    df = df[['x_num_nodes','x_prob_triangle','x_conv_threshold','x_est_prob']]
    x_ticks = ['']
    
    # Create figure
    fig = plt.figure(dpi=300, figsize=fs.fig_size(1,0.15))
    ax = fig.gca()
    df.plot(kind='bar',ax=ax, legend=False)
    
    # Legend
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles,
               ['Num. Nodes.','Tri. Prob.','Conv. Thresh.','Fut. Est. Prob.'],
               loc='lower center', ncol=4)
    
    fig.tight_layout(rect=[0,0.03,1,1])
    fig.show()
    
elif fig_opt == 3:
    
    df = df[['x_num_nodes',
             'x_prob_triangle',
             'x_conv_threshold',
             'x_est_prob']]
    outcomes = ['Sys. Perf.','Num. Cycles']
    # outcomes = pd.Series({
    #     'absolute-sum_y_sys_perf': 'Sys. Perf.',
    #     'absolute-sum_y_num_cycles': 'Num. Cycles',
    #     'sphere_y_sys_perf': 'Sys. Perf.',
    #     'sphere_y_num_cycles': 'Num. Cycles',
    #     'ackley_y_sys_perf': 'Sys. Perf.',
    #     'ackley_y_num_cycles': 'Num. Cycles',
    #     'levy_y_sys_perf': 'Sys. Perf.',
    #     'levy_y_num_cycles': 'Num. Cycles',
    #     })
    # inputs = ['Num. Nodes.','Tri. Prob.','Conv. Thresh.','Fut. Est. Prob.']
    inputs = pd.Series({
        'x_num_nodes': 'Num. Nodes.',
        'x_prob_triangle': 'Tri. Prob.',
        'x_conv_threshold': 'Conv. Thresh.',
        'x_est_prob': 'Fut. Est. Prob.'})

    # Create figure
    fig = plt.figure(dpi=300, figsize=fs.fig_size(1,0.30))
    ax_big = fig.add_subplot(111, frameon=False)
    
    # Turn off axis lines and ticks of the big subplot
    ax_big.spines['top'].set_color('none')
    ax_big.spines['bottom'].set_color('none')
    ax_big.spines['left'].set_color('none')
    ax_big.spines['right'].set_color('none')
    ax_big.tick_params(labelcolor='w',
                       top=False, bottom=False, left=False, right=False)
    
    # Absolute-Sum
    fig.add_subplot(141)
    ax1 = fig.gca()
    loc = ['absolute-sum_y_sys_perf','absolute-sum_y_num_cycles']
    df.loc[loc].plot(kind='bar',ax=ax1,legend=False)
    plt.setp(ax1.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax1.set_xticklabels(outcomes,rotation=45)
    
    # Sphere
    fig.add_subplot(142)
    ax2 = fig.gca()
    loc = ['sphere_y_sys_perf','sphere_y_num_cycles']
    df.loc[loc].plot(kind='bar',ax=ax2,legend=False)
    plt.setp(ax2.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax2.set_xticklabels(outcomes,rotation=45)
    
    # Ackley
    fig.add_subplot(143)
    ax3 = fig.gca()
    loc = ['ackley_y_sys_perf','ackley_y_num_cycles']
    df.loc[loc].plot(kind='bar',ax=ax3,legend=False)
    plt.setp(ax3.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax3.set_xticklabels(outcomes,rotation=45)
    
    # Levy
    fig.add_subplot(144)
    ax4 = fig.gca()
    loc = ['levy_y_sys_perf','levy_y_num_cycles']
    df.loc[loc].plot(kind='bar',ax=ax4,legend=False)
    plt.setp(ax4.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax4.set_xticklabels(outcomes,rotation=45)
    
    # Legend
    handles, labels = ax4.get_legend_handles_labels()
    fig.legend(handles, labels=inputs, loc='lower center', ncol=4)
    
    # Titles
    ax1.set_title('Absolute-Sum')
    ax2.set_title('Sphere')
    ax3.set_title('Ackley')
    ax4.set_title('Levy')
    
    # Axis Labels
    # ax_big.set_xlabel('Features')
    # ax_big.set_ylabel('Feature Importance')
    
    fig.tight_layout(rect=[0,0.03,1,1])
    fig.savefig('../figures/feat_importances.eps', bbox_inches='tight')