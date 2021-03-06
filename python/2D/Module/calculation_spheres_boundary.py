# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:50:34 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Calculate boundaries from spheres system
"""

"""
1 Rasterization and calculate the pixels which spheres take up
2 Boundary Tracking: a method in Computer Vision
"""

'''
demand:
simple spheres boundary np.where to calculate the content 
'''

import numpy as np
import matplotlib.pyplot as plt

import o_mesh
import o_circle

import calculation_image as C_I

#------------------------------------------------------------------------------
"""
Calculate the pixels up which the spheres take

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    a mesh object presenting content and img
"""
def SpheresContent(which_spheres,length,factor=1,show=False):
    
    print('')
    print('-- Spheres Content')
    print('-> grid length:',length)
    
    #find out the coordinate range of the grid
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #the radius of the maximum and minimum
    radius_of_min=which_spheres[x_spheres.index(min(x_spheres))].radius
    radius_of_max=which_spheres[y_spheres.index(max(y_spheres))].radius
    
    #x,y boundary
    boundary_x=[min(x_spheres)-radius_of_min,max(x_spheres)+radius_of_min]
    boundary_y=[min(y_spheres)-radius_of_max,max(y_spheres)+radius_of_max]
    
    #x,y length
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]

    #The number of grids in the x,y direction
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))

    #total pixels
    spheres_content=[]
                 
    #traverse spheres
    for this_sphere in which_spheres:
        
        #expire sphere from uplift
        if this_sphere.tag==9:
            
            continue
        
        #new 2D circle
        new_circle=o_circle.circle()
        
        new_circle.radius=this_sphere.radius*factor
        new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])*factor
        
        new_circle.Init()
        
        for this_pos in new_circle.points_inside:
            
            this_x=int(np.floor((this_pos[0]-boundary_x[0])/length))
            this_y=int(np.floor((this_pos[1]-boundary_y[0])/length))

            if 0<=this_x<amount_grid_x and 0<=this_y<amount_grid_y:
                    
                if [this_x,this_y] not in spheres_content:
                    
                    spheres_content.append([this_x,this_y])  

    #check the shape
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
   
    for this_i,this_j in spheres_content:
               
        #restrict the boundary  
        if 0<=this_i<amount_grid_x and 0<=this_j<amount_grid_y:

            img_tag_mesh[this_i,this_j]=1

    #define new mesh
    that_mesh=o_mesh.mesh()
    
    #Rotatation is in need
    that_mesh.img_tag=C_I.ImgFlip(C_I.ImgRotate(img_tag_mesh),0)
    that_mesh.content=spheres_content   

    if show:
        
        plt.imshow(img_tag_mesh,cmap='gray')
    
    return that_mesh

#------------------------------------------------------------------------------
"""
Calculate the max and min valid index of every col in an image

Args:
    which_spheres: spheres to calculate
    length: pixel step
    
Returns:
    map of min and max index in every col
"""
def SpheresTopAndBottomMap(which_spheres,length):
    
    print('')
    print('-- Spheres Top and Bottom Map')
    print('-> grid length:',length)
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
    
    #surfave map
    map_j_i_top_bottom={}
    
    #map from maximum and minimum
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        this_i_list=np.where(that_mesh.img_tag[:,j]!=0)
        
        try:
            
            map_j_i_top_bottom[j]=[np.min(this_i_list),np.max(this_i_list)]
        
        except:
            
            map_j_i_top_bottom[j]=None
            
    return map_j_i_top_bottom

'''
Calculate the elavation
the surface could be calculated, do do the 'left' 'right' 'top' 'bottom'
'''
#------------------------------------------------------------------------------
"""
Calculate the min valid index of every col in an image

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    
Returns:
    an dictionary presenting the elavation
"""
def SpheresTopMap(which_spheres,length,factor=1):

    print('')
    print('-- Spheres Top Map')
    print('-> grid length:',length)
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #surfave dictionary
    map_j_i_top={}
    
    #img tag
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        map_j_i_top[j]=0
        
        for i in range(np.shape(that_mesh.img_tag)[0]):

            if that_mesh.img_tag[i,j]!=0:
                             
                map_j_i_top[j]=i
                
                break
            
    return map_j_i_top 
 
#------------------------------------------------------------------------------
"""
Calculate img to present the surface

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an img tag presenting the elavation
"""
def SpheresTopImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the surface map
    map_j_i_top=SpheresTopMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
    
    #surface map to img tag
    for k in range(len(map_j_i_top)):
        
        this_j=list(map_j_i_top.keys())[k]
        this_i=list(map_j_i_top.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag,cmap='gray')
      
    return that_img_tag
 
#------------------------------------------------------------------------------
"""
Calculate the max valid index of every col in an image

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    
Returns:
    an dictionary presenting the bottom
"""
def SpheresBottomMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_j_i_bottom={}
    
    #img tag
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        map_j_i_bottom[j]=np.shape(that_mesh.img_tag)[0]
        
        for i in range(np.shape(that_mesh.img_tag)[0]-1,-1,-1):

            if that_mesh.img_tag[i,j]!=0:
                              
                map_j_i_bottom[j]=i
                
                break
            
    return map_j_i_bottom 

#------------------------------------------------------------------------------
"""
Calculate img to present the bottom

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an img tag presenting the bottom
"""
def SpheresBottomImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_j_i_bottom=SpheresBottomMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
    
    #bottom map to img tag
    for k in range(len(map_j_i_bottom)):
        
        this_j=list(map_j_i_bottom.keys())[k]
        this_i=list(map_j_i_bottom.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag,cmap='gray')
      
    return that_img_tag

#------------------------------------------------------------------------------
"""
Calculate the max left valid index of every col in an image

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    
Returns:
    an dictionary presenting the left boundary
