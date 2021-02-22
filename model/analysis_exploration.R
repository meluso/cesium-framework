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
    library(estimatr)
    library(stargazer)
    # library(lmtest)
    # library(car)
    library(sandwich)
    # library(bucky)
    library(MASS)

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

# Miscommunication Plots -------------------------------------------------------
    
    fn.miscomm <- function(df,main_title){
        plotmeans(y_sys_perf ~ x_est_prob,
                  data = df,
                  n.label = FALSE,
                  xlab = "Future Estimate Probability",
                  ylab = "Sys Perf Degradation")
        title(main_title)
    }
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    fn.miscomm(df_abs,"Absolute-Sum Function")
    fn.miscomm(df_sph,"Sphere Function")
    fn.miscomm(df_ack,"Ackley Function")
    fn.miscomm(df_lvy,"Levy Function")
    
# Performance Mean Plots -------------------------------------------------------
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_sys_perf ~ x_num_nodes, data = df_abs, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_prob_triangle, data = df_abs, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_conv_threshold, data = df_abs, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_est_prob, data = df_abs, n.label = FALSE)
    mtext("Absolute-Sum Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_sys_perf ~ x_num_nodes, data = df_sph, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_prob_triangle, data = df_sph, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_conv_threshold, data = df_sph, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_est_prob, data = df_sph, n.label = FALSE)
    mtext("Sphere Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_sys_perf ~ x_num_nodes, data = df_ack, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_prob_triangle, data = df_ack, n.label = FALSE, log = "y")
    plotmeans(y_sys_perf ~ x_conv_threshold, data = df_ack, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_est_prob, data = df_ack, n.label = FALSE, log = "y")
    mtext("Ackley Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_sys_perf ~ x_num_nodes, data = df_lvy, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_prob_triangle, data = df_lvy, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_conv_threshold, data = df_lvy, n.label = FALSE)
    plotmeans(y_sys_perf ~ x_est_prob, data = df_lvy, n.label = FALSE)
    mtext("Levy Fn System Performance Slices", side = 3, line = -2, outer = TRUE)

# Convergence Time Mean Plots --------------------------------------------------
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_num_cycles ~ x_num_nodes, data = df_abs, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_prob_triangle, data = df_abs, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_conv_threshold, data = df_abs, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_est_prob, data = df_abs, n.label = FALSE)
    mtext("Absolute-Sum Fn Convergence Time Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_num_cycles ~ x_num_nodes, data = df_sph, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_prob_triangle, data = df_sph, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_conv_threshold, data = df_sph, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_est_prob, data = df_sph, n.label = FALSE)
    mtext("Sphere Fn Convergence Time Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_num_cycles ~ x_num_nodes, data = df_ack, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_prob_triangle, data = df_ack, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_conv_threshold, data = df_ack, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_est_prob, data = df_ack, n.label = FALSE)
    mtext("Ackley Fn Convergence Time Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    plotmeans(y_num_cycles ~ x_num_nodes, data = df_lvy, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_prob_triangle, data = df_lvy, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_conv_threshold, data = df_lvy, n.label = FALSE)
    plotmeans(y_num_cycles ~ x_est_prob, data = df_lvy, n.label = FALSE)
    mtext("Levy Fn Convergence Time Slices", side = 3, line = -2, outer = TRUE)
    
# Box Plots -------------------------------------------------------------------
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_num_nodes, data = df_abs)
    boxplot(y_sys_perf ~ x_prob_triangle, data = df_abs)
    boxplot(y_sys_perf ~ x_conv_threshold, data = df_abs)
    boxplot(y_sys_perf ~ x_est_prob, data = df_abs)
    mtext("Absolute-Sum Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_num_nodes, data = df_sph)
    boxplot(y_sys_perf ~ x_prob_triangle, data = df_sph)
    boxplot(y_sys_perf ~ x_conv_threshold, data = df_sph)
    boxplot(y_sys_perf ~ x_est_prob, data = df_sph)
    mtext("Sphere Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_num_nodes, data = df_ack)
    boxplot(y_sys_perf ~ x_prob_triangle, data = df_ack)
    boxplot(y_sys_perf ~ x_conv_threshold, data = df_ack)
    boxplot(y_sys_perf ~ x_est_prob, data = df_ack)
    mtext("Ackley Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_num_nodes, data = df_lvy)
    boxplot(y_sys_perf ~ x_prob_triangle, data = df_lvy)
    boxplot(y_sys_perf ~ x_conv_threshold, data = df_lvy)
    boxplot(y_sys_perf ~ x_est_prob, data = df_lvy)
    mtext("Levy Fn System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_est_prob, data = df_abs, ylim = c(0,200), xlab = "Absolute-Sum")
    boxplot(y_sys_perf ~ x_est_prob, data = df_sph, xlab = "Sphere")
    boxplot(y_sys_perf ~ x_est_prob, data = df_ack, xlab = "Ackley")
    boxplot(y_sys_perf ~ x_est_prob, data = df_lvy, xlab = "Levy")
    mtext("x_est_prob System Performance Slices", side = 3, line = -2, outer = TRUE)
    
    par(mfrow=c(2,2), mar=c(4,4,3,1)+0.1)
    boxplot(y_sys_perf ~ x_est_prob, data = df_abs, log = "y", xlab = "Absolute-Sum")
    boxplot(y_sys_perf ~ x_est_prob, data = df_sph, log = "y", xlab = "Sphere")
    boxplot(y_sys_perf ~ x_est_prob, data = df_ack, log = "y", xlab = "Ackley")
    boxplot(y_sys_perf ~ x_est_prob, data = df_lvy, log = "y", xlab = "Levy")
    mtext("x_est_prob System Performance Slices in Log", side = 3, line = -2, outer = TRUE)
    
    ggplot(df_abs, aes(factor(x_est_prob), y_sys_perf)) + geom_violin(draw_quantiles = c(0.25, 0.5, 0.75)) + scale_y_log10()
    ggplot(df_sph, aes(factor(x_est_prob), y_sys_perf)) + geom_violin(draw_quantiles = c(0.25, 0.5, 0.75)) + scale_y_log10()
    ggplot(df_ack, aes(factor(x_est_prob), y_sys_perf)) + geom_violin(draw_quantiles = c(0.25, 0.5, 0.75)) + scale_y_log10()
    ggplot(df_lvy, aes(factor(x_est_prob), y_sys_perf)) + geom_violin(draw_quantiles = c(0.25, 0.5, 0.75)) + scale_y_log10()

    
# Regressions (w/ lm_robust) ---------------------------------------------------
    
    # Performance w/ All Objectives
    perf.all.rse <- lm_robust(log(y_sys_perf)
                            ~ x_num_nodes
                            + x_objective_fn
                            + x_prob_triangle
                            + x_conv_threshold
                            + x_est_prob
                            , data=df
                            , se_type="stata")
    summary(perf.all.rse)

    # Performance w/ Absolute sum only
    perf.abs.rse <- lm_robust(log(y_sys_perf)
                            ~ x_num_nodes
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
                            + x_conv_threshold
                            + x_est_prob
                            , data=df_sph
                            , se_type="stata")
    summary(perf.sph.rse)
    
    # Performance w/ Ackley only
    perf.ack.rse <- lm_robust(log(y_sys_perf)
                            ~ x_num_nodes
                            + x_prob_triangle
                            + x_conv_threshold
                            + x_est_prob
                            , data=df_ack
                            , se_type="stata")
    summary(perf.ack.rse)

    # Performance w/ Levy only
    perf.lvy.rse <- lm_robust(log(y_sys_perf)
                            ~ x_num_nodes
                            + x_prob_triangle
                            + x_conv_threshold
                            + x_est_prob
                            , data=df_lvy
                            , se_type="stata")
    summary(perf.lvy.rse)
    
    
# Regressions (w/ lm & vcov) ---------------------------------------------------
    
    # All in one
    perf.all.se <- lm(y_sys_perf
                      ~ x_num_nodes
                      + x_objective_fn
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df)
    boxcox(perf.all.se, plotit=TRUE)
    summary(perf.all.se)
    
    
    # Absolute sum only
    perf.abs.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_abs)
    summary(perf.abs.se)
    
    # Sphere only
    perf.sph.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_sph)
    summary(perf.sph.se)
    
    # Ackley only
    perf.ack.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
                      + x_est_prob
                      , data=df_ack)
    summary(perf.ack.se)
    
    # Levy only
    perf.lvy.se <- lm(log(y_sys_perf)
                      ~ x_num_nodes
                      + x_prob_triangle
                      + x_conv_threshold
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
            "Absolute-Sum Fn",
            "Sphere Fn",
            "Ackley Fn",
            "Levy Fn"
        ),
        omit.stat = "f")






