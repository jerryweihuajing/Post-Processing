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
     
demand 11:
    gaussian convolution by matrix 
    
demand 12:
    convolution considering nan
'''

from __init__ import *

#A experiment
experiment_path=os.getcwd()+'\\Data\\100-1000\\base detachment\\fric=0.0 v=0.2'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

EP.ExperimentPlotAll(experiment_path)

#path_A=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=2.72\structural deformation\images\19.68%.png'
#path_B=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=2.72\periodical strain\distortional\images\19.68%.png'
#
##Input 2 PNG images
#image_A=plt.imread(path_A)
#image_B=plt.imread(path_B)

#IS.OpacitySuperposeImages(image_A,image_B)

'''for testing'''
#case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45'
#
#PP.ProgressStructuralDeformation(case_path,with_fracture=True)
#
#file_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45\structural deformation\values\27.87%.txt'
#
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='standard',with_fracture=True)
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='all',with_fracture=True)

#        
#txt_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=10.89\periodical strain\distortional\values\27.87%.txt'
#mat=Mat.ImportMatrixFromTXT(txt_path)

#window=Window(mat,30,2,5)
#kernel=GaussianKernel(0,1,5)
#
#a=Convolution(window,kernel)

#s=ImageSmooth(mat)
#
#plt.figure()
#plt.subplot(211)
#plt.imshow(mat,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))
#
#plt.subplot(212)
#plt.imshow(s,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))