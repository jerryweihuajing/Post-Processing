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
'''

from __init__ import *

case_path=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\input\single'

#step 1
C_C_E.CaseCalculation(case_path,which_mode_list='standard')

##step 2
#case_path=case_path.replace('input','output')
#
#V_C.CaseVisualization(case_path)

        