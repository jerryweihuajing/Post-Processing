# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:25:52 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation of Spheres in Image
"""

'''
demand:
Calculate strain via displacement
'''

import copy as cp
import numpy as np

import matplotlib.pyplot as plt
    
from o_grid import grid
from o_mesh import mesh
from o_square import square
from o_circle import circle
from o_scatter import scatter
from o_strain_2D import strain_2D

import operation_dictionary as O_D

import calculation_image as C_Im
import calculation_stress as C_S
import calculation_rasterization as C_R
import calculation_interpolation as C_In
import calculation_spheres_boundary as C_S_B

from data_yade_color import yade_rgb_list

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
        new_discrete_point=scatter()
        
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
            this_grid=grid() 
            
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
    
    #建立tag_color映射关系字典
    for this_sphere in which_spheres:

        this_sphere.tag=yade_rgb_list.index(this_sphere.color)

    if method=='B':
        
        tag_list=[k for k in range(len(yade_rgb_list))]
        
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
            this_grid.tag=O_D.DictKeyOfValue(this_grid.map_tag_color,max(list(this_grid.map_tag_color.values())))
            
    #        print(this_grid.tag)
                  
            #与之对应的color
            this_grid.color=yade_rgb_list[this_grid.tag]       
            
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
            new_square=square()
            
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
                    new_circle=circle()
                    
                    new_circle.radius=this_sphere.radius*factor
                    new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])
                    
                    new_circle.Init()
                    
                #    print(new_circle.center)
                #    print(new_circle.area)
                #    print(len(new_circle.points_inside))
                
                    #同样一个像素点不同的circle表示的面积是不一样的
                    area_this_sphere_in_this_grid=new_circle.area*len(C_R.ContentSquareCrossCircle(new_square,new_circle))/len(new_circle.points_inside)
                    
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
                        
#                print(map_tag_area)
                #print(area_inside)
                        
        #        print(DictKeyOfValue(map_tag_area,max(list(map_tag_area.values()))))
                
                this_grid.tag=O_D.DictKeyOfValue(map_tag_area,max(list(map_tag_area.values())))
                
                #与之对应的color
                this_grid.color=yade_rgb_list[this_grid.tag] 
        
            #集合为空
            if this_grid.spheres_inside==[]:
                
                this_grid.tag=-1
                this_grid.color=np.array([1.0,1.0,1.0])
        
    #输出图像
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
    img_color_mesh=np.full((amount_grid_x,amount_grid_y,3),np.array([1.0,1.0,1.0]))
   
    for this_grid in grids:
        
        img_tag_mesh[this_grid.index_x,this_grid.index_y]=this_grid.tag
        img_color_mesh[this_grid.index_x,this_grid.index_y]=this_grid.color
        
    #要输出的mesh对象
    that_mesh=mesh()
    
    #赋值
    that_mesh.grids=grids
    that_mesh.img_tag=C_Im.ImgFlip(C_Im.ImgRotate(cp.deepcopy(img_tag_mesh)),0)
    that_mesh.img_color=C_Im.ImgFlip(C_Im.ImgRotate(cp.deepcopy(img_color_mesh)),0)
    
    return that_mesh

#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX]' displacement in 3 planes
    which_direction: ['x','y','z'] displacement in 3 different direction
    which_input_mode: ['periodical_strain','cumulative_strain'] dispalcement mode
    
Returns:
    discrete points objects list
"""
def DiscreteValueDisplacement(which_spheres,which_plane,which_direction,which_input_mode):
    
    print('')
    print('-- Discrete Value Displacement')
    print('-> plane:',which_plane)
    print('-> direction:',which_direction)
    print('-> input mode:',which_input_mode.replace('_',' '))
    
    #result list
    scatters=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #new discrete point object
        new_scatter=scatter()
        
#        print(this_sphere.position)
#        print(this_sphere.displacemnet_3D_periodical)
#        print(this_sphere.displacemnet_3D_cumulative)
        
