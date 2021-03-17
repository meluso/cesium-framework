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
    
    # Import data
    df <- read.csv("~/GitHub/cesium/data/sets/execset001_summary.csv",
                   header=FALSE)
    df <- df[c(3:4,6:7,12,14:15)]
    # Name variables
    names(df) = c('x_num_nodes', # nod = [50, 100, 500, 1000]
                  'x_objective_fn', # obj = ["absolute-sum","sphere","levy","ackley"]
                  'x_prob_triangle', # tri = np.round(np.arange(0,1.1,0.1),decimals=1)
                  'x_conv_threshold', # con = np.array([0.01,0.05,0.1,0.5,1,5,10])
                  'x_est_prob', # prb = np.round(np.arange(0,1.1,0.1),decimals=1)
                  'y_num_cycles',
                  'y_sys_perf'
    )
    
    robust <- function(linmod){
        cov <- vcovHC(linmod, type = "HC1")
        rse <- sqrt(diag(cov))
    }
    
    # Slice by objective function
    df_abs <- df[df$x_objective_fn == "absolute-sum",-c(2)]
    df_sph <- df[df$x_objective_fn == "sphere",-c(2)]
    df_ack <- df[df$x_objective_fn == "ackley",-c(2)]
    df_lvy <- df[df$x_objective_fn == "levy",-c(2)]


# Performance Regressions (w/ lm & vcov) ---------------------------------------

    # All in one 1
    perf.all1 <- lm(y_sys_perf ~ . - y_num_cycles, data=df)
    summary(perf.all1)
    #perf.all1.res <- density(resid(perf.all1))
    #plot(perf.all1.res)
    
    # All in one 2
    perf.all2 <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles), data=df)
    summary(perf.all2)
    #perf.all2.res <- density(resid(perf.all2))
    #plot(perf.all2.res)
    
    # All in one 3
    perf.all3 <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles)*(. - y_num_cycles - x_objective_fn), data=df)
    summary(perf.all3)
    #perf.all3.res <- density(resid(perf.all3))
    #plot(perf.all3.res)
    
    # All in one 4
    perf.all4 <- lm(y_sys_perf ~ x_objective_fn*(. - y_num_cycles - x_objective_fn), data=df)
    summary(perf.all4)
    #perf.all4.res <- density(resid(perf.all4))
    #plot(perf.all4.res)
    
    # Absolute sum only
    perf.abs <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_abs)
    summary(perf.abs)
    #perf.abs.res <- density(resid(perf.abs))
    #plot(perf.abs.res)
    
    # Sphere only 1
    perf.sph1 <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_sph)
    summary(perf.sph1)
    #perf.sph1.res <- density(resid(perf.sph1))
    #plot(perf.sph1.res)
    
    # Ackley only
    perf.ack <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_ack)
    summary(perf.ack)
    #perf.ack.res <- density(resid(perf.ack))
    #plot(perf.ack.res)
    
    # Levy only
    perf.lvy <- lm(y_sys_perf ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_lvy)
    summary(perf.lvy)
    #perf.lvy.res <- density(resid(perf.lvy))
    #plot(perf.lvy.res)
    
    # Transforms Sphere variables
    x_nn_log <- log(df_sph$x_num_nodes)
    df_sph$x_num_nodes <- x_nn_log
    x_ct_log <- log(df_sph$x_conv_threshold)
    df_sph$x_conv_threshold <- x_ct_log
    
    # Sphere only 2
    perf.sph2 <- lm(log(y_sys_perf) ~ (. - y_num_cycles)*(. - y_num_cycles) , data=df_sph)
    summary(perf.sph2)
    #perf.sph2.res <- density(resid(perf.sph2))
    #plot(perf.sph2.res)


