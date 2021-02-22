# Setup ------------------------------------------------------------------------

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

    # Clear the environment and console
    rm(list = ls())
    cat("\014")
     
    # Import libraries
    library(ggplot2)
    library(gplots)
    library(fitdistrplus)
    library(estimatr)
    library(stargazer)
    # library(lmtest)
    # library(car)
    library(sandwich)
    # library(bucky)
    library(MASS)
    library(dplyr)

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
    df_ack <- df[df$x_objective_fn == "ackley",]
    df_lvy <- df[df$x_objective_fn == "levy",]
    
    robust.se <- function(linmod){
        cov <- vcovHC(linmod, type = "HC1")
        rse <- sqrt(diag(cov))
    }
    

# Robust performance regressions test ------------------------------------------
    
    # Performance w/ All Objectives
    perf.all.rse <- lm_robust(log(y_sys_perf)
                              ~ x_num_nodes
                              + x_objective_fn
                              + x_prob_triangle
                              + poly(x_conv_threshold, 2, raw=TRUE)
                              + x_est_prob
                              , data=df
                              , se_type="stata")
    summary(perf.all.rse)
    
    # Performance w/ Absolute sum only
    perf.abs.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes + I(1/x_num_nodes) + I(1/x_num_nodes^2)
                              + x_prob_triangle
                              + x_conv_threshold
                              + x_est_prob
                              , data=df_abs
                              , se_type="stata")
    summary(perf.abs.rse)
    
    # Performance w/ Sphere only
    perf.sph.rse <- lm_robust(log(y_sys_perf)
                              ~ x_num_nodes
                              + x_prob_triangle
                              + poly(x_conv_threshold, 5, raw=TRUE)
                              + x_est_prob
                              , data=df_sph
                              , se_type="stata")
    summary(perf.sph.rse)
    
    # Performance w/ Ackley only
    perf.ack.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes
                              + x_prob_triangle
                              + x_conv_threshold
                              + x_est_prob
                              , data=df_ack
                              , se_type="stata")
    summary(perf.ack.rse)
    
    # Performance w/ Levy only
    perf.lvy.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes
                              + x_prob_triangle
                              + x_conv_threshold + I(1/x_conv_threshold)
                              + x_est_prob
                              , data=df_lvy
                              , se_type="stata")
    summary(perf.lvy.rse)
    
    
        
# Performance Regressions (w/ lm & vcov) ---------------------------------------
    
    # All in one
    perf.all.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_objective_fn
                      + x_prob_triangle
                      + poly(x_conv_threshold, 2, raw=TRUE)
                      + x_est_prob
                      , data=df)
    summary(perf.all.se)
    
    
    # Absolute sum only
    perf.abs.se <- lm(y_sys_perf
                      ~ x_num_nodes + I(1/x_num_nodes) + I(1/x_num_nodes^2)
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_abs)
    summary(perf.abs.se)
    
    # Sphere only
    perf.sph.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + poly(x_conv_threshold, 5, raw=TRUE)
                      + x_est_prob
                      , data=df_sph)
    summary(perf.sph.se)
    
    # Ackley only
    perf.ack.se <- lm(y_sys_perf
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_ack)
    summary(perf.ack.se)
    
    # Levy only
    perf.lvy.se <- lm(y_sys_perf
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold + I(1/x_conv_threshold)
                      + x_est_prob
                      , data=df_lvy)
    summary(perf.lvy.se)


# Robust cycle regressions test ------------------------------------------------
    
    # Performance w/ All Objectives
    perf.all.rse <- lm_robust(log(y_sys_perf)
                              ~ x_num_nodes
                              + x_objective_fn
                              + x_prob_triangle
                              + poly(x_conv_threshold, 2, raw=TRUE)
                              + x_est_prob
                              , data=df
                              , se_type="stata")
    summary(perf.all.rse)
    
    # Performance w/ Absolute sum only
    perf.abs.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes + I(1/x_num_nodes) + I(1/x_num_nodes^2)
                              + x_prob_triangle
                              + x_conv_threshold
                              + x_est_prob
                              , data=df_abs
                              , se_type="stata")
    summary(perf.abs.rse)
    
    # Performance w/ Sphere only
    perf.sph.rse <- lm_robust(log(y_sys_perf)
                              ~ x_num_nodes
                              + x_prob_triangle
                              + poly(x_conv_threshold, 5, raw=TRUE)
                              + x_est_prob
                              , data=df_sph
                              , se_type="stata")
    summary(perf.sph.rse)
    
    # Performance w/ Ackley only
    perf.ack.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes
                              + x_prob_triangle
                              + x_conv_threshold
                              + x_est_prob
                              , data=df_ack
                              , se_type="stata")
    summary(perf.ack.rse)
    
    # Performance w/ Levy only
    perf.lvy.rse <- lm_robust(y_sys_perf
                              ~ x_num_nodes
                              + x_prob_triangle
                              + x_conv_threshold + I(1/x_conv_threshold)
                              + x_est_prob
                              , data=df_lvy
                              , se_type="stata")
    summary(perf.lvy.rse)
    
    
    
