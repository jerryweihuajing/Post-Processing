# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:23:14 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：calculation script
"""

from __init__ import *

version='lite'
#version='pro'

folder_input=r'H:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\input'
folder_output=folder_input.replace('input','output')

list_case_input=[this_case_name for this_case_name in os.listdir(folder_input)]
list_case_output=[this_case_name for this_case_name in os.listdir(folder_output)]

for this_case_name in list_case_input:

    if version=='lite':
        
        if this_case_name not in list_case_output or O_P.FilesAmount(folder_output+'\\'+this_case_name)[2]==0:
            
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list=['structural_deformation'])
        
    if version=='pro':
        
        if O_P.FilesAmount(folder_output+'\\'+this_case_name)[2]!=56:
            
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list='standard',final_only=False)
            