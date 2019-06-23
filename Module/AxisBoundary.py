# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:23:09 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Axis Boundary
"""

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Module import Path as Pa
from Module import SpheresGeneration as SG

#==============================================================================
#根据spheres确定边界：单独一期的参数
def LocalAxisBoundary(which_spheres):
    
    #所有的x,y坐标
    X=[this_sphere.position[0] for this_sphere in which_spheres]
    Y=[this_sphere.position[1] for this_sphere in which_spheres]
    R=[this_sphere.radius for this_sphere in which_spheres]
    
    #临界值加减最大半径
    x_boundary=[min(X)-max(R),max(X)+max(R)]
    y_boundary=[min(Y)-max(R),max(Y)+max(R)]
    
    #输出的列表
    local_axis_boundary=x_boundary+y_boundary
      
    return local_axis_boundary
        
#==============================================================================
#根据文件夹folder_path确定边界：适用于所有期次的参数
def GlobalAxisBoundary(which_case_path):
    
    #concrete file path
    input_file_path=which_case_path+'\stress'
    
    #输入文件名
    input_file_names=Pa.GenerateFileNames(input_file_path)

    #所有期次的LocalAxisBoundary
    total_local_axis_boundary=[]
    
    #绘制不同期次的形态
    for this_new_file_name in input_file_names:
        
        #输入路径
        this_input_path=input_file_path+'\\'+this_new_file_name
        
        #生成颗粒体系
        this_spheres=SG.GenerateSpheresFromTXT(this_input_path)[0]
        
        #将它们都收录进来
        total_local_axis_boundary.append(LocalAxisBoundary(this_spheres))
        
    #四个顶点
    x_boundary_min=min([this_local_axis_boundary[0] for this_local_axis_boundary in total_local_axis_boundary])
    x_boundary_max=max([this_local_axis_boundary[1] for this_local_axis_boundary in total_local_axis_boundary])
    y_boundary_min=min([this_local_axis_boundary[2] for this_local_axis_boundary in total_local_axis_boundary])
    y_boundary_max=max([this_local_axis_boundary[3] for this_local_axis_boundary in total_local_axis_boundary])
    
    #适当增加一些边界
    x_padding=(x_boundary_max-x_boundary_min)/100
    y_padding=(y_boundary_max-y_boundary_min)/100
    
    #将他们组合
    global_axis_boundary=[x_boundary_min-x_padding,
                          x_boundary_max+x_padding,
                          y_boundary_min-y_padding,
                          y_boundary_max+y_padding]
    
    #直接作用
#    plt.axis(global_axis_boundary)
            
#    print(global_axis_boundary)
    
    return global_axis_boundary