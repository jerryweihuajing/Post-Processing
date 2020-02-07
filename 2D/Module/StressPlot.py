# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:07:33 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Plot the Stress
"""

import numpy as np
import matplotlib.pyplot as plt
    
from o_stress_2D import stress_2D
from o_discrete_point import discrete_point

import calculation_spheres_matrix as C_S_M
import Interpolation as In
import SpheresBoundary as SB

#============================================================================== 
#表征应力的discrete_point对象列表
def DiscreteValueStress(which_spheres,plane,input_mode,output_mode):
    
    if input_mode!='stress':
        
        print('ERROR:Incorrect input mode')
        
        return
    
    #结果列表
    discrete_points=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #创建discrete_point对象
        new_discrete_point=discrete_point()
        
        #定义基本属性
        new_discrete_point.pos_x=this_sphere.position[0]
        new_discrete_point.pos_y=this_sphere.position[1]
        
        #new stress object
        new_stress_2D=stress_2D()
        
#        print(this_sphere.stress_tensor_2D)

        '''plane'''
        list_plane=['XoY','YoZ','ZoX']
        list_position_index=[(0,1),(1,2),(2,0)]
        
        #create index-value map
        map_plane_position_index=dict(zip(list_plane,list_position_index))
        
        #true: default (0,1)
        this_position_index=map_plane_position_index[plane]
        
        #XY
        new_discrete_point.pos_x=this_sphere.position[this_position_index[0]]
        new_discrete_point.pos_y=this_sphere.position[this_position_index[1]]
        
        #radius
        new_discrete_point.radius=this_sphere.radius
        
        #define new 2D stess tensor
        this_stress_tensor=np.zeros((2,2))
        
        for i in range(2):
            
            for j in range(2):
                
#                print(this_position_index[i])
#                print(this_position_index[j])
#                
#                print(this_sphere.stress_tensor)
                
                this_stress_tensor[i,j]=this_sphere.stress_tensor[this_position_index[i],this_position_index[j]]
        
#        print(this_stress_tensor)
        
        #Initialize and gain attributes
        new_stress_2D.Init(this_stress_tensor)
        
        #x方向上正应力
        if output_mode=='x_normal':
        
            new_discrete_point.pos_z=new_stress_2D.x_normal_stress
            
        #y方向上正应力
        if output_mode=='y_normal':
        
            new_discrete_point.pos_z=new_stress_2D.y_normal_stress
         
        #剪应力
        if output_mode=='shear':
        
            new_discrete_point.pos_z=new_stress_2D.shear_stress
        
        #平均剪应力
        if output_mode=='mean_normal':
        
            new_discrete_point.pos_z=new_stress_2D.mean_normal_stress
        
        #最大剪应力
        if output_mode=='maximal_shear':
            
            new_discrete_point.pos_z=new_stress_2D.maximal_shear_stress
            
        #删除z值无限大的点
        if new_discrete_point.pos_z==np.inf or new_discrete_point.pos_z==-np.inf:
            
            print(new_discrete_point.pos_z)
            
            continue
            
        discrete_points.append(new_discrete_point)
        
    return discrete_points

#============================================================================== 
#系列图：1 构造形态 2 应力偏量 3 剪切形变
#pixel_step:网格点边长的长度
def StressSeriesPlot(which_spheres,pixel_step):
     
    ax=plt.subplot(6,1,1)
   
    #构造形态的绘制
    #图形
#    SpheresPlot(which_spheres)
    
    #图像
    spheres_grids=C_S_M.SpheresGrids(ax,which_spheres,pixel_step)
    spheres_grids.Plot()
    
#    print(np.shape(spheres_grids.img_tag))
    
    #表面兄弟
    surface=SB.SpheresSurface(spheres_grids)
    
    #标题与细节
#    ChineseTitle('构造形态')
    In.TicksAndSpines(ax)
    
    #各种应力
    discrete_points_σ_x=DiscreteValueStress(which_spheres,'x_normal_stress') 
    discrete_points_σ_y=DiscreteValueStress(which_spheres,'y_normal_stress') 
    discrete_points_τ_xy=DiscreteValueStress(which_spheres,'shear_stress')    
    discrete_points_σ_m=DiscreteValueStress(which_spheres,'mean_normal_stress') 
    discrete_points_τ_max=DiscreteValueStress(which_spheres,'maximal_shear_stress')  

    #所有哥的列表
    discrete_points=[discrete_points_σ_x,
                     discrete_points_σ_y,
                     discrete_points_τ_xy,
                     discrete_points_σ_m,
                     discrete_points_τ_max]
    #子图索引
    number=1
    
    for this_discrete_points in discrete_points:
        
        number+=1
        this_ax=plt.subplot(6,1,number)
    
        #网格点
        this_mesh_points=In.MeshGrid(this_ax,this_discrete_points,pixel_step)
        
#    return In.IDWInterpolation(ax,this_discrete_points,this_mesh_points,surface)

#        print(this_mesh_points)
#        
        #最终矩阵
        this_img=In.ImgFlip(In.ImgRotate(In.IDWInterpolation(ax,this_discrete_points,this_mesh_points,surface)),0)  
        
        plt.imshow(this_img,cmap='gist_rainbow')
        
#        print(np.shape(this_img)[:2])
        
        #标题与细节
    #    ChineseTitle('应力偏量σ_m')
    
        In.TicksAndSpines(this_ax)
            
#============================================================================== 
#σ_ij为应力张量
def Stress2D(σ_ij):
    
    #如果是列表改变尺寸
    if isinstance(σ_ij,list):
        
        σ_ij=σ_ij.reshape((int(np.sqrt(len(σ_ij))),int(np.sqrt(len(σ_ij)))))
    
    #张应力
    σ_x=σ_ij[0,0]
    σ_y=σ_ij[1,1]
    
    #平均应力
    σ_m=(σ_x+σ_y)/2
    
    #print(σ_m)
    
    #剪应力
    τ_xy=(σ_ij[0,1]+σ_ij[1,0])/2
    
    #计算最大最小主应力
    #剪应力
    τ_max=+np.sqrt((σ_x-σ_y)**2+τ_xy**2)
    τ_min=-np.sqrt((σ_x-σ_y)**2+τ_xy**2)
    
#    print(τ_max,τ_min)
    
    #正应力
    σ_max=σ_m+τ_max
    σ_min=σ_m+τ_min
    
#    print(σ_max,σ_min)
    
    #差异应力
    σ_d=σ_max-σ_min
    
#    print(σ_m,σ_d)
    
    #正应力对应的主方向
    θ_σ_max=np.arctan(2*τ_xy/(σ_x-σ_y))
    θ_σ_min=θ_σ_max+np.pi/2
    
#    print(θ_σ_max,θ_σ_min)
    
    #剪应力对应的主方向
    θ_τ_max=θ_σ_max+np.pi/4
    θ_τ_min=θ_σ_max-np.pi/4

#    print(θ_τ_max,θ_τ_min)
    
    #定义新的应力变量
    that_stress_2D=o_stress_2D.stress_2D() 
    
    #赋值  
    that_stress_2D.σ_ij=σ_ij
    that_stress_2D.σ_x=σ_x
    that_stress_2D.σ_y=σ_y
    that_stress_2D.σ_m=σ_m
    that_stress_2D.σ_d=σ_d
    that_stress_2D.σ_max=σ_max
    that_stress_2D.σ_min=σ_min
    that_stress_2D.τ_xy=τ_xy
    that_stress_2D.τ_max=τ_max
    that_stress_2D.τ_min=τ_min
    that_stress_2D.θ_σ_max=θ_σ_max
    that_stress_2D.θ_σ_min=θ_σ_min
    that_stress_2D.θ_τ_max=θ_τ_max
    that_stress_2D.θ_τ_min=θ_τ_min
    
    return that_stress_2D