# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 01:27:55 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot of an experiment
"""

import os

import ProgressPlot as PP
import AnimationPlot as AP
import IntegralAnalysisPlot as IAP

#------------------------------------------------------------------------------   
"""
Total export depending on mode list of an experiment which contain a branch of cases

Args:
   experiment_path: load path of all input files cases
   
Returns:
    mass of PNGs, TXTs, GIFs in output folder
""" 
def ExperimentPlotAll(experiment_path):
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        #with and without fracture
        for this_bool in [True,False]:
            
            #plot everything
            PP.ProgressAll(this_case_path,with_fracture=this_bool)   
            AP.AnimationAll(this_case_path,with_fracture=this_bool)
            IAP.IntegralAnalysisAll(this_case_path,with_fracture=this_bool)