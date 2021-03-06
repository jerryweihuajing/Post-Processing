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

case_path=r'E:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single base fracture bT=2.4 fI=-30 fO=50 fD=0-50'

#step 1
C_C_E.CaseCalculation(case_path)

##step 2
case_path=case_path.replace('input','output')

V_C.CaseVisualization(case_path)
