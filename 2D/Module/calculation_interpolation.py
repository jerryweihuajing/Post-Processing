# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:17:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Spatial Interpolation
"""

'''
Interpolation algorithm:
1 Adjacent Points Interpolation
2 Linear Interpolation
3 Bilinear Interpolation
4 Kriging Interpolation
'''

'''
demand:
1 scatters in grid
2 grids in scatter
'''

import time
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

import calculation_image as C_I
import calculation_scatters_mesh as C_S_M

#------------------------------------------------------------------------------   
"""
Calculate the distance between two points

Args:
   pos_A: coordinate of point A
   pos_B: coordinate of point B
   
Returns:
    the distance between two points
""" 
def Distance(pos_A,pos_B):
    
    #determine that the data types of pos_A,pos_B, they are converted to np.array anyway
    if type(pos_A) is not np.array:
       
        pos_A=np.array(pos_A)
    
    if type(pos_B) is not np.array:
       
        pos_B=np.array(pos_B)
  
    return np.sqrt(np.sum((pos_A-pos_B)**2))   
 
#------------------------------------------------------------------------------   
"""
Genertate the neighbor points index

Args:
   which_index: index (i, j)
   pad: half length of neighbor area
   
Returns:
    the neighbor points index
""" 
def Neighbor(which_index,pad):
    
    #index plus tuple offset is neighbor index
    return [(which_index[0]+i,which_index[1]+j)
            for i in np.linspace(-pad,pad,2*pad+1) 
            for j in np.linspace(-pad,pad,2*pad+1)]

#------------------------------------------------------------------------------   
"""
Delete nan in index list in an img

Args:
   which_img: image to be operated
   index_list: list of index
   
Returns:
    index list without nan
""" 
def NanExpire(which_img,index_list):
    
    exist_index_list=[]
    
    for k in range(len(index_list)):
        
        i,j=index_list[k]
        
        #index in img
        if 0<=i<np.shape(which_img)[0] and 0<=j<np.shape(which_img)[1]:
            
            if not np.isnan(which_img[int(i),int(j)]):
            
                exist_index_list.append(k)
  
    return [index_list[this_index] for this_index in exist_index_list]
   
#------------------------------------------------------------------------------   
"""
Calculate weight of inverse distance weighting

Args:
   which_pos: point to be operated
   which_other_points: points to calculate
   
Returns:
    weight of inverse distance weighting
"""          
def InverseDistanceWeight(which_pos,which_other_points):
    
    #construct the coordinates of which other points
    if isinstance(which_other_points[0],list) or isinstance(which_other_points[0],tuple):
        
        which_other_pos=cp.deepcopy(which_other_points)
        
    else:

        which_other_pos=[[this_point.pos_x,this_point.pos_y] for this_point in which_other_points]
    
    #inverse distance weighted denominator
    denominator=np.sum([1/Distance(which_pos,this_pos) for this_pos in which_other_pos])
    
    #weight list
    weight=[]
    
    #the weight of all the points in the set of points to which pos
    for this_pos in which_other_pos:
        
        weight.append(1/Distance(which_pos,this_pos)/denominator)
    
    return np.array(weight)
   
'''all the scatters will take part in the interpolation'''
#------------------------------------------------------------------------------   
"""
Calculation of global inverse distance weighting

Args:
   which_scatters: scatter objects to be operated
   grid_length: length of grid
   which_surface_map: to save computation time by not directly participating in interpolation calculation
   show: whether to show (default: False)
   
Returns:
    mesh_points from inverse distance weighting interpolation
"""  
def GlobalIDWInterpolation(which_scatters,
                           grid_length,
                           which_surface_map=None,
                           show=False):
    
    print('')
    print('-- Global IDW Interpolation')
    
    #construct mesh points
    mesh_points=C_S_M.MeshGrid(which_scatters,grid_length,show=False)
    
    #which_surface default to be None
    if which_surface_map==None:
        
        which_surface={}
        
        for k in range(np.shape(mesh_points)[0]):
            
            which_surface[k]=0
    
#    print(len(which_surface))
#    print(np.shape(mesh_points))
       
    #judge whether which_surface matches mesh_points or not
    if len(which_surface_map)!=np.shape(mesh_points)[0]:
        
        print('ERROR:Incorrect dimension')
        
        return
    
    #网格点上的z值
    z_mesh_points=np.zeros(np.shape(mesh_points)[0:2])
    
    '''set the threshold here'''
    #inverse distance weighting is applied to grid points
    for i in range(np.shape(mesh_points)[0]):
        
        for j in range(np.shape(mesh_points)[1]):
            
            if j>=np.shape(mesh_points)[1]-which_surface_map[i]:
                
                z_mesh_points[i,j]=np.nan
                
                continue
            
#            print(mesh_points[i,j])
            
            this_pos=mesh_points[i,j]+np.array([grid_length,grid_length])/2
            
#            print(this_pos)

            #calculate the weights for each point
            weight=InverseDistanceWeight(this_pos,which_scatters)
            
            #vector of z value
            z_discrete_points=np.array([this_discrete_point.pos_z for this_discrete_point in which_scatters])
            
            #assgin the value one by one
            z_mesh_points[i,j]=np.dot(z_discrete_points,weight)

    #显示吗哥
    if show:
        
        plt.imshow(z_mesh_points)  

    return C_I.ImgFlip(C_I.ImgRotate(z_mesh_points),0)

'''surface is necessary to avoid void mesh point''' 
#------------------------------------------------------------------------------   
"""
Calculation of global inverse distance weighting

