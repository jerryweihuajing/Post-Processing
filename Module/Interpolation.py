# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:17:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Spatial Interpolation
"""

'''
Interpolation Method:
1 Adjacent Points Interpolation
2 Linear Interpolation
3 Bilinear Interpolation
4 Kriging Interpolation
'''

import numpy as np
import matplotlib.pyplot as plt

import sys,os
sys.path.append(os.getcwd())

#==============================================================================     
#事后将其写进类里
#计算两点之间的距离
def Distance(pos_A,pos_B):
    
    #判断pos_A,pos_B的数据类型，无论如何都转化为np.array
    if type(pos_A) is not np.array:
       
        pos_A=np.array(pos_A)
    
    if type(pos_B) is not np.array:
       
        pos_B=np.array(pos_B)
  
    return np.sqrt(np.sum((pos_A-pos_B)**2))    

     
#==============================================================================
#显示二维散点
def ScatterPlot(ax,which_discrete_points):
    
#    #判断类型  
#    if isinstance(which_discrete_points[0],sphere):
#        
#        for this_point in which_discrete_points:
#            
#            plt.scatter(this_point.pos_x,this_point.pos_y,color='c')
        
    if isinstance(which_discrete_points[0],discrete_point):
        
        for this_point in which_discrete_points:
            
            plt.scatter(this_point.pos_x,this_point.pos_y,color='c') 
            
    if isinstance(which_discrete_points[0],list) and len(which_discrete_points[0])==2:
        
        for this_point in which_discrete_points:
            
            plt.scatter(this_point[0],this_point[1],color='c') 
         
#==============================================================================         
#生成离散颗粒对象列表
#width,length为建立插值区域的尺寸
#m_width,n_length表示width和length的等分数量
def GeneratePoints(ax,width,length,m_width,n_length,show=False):
    
    #结果列表
    discrete_points=[]
    
    for m in range(m_width):
        
        for n in range(n_length):
            
            #建立新的点
            this_point=discrete_point()
            
            #院有网格上的点坐标
            original_m=m*width/m_width
            original_n=n*length/n_length
            
            #新的点坐标
            new_m=original_m+np.random.rand()
            new_n=original_n+np.random.rand()
            
            #开始定义各个属性
            this_point.pos_x=new_m
            this_point.pos_y=new_n
            
            #z的大小：视情况而定
            for k in range(5):
                
                if k*(width/5)<=original_m<=(k+1)*(width/5):
                
                    this_point.pos_z=k
          
            #收录进列表里
            discrete_points.append(this_point)
    
    #显示吗哥
    if show:
            
        ScatterPlot(ax,discrete_points)
            
    return discrete_points

#@pysnooper.snoop()
#==============================================================================     
#反距离加权：权重
def InverseDistanceWeight(which_pos,which_other_points):
    
    #构造which_other_points的坐标
    which_other_pos=[[this_point.pos_x,this_point.pos_y] for this_point in which_other_points]
    
    #反距离加权的分母
    denominator=np.sum([1/Distance(which_pos,this_pos) for this_pos in which_other_pos])
    
    #权重列表
    weight=[]
    
    #点集中所有点到which_pos的加权
    for this_pos in which_other_pos:
        
        weight.append(1/Distance(which_pos,this_pos)/denominator)
    
    return np.array(weight)

#==============================================================================  
#构造网格点矩阵
def MeshGrid(ax,which_discrete_points,step,show=False):
    
    #x,y方向上的步长
    step_x=step_y=step
    
    #首先找出网格的坐标范围
    x_discrete_points=[this_point.pos_x for this_point in which_discrete_points]
    y_discrete_points=[this_point.pos_y for this_point in which_discrete_points]
    
    #xy边界
    boundary_x=[min(x_discrete_points),max(x_discrete_points)]
    boundary_y=[min(y_discrete_points),max(y_discrete_points)]
    
    #xy边长
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
         
    #xy方向上的网格数
    amount_grid_x=int(np.ceil(length_x/step_x))
    amount_grid_y=int(np.ceil(length_y/step_y))
    
    #xy方向上的网格交点数
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    #显示吗哥
    if show:
        
        #x向
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*step_x,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*step_y,
                       color='k',
                       linestyles="--")
            
        #y向
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*step_y,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*step_x,
                       color='k',
                       linestyles="--")
     
#    print('length_x:',amount_x)
#    print('length_y:',amount_y)
          
    #生成网格交点的坐标矩阵
    mesh_points=[]
    
    for k_x in range(amount_grid_x):
        
        for k_y in range(amount_grid_y):
            
            mesh_points.append([boundary_x[0]+k_x*step_x,boundary_y[0]+k_y*step_y])
            
#    print(len(mesh_points),amount_x*amount_y)
    
    return np.array(mesh_points).reshape((amount_grid_x,amount_grid_y,2)) 
   
'''surface目的：直接不参与插值计算，节省计算时间'''
#==============================================================================   
#反距离加权插值：
#将离散点discrete_points插至mesh_points网格点上
#which_surface_map用于限制点的范围，减少计算量
def IDWInterpolation(ax,discrete_points,mesh_points,which_surface_map=None,show=False):
    
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
            
            this_pos=mesh_points[i,j]

            #计算各个点的权重
            weight=InverseDistanceWeight(this_pos,discrete_points)
            
            #值的向量
            z_discrete_points=np.array([this_discrete_point.pos_z for this_discrete_point in discrete_points])
            
            #逐个赋值
            z_mesh_points[i,j]=np.dot(z_discrete_points,weight)

    #显示吗哥
    if show:
        
        ax.imshow(z_mesh_points)  

    return z_mesh_points
        


#ax=plt.subplot(3,1,1)
#discrete_points=GeneratePoints(ax,20,10,20,20,1)
#
#ax=plt.subplot(3,1,2)
#mesh_points=MeshGrid(ax,discrete_points,0.5,0.5,1)
# 
#ax=plt.subplot(3,1,3)
#IDWInterpolation(ax,discrete_points,mesh_points,1)
