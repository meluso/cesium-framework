# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 17:24:47 2021

@author: Jim Bagrow, John Meluso
"""

import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor


df = pd.read_csv("../data/sets/cesium_execset001.csv", index_col=0)
cols = list(df.columns)
variables = [c for c in cols if c.startswith("x_")]
outcomes  = [c for c in cols if c.startswith("y_")]
obj_funs = list(df['x_objective_fn'].unique())

MAX_DEPTH = 4
SEED = 42

save_data = []

for ofn in obj_funs:
    for out in outcomes:
        print(f"Analyzing {ofn} & {out}")

        this_df = df[df['x_objective_fn']==ofn].copy()
        X = this_df[variables].copy()
        X.drop(columns=["x_objective_fn"], inplace=True)
        y = this_df[out].copy()

        forest = RandomForestRegressor(max_depth=MAX_DEPTH, random_state=SEED)
        forest.fit(X,y)

        importances = forest.feature_importances_
        std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                     axis=0)
        indices = np.argsort(importances)[::-1]

        feat_importances = pd.Series(forest.feature_importances_,
                                     index=X.columns,
                                     name=f'{ofn}_{out}')
        save_data.append(feat_importances.nlargest())
            
with open('../figures/random_forest.pickle', 'wb') as f:
    pickle.dump(save_data, f)