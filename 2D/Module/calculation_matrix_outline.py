# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 23:32:12 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation about matrix outline
"""

import numpy as np

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
    
            #calculate relative position and collect new coordinates
            if content_surface[k][0]>content_surface[k+1][0]:
                
                offset=content_surface[k][0]-content_surface[k+1][0]
                
                for this_offset in range(1,offset):
                    
                    content_to_add.append([content_surface[k+1][0]+int(this_offset),content_surface[k+1][1]])
            
            if content_surface[k][0]<content_surface[k+1][0]:
                
                offset=content_surface[k+1][0]-content_surface[k][0]
               
                for this_offset in range(1,offset):
                    
                    content_to_add.append([content_surface[k][0]+int(this_offset),content_surface[k][1]])

    img_outline=np.full(np.shape(outline),np.nan)
    
    #plot surface
    for this_i,this_j in content_surface+content_to_add:
        
        img_outline[this_i,this_j]=1
        
#    plt.imshow(img_surface,cmap='gray')
    
    return img_outline

#------------------------------------------------------------------------------
"""
Generate outline matrix from matrix

Args:
    which_matrix: matrix to be operated
    
Returns:
    outline matrix
"""
def OutlineFromMatrix(which_matrix):
    
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
    
    return OutlineImprovement(outline_matrix)