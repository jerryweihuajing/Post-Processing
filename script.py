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
    
demand 9:
     unit and font
     
demand 10:
    smooth stress and strain
'''

from __init__ import *

#A experiment
experiment_path=os.getcwd()+'\\Data\\100-1000\\salt detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

EP.ExperimentPlotAll(experiment_path)