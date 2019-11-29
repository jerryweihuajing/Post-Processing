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

#HPC_EP.ExperimentPlotAll(experiment_path)

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

case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\salt detachment\fric=0.0 v=0.2\output\salt=10.87'

#A experiment
#experiment_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2'

#a_case=CO.CaseConstruction(case_path)

structural_deformation_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=10.87\structural deformation\values\27.87%.txt'

a_progress=PO.ProgressConstruction(structural_deformation_path)

#output_folder=r'C:\Users\whj\Desktop\fig'

#CO.CasePostProcessing(case_path,output_folder)

import cv2

import Image as Img

img_rgb=Img.ImgFlip(a_progress.structural_deformation,0)
img_tag=Img.ImgFlip(a_progress.img_tag,0)

import matplotlib.pyplot as plt

laplacian=cv2.Laplacian(img_tag,cv2.CV_64F)

#sobel=cv2.Sobel(img_tag,cv2.CV_64F,1,1,ksize=3)
#sobelx=cv2.Sobel(img_tag,cv2.CV_64F,1,0,ksize=3)
#sobely=cv2.Sobel(img_tag,cv2.CV_64F,0,1,ksize=3)
#
#plt.figure()
#plt.subplot(221),plt.imshow(laplacian)
#plt.subplot(222),plt.imshow(sobel)
#plt.subplot(223),plt.imshow(sobelx)
#plt.subplot(224),plt.imshow(sobelx)

'''ok!'''
plt.figure()
plt.subplot(211),plt.imshow(img_rgb)
plt.subplot(212),plt.imshow(laplacian)