# Performance Latex Tables -----------------------------------------------------

    # Rename functions
    mod_list = list()
    mod_list[['Model II.1']] <- perf.all1
    mod_list[['Model II.2']] <- perf.all2
    mod_list[['Model II.3']] <- perf.abs
    mod_list[['Model II.4']] <- perf.sph1
    mod_list[['Model II.7']] <- perf.sph2
    mod_list[['Model II.5']] <- perf.ack
    mod_list[['Model II.6']] <- perf.lvy
    
    # Set Objective Function Column Headers
    spanlist = c(" " = 1,
                 "All Functions" = 2,
                 "Absolute Sum" = 1,
                 "Sphere" = 2,
                 "Ackley" = 1,
                 "Levy" = 1)
    
    # Insert dependent variable
    rows <- tribble(~term, ~M1, ~M2, ~M3, ~M4, ~M5, ~M6, ~M7,
                    'Dependent Variable',
                    'Sys. Perf.',
                    'Sys. Perf.',
                    'Sys. Perf.',
                    'Sys. Perf.',
                    'log(Sys. Perf.)',
                    'Sys. Perf.',
                    'Sys. Perf.',
                    '','','','','','','',''
                    )
    attr(rows, 'position') <- c(1,2)
    
    # Create rows
    cm = c(
        '(Intercept)' = 'Constant',
        'x_objective_fnsphere' = 'Fn: Sphere',
        'x_objective_fnackley' = 'Fn: Ackley',
        'x_objective_fnlevy' = 'Fn: Levy',
        'x_num_nodes' = 'Num. Nodes',
        'x_prob_triangle' = 'Tri. Prob.',
        'x_conv_threshold' = 'Conv. Thresh.',
        'x_est_prob' = 'Fut. Est. Prob.',
        'x_num_nodes:x_prob_triangle' = 'Num. Nodes x Tri. Prob.',
        'x_num_nodes:x_conv_threshold' = 'Num. Nodes x Conv. Thresh.',
        'x_num_nodes:x_est_prob' = 'Num. Nodes x Fut. Est. Prob.',
        'x_prob_triangle:x_conv_threshold' = 'Tri. Prob. x Conv. Thresh.',
        'x_prob_triangle:x_est_prob' = 'Tri. Prob. x Fut. Est. Prob.',
        'x_conv_threshold:x_est_prob' = 'Conv. Thresh. x Fut. Est. Prob.',
        'x_num_nodes:x_objective_fnsphere' = 'Fn: Sphere x Num. Nodes',
        'x_objective_fnsphere:x_prob_triangle' = 'Fn: Sphere x Tri. Prob.',
        'x_objective_fnsphere:x_conv_threshold' = 'Fn: Sphere x Conv. Thresh.',
        'x_objective_fnsphere:x_est_prob' = 'Fn: Sphere x Fut. Est. Prob.',
        'x_num_nodes:x_objective_fnackley' = 'Fn: Ackley x Num. Nodes',
        'x_objective_fnackley:x_prob_triangle' = 'Fn: Ackley x Tri. Prob.',
        'x_objective_fnackley:x_conv_threshold' = 'Fn: Ackley x Conv. Thresh.',
        'x_objective_fnackley:x_est_prob' = 'Fn: Ackley x Fut. Est. Prob.',
        'x_num_nodes:x_objective_fnlevy' = 'Fn: Levy x Num. Nodes',
        'x_objective_fnlevy:x_prob_triangle' = 'Fn: Levy x Tri. Prob.',
        'x_objective_fnlevy:x_conv_threshold' = 'Fn: Levy x Conv. Thresh.',
        'x_objective_fnlevy:x_est_prob' = 'Fn: Levy x Fut. Est. Prob.'
    )
    
    # Add a note about log variables
    notes = list('Variable log-transformed for Model II.7 only')
    
    # Update stats to include
    gm <- modelsummary::gof_map
    gm$omit <- FALSE
    
    # Construct table
    tab = modelsummary(mod_list,
                       add_rows = rows,
                       coef_map = cm,
                       output = 'latex',
                       stars = c('+' = .05, '*' = 0.01, '**' = 0.005, '***' = 0.001),
                       vcov = 'stata',
                       gof_map = gm,
                       gof_omit = 'DF|Deviance|AIC|BIC|Statistics|Log|p|F',
                       notes = notes
    )
    
    # Create spanner
    tab = add_header_above(tab,spanlist)
    
    # Save to file
    save_kable(tab,file = "C:/Users/Juango the Blue/Documents/GitHub/cesium/figures/table_reg_perf.tex")
    
    
# Cycle Regressions (w/ lm & vcov) ---------------------------------------
    
    # All in one 1
    cycl.all1 <- lm(y_num_cycles ~ . - y_num_cycles, data=df)
    summary(cycl.all1)
    #cycl.all1.res <- density(resid(cycl.all1))
    #plot(cycl.all1.res)
    
    # All in one 2
    cycl.all2 <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df)
    summary(cycl.all2)
    #cycl.all2.res <- density(resid(cycl.all2))
    #plot(cycl.all2.res)
    
    # Absolute sum only
    cycl.abs <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_abs)
    summary(cycl.abs)
    #cycl.abs.res <- density(resid(cycl.abs))
    #plot(cycl.abs.res)
    
    # Sphere only
    cycl.sph <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_sph)
    summary(cycl.sph)
    #cycl.sph.res <- density(resid(cycl.sph))
    #plot(cycl.sph.res)
    
    # Ackley only
    cycl.ack <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_ack)
    summary(cycl.ack)
    #cycl.ack.res <- density(resid(cycl.ack))
    #plot(cycl.ack.res)
    
    # Levy only
    cycl.lvy <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_lvy)
    summary(cycl.lvy)
    #cycl.lvy.res <- density(resid(cycl.lvy))
    #plot(cycl.lvy.res)
    
    # # Levy only
    # df_lvy$x_ep_poly <- with(df_lvy, poly(x_est_prob, degree = 2))[, c(-1)]
    # cycl.lvy <- lm(y_num_cycles ~ (. - y_num_cycles)*(. - y_num_cycles), data=df_lvy)
    # summary(cycl.lvy)
    # cycl.lvy.res <- density(resid(cycl.lvy))
    # plot(cycl.lvy.res)

    
