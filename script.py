# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

''' 
demand 3:
    improve morphorlogy of outline
    
demand 4:
    combine 2 images on transparency
    
demand 10:
    smooth stress and strain
'''

from __init__ import *

#A experiment
experiment_path=os.getcwd()+'\\Data\\100-1000\\base detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

EP.ExperimentPlotAll(experiment_path)


'''for testing'''
#case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45'
#
#PP.ProgressStructuralDeformation(case_path,with_fracture=True)
#
#file_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45\structural deformation\values\27.87%.txt'
#
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='standard',with_fracture=True)
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='all',with_fracture=True)