# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

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

#A experiment
experiment_path=os.getcwd()+'\\Data\\100-500\\base detachment\\fric=0.1 v=0.2'

CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

EP.ExperimentPlotAll(experiment_path)
