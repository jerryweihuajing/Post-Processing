# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 22:35:33 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Discrete points to mesh points
"""

import numpy as np
import matplotlib.pyplot as plt

import sys,os
sys.path.append(os.getcwd())

import o_grid
import o_mesh
import o_discrete_point

#==============================================================================
#显示二维散点
def ScatterPlot(ax,which_discrete_points):
    
#    #判断类型  
#    if isinstance(which_discrete_points[0],sphere):
#        
#        for this_point in which_discrete_points:
#            
#            plt.scatter(this_point.pos_x,this_point.pos_y,color='c')
        
    if isinstance(which_discrete_points[0],o_discrete_point.discrete_point):
        
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
            this_point=o_discrete_point.discrete_point()
            
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

#==============================================================================  
#构造网格点矩阵
def MeshGrid(which_discrete_points,step,show=False):
    
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

#==============================================================================  
#disrete points grid is better
def DiscretePointsGrids(which_discrete_points,length,show=False):

    #首先找出网格的坐标范围
    x_discrete_points=[this_discrete_point.pos_x for this_discrete_point in which_discrete_points]
    y_discrete_points=[this_discrete_point.pos_y for this_discrete_point in which_discrete_points]
    
    #xy边界
    boundary_x=[min(x_discrete_points),max(x_discrete_points)]
    boundary_y=[min(y_discrete_points),max(y_discrete_points)]
    
    #xy边长
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
        
    #xy方向上的网格数
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))
    
    #xy方向上的网格交点数
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    #显示吗哥
    if show:
        
        #x向
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*length,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*length,
                       color='k',
                       linestyles="--")
            
        #y向
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*length,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*length,
                       color='k',
                       linestyles="--")
             
    #Initialize grids list
    grids=[]
    
    for k_x in range(amount_grid_x):
        
        for k_y in range(amount_grid_y):
            
            #new grid
            this_grid=o_grid.grid() 
            
            #assignment
            this_grid.length=length
            this_grid.index_x=k_x
            this_grid.index_y=k_y
            this_grid.index=[this_grid.index_x,this_grid.index_y]
            this_grid.position_x=boundary_x[0]+this_grid.index_x*this_grid.length
            this_grid.position_y=boundary_y[0]+this_grid.index_y*this_grid.length
            this_grid.position=np.array([this_grid.position_x,this_grid.position_y])
            this_grid.spheres_inside=[]
            
            #involved
            grids.append(this_grid)
            
    #输出图像
    img_tag_mesh=np.full((amount_grid_x,amount_grid_y),np.nan) 
    
    #要输出的mesh对象
    that_mesh=o_mesh.mesh()
    
    #赋值
    that_mesh.grids=grids
    that_mesh.img_tag=img_tag_mesh
      
    return that_mesh