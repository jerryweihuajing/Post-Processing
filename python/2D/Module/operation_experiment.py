# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:40:58 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Experiment Operation
"""

#------------------------------------------------------------------------------   
"""
Construct an experiment object

Args:
   experiment_path: path to construct
   
Returns:
    experiment object
""" 
def ExperimentConstruction(experiment_path):
    
    that_experiment=experiment()
    
    that_experiment.parameter=experiment_path.split('\\')[-1]
    that_experiment.list_case=[]
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        that_experiment.list_case.append(CaseConstruction(this_case_path))
        
    return that_experiment