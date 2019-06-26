# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:17:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

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
1 sphere in grid
2 grid in sphere
'''

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

import sys,os
sys.path.append(os.getcwd())

from Module import Image as Img
from Module import MeshPoints as Mesh

#==============================================================================     
#计算两点之间的距离
def Distance(pos_A,pos_B):
    
    #判断pos_A,pos_B的数据类型，无论如何都转化为np.array
    if type(pos_A) is not np.array:
       
        pos_A=np.array(pos_A)
    
    if type(pos_B) is not np.array:
       
        pos_B=np.array(pos_B)
  
    return np.sqrt(np.sum((pos_A-pos_B)**2))    

#============================================================================== 
#genertate the neighbor points
#pad: size:(size*2+1)X(size*2+1)
def Neighbor(which_index,pad):
    
    #index plus tuple offset is neighbor index
    return [(which_index[0]+i,which_index[1]+j)
            for i in np.linspace(-pad,pad,2*pad+1) 
            for j in np.linspace(-pad,pad,2*pad+1)]

#============================================================================== 
#delete nan in index list in an img
def NanExpire(which_img,index_list):
    
    exist_index_list=[]
    
    for k in range(len(index_list)):
        
        i,j=index_list[k]
        
        #index in img
        if 0<=i<np.shape(which_img)[0] and 0<=j<np.shape(which_img)[1]:
            
            if not np.isnan(which_img[int(i),int(j)]):
            
                exist_index_list.append(k)
                
#    print(exist_index_list)
    
    return [index_list[this_index] for this_index in exist_index_list]
            
#@pysnooper.snoop()
#==============================================================================     
#反距离加权：权重
def InverseDistanceWeight(which_pos,which_other_points):
    
    #构造which_other_points的坐标
    if isinstance(which_other_points[0],list) or isinstance(which_other_points[0],tuple):
        
        which_other_pos=cp.deepcopy(which_other_points)
        
    else:

        which_other_pos=[[this_point.pos_x,this_point.pos_y] for this_point in which_other_points]
    
    #反距离加权的分母
    denominator=np.sum([1/Distance(which_pos,this_pos) for this_pos in which_other_pos])
    
    #权重列表
    weight=[]
    
    #点集中所有点到which_pos的加权
    for this_pos in which_other_pos:
        
        weight.append(1/Distance(which_pos,this_pos)/denominator)
    
    return np.array(weight)
   
'''surface目的：直接不参与插值计算，节省计算时间'''
#==============================================================================   
#反距离加权插值：
#将离散点discrete_points插至mesh_points网格点上
#which_surface_map用于限制点的范围，减少计算量
#all the discrete points will take part in the interpolation
def GlobalIDWInterpolation(which_discrete_points,grid_length,which_surface_map=None,show=False):
    
    #construct mesh points
    mesh_points=Mesh.MeshGrid(which_discrete_points,grid_length,show=False)
    
    #默认的which_surface是不存在的
    if which_surface_map==None:
        
        which_surface={}
        
        for k in range(np.shape(mesh_points)[0]):
            
            which_surface[k]=0
    
#    print(len(which_surface))
#    print(np.shape(mesh_points))
       
    #先判断which_surface和mesh_points是否匹配
    if len(which_surface_map)!=np.shape(mesh_points)[0]:
        
        print('ERROR:Incorrect dimension')
        
        return
    
    #网格点上的z值
    z_mesh_points=np.zeros(np.shape(mesh_points)[0:2])
    
    '''在这里加区间'''
    #对网格点反距离加权 
    for i in range(np.shape(mesh_points)[0]):
        
        for j in range(np.shape(mesh_points)[1]):
            
            if j>=np.shape(mesh_points)[1]-which_surface_map[i]:
                
                z_mesh_points[i,j]=np.nan
                
                continue
            
#            print(mesh_points[i,j])
            
            this_pos=mesh_points[i,j]+np.array([grid_length,grid_length])/2
            
#            print(this_pos)

            #计算各个点的权重
            weight=InverseDistanceWeight(this_pos,which_discrete_points)
            
            #值的向量
            z_discrete_points=np.array([this_discrete_point.pos_z for this_discrete_point in which_discrete_points])
            
            #逐个赋值
            z_mesh_points[i,j]=np.dot(z_discrete_points,weight)

    #显示吗哥
    if show:
        
        plt.imshow(z_mesh_points)  

    return Img.ImgFlip(Img.ImgRotate(z_mesh_points),0)
 
#==============================================================================  
#Interpolation in each grid
#surface is no need: skip the grid which has no discrete point inside
'''surface is necessary to avoid void mesh point'''
def LocalIDWInterpolation(which_discrete_points,grid_length,which_surface_map=None,show=False):
            
    #generate grid object
    that_mesh=Mesh.DiscretePointsGrids(which_discrete_points,grid_length)

    #re-define
    img_tag=that_mesh.img_tag
    grids=that_mesh.grids
    
    #将sphere投入grid
    for this_grid in grids:
        
        this_grid.discrete_points_inside=[]
            
        for this_discrete_point in which_discrete_points:
            
            #judge whether the discrete point is inside
            if this_grid.DiscretePointInside(this_discrete_point):

                this_grid.discrete_points_inside.append(this_discrete_point)  
    
    #IDW
    for this_grid in grids:
    
        if this_grid.discrete_points_inside!=[]:
                
#            print(this_grid.position)
            
            this_pos=this_grid.position+np.array([this_grid.length,this_grid.length])/2
            
#            print(this_pos)
            
            #calculate the weight each point
            this_weight=InverseDistanceWeight(this_pos,this_grid.discrete_points_inside)
        
            #值的向量
            z_discrete_points=np.array([this_discrete_point.pos_z for this_discrete_point in this_grid.discrete_points_inside])

            #逐个赋值
            img_tag[this_grid.index_x,this_grid.index_y]=np.dot(z_discrete_points,this_weight)
   
    #comfortable
    z_mesh_points=Img.ImgFlip(Img.ImgRotate(img_tag),0)
    
    #preview
    if show:
        
        plt.imshow(z_mesh_points)
    
    #default: which_surface does not exist
    if which_surface_map==None:
        
        which_surface_map={}
        
        for k in range(np.shape(z_mesh_points)[0]):
            
            which_surface_map[k]=0
        
#    print(which_surface_map)
#    print(len(which_surface_map))
#    print(np.shape(z_mesh_points))
#       
    #先判断which_surface和mesh_points是否匹配
    if len(which_surface_map)!=np.shape(z_mesh_points)[1]:
        
        print('ERROR:Incorrect dimension')
        
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
                
                '''直接用邻居网格上的值插'''
                #calculate the weight each point
                this_weight=InverseDistanceWeight(this_index,this_neighbor_expire_nan)
                 
                #值的向量
                z_this_neighbor=np.array([z_mesh_points[int(this_neighbor_index[0]),
                                                        int(this_neighbor_index[1])]
                                                        for this_neighbor_index in this_neighbor_expire_nan])
                
                #逐个赋值
                z_mesh_points[i,j]=np.dot(z_this_neighbor,this_weight)
                
          
    return z_mesh_points

       
#ax=plt.subplot(3,1,1)
#discrete_points=GeneratePoints(ax,20,10,20,20,1)
#
#ax=plt.subplot(3,1,2)
#mesh_points=MeshGrid(ax,discrete_points,0.5,0.5,1)
# 
#ax=plt.subplot(3,1,3)
#IDWInterpolation(ax,discrete_points,mesh_points,1)
