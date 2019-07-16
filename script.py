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
    plane: 'XoY''YoZ''ZoX' displacement in 3 planes
    direction: 'x' 'y' 'z' displacement in 3 different direction
    mode: 'periodical''cumulative' dispalcement mode
    
Returns:
    discrete points objects list
"""
def DiscreteValueDisplacement(which_spheres,plane,direction,mode):
    
    #result list
    discrete_points=[]
    
    #遍历所有的sphere
    for this_sphere in which_spheres:
    
        #new discrete point object
        new_discrete_point=discrete_point()
        
        #plane
        if plane=='XoY':
            
            new_discrete_point.pos_x=this_sphere.position[0]
            new_discrete_point.pos_y=this_sphere.position[1]
        
        if plane=='YoZ':
            
            new_discrete_point.pos_x=this_sphere.position[1]
            new_discrete_point.pos_y=this_sphere.position[2]
            
        if plane=='ZoX':
            
            new_discrete_point.pos_x=this_sphere.position[2]
            new_discrete_point.pos_y=this_sphere.position[0]
            
        #dispalcement mode
        if mode=='periodical':
            
            this_displacment=cp.deepcopy(this_sphere.displacemnet_3D_periodical)
        
        if mode=='cumulative':
            
            this_displacment=cp.deepcopy(this_sphere.displacemnet_3D_cumulative)
        
        #direction
        if direction=='x':
            
            new_discrete_point.pos_z=this_displacment[0]
            
        if direction=='y':
            
            new_discrete_point.pos_z=this_displacment[1]
        
        if direction=='z':
            
            new_discrete_point.pos_z=this_displacment[2]
            
        discrete_points.append(new_discrete_point)
        
    return discrete_points

spheres=MAP[5]  
          
a=DiscreteValueDisplacement(spheres,plane='XoY',direction='x',mode='cumulative')    

surface_map=SB.SpheresTopMap(spheres,10)

In.SpheresInGridIDW(a,10,surface_map,show=True)

#print(folder_path)

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
      
