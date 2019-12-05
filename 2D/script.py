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

manual_gradient_x=SimpleGradient(img_tag,0)
manual_gradient_y=SimpleGradient(img_tag,1)

#plt.figure()
#plt.subplot(211),plt.imshow(manual_gradient_x)
#plt.subplot(212),plt.imshow(manual_gradient_y)

manual_gradient=manual_gradient_x+manual_gradient_y

strata_surface=np.full(np.shape(manual_gradient),np.nan)

strata_surface[np.where(manual_gradient!=0)]=1

#detachment surface which is intersection of surface and detachment 
detachment_surface=np.full(np.shape(manual_gradient),np.nan)

for i in range(np.shape(detachment_surface)[0]):
    
    for j in range(np.shape(detachment_surface)[1]):
        
        if strata_surface[i,j]==1 and img_tag[i,j]==1:
            
            detachment_surface[i,j]=1

#RGB channel

#surface outline show some similarity

#find element whose tag


'''content to add algorithm'''
'''horizontal and vertical'''

plt.figure()
plt.imshow(img_rgb)
plt.imshow(detachment_surface,cmap='gray')
    
#------------------------------------------------------------------------------
"""
Calculate 8-neighborhood based on index in an image

Args:
    index: image pixel index

Returns:
    8-neighborhood coordinates list
"""
def NeighborInImage(index):
    
    i,j=index
    
    return [[i+x,j+y] for x in[-1,0,1] for y in [-1,0,1]]

#------------------------------------------------------------------------------
"""
Improve morphorlogy of surface

Args:
    outline: 0,1 matrix of surface

Returns:
    new surface matrix
"""
def SurfaceHorizontalImprovement(which_surface):
    
    #store surface information
    map_surface={}
    
    for j in range(np.shape(which_surface)[1]):
        
        for i in range(np.shape(which_surface)[0]):
            
            if which_surface[i,j]==1:
                
                map_surface[j]=i
                
                break
    
    #to plot the surface
    new_surface=np.zeros(np.shape(which_surface))
    
    #coordinates of surface
    content_surface=[]
    
    for this_j in list(map_surface.keys()):
        
        new_surface[map_surface[this_j],this_j]=1
        content_surface.append([map_surface[this_j],this_j])
        
    #plt.imshow(img_surface,cmap='gray')
    
    #improve surface
    content_to_add=[]
        
    for k in range(len(content_surface)-1):
        
        if content_surface[k] not in NeighborInImage(content_surface[k+1]):
    
            #relative position
            if content_surface[k][0]>content_surface[k+1][0]:
                
                offset=content_surface[k+1][0]+1-content_surface[k][0]
                
            if content_surface[k][0]<content_surface[k+1][0]:
                
                offset=content_surface[k+1][0]-1-content_surface[k][0]
               
            #collect new coordinates
            for this_offset in list(np.linspace(offset,0,abs(offset)+1)):
                
                if this_offset==0:
                    
                    continue
    
                content_to_add.append([content_surface[k][0]+int(this_offset),content_surface[k][1]])
    
    #plot surface
    for this_i,this_j in content_surface+content_to_add:
        
        new_surface[this_i,this_j]=1
        
    return new_surface