# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:07:33 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot the Stress
"""

import numpy as np
import matplotlib.pyplot as plt
    
from o_scatter import scatter
from o_stress_2D import stress_2D

import operation_decoration as O_D

import calculation_image as C_Im
import calculation_interpolation as C_In
import calculation_spheres_matrix as C_S_M
import calculation_spheres_boundary as C_S_B

#------------------------------------------------------------------------------
"""
Generate stress scatters

Args:
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX]' displacement in 3 planes
    which_direction: ['xx','xy','xy'] displacement in 3 different direction
    
Returns:
    scatters objects list
"""
def ScattersStress(which_spheres,which_plane,which_direction):
    
    #final result
    scatters=[]
    
    #traverse all spheres
    for this_sphere in which_spheres:
    
#        #expire sphere from uplift
#        if this_sphere.tag==9:
#            
#            continue
        
        #construct new scatter
        new_scatter=scatter()
        
        #plane
        list_plane=['XoY','YoZ','ZoX']
        list_position_index=[(0,1),(1,2),(2,0)]
        
        #create index-value map
        map_plane_position_index=dict(zip(list_plane,list_position_index))
        
        #true: default (0,1)
        this_position_index=map_plane_position_index[which_plane]
       
        #XY
        ix_x=this_position_index[0]
        ix_y=this_position_index[1]
        
        #define basic attributes
        new_scatter.pos_x=this_sphere.position[ix_x]
        new_scatter.pos_y=this_sphere.position[ix_y]
        
        #radius
        new_scatter.radius=this_sphere.radius
        
        if which_direction=='xx':
            
            new_scatter.pos_z=this_sphere.stress_tensor[ix_x,ix_x]
        
        if which_direction=='yy':
            
            new_scatter.pos_z=this_sphere.stress_tensor[ix_y,ix_y]
            
        if which_direction=='xy':
            
            new_scatter.pos_z=0.5*(this_sphere.stress_tensor[ix_x,ix_y]+\
                                   this_sphere.stress_tensor[ix_y,ix_x])
            
        scatters.append(new_scatter)
        
    return scatters

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
    
    #表面兄弟
    surface=C_S_B.SpheresSurface(spheres_grids)
    
    #标题与细节
#    ChineseTitle('构造形态')
    O_D.TicksAndSpines(ax)
    
    #各种应力
    discrete_points_σ_x=ScattersStress(which_spheres,'x_normal_stress') 
    discrete_points_σ_y=ScattersStress(which_spheres,'y_normal_stress') 
    discrete_points_τ_xy=ScattersStress(which_spheres,'shear_stress')    
    discrete_points_σ_m=ScattersStress(which_spheres,'mean_normal_stress') 
    discrete_points_τ_max=ScattersStress(which_spheres,'maximal_shear_stress')  

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
        this_mesh_points=C_S_M.MeshGrid(this_ax,this_discrete_points,pixel_step)
        
#    return In.IDWInterpolation(ax,this_discrete_points,this_mesh_points,surface)
       
        #最终矩阵
        this_img=C_Im.ImgFlip(C_Im.ImgRotate(C_In.IDWInterpolation(ax,this_discrete_points,this_mesh_points,surface)),0)  
        
        plt.imshow(this_img,cmap='gist_rainbow')
        
        #标题与细节
    #    ChineseTitle('应力偏量σ_m')
    
        C_In.TicksAndSpines(this_ax)
            
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
    
    #正应力
    σ_max=σ_m+τ_max
    σ_min=σ_m+τ_min
 
    #差异应力
    σ_d=σ_max-σ_min
    
    #正应力对应的主方向
    θ_σ_max=np.arctan(2*τ_xy/(σ_x-σ_y))
    θ_σ_min=θ_σ_max+np.pi/2

    #剪应力对应的主方向
    θ_τ_max=θ_σ_max+np.pi/4
    θ_τ_min=θ_σ_max-np.pi/4

    #定义新的应力变量
    that_stress_2D=stress_2D() 
    
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