Args:
   which_scatters: scatter objects to be operated
   grid_length: length of grid
   which_surface_map: to save computation time by not directly participating in interpolation calculation
   show: whether to show (default: False)
   method: method of putting scatters into grids (default: 'advanced')
   
Returns:
    mesh_points from inverse distance weighting interpolation
"""
def ScattersInGridIDW(which_scatters,grid_length,which_surface_map=None,show=False,method='advanced'):
            
    print('')
    print('-- Scatters In Grid IDW')
    
    #generate grid object
    that_mesh=C_S_M.ScattersMesh(which_scatters,grid_length)

    #re-define
    img_tag=that_mesh.img_tag
    grids=that_mesh.grids
    
    #offset in minus value
    offset_x=that_mesh.boundary_x[0]
    offset_y=that_mesh.boundary_y[0]
    
    start_time=time.time()
    
    '''raw method'''
    if method=='raw':
        
        raw_sum=0
        
        #put scatters into the grid
        for this_grid in grids:
            
            this_grid.scatters_inside=[]
                
            for this_scatter in which_scatters:
                
                #judge whether the discrete point is inside
                if this_grid.ScatterInside(this_scatter):
    
                    this_grid.scatters_inside.append(this_scatter)  
             
            raw_sum+=len(this_grid.scatters_inside)*grids.index(this_grid)
        
        print('-> raw sum:',raw_sum)   
        
    '''advanced method (in essay)'''
    if method=='advanced':
        
        advanced_sum=0
        
        #init grids
        for this_grid in grids:
            
            this_grid.scatters_inside=[]
            
        for this_scatter in which_scatters:
            
            index_x=int(np.floor((this_scatter.pos_x-offset_x)/grid_length))
            index_y=int(np.floor((this_scatter.pos_y-offset_y)/grid_length))
            
            grids[np.shape(img_tag)[1]*index_x+index_y].scatters_inside.append(this_scatter)  
                 
        for this_grid in grids:
            
            advanced_sum+=len(this_grid.scatters_inside)*grids.index(this_grid)
           
        print('-> advanced sum:',advanced_sum)
    
    print('-> time consumed:',time.time()-start_time)
    
    #IDW
    for this_grid in grids:
    
        '''surface is no need: skip the grid which has no discrete point inside'''
        if this_grid.scatters_inside!=[]:
                
            this_pos=this_grid.position+np.array([this_grid.length,this_grid.length])/2
            
            #calculate the weight each point
            this_weight=InverseDistanceWeight(this_pos,this_grid.scatters_inside)
        
            #vector of z value
            z_scatters=np.array([this_scatter.pos_z for this_scatter in this_grid.scatters_inside])

            #assign the value one by one
            img_tag[this_grid.index_x,this_grid.index_y]=np.dot(z_scatters,this_weight)
   
    #comfortable
    z_mesh_points=C_I.ImgFlip(C_I.ImgRotate(img_tag),0)
    
    #preview
    if show:
        
        plt.imshow(z_mesh_points)
    
    #default: which_surface does not exist
    if which_surface_map==None:
        
        which_surface_map={}
        
        for k in range(np.shape(z_mesh_points)[0]):
            
            which_surface_map[k]=0
         
    #judge whether which_surface matches mesh_points or not
    if len(which_surface_map)!=np.shape(z_mesh_points)[1]:
        
        print('ERROR: Incorrect dimension')
        
        return
    
    #check where the nan is
    for j in range(np.shape(z_mesh_points)[1]):
        
        for i in range(which_surface_map[j],np.shape(z_mesh_points)[0]):
                 
            #fill the nan by interpolation
            if np.isnan(z_mesh_points[i,j]):
                
                this_index=[i,j]
                
                #Initial a pad
                pad=1
                  
                #index of this neighbor
                this_neighbor=Neighbor(this_index,pad)
                   
                #expire the nan
                this_neighbor_expire_nan=NanExpire(z_mesh_points,this_neighbor)

#                print(this_neighbor_expire_nan)
                
                #into the loop
                while not len(this_neighbor_expire_nan):
                    
                    pad+=1
  
                    #index of this neighbor
                    this_neighbor=Neighbor(this_index,pad)
                       
                    #expire the nan
                    this_neighbor_expire_nan=NanExpire(z_mesh_points,this_neighbor)
                    
#                    print(this_neighbor_expire_nan)
                
                '''interpolate directly with the values on the neighbor grid'''
                #calculate the weight each point
                this_weight=InverseDistanceWeight(this_index,this_neighbor_expire_nan)
                 
                #vector of z value
                z_this_neighbor=np.array([z_mesh_points[int(this_neighbor_index[0]),
                                                        int(this_neighbor_index[1])]
                                                        for this_neighbor_index in this_neighbor_expire_nan])
                
                #assgin the value one by one
                z_mesh_points[i,j]=np.dot(z_this_neighbor,this_weight)
                
    return z_mesh_points

def GridsInScatterIDW():
    
    pass