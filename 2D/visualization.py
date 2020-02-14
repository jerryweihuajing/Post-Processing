# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:03:54 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：visualization script
"""

from __init__ import *

#version='lite'
version=''

folder_output=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\output'
folder_Figures=folder_output.replace('output','Figures')

list_case_output=[this_case_name for this_case_name in os.listdir(folder_output)]
list_case_Figures=[this_case_name for this_case_name in os.listdir(folder_Figures)]

for this_case_name in list_case_output:
    
    if this_case_name not in list_case_Figures:
        
        if version=='lite':
            
            progress_folder=folder_output+'\\'+this_case_name+'\\structural deformation\\values'
            progress_name=os.listdir(progress_folder)[-1]
            
            final_progress=V_P.ProgressConstruction(progress_folder+'\\'+progress_name,lite=True)
            
            V_I.Individual(folder_Figures+'\\'+this_case_name,final_progress,situation='progress')
            
        else:
            
            V_C.CaseVisualization(folder_output+'\\'+this_case_name)
            
    else:
        
        if O_P.FilesAmount(folder_Figures+'\\'+this_case_name)[2]!=174:
            
            V_C.CaseVisualization(folder_output+'\\'+this_case_name)
                