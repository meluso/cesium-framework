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
    library(modelsummary)
    library(knitr)
    library(kableExtra)
    library(gt)
    library(tibble)
    library(magrittr)
    # library(stargazer)
    library(sandwich)
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
    
    robust <- function(linmod){
        cov <- vcovHC(linmod, type = "HC1")
        rse <- sqrt(diag(cov))
    }


# Performance Regressions (w/ lm & vcov) ---------------------------------------

    # All in one
    perf.all <- lm(log(y_sys_perf)
                   ~ log(x_num_nodes)
                   + x_objective_fn
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df)
    summary(perf.all)
    #plot(perf.all,which=c(2))
    perf.all.res <- density(resid(perf.all))
    plot(perf.all.res)
    
    
    # Absolute sum only
    perf.abs <- lm(log(y_sys_perf)
                   ~ log(x_num_nodes)
                   #+ x_num_nodes + I(1/x_num_nodes) + I(1/x_num_nodes^2)
                   + x_prob_triangle
                   #+ x_conv_threshold + I(1/x_conv_threshold) + I(1/x_conv_threshold^2)
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_abs)
    summary(perf.abs)
    #plot(perf.abs,which=c(2))
    perf.abs.res <- density(resid(perf.abs))
    plot(perf.abs.res)
    
    # Sphere only
    df_sph$x_ep_poly <- with(df_sph, poly(x_est_prob, degree = 3))[, c(-1)]
    perf.sph <- lm(log(y_sys_perf)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   #+ x_ep_poly
                   , data=df_sph)
    summary(perf.sph)
    #plot(perf.sph,which=c(2))
    perf.sph.res <- density(resid(perf.sph))
    plot(perf.sph.res)
    
    # Ackley only
    perf.ack <- lm(log(y_sys_perf)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_ack)
    summary(perf.ack)
    #plot(perf.ack,which=c(2))
    perf.ack.res <- density(resid(perf.ack))
    plot(perf.ack.res)
    
    # Levy only
    perf.lvy <- lm(log(y_sys_perf)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_lvy)
    summary(perf.lvy)
    #plot(perf.lvy,which=c(2))
    perf.lvy.res <- density(resid(perf.lvy))
    plot(perf.lvy.res)


    ### Performance Latex Tables ###

    # Rename functions
    mod_list = list()
    mod_list[['All Functions']] <- perf.all
    mod_list[['Absolute-Sum']] <- perf.abs
    mod_list[['Sphere']] <- perf.sph
    mod_list[['Ackley']] <- perf.ack
    mod_list[['Levy']] <- perf.lvy
    
    # Insert dependent variable
    rows <- tribble(~term, ~M1, ~M2, ~M3, ~M4, ~M5,
                    'Dependent Variable',
                    'log(Sys. Perf.)',
                    'log(Sys. Perf.)',
                    'log(Sys. Perf.)',
                    'log(Sys. Perf.)',
                    'log(Sys. Perf.)',
                    '','','','','','')
    attr(rows, 'position') <- c(1,2)
    
    # Create rows
    cm = c('(Intercept)' = 'Constant',
           'x_objective_fnsphere' = 'Fn: Sphere',
           'x_objective_fnackley' = 'Fn: Ackley',
           'x_objective_fnlevy' = 'Fn: Levy',
           'log(x_num_nodes)' = 'log(Number of Nodes)',
           'log(x_conv_threshold)' = 'log(Convergence Threshold)',
           'x_prob_triangle' = 'Triangle Probability',
           'x_est_prob' = 'Future Estimate Probability',
           'x_ep_poly2' = '(Future Estimate Probability)^2',
           'x_ep_poly3' = '(Future Estimate Probability)^3'
    )
    
    # Construct table
    tab = modelsummary(mod_list,
                       add_rows = rows,
                       coef_map = cm,
                       gof_omit = 'IC|Log',
                       output = 'latex',
                       stars = c('+' = .05, '*' = 0.01, '**' = 0.005, '***' = 0.001),
                       vcov = 'stata'
    )
    
    # Save to file
    save_kable(tab,file = "C:/Users/Juango the Blue/Documents/GitHub/cesium/figures/table_reg_perf.tex")
    
    
