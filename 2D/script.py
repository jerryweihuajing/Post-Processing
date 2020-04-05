# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:14:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

'''
demand:
    content to print should be consecutive
'''

from __init__ import *

case_path=r'D:\GitHub\YADEM\Controlling-Simulation\2D\extension 150-600\Data\input\double diff-1'

#step 1
#C_C_E.CaseCalculation(case_path,which_mode_list=['-Periodical','-Instantaneous'])

#step 2
case_path=case_path.replace('input','output')

V_C.CaseVisualization(case_path)
