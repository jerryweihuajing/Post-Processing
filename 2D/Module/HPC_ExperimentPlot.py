# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:57:21 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Plot of an experiment
"""

import os

import HPC_ProgressPlot as HPC_PP
import HPC_AnimationPlot as HPC_AP
import HPC_IntegralAnalysisPlot as HPC_IAP

#------------------------------------------------------------------------------   
"""
Total export depending on mode list of an experiment which contain a branch of cases

Args:
   experiment_path: load path of all input files cases
   
Returns:
    mass of PNGs, TXTs, GIFs in output folder
""" 
def ExperimentPlotAll(experiment_path):
    
    print('')
    print('-- Experiment Plot All')
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        #with and without fracture
        for this_bool in [True,False]:
            
            #plot everything
            HPC_PP.ProgressAll(this_case_path,with_fracture=this_bool)   
            HPC_AP.AnimationAll(this_case_path,with_fracture=this_bool)
            HPC_IAP.IntegralAnalysisAll(this_case_path,with_fracture=this_bool)
            
#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    
    def __init__(self,
                 percentage=None,
                 mean_normal_stress=None,
                 maximal_shear_stress=None,
                 periodical_volumrtric_strain=None,
                 periodical_distortional_strain=None,
                 cumulative_volumrtric_strain=None,
                 cumulative_distortional_strain=None,
                 fracture=None):
        
        self.percentage=percentage
        self.mean_normal_stress=mean_normal_stress
        self.maximal_shear_stress=maximal_shear_stress
        self.periodical_volumrtric_strain=periodical_volumrtric_strain
        self.periodical_distortional_strain=periodical_distortional_strain
        self.cumulative_volumrtric_strain=cumulative_volumrtric_strain
        self.cumulative_distortional_strain=cumulative_distortional_strain
        self.fracture=fracture
        
#==============================================================================
#object case to manage data efficiently
#==============================================================================    
class case:
    
    def __init__(self,
                 condition=None,
                 list_progress=None):
        
        self.condition=condition
        self.list_progress=list_progress

#==============================================================================
#object experiment to manage data efficiently
#==============================================================================     
class experiment:
    
    def __init__(self,
                 prameter=None,
                 list_case=None):
    
        self.parameter=parameter
        self.list_case=list_case