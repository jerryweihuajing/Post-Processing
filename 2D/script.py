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
#experiment_path=os.getcwd()+'\\Data\\100-500\\base detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

#EP.ExperimentPlotAll(experiment_path)

#experiment_folder=os.getcwd()+'\\Data\\100-500\\base detachment'
#
#for this_experiment in os.listdir(experiment_folder):
#    
#    #concat data path
#    this_experiment_path=experiment_folder+'\\'+this_experiment
#    
#    print(this_experiment_path)
#    
#    CP.ExperimentPlot(this_experiment_path,'XoY',1,'standard')
#
#    EP.ExperimentPlotAll(this_experiment_path)
    

#a=[[0.50,0.50,0.50],[1.00,0.00,0.00],[0.00,1.00,0.00],[1.00,1.00,0.00],[0.85,0.85,0.85],[0.00,1.00,1.00],]
#
#b=[]
#
#for this in a:
#    
#    that=[]
#    
#    for item in this:
#        
#        bit=int(item*256)
#        
#        if bit>0:
#            
#            that.append(bit-1)
#            
#        else:
#            
#            that.append(bit)
#        
#    b.append(that)
#    
#    
#c=[k for k in range(len(b))]
#
#map_color=dict(zip(c,b))