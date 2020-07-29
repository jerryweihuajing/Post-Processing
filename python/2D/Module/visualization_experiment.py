# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:57:21 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Plot of an experiment
"""

import os

import visualization_series as V_S
import visualization_animation as V_A
import visualization_integral_analysis as V_I_A

#------------------------------------------------------------------------------   
"""
Total export depending on mode list of an experiment which contain a branch of cases

Args:
    experiment_path: load path of all input files cases
   
Returns:
    None
""" 
def VisualizationExperiment(experiment_path):
    
    print('')
    print('-- Visualization Experiment')
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        #with and without fracture
        for this_bool in [True,False]:
            
            #plot everything
            V_S.ProgressAll(this_case_path,with_fracture=this_bool)   
            V_A.AnimationAll(this_case_path,with_fracture=this_bool)
            V_I_A.IntegralAnalysisAll(this_case_path,with_fracture=this_bool)
                    