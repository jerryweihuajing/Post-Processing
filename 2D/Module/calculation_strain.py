# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:08:13 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Plot the Strain
"""

import copy as cp
import numpy as np

from o_scatter import scatter    
from o_strain_2D import strain_2D

import calculation_interpolation as C_In
import calculation_spheres_boundary as C_S_B

import calculation_tensor2D as C_T2D

#------------------------------------------------------------------------------
"""
Generate displacement scatters

Args:
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX]' displacement in 3 planes
    which_direction: ['x','y','z'] displacement in 3 different direction
    which_input_mode: ['periodical_strain','cumulative_strain'] dispalcement mode
    
Returns:
    scatters objects list
"""
def ScattersDisplacement(which_spheres,which_plane,which_direction,which_input_mode):
    
    print('')
    print('-- Scatters Displacement')
    print('-> plane:',which_plane)
    print('-> direction:',which_direction)
    print('-> input mode:',which_input_mode.replace('_',' '))
    
    #result list
    scatters=[]
    
    #traverse all spheres
    for this_sphere in which_spheres:
    
        #new discrete point object
        new_scatter=scatter()

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
     
        #create index-value map
        map_mode_displacement=dict(zip(list_mode,list_displacement))
        
        this_displacement=map_mode_displacement[which_input_mode]
                    
        #direction
        list_direction=['x','y','z']
        list_displacement_index=[0,1,2]
        
        #create index-value map
        map_direction_displacment_index=dict(zip(list_direction,list_displacement_index))
 
        #value
        new_scatter.pos_z=this_displacement[map_direction_displacment_index[which_direction]]
              
        #radius
        new_scatter.radius=this_sphere.radius
             
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
    scatters=ScattersDisplacement(which_spheres,
                                  which_plane,
                                  which_direction,
                                  which_input_mode)    

    #top surface map
    surface_map=C_S_B.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='scatters_in_grid':
        
        return C_In.ScattersInGridIDW(scatters,pixel_step,surface_map,show)

#============================================================================== 
#表征strain的discrete_point对象列表
#input_mode:'cumulative' 'periodical'
#output_mode: 'x' 'y' 'shear' 'volumetric' 'distortional'
def ScattersStrain(which_spheres,input_mode,output_mode):
      
    #for output
    scatters_strain=[]
    
    count=-1
    
    #traverse
    for this_sphere in which_spheres:
        
        this_scatter=scatter()
        
        count+=1
      
        #define the attribute
        if isinstance(this_sphere.position,str):
                
            this_scatter.pos_x=float(this_sphere.position.split()[0])
            this_scatter.pos_y=float(this_sphere.position.split()[1])
            
        else:
            
            this_scatter.pos_x=this_sphere.position[0]
            this_scatter.pos_y=this_sphere.position[1]
 
        #cumulative
        if input_mode=='cumulative_strain':
        
            this_strain_tensor=this_sphere.strain_tensor_3D_cumulative
        
        #periodical
        if input_mode=='periodical_strain':
            
            this_strain_tensor=this_sphere.strain_tensor_3D_periodical
             
        #create new strain obkect
        new_strain_2D=strain_2D()
        
        #Initialize and gain attributes
        new_strain_2D.Init(this_strain_tensor)
    
        #x方向上正应变
        if output_mode=='x_normal_strain':
        
            this_scatter.pos_z=new_strain_2D.x_normal_strain
        
        #y方向上正应变
        if output_mode=='y_normal_strain':
        
            this_scatter.pos_z=new_strain_2D.y_normal_strain
        
        #剪切应变
        if output_mode=='shear_strain':
        
            this_scatter.pos_z=new_strain_2D.shear_strain
        
        #体积应变
        if output_mode=='volumetric_strain':
        
            this_scatter.pos_z=new_strain_2D.volumetric_strain
        
        #变形应变
        if output_mode=='distortional_strain':
        
            this_scatter.pos_z=new_strain_2D.distortional_strain              
        
        #删除z值无限大的点
        if this_scatter.pos_z==np.inf or this_scatter.pos_z==-np.inf:

            continue
        
        scatters_strain.append(this_scatter)
        
    return scatters_strain

#============================================================================== 
#pixel_step:网格点边长的长度
def StrainsSeriesPlot(which_spheres,pixel_step):
    
    return

#============================================================================== 
#σ_ij为应力张量
def Strain2D(which_strain_tensor):
    
    which_strain_tensor=np.array(which_strain_tensor)

    #如果是列表改变尺寸
    if isinstance(which_strain_tensor,list):
            
        which_strain_tensor=np.array(which_strain_tensor).reshape((int(np.sqrt(len(which_strain_tensor))),
                           int(np.sqrt(len(which_strain_tensor)))))
    
    else:
        
        #scalar of all elements
        if np.shape(which_strain_tensor)[0]==None:
            
            product=np.shape(which_strain_tensor)[1]
            
        else:
            
            product=np.shape(which_strain_tensor)[0]
            
        which_strain_tensor=which_strain_tensor.reshape((int(np.sqrt(product)),int(np.sqrt(product))))
    
    x_normal_strain=which_strain_tensor[0,0]
    y_normal_strain=which_strain_tensor[1,1]
    
    shear_strain=which_strain_tensor[0,1]+which_strain_tensor[1,0]
    
#    shear_strain=np.sqrt(which_strain_tensor[0,1]**2+\
#                         which_strain_tensor[0,2]**2+\
#                         which_strain_tensor[1,2]**2)
        
    volumetric_strain=C_T2D.Tensor1stInvariant(which_strain_tensor)
    distortional_strain=C_T2D.Tensor2ndInvariant(which_strain_tensor)
    
    #定义新的应变变量
    that_strain_2D=strain_2D() 
    
    #赋值  
    that_strain_2D.strain_tensor=which_strain_tensor
    that_strain_2D.x_normal_strain=x_normal_strain
    that_strain_2D.y_normal_strain=y_normal_strain
    that_strain_2D.shear_strain=shear_strain
    that_strain_2D.volumetric_strain=volumetric_strain
    that_strain_2D.distortional_strain=distortional_strain
    
    return that_strain_2D