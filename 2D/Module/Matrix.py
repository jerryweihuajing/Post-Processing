# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:14:43 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation about matrix
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import Image as Img
import Global as Glo
import ImageSmoothing as ISm

'''
demand: 
1 improve morphorlogy of outline
'''

#------------------------------------------------------------------------------
"""
Generate image matrix from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    image matrix oject
"""
def ImportMatrixFromTXT(txt_path):
    
    #read lines
    lines=open(txt_path).readlines()
    
    value_lines=[]
    
    for this_line in lines:
        
        value_lines.append(this_line.strip('\n').split(','))  
        
    #check if length every single line is equal
    for this_value_line in value_lines:
        
        if len(this_value_line)!=len(value_lines[0]):
            
            print('ERROR: Incorrect length!')
            
            break
        
    value_matrix=np.zeros((len(value_lines),len(value_lines[0])))
    
    for i in range(np.shape(value_matrix)[0]):
        
        for j in range(np.shape(value_matrix)[1]):
            
            value_matrix[i,j]=float(value_lines[i][j])
              
    return value_matrix
  
#------------------------------------------------------------------------------
"""
Display image matrix from txt file

Args:
    txt_path: file path which contains values matrix
    smooth: (bool) whether image is smooth
    flip: (bool) whether the image flips
    global_norm: external output to reduce calculation
    
Returns:
    None
"""
def DisplayImageFromTXT(txt_path,smooth=True,flip=False,global_norm=None):
    
    #image matrix
    matrix=ImportMatrixFromTXT(txt_path)
    
    if flip:
        
        matrix=Img.ImgFlip(matrix,0)
        
    if smooth:
        
        matrix=ISm.ImageSmooth(matrix)
        
    #strain
    if 'strain' in txt_path:
        
        colormap='seismic'
        
        if global_norm==None:
            
            global_norm=colors.Normalize(vmin=-1,vmax=1)
   
    #stress
    if 'stress' in txt_path:
        
        colormap='gist_rainbow'
        
        if global_norm==None:
            
            global_norm=Glo.GlobalNormFromCase(txt_path)

    plt.imshow(matrix,cmap=colormap,norm=global_norm)
    
    #structural deformation
    if 'structural_deformation' in txt_path:
        
        plt.imshow(matrix)
 
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
Improve morphorlogy of outline

Args:
    outline: 0,1 matrix of outline

Returns:
    content to add to outline image
"""
def OutlineImprovement(outline):
    
    #store surface information
    map_surface={}
    
    for j in range(np.shape(outline)[1]):
        
        for i in range(np.shape(outline)[0]):
            
            if outline[i,j]==1:
                
                map_surface[j]=i
                
                break
    
    #to plot the surface
    img_surface=np.zeros(np.shape(outline))
    
    #coordinates of surface
    content_surface=[]
    
    for this_j in list(map_surface.keys()):
        
        img_surface[map_surface[this_j],this_j]=1
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
        
        img_surface[this_i,this_j]=1
        
#    plt.imshow(img_surface,cmap='gray')
    
    return content_to_add
       
#------------------------------------------------------------------------------
"""
Calculate outline from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    Outline matrix
"""
def ImportOutlineFromTXT(txt_path):
        
    #image matrix
    which_matrix=ImportMatrixFromTXT(txt_path)
    
    #matrix to draw outline image
    outline_matrix=np.full(np.shape(which_matrix),np.nan)
    
    #top and bottom
    for j in range(np.shape(which_matrix)[1]):
        
        for i in range(np.shape(which_matrix)[0]):    
            
            if not np.isnan(which_matrix[i,j]):
  
                if i:
                    i-=1
                    
                outline_matrix[i,j]=1
                outline_matrix[-1,j]=1
                
                break

    #left and right
    for j in [0,-1]:
        
        for i in range(np.shape(which_matrix)[0]): 
            
            if not np.isnan(which_matrix[i,j]):
                
                outline_matrix[i:,j]=1          
    
    #improve outline
    for this_i,this_j in OutlineImprovement(outline_matrix):
        
        outline_matrix[this_i,this_j]=1 
        
    return outline_matrix

#------------------------------------------------------------------------------
"""
Display outline from txt file

Args:
    txt_path: file path which contains values matrix
    flip: (bool) whether the image flips
    
Returns:
    None
"""
def DisplayOutlineFromTXT(txt_path,flip=False):
    
    #outline matrix
    outline_matrix=ImportOutlineFromTXT(txt_path)
    
    if flip:
        
        outline_matrix=Img.ImgFlip(outline_matrix,0)
        
    plt.imshow(outline_matrix,cmap='gray') 
      
#------------------------------------------------------------------------------
"""
Calculate maximum of a matrix

Args:
    which_matrix: matrix to be calculated
    
Returns:
    Maximum of a matrix
"""
def MatrixMaximum(which_matrix):
    
    #figure in this matrix
    content=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                content.append(which_matrix[i,j])   
            
    return np.max(content)
     
#------------------------------------------------------------------------------
"""
Calculate minimum of a matrix

Args:
    which_matrix: matrix to be calculated
    
Returns:
    Minimum of a matrix
"""
def MatrixMinimum(which_matrix):
    
    #figure in this matrix
    content=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                content.append(which_matrix[i,j])
            
    return np.min(content)

#------------------------------------------------------------------------------
"""
Matrix values list except nan

Args:
    which_matrix: matrix to be calculated
    
Returns:
    value list
"""
def MatrixValues(which_matrix):
    
    #value list
    values=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                values.append(which_matrix[i,j])
                
    return values

#------------------------------------------------------------------------------
"""
Filter the matrix value between low value and high value

Args:
    which_matrix: matrix to be calculated
    lower_value: lower threshold
    upper_value: upper threshold
    show: Display or not
    
Returns:
    New matrix with the position whose value between low value and high value present 1
"""
def MatrixFilter(which_matrix,lower_value,upper_value,show=False):
    
    #if valid
    if MatrixMinimum(which_matrix)>lower_value or MatrixMaximum(which_matrix)<upper_value:
    
        print('ERROR: Incorrect value range!')
        
        return False
        
    #result matrix
    new_matrix=np.full(np.shape(which_matrix),np.nan)
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                if lower_value<=which_matrix[i,j]<=upper_value:
                    
                    new_matrix[i,j]=which_matrix[i,j]
    
    if show:
        
        plt.imshow(Img.ImgFlip(new_matrix,0),cmap='gray')
            
    return new_matrix