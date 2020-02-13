# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:03:54 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：visualization script
"""

from __init__ import *

folder_output=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\output'
folder_Figures=folder_output.replace('output','Figures')

list_case_output=[folder_output+'\\'+this_case_name for this_case_name in os.listdir(folder_output)]
list_case_Figures=[folder_Figures+'\\'+this_case_name for this_case_name in os.listdir(folder_Figures)]

for this_case_path in list_case_output:
    
    if this_case_path not in list_case_Figures:
        
        V_C.CaseVisualization(this_case_path)