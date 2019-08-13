# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:02:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculate spheres attributes matrix
"""

'''
demand:
Calculate strain via displacement
'''

import copy as cp
import numpy as np

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from o_strain_2D import strain_2D
from o_discrete_point import discrete_point

import Interpolation as In
import SpheresBoundary as SB
import StressPlot as Stress

#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    which_spheres: input sphere objects list
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    which_direction: 'x' 'y' 'z' displacement in 3 different direction
    which_input_mode: 'periodical_strain' 'cumulative_strain' dispalcement mode
    
Returns:
    discrete points objects list
"""
def DiscreteValueDisplacement(which_spheres,which_plane,which_direction,which_input_mode):
    
    #result list
    discrete_points=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #new discrete point object
        new_discrete_point=discrete_point()
        
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
        
        new_discrete_point.pos_x=this_sphere.position[map_plane_position_index[which_plane][0]]
        new_discrete_point.pos_y=this_sphere.position[map_plane_position_index[which_plane][1]]
                   
        #dispalcement mode
        list_mode=['periodical_strain','cumulative_strain']
        list_displacement=[cp.deepcopy(this_sphere.periodical_displacemnet),
                           cp.deepcopy(this_sphere.cumulative_displacemnet)]
        
        #create index-value map
        map_mode_displacement=dict(zip(list_mode,list_displacement))
        
        this_displacement=map_mode_displacement[which_input_mode]
                    
        #direction
        list_direction=['x','y','z']
        list_displacement_index=[0,1,2]
        
        #create index-value map
        map_direction_displacment_index=dict(zip(list_direction,list_displacement_index))
        
        new_discrete_point.pos_z=this_displacement[map_direction_displacment_index[which_direction]]
                
#        print(this_displacement)
#        print(map_direction_displacment_index)
#        print(map_direction_displacment_index[which_direction])
#        print(this_displacement[map_direction_displacment_index[which_direction]] )
        
#        print(new_discrete_point.pos_x)
#        print(new_discrete_point.pos_y)
#        print(new_discrete_point.pos_z)
        
        discrete_points.append(new_discrete_point)
        
    return discrete_points

#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    pixel_step: length of single pixel
    which_spheres: input sphere objects list
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    which_direction: 'x' 'y' 'z' displacement in 3 different direction
    which_input_mode: 'periodical' 'cumulative' dispalcement mode
    which_interpolation: 'spheres_in_grid' 'global'
    
Returns:
    Displacement matrix in one direction
"""
def SpheresDisplacementMatrix(pixel_step,
                              which_spheres,
                              which_plane,
                              which_direction,
                              which_input_mode,
                              which_interpolation='spheres_in_grid',
                              show=False):
    
    #discrete point objects
    discrete_points=DiscreteValueDisplacement(which_spheres,
                                              which_plane,
                                              which_direction,
                                              which_input_mode)    

    #top surface map
    surface_map=SB.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='spheres_in_grid':
        
        return In.SpheresInGridIDW(discrete_points,pixel_step,surface_map,show)

#------------------------------------------------------------------------------
"""
Spheres strain objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel
    which_spheres: input sphere objects list
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    which_input_mode: 'periodical' 'cumulative' dispalcement mode
    which_output_mode: 'x_normal' 'y_normal' 'shear' 'volumetric' 'distortional'
    which_interpolation: 'spheres_in_grid' 'global'
    
Returns:
    Spheres strain values matrix
"""   
def SpheresStrainMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_input_mode,
                        which_output_mode,
                        which_interpolation='spheres_in_grid'):
    
    #displacemnt in x direction
    x_displacement=SpheresDisplacementMatrix(pixel_step,
                                             which_spheres,
                                             which_plane,
                                             'x',
                                             which_input_mode)
    
    #displacemnt in y direction
    y_displacement=SpheresDisplacementMatrix(pixel_step,
                                             which_spheres,
                                             which_plane,
                                             'y',
                                             which_input_mode)
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
        
        print('ERROR:Incorrect dimension')
        
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
    pixel_step: length of single pixel
    which_spheres: input sphere objects list
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    which_input_mode: 'stress'
    which_output_mode: 'x_normal' 'y_normal' 'shear' 'mean_normal' 'maximal_shear'
    which_interpolation: 'spheres_in_grid' 'global'
    
Returns:
    Spheres stress value matrix
"""   
def SpheresStressMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_input_mode,
                        which_output_mode,
                        which_interpolation='spheres_in_grid'):

    if which_input_mode!='stress':
        
        print('ERROR:you idiot!')        
        
        return 

    #discrete point objects
    discrete_points=Stress.DiscreteValueStress(which_spheres,
                                               which_plane,
                                               which_input_mode,
                                               which_output_mode)   

    #top surface map
    surface_map=SB.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='spheres_in_grid':
        
        return In.SpheresInGridIDW(discrete_points,pixel_step,surface_map)
    
#------------------------------------------------------------------------------
"""
Spheres values objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel
    which_spheres: input sphere objects list
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    which_input_mode: 'stress' 'cumulative_strain' 'periodical_strain' 
    which_output_mode: 'x_normal' 'y_normal' 'shear' ......
    which_interpolation: 'spheres_in_grid' 'global'
    
Returns:
    Spheres value matrix
"""   
def SpheresValueMatrix(pixel_step,
                       which_spheres,
                       which_plane,
                       which_input_mode,
                       which_output_mode,
                       which_interpolation='spheres_in_grid'):
    
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
        