"""
def SpheresLeftMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_i_j_left={}
    
    #img tag
    for i in range(np.shape(that_mesh.img_tag)[0]):
        
        map_i_j_left[i]=0
        
        for j in range(np.shape(that_mesh.img_tag)[1]):

            if that_mesh.img_tag[i,j]!=0:
                
                map_i_j_left[i]=j
                
                break
            
    return map_i_j_left 

#------------------------------------------------------------------------------
"""
Calculate img to present the left boundary

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an img tag presenting the left boundary
"""
def SpheresLeftImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_i_j_left=SpheresLeftMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan)    
    
    #bottom map to img tag
    for k in range(len(map_i_j_left)):
        
        this_i=list(map_i_j_left.keys())[k]
        this_j=list(map_i_j_left.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag,cmap='gray')
      
    return that_img_tag

#------------------------------------------------------------------------------
"""
Calculate the max right valid index of every col in an image

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    
Returns:
    an dictionary presenting the right boundary
"""
def SpheresRightMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length)
 
    #地表的列表
    map_i_j_right={}
    
    #img tag
    for i in range(np.shape(that_mesh.img_tag)[0]):
        
        map_i_j_right[i]=np.shape(that_mesh.img_tag)[1]
        
        for j in range(np.shape(that_mesh.img_tag)[1]-1,-1,-1):

            if that_mesh.img_tag[i,j]!=0:
                
                map_i_j_right[i]=j
                
                break
            
    return map_i_j_right   
 
#------------------------------------------------------------------------------
"""
Calculate img to present the right boundary

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an img tag presenting the right boundary
"""
def SpheresRightImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #fetch the bottom map
    map_i_j_right=SpheresRightMap(which_spheres,length)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan)    
    
    #bottom map to img tag
    for k in range(len(map_i_j_right)):
        
        this_i=list(map_i_j_right.keys())[k]
        this_j=list(map_i_j_right.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag,cmap='gray')
      
    return that_img_tag

#------------------------------------------------------------------------------
"""
Calculate map to present the boundary

Args:
    which_spheres: spheres to calculate
    length: pixel step
    side: ['top','left','right','bottom]
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an dictionary presenting the boundary
"""
def SpheresBoundaryMap(which_spheres,length,side,factor=1,show=False):
    
    if side=='top':
    
        return SpheresTopMap(which_spheres,length,factor)
        
    if side=='left':
        
        return SpheresLeftMap(which_spheres,length,factor)
    
    if side=='right':
        
        return SpheresRightMap(which_spheres,length,factor)
        
    if side=='bottom':
        
        return SpheresBottomMap(which_spheres,length,factor)
    
#------------------------------------------------------------------------------
"""
Calculate img to present the boundary

Args:
    which_spheres: spheres to calculate
    length: pixel step
    side: ['top','left','right','bottom]
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an img tag presenting the boundary
"""
def SpheresBoundaryImg(which_spheres,length,side,factor=1,show=False):
    
    if side=='top':
    
        return SpheresTopImg(which_spheres,length,factor)
        
    if side=='left':
        
        return SpheresLeftImg(which_spheres,length,factor)
    
    if side=='right':
        
        return SpheresRightImg(which_spheres,length,factor)
        
    if side=='bottom':
        
        return SpheresBottomImg(which_spheres,length,factor)   
    
#------------------------------------------------------------------------------
"""
Calculate coordinate list to present the boundary

Args:
    which_spheres: spheres to calculate
    length: pixel step
    factor: zoom factor (defualt: 1)
    show: (bool) whether to display (default: False)
    
Returns:
    an coordinates list presenting the boundary
"""
def SimpleSpheresBoundary(which_spheres,length,factor=1,show=False):
   
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #img to present the elavation
    that_img_tag=np.full(np.shape(that_mesh.img_tag),np.nan) 
    
    map_j_i_top={}

    for j in range(np.shape(that_mesh.img_tag)[1]):
        
#        map_j_i_top[j]=0
        
        for i in range(np.shape(that_mesh.img_tag)[0]):

            if that_mesh.img_tag[i,j]!=0:
                          
                map_j_i_top[j]=i
                
                break
    
    for k in range(len(map_j_i_top)):
        
        this_j=list(map_j_i_top.keys())[k]
        this_i=list(map_j_i_top.values())[k]
            
        '''top'''
        that_img_tag[this_i,this_j]=1    
    
    '''bottom'''
    that_img_tag[np.shape(that_mesh.img_tag)[0]-1,:]=1   
        
    '''right'''
    that_img_tag[map_j_i_top[0]:,0]=1
        
    '''left'''
    that_img_tag[map_j_i_top[len(map_j_i_top)-1]:,len(map_j_i_top)-1]=1

    #result
    boundary=[]

    #tag==1 content
    I=np.where(that_img_tag==1)[0]
    J=np.where(that_img_tag==1)[1]
        
    for k in range(len(I)):
        
        if [I[k],J[k]] not in boundary:
            
            boundary.append([I[k],J[k]])
    
    if show:
              
        #draw boundary
        plt.imshow(C_I.ImgFlip(that_img_tag,0),cmap='gray')
            
    return boundary
 