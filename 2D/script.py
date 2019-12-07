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

case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=2.72'

#A experiment
#experiment_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2'

#a_case=CO.CaseConstruction(case_path)

structural_deformation_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=5.43\structural deformation\values\27.87%.txt'

a_progress=PO.ProgressConstruction(structural_deformation_path) 

output_folder=r'C:\Users\whj\Desktop\fig'

#CO.CasePostProcessing(case_path,output_folder)

import Image as Img

img_rgb=Img.ImgFlip(a_progress.structural_deformation,0)
img_tag=Img.ImgFlip(a_progress.img_tag,0)

import numpy as np
import matplotlib.pyplot as plt

#import cv2
#laplacian=cv2.Laplacian(img_tag,cv2.CV_64F)
#
#gradient_x=np.gradient(img_tag)[0]
#gradient_y=np.gradient(img_tag)[1]

#sobel=cv2.Sobel(img_tag,cv2.CV_64F,1,1,ksize=3)
#sobelx=cv2.Sobel(img_tag,cv2.CV_64F,1,0,ksize=3)
#sobely=cv2.Sobel(img_tag,cv2.CV_64F,0,1,ksize=3)
#
#plt.figure()
#plt.subplot(221),plt.imshow(laplacian)
#plt.subplot(222),plt.imshow(sobel)
#plt.subplot(223),plt.imshow(sobelx)
#plt.subplot(224),plt.imshow(sobelx)
#
#'''ok!'''
#plt.figure()
#plt.subplot(211),plt.imshow(img_rgb)
#plt.subplot(212),plt.imshow(laplacian)
#
#
#plt.figure()
#plt.subplot(211),plt.imshow(gradient_x)
#plt.subplot(212),plt.imshow(gradient_y)
#
#np.where(laplacian!=0)

def SimpleGradient(which_matrix,axis=0):
    
    simple_gradient=np.zeros(np.shape(which_matrix))
    
    if axis==0:
        
        simple_gradient[1:,:]=which_matrix[1:,:]-which_matrix[:-1,:]
        
    if axis==1:
        
        simple_gradient[:,1:]=which_matrix[:,1:]-which_matrix[:,:-1]
        
    return simple_gradient

#RGB channel

#surface outline show some similarity

#find element whose tag


'''content to add algorithm'''

'''
1 erosion and expand-cv2: no good
2 tracing based on gradient
'''

def AllStrataSurface(which_progress,show=False):
    
    #Calculate gradient
    manual_gradient_x=SimpleGradient(img_tag,0)
    manual_gradient_y=SimpleGradient(img_tag,1)
    manual_gradient=manual_gradient_x+manual_gradient_y
    
    #surface of all strata
    strata_surface=np.full(np.shape(manual_gradient),np.nan)
    strata_surface[np.where(manual_gradient!=0)]=1
    
    if show:
        
        plt.imshow(strata_surface,cmap='gray')
        
    return strata_surface
    
def DetachmentSurfaceBasedOnTag(which_progress,which_tag,show=False):
    
    #Calculate gradient
    manual_gradient_x=SimpleGradient(img_tag,0)
    manual_gradient_y=SimpleGradient(img_tag,1)
    manual_gradient=manual_gradient_x+manual_gradient_y
    
    #surface of all strata
    strata_surface=np.full(np.shape(manual_gradient),np.nan)
    strata_surface[np.where(manual_gradient!=0)]=1
    
    #detachment surface which is intersection of surface and detachment 
    detachment_surface=np.full(np.shape(manual_gradient),np.nan)
    
    for i in range(np.shape(detachment_surface)[0]):
        
        for j in range(np.shape(detachment_surface)[1]):
            
            if strata_surface[i,j]==1 and img_tag[i,j]==which_tag:
                
                detachment_surface[i,j]=1

    if show:
        
        plt.imshow(detachment_surface,cmap='gray')  
        
    return detachment_surface

'''cv2 erosion: no good'''
def CV2ErosionBasedOnTag(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),np.nan)
    this_strata[np.where(img_tag==which_tag)]=1
        
    #construct kernel parameter to make erosion operation
    erosion_kernel=np.ones((5, 5),np.uint8)
    erosion=cv2.erode(this_strata,erosion_kernel,iterations=1)
    
    #nan 2 float
    this_strata=np.nan_to_num(this_strata)
    erosion=np.nan_to_num(erosion)
    
    #subduction operation
    this_strata_surface=this_strata-erosion
    
    #fill 0 with np.nan
    this_strata_surface[np.where(this_strata_surface==0)]=np.nan
    
    if show:
            
        plt.figure()
        
        plt.subplot(311),plt.imshow(this_strata,cmap='gray')
        plt.subplot(312),plt.imshow(erosion,cmap='gray')
        plt.subplot(313),plt.imshow(this_strata_surface,cmap='gray')
    
'''cv2 dilation: no good'''
def CV2DilationBasedOnTag(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),np.nan)
    this_strata[np.where(img_tag==which_tag)]=1

    #construct kernel parameter to make erosion operation
    dilation_kernel=np.ones((5, 5),np.uint8)
    dilation=cv2.erode(this_strata,dilation_kernel,iterations=1)

    #nan 2 float
    this_strata=np.nan_to_num(this_strata)
    dilation=np.nan_to_num(dilation)
    
    #subduction operation
    this_strata_surface=dilation-this_strata
    
    #fill 0 with np.nan
    this_strata_surface[np.where(this_strata_surface==0)]=np.nan
    
    if show:
        
        plt.figure()
        
        plt.subplot(311),plt.imshow(this_strata,cmap='gray')
        plt.subplot(312),plt.imshow(dilation,cmap='gray')
        plt.subplot(313),plt.imshow(this_strata_surface,cmap='gray')

'''cv2 finding contours: no good'''
def CV2FindContours(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),0,np.uint8)
    this_strata[np.where(img_tag==which_tag)]=255    
     
    #find contour
    image, contours, hierarchy = cv2.findContours(this_strata, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    print("contours size: ", len(contours))
    
    #draw contours
    cv2.drawContours(this_strata, contours, -1, (0, 0, 255), 3)
    
    if show:
        
        cv2.imshow("img", this_strata)
        cv2.waitKey(0)

which_tag=1 
  
plt.figure()
plt.imshow(img_rgb)
#AllStrataSurface(a_progress,1)
DetachmentSurfaceBasedOnTag(a_progress,9,1)

import cv2 

'''Edge tracing based on gradients'''

