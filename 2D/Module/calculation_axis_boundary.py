# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:23:09 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Axis Boundary
"""

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
 
#------------------------------------------------------------------------------       
"""
Global axis boundary in different phase

Args:
    which_Spheres_list: spheres list
    
Returns:
    axis boundary list
"""
def GlobalAxisBoundary(spheres_list):
    
    #所有期次的LocalAxisBoundary
    total_local_axis_boundary=[]
    
    #绘制不同期次的形态
    for k in range(len(spheres_list)):
        
        #生成颗粒体系
        this_spheres=spheres_list[k]
        
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