#        if which_plane=='XoY':
#            
#            new_discrete_point.pos_x=this_sphere.position[0]
#            new_discrete_point.pos_y=this_sphere.position[1]
#        
#        if which_plane=='YoZ':
#            
#            new_discrete_point.pos_x=this_sphere.position[1]
#            new_discrete_point.pos_y=this_sphere.position[2]
#            
#        if which_plane=='ZoX':
#            
#            new_discrete_point.pos_x=this_sphere.position[2]
#            new_discrete_point.pos_y=this_sphere.position[0]
#            
#        if which_mode=='periodical':
#            
#            this_displacment=cp.deepcopy(this_sphere.displacemnet_3D_periodical)
#        
#        if which_mode=='cumulative':
#            
#            this_displacment=cp.deepcopy(this_sphere.displacemnet_3D_cumulative)
#            
#        if which_direction=='x':
#            
#            new_discrete_point.pos_z=this_displacment[0]
#            
#        if which_direction=='y':
#            
#            new_discrete_point.pos_z=this_displacment[1]
#        
#        if which_direction=='z':
#            
#            new_discrete_point.pos_z=this_displacment[2]
            
        #plane
        list_plane=['XoY','YoZ','ZoX']
        list_position_index=[(0,1),(1,2),(2,0)]
        
        #create index-value map
        map_plane_position_index=dict(zip(list_plane,list_position_index))
        
        new_scatter.pos_x=this_sphere.position[map_plane_position_index[which_plane][0]]
        new_scatter.pos_y=this_sphere.position[map_plane_position_index[which_plane][1]]
                   
        #dispalcement mode
        list_mode=['periodical_strain','cumulative_strain']
        list_displacement=[cp.deepcopy(this_sphere.periodical_displacement),
                           cp.deepcopy(this_sphere.cumulative_displacement)]
        
#        print(list_displacement)
        
        #create index-value map
        map_mode_displacement=dict(zip(list_mode,list_displacement))
        
        this_displacement=map_mode_displacement[which_input_mode]
                    
        #direction
        list_direction=['x','y','z']
        list_displacement_index=[0,1,2]
        
        #create index-value map
        map_direction_displacment_index=dict(zip(list_direction,list_displacement_index))

#        print(map_direction_displacment_index)
#        print(which_direction)
        
        #value
        new_scatter.pos_z=this_displacement[map_direction_displacment_index[which_direction]]
              
        #radius
        new_scatter.radius=this_sphere.radius
        
#        print(this_displacement)
#        print(map_direction_displacment_index)
#        print(map_direction_displacment_index[which_direction])
#        print(this_displacement[map_direction_displacment_index[which_direction]] )
        
#        print(new_discrete_point.pos_x)
#        print(new_discrete_point.pos_y)
#        print(new_discrete_point.pos_z)
        
        scatters.append(new_scatter)
        
    return scatters

