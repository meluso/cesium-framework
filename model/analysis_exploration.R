# Background -------------------------------------------------------------------

# Independent variables to try
# - Nodes (x_num_nodes) (4 options)
# - Objective Functions (x_objective_fn) (4 options)
# - Triangle Formation Probability (x_prob_triangle) (11 options)
# - System Convergence Threshold (x_conv_threshold) (7 options)
# - Future Estimate Probability (x_est_prob) (11 options)

# Create array for each input parameter.
# nod = [50, 100, 500, 1000]
# obj = ["absolute-sum","sphere","levy","ackley"]
# edg = [2]
# tri = np.round(np.arange(0,1.1,0.1),decimals=1)
# con = np.array([0.01,0.05,0.1,0.5,1,5,10])
# cyc = [100]
# tmp = [0.1]
# itr = [1]
# mth = ["future"]
# prb = np.round(np.arange(0,1.1,0.1),decimals=1)
# crt = [2.62]

# Dependent variables to try
# - Number of Cycles to Convergence or Timeout (y_num_cycles)
# - Ending System Performance (y_sys_perf)

# Setup ------------------------------------------------------------------------

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
     
    # Import libraries
    library(ggplot2)
    library(gplots)
    library(fitdistrplus)
    library(lmtest)
    library(car)

    df <- read.csv("~/GitHub/cesium/data/sets/execset001_summary.csv",
                   header=FALSE)
    names(df) = c('index_case',
                  'index_run',
                  'x_num_nodes', # nod = [50, 100, 500, 1000]
                  'x_objective_fn', # obj = ["absolute-sum","sphere","levy","ackley"]
                  'x_num_edges',
                  'x_prob_triangle', # tri = np.round(np.arange(0,1.1,0.1),decimals=1)
                  'x_conv_threshold', # con = np.array([0.01,0.05,0.1,0.5,1,5,10])
                  'x_max_cycles',
                  'x_init_temp',
                  'x_anneal_iter',
                  'x_est_method',
                  'x_est_prob', # prb = np.round(np.arange(0,1.1,0.1),decimals=1)
                  'x_anneal_coolrate',
                  'y_num_cycles',
                  'y_sys_perf'
                  )
    
    # Slice by objective function
    df_abs <- df[df$x_objective_fn == "absolute-sum",]
    df_sph <- df[df$x_objective_fn == "sphere",]
    df_lvy <- df[df$x_objective_fn == "levy",]
    df_ack <- df[df$x_objective_fn == "ackley",]

# Experiments ------------------------------------------------------------------
    
    # All in one
    mod_all01 <- lm(log(y_sys_perf)
                    ~ log(x_num_nodes)
                    + x_objective_fn
                    + x_prob_triangle
                    + log(x_conv_threshold)
                    + x_est_prob
                    - 1 
                     , data=df)
    summary(mod_all01)
    bptest(mod_all01)
    ncvTest(mod_all01)

    # Absolute sum only
    mod_abs01 <- lm(y_sys_perf
                    ~ x_num_nodes
                    + x_prob_triangle
                    + x_conv_threshold
                    + x_est_prob
                    - 1
                    , data=df_abs)
    summary(mod_abs01)
    bptest(mod_abs01)
    ncvTest(mod_abs01)
    
    # Sphere only
    mod_sph01 <- lm(log(y_sys_perf)
                    ~ log(x_num_nodes)
                    + x_prob_triangle
                    + log(x_conv_threshold)
                    + x_est_prob
                    - 1
                    , data=df_sph)
    summary(mod_sph01)
    bptest(mod_sph01)
    ncvTest(mod_sph01)

    # Levy only
    mod_lvy01 <- lm(y_sys_perf
                    ~ x_num_nodes
                    + x_prob_triangle
                    + x_conv_threshold
                    + x_est_prob
                    - 1
                    , data=df_lvy)
    summary(mod_lvy01)
    bptest(mod_lvy01)
    ncvTest(mod_lvy01)
    
    # Ackley only
    mod_ack01 <- lm(y_sys_perf
                    ~ x_num_nodes
                    + x_prob_triangle
                    + x_conv_threshold
                    + x_est_prob
                    - 1
                    , data=df_ack)
    summary(mod_ack01)
    bptest(mod_ack01)
    ncvTest(mod_ack01)














