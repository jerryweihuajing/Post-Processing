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
'''

from __init__ import *

case_path=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-500\input\single'

that_case=C_C_E.CaseGeneration(case_path)

##step 1
#C_C_E.CaseCalculation(case_path,which_mode_list='standard',final_only=False)
#
##step 2
#case_path=case_path.replace('input','output')
##
#V_C.CaseVisualization(case_path)
#         
#case_folder=r'H:\GitHub\YADE\Controlling-Simulation\2D\extension 100-200\input'
#
#for this_case_name in os.listdir(case_folder):
#    
#    C_C_E.CaseCalculation(case_folder+'\\'+this_case_name,which_mode_list=['structural_deformation'],final_only=False)