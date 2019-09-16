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
     
demand 10:
    smooth stress and strain
'''

from __init__ import *

#A experiment
experiment_path=os.getcwd()+'\\Data\\100-1000\\base detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

#EP.ExperimentPlotAll(experiment_path)

#path_A=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=8.17\structural deformation\images\27.87%.png'
#path_B=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=8.17\periodical strain\distortional\images\27.87%.png'
#
##Input 2 PNG images
#image_A=plt.imread(path_A)
#image_B=plt.imread(path_B)
#
#IS.SuperposeImages(image_A,image_B)

'''for testing'''
#case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45'
#
#PP.ProgressStructuralDeformation(case_path,with_fracture=True)
#
#file_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45\structural deformation\values\27.87%.txt'
#
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='standard',with_fracture=True)
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='all',with_fracture=True)

#------------------------------------------------------------------------------
"""
Smooth image

Args:
    which_image: image matrix to be smoothed
    smooth_operator: operator which performs (default: Gaussian)
        
Returns:
    image matrix which has been smoothed
"""
def Smooth(which_image,smooth_operator='Gaussian'):
    
    pass
    
    
    