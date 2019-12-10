# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:25:52 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：导入应力张量
"""
import copy as cp
import numpy as np
import matplotlib.pyplot as plt
    
import o_grid
import o_mesh
import o_square
import o_circle
import o_discrete_point

import Image as Img
import Dictionary as Dict
import Rasterization as Ra
 
#==============================================================================
#绘制所有的sphere对象
def SpheresPlot(which_spheres):
    
    for this_sphere in which_spheres:
        
        plt.plot(this_sphere.position[0],
                 this_sphere.position[1],
                 marker='o',
                 markersize=this_sphere.radius,
                 color=this_sphere.color)           
  
#============================================================================== 
#表征构造形态rgb颗粒列表
def DiscreteValue_rgb(which_spheres):
    
     #结果列表
    discrete_points=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #创建discrete_point对象
        new_discrete_point=o_discrete_point.discrete_point()
        
        #定义基本属性
        new_discrete_point.pos_x=this_sphere.position[0]
        new_discrete_point.pos_y=this_sphere.position[1]
        new_discrete_point.pos_z=this_sphere.color
        
        #删除z值无限大的点
        if max(new_discrete_point.pos_z)>1 or min(new_discrete_point.pos_z)<0:
            
            print(new_discrete_point.pos_z)
            
            continue
            
        discrete_points.append(new_discrete_point)
        
    return discrete_points
        
"""
将sphere投入grid的2种投射方法:
A grid内spheres的面积
B grid内spheres的数量
attention:1和2面临网格小于颗粒的情况，分辨率受限
"""        
#==============================================================================  
#构造颗粒映射网格
#length为网格边长
#factor: very important paramete
'''the calculation corresponding with factor is not correct'''
def SpheresGrids(which_spheres,length,show=False):

    #首先找出网格的坐标范围
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #xy边界
    boundary_x=[min(x_spheres),max(x_spheres)]
    boundary_y=[min(y_spheres),max(y_spheres)]
    
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
            
    return grids

#============================================================================== 
#transgorm spheres into image
def SpheresImage(which_spheres,length,show=False,method='A',factor=1):

    #generate spheres grids
    grids=SpheresGrids(which_spheres,length)
    
    #restruct
    amount_grid_x=max([this_grid.index_x for this_grid in grids])+1
    amount_grid_y=max([this_grid.index_y for this_grid in grids])+1
    
    #总的color数量和种类
    color_list=[]
    
    #建立映射关系
    map_tag_color={}
    map_tag_color[0]=[1.0,1.0,1.0]
    
    #建立tag_color映射关系字典
    for this_sphere in which_spheres:
        
        if list(this_sphere.color) not in color_list:
            
            color_list.append(list(this_sphere.color))
    
            map_tag_color[len(color_list)]=list(this_sphere.color)
            
        this_sphere.tag=Dict.DictKeyOfValue(map_tag_color,list(this_sphere.color))
        
#    print(map_tag_color)
    
    #建立tag列表
    tag_list=list(map_tag_color.keys())    
    
    if method=='B':
        
        #将sphere投入grid
        for this_sphere in which_spheres:
            
            for this_grid in grids:
                
                #判断是否在grid内
                if this_grid.position_x<=this_sphere.position[0]<this_grid.position_x+this_grid.length and\
                   this_grid.position_y<=this_sphere.position[1]<this_grid.position_y+this_grid.length:
                    
                    this_grid.spheres_inside.append(this_sphere)  
                    
        #各个tag的数量字典
        grid_map_tag_color=dict(zip(tag_list,len(tag_list)*[0]))
             
        #计算某种各颜色的数量           
        for this_grid in grids:     
            
            #每个grid都会有的
            this_grid.map_tag_color=cp.deepcopy(grid_map_tag_color)
            
            #grid内的所有sphere
            for this_sphere_inside in this_grid.spheres_inside:
                
                this_grid.map_tag_color[this_sphere_inside.tag]+=1
            
    #        print(this_grid.map_tag_color)
            
            #数量最多的像素
            this_grid.tag=Dict.DictKeyOfValue(this_grid.map_tag_color,max(list(this_grid.map_tag_color.values())))
            
    #        print(this_grid.tag)
                  
            #与之对应的color
            this_grid.color=map_tag_color[this_grid.tag]       
            
    #        print(this_grid.color)
        
    #    print(amount_grid_x,amount_grid_y)
    
    '''A'''
    if method=='A':
        
        #spheres中最大半径
        radius_list=[this_sphere.radius for this_sphere in which_spheres]
        radius_max=max(radius_list)
        
        #traverse the grids
        for this_grid in grids:
                
            #new 2D square 
            new_square=o_square.square()
            
            new_square.length=this_grid.length*factor
            new_square.center=this_grid.position+np.array([new_square.length/2,new_square.length/2])
            new_square.Init()
    
            #print(new_square.area)
            #print(len(new_square.points_inside))
            
            #print(which_grid.position_x)
            #print(which_grid.position_y)
            
            virtual_grid=cp.deepcopy(this_grid)
            virtual_grid.position_x-=radius_max
            virtual_grid.position_y-=radius_max
            virtual_grid.position=np.array([virtual_grid.position_x,virtual_grid.position_y])
            virtual_grid.length+=2*radius_max
            
            #画出虚拟边框
            if show:
                     
                #画一个虚拟边框，半径为a+r_max
                plt.vlines(virtual_grid.position_x,
                           virtual_grid.position_y,
                           virtual_grid.position_y+virtual_grid.length,
                           color='r',
                           linestyles="--")
                
                plt.vlines(virtual_grid.position_x+virtual_grid.length,
                           virtual_grid.position_y,
                           virtual_grid.position_y+virtual_grid.length,
                           color='r',
                           linestyles="--")
                
                plt.hlines(virtual_grid.position_y,
                           virtual_grid.position_x,
                           virtual_grid.position_x+virtual_grid.length,
                           color='r',
                           linestyles="--")
                
                plt.hlines(virtual_grid.position_y+virtual_grid.length,
                           virtual_grid.position_x,
                           virtual_grid.position_x+virtual_grid.length,
                           color='r',
                           linestyles="--")
            
            #判断哪些圆心在红色方框内
            for this_sphere in which_spheres:
                
                if virtual_grid.SphereInside(this_sphere):
                    
                    this_grid.spheres_inside.append(this_sphere)
            
            #计算总面积
            area_inside_this_grid=0
            
            #tag频率的映射
            map_tag_area={}
            
            #在spheres_inside里做文章
            if this_grid.spheres_inside!=[]:
                    
                for this_sphere in this_grid.spheres_inside:
                    
                    #二维圆
                    new_circle=o_circle.circle()
                    
                    new_circle.radius=this_sphere.radius*factor
                    new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])
                    
                    new_circle.Init()
                    
                #    print(new_circle.center)
                #    print(new_circle.area)
                #    print(len(new_circle.points_inside))
                
                    #同样一个像素点不同的circle表示的面积是不一样的
                    area_this_sphere_in_this_grid=new_circle.area*len(Ra.ContentSquareCrossCircle(new_square,new_circle))/len(new_circle.points_inside)
                    
                    #面积累加
                    area_inside_this_grid+=area_this_sphere_in_this_grid
                    
                #    print(area_this_sphere_in_this_grid)
                    
                #    print(this_sphere.tag)
                    
                    #事先存在
                    if this_sphere.tag in map_tag_area.keys():
                
                        map_tag_area[this_sphere.tag]+=area_this_sphere_in_this_grid    
                        
                    #初次添加
                    if this_sphere.tag not in map_tag_area.keys():
                
                        map_tag_area[this_sphere.tag]=area_this_sphere_in_this_grid
                        
                #print(map_tag_area)
                #print(area_inside)
                        
        #        print(DictKeyOfValue(map_tag_area,max(list(map_tag_area.values()))))
                
                this_grid.tag=Dict.DictKeyOfValue(map_tag_area,max(list(map_tag_area.values())))
                
                #与之对应的color
                this_grid.color=map_tag_color[this_grid.tag] 
        
            #集合为空
            if this_grid.spheres_inside==[]:
                
                this_grid.tag=0
                this_grid.color=np.array([1.0,1.0,1.0])
        
    #输出图像
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
    img_color_mesh=np.full((amount_grid_x,amount_grid_y,3),np.array([1.0,1.0,1.0]))
   
    for this_grid in grids:
        
        img_tag_mesh[this_grid.index_x,this_grid.index_y]=this_grid.tag
        img_color_mesh[this_grid.index_x,this_grid.index_y]=this_grid.color
        
    #要输出的mesh对象
    that_mesh=o_mesh.mesh()
    
    #赋值
    that_mesh.grids=grids
    that_mesh.img_tag=Img.ImgFlip(Img.ImgRotate(cp.deepcopy(img_tag_mesh)),0)
    that_mesh.img_color=Img.ImgFlip(Img.ImgRotate(cp.deepcopy(img_color_mesh)),0)
    
    return that_mesh