# Cycles Latex Tables ----------------------------------------------------------
    
    # Rename functions
    mod_list = list()
    mod_list[['Model III.1']] <- cycl.all1
    mod_list[['Model III.2']] <- cycl.all2
    mod_list[['Model III.3']] <- cycl.abs
    mod_list[['Model III.4']] <- cycl.sph
    mod_list[['Model III.5']] <- cycl.ack
    mod_list[['Model III.6']] <- cycl.lvy
    
    # Set Objective Function Column Headers
    spanlist = c(" " = 1,
                 "All Functions" = 2,
                 "Absolute Sum" = 1,
                 "Sphere" = 1,
                 "Ackley" = 1,
                 "Levy" = 1)

    # Insert dependent variable
    rows <- tribble(~term, ~M1, ~M2, ~M3, ~M4, ~M5, ~M6,
                    'Dependent Variable',
                    'Num. Cycles',
                    'Num. Cycles',
                    'Num. Cycles',
                    'Num. Cycles',
                    'Num. Cycles',
                    'Num. Cycles',
                    '','','','','','','')
    attr(rows, 'position') <- c(1,2)
    
    # Create rows
    cm = c('(Intercept)' = 'Constant',
           'x_objective_fnsphere' = 'Fn: Sphere',
           'x_objective_fnackley' = 'Fn: Ackley',
           'x_objective_fnlevy' = 'Fn: Levy',
           'x_num_nodes' = 'Num. Nodes',
           'x_prob_triangle' = 'Tri. Prob.',
           'x_conv_threshold' = 'Conv. Thresh.',
           'x_est_prob' = 'Fut. Est. Prob.',
           'x_num_nodes:x_prob_triangle' = 'Num. Nodes x Tri. Prob.',
           'x_num_nodes:x_conv_threshold' = 'Num. Nodes x Conv. Thresh.',
           'x_num_nodes:x_est_prob' = 'Num. Nodes x Fut. Est. Prob.',
           'x_prob_triangle:x_conv_threshold' = 'Tri. Prob. x Conv. Thresh.',
           'x_prob_triangle:x_est_prob' = 'Tri. Prob. x Fut. Est. Prob.',
           'x_conv_threshold:x_est_prob' = 'Conv. Thresh. x Fut. Est. Prob.',
           'x_num_nodes:x_objective_fnsphere' = 'Fn: Sphere x Num. Nodes',
           'x_objective_fnsphere:x_prob_triangle' = 'Fn: Sphere x Tri. Prob.',
           'x_objective_fnsphere:x_conv_threshold' = 'Fn: Sphere x Conv. Thresh.',
           'x_objective_fnsphere:x_est_prob' = 'Fn: Sphere x Fut. Est. Prob.',
           'x_num_nodes:x_objective_fnackley' = 'Fn: Ackley x Num. Nodes',
           'x_objective_fnackley:x_prob_triangle' = 'Fn: Ackley x Tri. Prob.',
           'x_objective_fnackley:x_conv_threshold' = 'Fn: Ackley x Conv. Thresh.',
           'x_objective_fnackley:x_est_prob' = 'Fn: Ackley x Fut. Est. Prob.',
           'x_num_nodes:x_objective_fnlevy' = 'Fn: Levy x Num. Nodes',
           'x_objective_fnlevy:x_prob_triangle' = 'Fn: Levy x Tri. Prob.',
           'x_objective_fnlevy:x_conv_threshold' = 'Fn: Levy x Conv. Thresh.',
           'x_objective_fnlevy:x_est_prob' = 'Fn: Levy x Fut. Est. Prob.'
    )
    
    # Update stats to include
    gm <- modelsummary::gof_map
    gm$omit <- FALSE
    
    # Construct table
    tab = modelsummary(mod_list,
                       add_rows = rows,
                       coef_map = cm,
                       output = 'latex',
                       stars = c('+' = .05, '*' = 0.01, '**' = 0.005, '***' = 0.001),
                       vcov = 'stata',
                       gof_map = gm,
                       gof_omit = 'DF|Deviance|AIC|BIC|Statistics|Log|p|F'
    )
    
    # Create spanner
    tab = add_header_above(tab,spanlist)
    
    # Save to file
    save_kable(tab,file = "C:/Users/Juango the Blue/Documents/GitHub/cesium/figures/table_reg_cycl.tex")
