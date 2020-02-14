# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:03:54 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：visualization script
"""

from __init__ import *

version='lite'
#version='pro'

folder_output=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\output'
folder_Figures=folder_output.replace('output','Figures')

list_case_output=[this_case_name for this_case_name in os.listdir(folder_output)]
list_case_Figures=[this_case_name for this_case_name in os.listdir(folder_Figures)]

for this_case_name in list_case_output:
    
    amount_files=O_P.FilesAmount(folder_Figures+'\\'+this_case_name)[2]
    
    if version=='lite':
        
        if this_case_name not in list_case_Figures or amount_files==0:
            
            progress_folder=folder_output+'\\'+this_case_name+'\\structural deformation\\values'
            
            #looking for final progress by index of max
            list_percentage=[float(this_str.split('%')[0]) for this_str in os.listdir(progress_folder)]
            progress_name=os.listdir(progress_folder)[list_percentage.index(max(list_percentage))]
            
            final_progress=V_P.ProgressConstruction(progress_folder+'\\'+progress_name)
            
            V_I.Individual(folder_Figures+'\\'+this_case_name,final_progress,situation='progress')
            
    if version=='pro':
    
        if amount_files!=174:
            
            V_C.CaseVisualization(folder_output+'\\'+this_case_name,lite=False)
                