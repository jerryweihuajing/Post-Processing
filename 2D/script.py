# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:14:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

''' 
demand 4:
    add colorbar
    
demand 5:
    comparision as an experiment
    
demand 6:
    individual and integral analysis in progress visualization
'''

from __init__ import *

case_path=r'C:\Users\魏华敬\Desktop\YADE\Data\extension 100-200\input\double diff-1'

#step 1
C_C_E.CaseCalculation(case_path,which_mode_list='standard')

#step 2
case_path=case_path.replace('in','out')
output_folder=r'C:\Users\魏华敬\Desktop\extension'

V_C.CaseVisualization(case_path,output_folder)
