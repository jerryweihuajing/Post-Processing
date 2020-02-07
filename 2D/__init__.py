# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 14:11:13 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：initialization script
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path)) 

import operation_case as O_C

import calculation_custom_export as C_C_E