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

folder_input=r'H:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\input'
folder_output=folder_input.replace('input','output')

list_case_input=[this_case_name for this_case_name in os.listdir(folder_input)]
list_case_output=[this_case_name for this_case_name in os.listdir(folder_output)]

for this_case_name in list_case_input:
    
    if this_case_name not in list_case_output:
        
        if version=='lite':
        
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list=['structural_deformation'])
        
        else:
            
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list='standard',final_only=False)
            