# Cycle Regressions (w/ lm & vcov) ---------------------------------------
    
    # All in one
    cycl.all <- lm(log(y_num_cycles)
                   ~ log(x_num_nodes)
                   + x_objective_fn
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df)
    summary(cycl.all)
    #plot(cycl.all,which=c(2))
    cycl.all.res <- density(resid(cycl.all))
    plot(cycl.all.res)
    
    
    # Absolute sum only
    cycl.abs <- lm(log(y_num_cycles)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_abs)
    summary(cycl.abs)
    #plot(cycl.abs,which=c(2))
    cycl.abs.res <- density(resid(cycl.abs))
    plot(cycl.abs.res)
    
    # Sphere only
    cycl.sph <- lm(log(y_num_cycles)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_sph)
    summary(cycl.sph)
    #plot(cycl.sph,which=c(2))
    cycl.sph.res <- density(resid(cycl.sph))
    plot(cycl.sph.res)
    
    # Ackley only
    cycl.ack <- lm(log(y_num_cycles)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + log(x_conv_threshold)
                   + x_est_prob
                   , data=df_ack)
    summary(cycl.ack)
    #plot(cycl.ack,which=c(2))
    cycl.ack.res <- density(resid(cycl.ack))
    plot(cycl.ack.res)
    
    # Levy only
    df_lvy$x_ep_poly <- with(df_lvy, poly(x_est_prob, degree = 2))[, c(-1)]
    cycl.lvy <- lm(log(y_num_cycles)
                   ~ log(x_num_nodes)
                   + x_prob_triangle
                   + x_conv_threshold
                   + x_est_prob
                   + x_ep_poly
                   , data=df_lvy)
    summary(cycl.lvy)
    #plot(cycl.lvy,which=c(2))
    cycl.lvy.res <- density(resid(cycl.lvy))
    plot(cycl.lvy.res)

    
    ### Cycles Latex Tables ###
    
    # Rename functions
    mod_list = list()
    mod_list[['All Functions']] <- cycl.all
    mod_list[['Absolute-Sum']] <- cycl.abs
    mod_list[['Sphere']] <- cycl.sph
    mod_list[['Ackley']] <- cycl.ack
    mod_list[['Levy']] <- cycl.lvy
    
    # Insert dependent variable
    rows <- tribble(~term, ~M1, ~M2, ~M3, ~M4, ~M5,
                    'Dependent Variable',
                    'log(Num. Cycles)',
                    'log(Num. Cycles)',
                    'log(Num. Cycles)',
                    'log(Num. Cycles)',
                    'log(Num. Cycles)',
                    '','','','','','')
    attr(rows, 'position') <- c(1,2)
    
    # Create rows
    cm = c('(Intercept)' = 'Constant',
           'x_objective_fnsphere' = 'Fn: Sphere',
           'x_objective_fnackley' = 'Fn: Ackley',
           'x_objective_fnlevy' = 'Fn: Levy',
           'log(x_num_nodes)' = 'log(Number of Nodes)',
           'log(x_conv_threshold)' = 'log(Convergence Threshold)',
           'x_prob_triangle' = 'Triangle Probability',
           'x_est_prob' = 'Future Estimate Probability',
           'x_ep_poly' = '(Future Estimate Probability)^2'
    )
    
    # Construct table
    tab = modelsummary(mod_list,
                       add_rows = rows,
                       coef_map = cm,
                       gof_omit = 'IC|Log',
                       output = 'latex',
                       stars = c('+' = .05, '*' = 0.01, '**' = 0.005, '***' = 0.001),
                       vcov = 'stata'
    )
    
    # Save to file
    save_kable(tab,file = "C:/Users/Juango the Blue/Documents/GitHub/cesium/figures/table_reg_cycl.tex")

    
# Save Distributions -----------------------------------------------------------
    
    dist.perf.x = data.frame(perf.all.res$x,
                             perf.abs.res$x,
                             perf.sph.res$x,
                             perf.ack.res$x,
                             perf.lvy.res$x)
    
    dist.perf.y = data.frame(perf.all.res$y,
                             perf.abs.res$y,
                             perf.sph.res$y,
                             perf.ack.res$y,
                             perf.lvy.res$y)
    
    dist.cycl.x = data.frame(cycl.all.res$x,
                             cycl.abs.res$x,
                             cycl.sph.res$x,
                             cycl.ack.res$x,
                             cycl.lvy.res$x)
    
    dist.cycl.y = data.frame(cycl.all.res$y,
                             cycl.abs.res$y,
                             cycl.sph.res$y,
                             cycl.ack.res$y,
                             cycl.lvy.res$y)