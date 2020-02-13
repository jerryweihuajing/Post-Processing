# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:23:14 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：calculation script
"""

from __init__ import *

folder_input=r'H:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\output'
folder_output=folder_input.replace('input','output')

list_case_input=[folder_input+'\\'+this_case_name for this_case_name in os.listdir(folder_input)]
list_case_output=[folder_output+'\\'+this_case_name for this_case_name in os.listdir(folder_output)]

for this_case_path in list_case_input:
    
    if this_case_path not in list_case_output:
        
        C_C_E.CaseCalculation(this_case_path,which_mode_list='standard')