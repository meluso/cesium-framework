# Setup ------------------------------------------------------------------------

  # Clear the environment and console
  rm(list = ls())
  cat("\014")
  
  # Import libraries
  library(ggplot2)
  library(gplots)
  
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