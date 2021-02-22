# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 13:25:44 2021

@author: John Meluso
"""

#import math
#import statistics
import numpy as np
#import scipy.stats
import pandas as pd
import data_import as di
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import plot_roc_curve

# Import data from file
df = di.import_execset()
params = di.import_params()

#%% Create preprocessing pipeline

# Specify features
numeric_columns = ['x_num_nodes','x_prob_triangle',
                    'x_conv_threshold','x_est_prob']
categorical_columns = ['x_objective_fn']

# Create X variable matrix and Y vectors
X = df[numeric_columns + categorical_columns]
y_num_cycles = np.ravel(df[['y_num_cycles']].to_numpy(),order='F')
y_sys_perf = np.ravel(df[['y_sys_perf']].to_numpy(),order='F')

# Create test and training sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y_sys_perf, stratify=X, random_state=42)

# Create variable transformers
numeric_pipe = Pipeline(steps=[('scaler', StandardScaler())])
categorical_encoder = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer([
    ('num', numeric_pipe, numeric_columns),
    ('cat', categorical_encoder, categorical_columns)
    ])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
rf = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier())
    ])


#%% Random Forest

# Create Random Forest
rf = rf.fit(X_train,y_train)
rf.score(X_test,y_test)
