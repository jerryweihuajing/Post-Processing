# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 21:23:14 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：calculation script
"""

from __init__ import *

#version='lite'
version='pro'

folder_input=r'D:\GitHub\YADE\Controlling-Simulation\2D\compression 100-800\input'
folder_output=folder_input.replace('input','output')

O_P.GenerateFolder(folder_output)

list_case_input=[this_case_name for this_case_name in os.listdir(folder_input)]
list_case_output=[this_case_name for this_case_name in os.listdir(folder_output)]

for this_case_name in list_case_input:

    if version=='lite':
        
        if this_case_name not in list_case_output or O_P.FilesAmount(folder_output+'\\'+this_case_name)[2]==0:
            
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list=['Structural Deformation'],exception='final only')
        
    if version=='pro':
        
        '''all: 728'''
        '''standard: 264'''
        '''final only all: 91'''
        '''final only standard: 33'''
        '''original and final all: 182'''
        '''original and final standard: 66'''
        if this_case_name not in list_case_output or O_P.FilesAmount(folder_output+'\\'+this_case_name)[2]<66:
            
            C_C_E.CaseCalculation(folder_input+'\\'+this_case_name,which_mode_list='standard',exception='original and final')
            