#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_direction: ['x','y','z'] displacement in 3 different direction
    which_input_mode: ['periodical','cumulative'] dispalcement mode
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Displacement matrix in one direction
"""
def SpheresDisplacementMatrix(pixel_step,
                              which_spheres,
                              which_plane,
                              which_direction,
                              which_input_mode,
                              which_interpolation,
                              show=False):
    
    #scatter objects
    scatters=DiscreteValueDisplacement(which_spheres,
                                       which_plane,
                                       which_direction,
                                       which_input_mode)    

    #top surface map
    surface_map=C_S_B.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='scatters_in_grid':
        
        return C_In.ScattersInGridIDW(scatters,pixel_step,surface_map,show)

#------------------------------------------------------------------------------
"""
Spheres strain objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_input_mode: ['periodical','cumulative'] dispalcement mode
    which_output_mode: ['x_normal','y_normal','shear','volumetric','distortional']
    which_interpolation: ['scatters_in_grid','grids_in_scatter]
    
Returns:
    Spheres strain values matrix
"""   
def SpheresStrainMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_input_mode,
                        which_output_mode,
                        which_interpolation):
    
    print('')
    print('-- Spheres Strain Matrix')
    
    #displacemnt in x direction
    x_displacement=SpheresDisplacementMatrix(pixel_step,
                                             which_spheres,
                                             which_plane,
                                             'x',
                                             which_input_mode,
                                             which_interpolation)
    
    #displacemnt in y direction
    y_displacement=SpheresDisplacementMatrix(pixel_step,
                                             which_spheres,
                                             which_plane,
                                             'y',
                                             which_input_mode,
                                             which_interpolation)
#    print(x_displacement)
#    print(y_displacement)
    
    #axis=0 x gradient
    #axis=1 y gradient
    gradient_xx=np.gradient(x_displacement,axis=0)
    gradient_xy=np.gradient(x_displacement,axis=1)
    gradient_yx=np.gradient(y_displacement,axis=0)
    gradient_yy=np.gradient(y_displacement,axis=1)
    
#    print(np.shape(gradient_xx))
#    print(np.shape(gradient_xy))
#    print(np.shape(gradient_yx))
#    print(np.shape(gradient_yy))
#    
#    print(gradient_xx)
#    print(gradient_xy)
#    print(gradient_yx)
#    print(gradient_yy)
    
    #make sure shape is same
    if not (np.shape(gradient_xx)==np.shape(gradient_xy)==np.shape(gradient_yx)==np.shape(gradient_yy)):
        
        print('=> ERROR: Incorrect dimension')
        
        return
    
    row,column=np.shape(gradient_xx)
    
    #result strain matrix
    strain_object_matrix=np.full((row,column),strain_2D())
    
    '''generate strain objects'''
    for i in range(row):
        
        for j in range(column):
            
            #defien new strain 2D object
            new_strain_2D=strain_2D()
            
            #new 2D strain object and its strain tensor
            this_strain_tensor=np.zeros((2,2))
            
            #give the value
            this_strain_tensor[0,0]=gradient_xx[i,j]
            this_strain_tensor[0,1]=(gradient_xy[i,j]+gradient_yx[i,j])/2
            this_strain_tensor[1,0]=(gradient_xy[i,j]+gradient_yx[i,j])/2
            this_strain_tensor[1,1]=gradient_yy[i,j]

#            print(this_strain_tensor)            
                      
            '''3D 2D Init is different'''
            new_strain_2D.Init(cp.deepcopy(this_strain_tensor))
            
#            print(new_strain_2D.strain_tensor)
#            print(new_strain_2D.x_normal_strain)
            
            strain_object_matrix[i,j]=cp.deepcopy(new_strain_2D)
            
    '''generate strain values'''
    strain_value_matrix=np.zeros(np.shape(strain_object_matrix))
    
    for i in range(row):
        
        for j in range(column):

            this_strain_2D=cp.deepcopy(strain_object_matrix[i,j])
          
            if which_output_mode=='x_normal':
  
                strain_value_matrix[i,j]=this_strain_2D.x_normal_strain
                
            if which_output_mode=='y_normal':
  
                strain_value_matrix[i,j]=this_strain_2D.y_normal_strain
                
            if which_output_mode=='shear':
                
                strain_value_matrix[i,j]=this_strain_2D.shear_strain
                
            if which_output_mode=='volumetric':
  
                strain_value_matrix[i,j]=this_strain_2D.volumetric_strain
            
            if which_output_mode=='distortional':
  
                strain_value_matrix[i,j]=this_strain_2D.distortional_strain
                
    return strain_value_matrix
    
#------------------------------------------------------------------------------
"""
Spheres stress values matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_input_mode: 'stress'
    which_output_mode: ['x_normal','y_normal','shear','mean_normal','maximal_shear']
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Spheres stress value matrix
"""   
def SpheresStressMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_input_mode,
                        which_output_mode,
                        which_interpolation):

    if which_input_mode!='stress':
        
        print('ERROR: you idiot!')        
        
        return 

    #discrete point objects
    discrete_points=C_S.ScattersStress(which_spheres,
                                               which_plane,
                                               which_input_mode,
                                               which_output_mode)   

    #top surface map
    surface_map=C_S_B.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='scatters_in_grid':
        
        return C_In.ScattersInGridIDW(discrete_points,pixel_step,surface_map)
    
#------------------------------------------------------------------------------
"""
Spheres values objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_input_mode: ['stress','cumulative_strain','periodical_strain']
    which_output_mode: ['x_normal','y_normal','shear',......]
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Spheres value matrix
"""   
def SpheresValueMatrix(pixel_step,
                       which_spheres,
                       which_plane,
                       which_input_mode,
                       which_output_mode,
                       which_interpolation):
    
    if which_input_mode=='stress':
        
        return SpheresStressMatrix(pixel_step,
                                   which_spheres,
                                   which_plane,
                                   which_input_mode,
                                   which_output_mode,
                                   which_interpolation)
        
    if 'strain' in which_input_mode:
        
        return SpheresStrainMatrix(pixel_step,
                                   which_spheres,
                                   which_plane,
                                   which_input_mode,
                                   which_output_mode,
                                   which_interpolation)