# Cycle Regressions (w/ lm & vcov) ---------------------------------------
    
    # All in one
    perf.all.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_objective_fn
                      + x_prob_triangle
                      + poly(x_conv_threshold, 2, raw=TRUE)
                      + x_est_prob
                      , data=df)
    summary(perf.all.se)
    
    
    # Absolute sum only
    perf.abs.se <- lm(y_sys_perf
                      ~ x_num_nodes + I(1/x_num_nodes) + I(1/x_num_nodes^2)
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_abs)
    summary(perf.abs.se)
    
    # Sphere only
    perf.sph.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + poly(x_conv_threshold, 5, raw=TRUE)
                      + x_est_prob
                      , data=df_sph)
    summary(perf.sph.se)
    
    # Ackley only
    perf.ack.se <- lm(y_sys_perf
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_ack)
    summary(perf.ack.se)
    
    # Levy only
    perf.lvy.se <- lm(y_sys_perf
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold + I(1/x_conv_threshold)
                      + x_est_prob
                      , data=df_lvy)
    summary(perf.lvy.se)    
    
        
# Latex Tables -----------------------------------------------------------------

    stargazer(
        perf.all.se,
        perf.abs.se,
        perf.sph.se,
        perf.ack.se,
        perf.lvy.se,
        se=c(
            robust.se(perf.all.se),
            robust.se(perf.abs.se),
            robust.se(perf.sph.se),
            robust.se(perf.ack.se),
            robust.se(perf.lvy.se)
        ),
        column.labels = c(
            "All Fns",
            "Absolute-Sum Fn",
            "Sphere Fn",
            "Ackley Fn",
            "Levy Fn"
        ),
        omit.stat = "f", single.row=TRUE, digits = 3, intercept.top = TRUE,
        intercept.bottom = FALSE, df = FALSE,
        star.char = c(".", "*", "**", "***"),
        star.cutoffs = c(.05, .01, .001, 0)
        )

# Horsing Around ---------------------------------------------------------------
    
    perf.all.cross <- lm(y_sys_perf
                         ~ x_objective_fn
                         + x_num_nodes
                         + x_prob_triangle
                         + x_conv_threshold
                         + x_est_prob
                         + x_objective_fn*x_num_nodes
                         + x_objective_fn*x_prob_triangle
                         + x_objective_fn*x_conv_threshold
                         + x_objective_fn*x_est_prob
                         + x_num_nodes*x_prob_triangle
                         + x_num_nodes*x_conv_threshold
                         + x_num_nodes*x_est_prob
                         + x_prob_triangle*x_conv_threshold
                         + x_prob_triangle*x_est_prob
                         + x_conv_threshold*x_est_prob
                         , data=df)
    summary(perf.all.cross)
    
    cycl.all.cross <- lm(y_num_cycles
                         ~ x_objective_fn
                         + x_num_nodes
                         + x_prob_triangle
                         + x_conv_threshold
                         + x_est_prob
                         + x_objective_fn*x_num_nodes
                         + x_objective_fn*x_prob_triangle
                         + x_objective_fn*x_conv_threshold
                         + x_objective_fn*x_est_prob
                         + x_num_nodes*x_prob_triangle
                         + x_num_nodes*x_conv_threshold
                         + x_num_nodes*x_est_prob
                         + x_prob_triangle*x_conv_threshold
                         + x_prob_triangle*x_est_prob
                         + x_conv_threshold*x_est_prob
                         , data=df)
    summary(cycl.all.cross)

