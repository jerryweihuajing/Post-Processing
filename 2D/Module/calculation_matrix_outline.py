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
Connect the outline

Args:
    content_outline: outline coordinates list

Returns:
    new outline content
"""
def OutlineImprovement(content_outline):
    
    #improve surface
    content_to_add=[]

    for k in range(len(content_outline)-1):
        
        if content_outline[k] not in NeighborInImage(content_outline[k+1]):
    
            #calculate relative position and collect new coordinates
            if content_outline[k][0]>content_outline[k+1][0]:
                
                offset=content_outline[k][0]-content_outline[k+1][0]
                
                for this_offset in range(1,offset):
                    
                    content_to_add.append([content_outline[k+1][0]+int(this_offset),content_outline[k][1]])
            
            if content_outline[k][0]<content_outline[k+1][0]:
                
                offset=content_outline[k+1][0]-content_outline[k][0]
               
                for this_offset in range(1,offset):
                    
                    content_to_add.append([content_outline[k][0]+int(this_offset),content_outline[k+1][1]])
    
    return content_outline+content_to_add

#------------------------------------------------------------------------------
"""
Improve morphorlogy of outline

Args:
    outline: 0,1 matrix of outline

Returns:
    content to add to outline image
"""
def SurfaceOutlineImprovement(outline):
    
    print('')
    print('-- Surface Outline Improvement')
    
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
    
    img_outline=np.full(np.shape(outline),np.nan)
    
    #plot surface
    for this_i,this_j in OutlineImprovement(content_surface):
        
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
    
    print('')
    print('-- Outline From Matrix')

    #matrix to draw outline image
    outline_matrix=np.full(np.shape(which_matrix),np.nan)
    
    #outline in all directions
    surface_outline_content=[]
    bottom_outline_content=[]
    right_outline_content=[]
    left_outline_content=[]
    
    #surface and bottom
    for j in range(np.shape(which_matrix)[1]):
        
        this_i_list=[]
        
        for i in range(np.shape(which_matrix)[0]):    
            
            if not np.isnan(which_matrix[i,j]):
                
                this_i_list.append(i)
        
        try:
            
            surface_outline_content.append([np.min(this_i_list)-1,j])
            bottom_outline_content.append([np.max(this_i_list)+1,j])
            
        except:
            
            pass
        
    #left and right
    for i in range(np.shape(which_matrix)[0]):
        
        this_j_list=[]
        
        for j in range(np.shape(which_matrix)[1]):    
            
            if not np.isnan(which_matrix[i,j]):
                
                this_j_list.append(j)
                
        try:
            
            right_outline_content.append([i,np.max(this_j_list)+1])
            left_outline_content.append([i,np.min(this_j_list)-1])
        
        except:
            
            pass
        
    #total outline content
    content_outline=OutlineImprovement(surface_outline_content)+\
                    OutlineImprovement(bottom_outline_content)+\
                    OutlineImprovement(right_outline_content)+\
                    OutlineImprovement(left_outline_content)
                    
    for this_i,this_j in content_outline:

        outline_matrix[this_i,this_j]=1

    return outline_matrix

#------------------------------------------------------------------------------
"""
Generate outline matrix from tag img 

Args:
    img_tag: img tag to be operated
    
Returns:
    outline matrix
"""
def OutlineFromImgTag(img_tag):
    
    print('')
    print('-- Outline From Img Tag')
    
    #matrix to draw outline img tag
    outline_img_tag=np.full(np.shape(img_tag),np.nan)
    
    #outline in all directions
    surface_outline_content=[]
    bottom_outline_content=[]
    right_outline_content=[]
    left_outline_content=[]
    
    #surface and bottom
    for j in range(np.shape(img_tag)[1]):
        
        this_i_list=[]
        
        for i in range(np.shape(img_tag)[0]):    
            
            if img_tag[i,j]!=-1:
                
                this_i_list.append(i)
        
        try:
            
            surface_outline_content.append([np.min(this_i_list)-1,j])
            bottom_outline_content.append([np.max(this_i_list)+1,j])
            
        except:
            
            pass
        
    #left and right
    for i in range(np.shape(img_tag)[0]):
        
        this_j_list=[]
        
        for j in range(np.shape(img_tag)[1]):    
            
            if img_tag[i,j]!=-1:
                
                this_j_list.append(j)
                
        try:
            
            right_outline_content.append([i,np.max(this_j_list)+1])
            left_outline_content.append([i,np.min(this_j_list)-1])
        
        except:
            
            pass
        
    #total outline content
    content_outline=OutlineImprovement(surface_outline_content)+\
                    OutlineImprovement(bottom_outline_content)+\
                    OutlineImprovement(right_outline_content)+\
                    OutlineImprovement(left_outline_content)
                    
    for this_i,this_j in content_outline:

        outline_img_tag[this_i,this_j]=1

    return outline_img_tag

#------------------------------------------------------------------------------
"""
Add bound to matrix

Args:
    which_matrix: matrix to be operated
    cell_padding: bound size (default: 1)
    bound_value: balue of bound (default: np.nan)
    
Returns:
    matrix with bound
"""
def AddBound(which_matrix,cell_padding=1,bound_value=np.nan):
    
    print('')
    print('-- Add Bound')
    
    shape_new_mat=(np.shape(which_matrix)[0]+2*cell_padding,np.shape(which_matrix)[1]+2*cell_padding)
    
    #new matrix
    new_mat=np.full(shape_new_mat,bound_value)
    
    new_mat[cell_padding:-cell_padding,cell_padding:-cell_padding]=which_matrix
    
    return new_mat
