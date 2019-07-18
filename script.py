# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：execution script
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Object.o_grid import grid
from Object.o_mesh import mesh
from Object.o_sphere import sphere
from Object.o_strain_2D import strain_2D
from Object.o_discrete_point import discrete_point

from Module import Path as Pa
from Module import NewPath as NP
from Module import ColorBar as CB
from Module import Animation as An
from Module import Dictionary as Dict
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import ContentBoundary as CB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG
from Module import NewSpheresGeneration as NSG

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

'''
demand 4:
draw surface with stress or strain figure

demand 5:
Calculate strain via displacement
'''

#data folder path
case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.3 v=1.0\\input\\base=0.00'

#file_names=FileNamesThisCase(case_path)
file_paths=NP.FilePathsThisCase(case_path)

#Generate map between phase index between spheres list 
MAP=NSG.GenerateSpheresMapWithSample(case_path)

#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    which_spheres: input sphere objects list
    which_plane: 'XoY''YoZ''ZoX' displacement in 3 planes
    which_direction: 'x' 'y' 'z' displacement in 3 different direction
    which_mode: 'periodical''cumulative' dispalcement mode
    
Returns:
    discrete points objects list
"""
def DiscreteValueDisplacement(which_spheres,which_plane,which_direction,which_mode):
    
    #result list
    discrete_points=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #new discrete point object
        new_discrete_point=discrete_point()
        
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
        list_mode=['periodical','cumulative']
        list_displacement=[cp.deepcopy(this_sphere.displacemnet_3D_periodical),
                           cp.deepcopy(this_sphere.displacemnet_3D_cumulative)]
        
        #create index-value map
        map_mode_displacement=dict(zip(list_mode,list_displacement))
        
        this_displacement=map_mode_displacement[which_mode]
                    
        #direction
        list_direction=['x','y','z']
        list_displacement_index=[0,1,2]
        
        #create index-value map
        map_direction_displacment_index=dict(zip(list_direction,list_displacement_index))
        
        new_discrete_point.pos_z=this_displacement[map_direction_displacment_index[which_direction]]
                
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
    which_mode: 'periodical' 'cumulative' dispalcement mode
    which_interpolation: 'spheres_in_grid' 'global'
    
Returns:
    Displacement matrix in one direction
"""
def SpheresDisplacementMatrix(pixel_step,
                              which_spheres,
                              which_plane,
                              which_direction,
                              which_mode,
                              which_interpolation='spheres_in_grid',
                              show=False):
    
    #discrete point objects
    discrete_points=DiscreteValueDisplacement(spheres,which_plane,which_direction,which_mode)    

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
                                  
            '''3D 2D Init is different'''
            new_strain_2D.Init(this_strain_tensor)
            
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
    
spheres=MAP[5]  
       
shear_strain_matrix=SpheresStrainMatrix(10,spheres,
                                        which_plane='XoY',
                                        which_input_mode='periodical',
                                        which_output_mode='shear')

plt.imshow(shear_strain_matrix)
#------------------------------------------------------------------------------
"""
Spheres stress objects matrix throughout args such as pixel step

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

    #discrete point objects
    discrete_points=Stress.DiscreteValueStress(which_spheres,
                                               which_input_mode,
                                               which_output_mode)   

    #top surface map
    surface_map=SB.SpheresTopMap(which_spheres,pixel_step)
    
    if which_interpolation=='spheres_in_grid':
        
        return In.SpheresInGridIDW(discrete_points,pixel_step,surface_map)
     

##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

#the mode which I search for
#mode_list=['shear_strain',
#           'volumetric_strain',
#           'distortional_strain']

#mode_list=['distortional_strain','volumetric_strain','shear_strain','y_normal_strain']

#mode_list=['distortional_strain']
#
#IP.SinglePlot(folder_path,'periodical_strain','y_normal_strain',1)

#load_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 1\output\periodical strain\x normal strain'

#load_path=r'C:\Users\whj\Desktop\operation'
##An.GenerateGIF(load_path)
##
#load_path=r'C:\魏华敬\Spyder\YADE\Stress Strain\Data\L=1000 v=1.0 r=1.0 layer=10 detachment=0-4\output\2019.6.19\case 4\periodical strain\y normal strain'
#
#An.GenerateGIF(load_path)

#output all images
#IP.TotalOuput(case_path,1)

#which_spheres=SG.GenerateSpheresFromTXT('progress=48.37%.txt')[0]

#pixel_step=1
#
#plt.figure()
#SB.SpheresLeftImg(which_spheres,pixel_step,show=True)
#SB.SpheresRightImg(which_spheres,pixel_step,show=True)
#SB.SpheresBottomImg(which_spheres,pixel_step,show=True)
#SB.SpheresSurfaceImg(which_spheres,pixel_step,show=True)

#plt.figure()
#
#SB.SimpleSpheresBoundary(which_spheres,pixel_step,show=True)

#edge=SB.SpheresEdge(spheres,pixel_step,True)
      
