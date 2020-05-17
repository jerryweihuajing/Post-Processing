# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay
"""

"""
demand:
。    improve the label font
"""

from __init__ import *

case_path=r'E:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single base salt bT=2.4 sT=5 sD=24 sO=200 sW=400'

'''spheres generation'''
pixel_step=1

that_case=case()

that_case.InitCalculation(case_path)

global_spheres=list(that_case.list_A_progress[-1].map_id_spheres.values())

'''local spheres'''
x_spheres=[this_sphere.position[0] for this_sphere in global_spheres]
y_spheres=[this_sphere.position[1] for this_sphere in global_spheres]

#the radius of the maximum and minimum
radius_of_min=global_spheres[x_spheres.index(min(x_spheres))].radius
radius_of_max=global_spheres[y_spheres.index(max(y_spheres))].radius

#x,y boundary
boundary_x=[min(x_spheres)-radius_of_min,max(x_spheres)+radius_of_min]
boundary_y=[min(y_spheres)-radius_of_max,max(y_spheres)+radius_of_max]
    
#maximum of radius
maximum_radius=np.max([this_sphere.radius for this_sphere in global_spheres])

#left lower corner point of virtual grid
xpos_grid,ypos_grid=52,47

length_grid=pixel_step
length_virtual_grid=maximum_radius*2+pixel_step

#4 boundary of interpolation area
x_min,x_max=400,500
y_min,y_max=0,100

'''real boundary box for image'''
x_min_relative,x_max_relative=0,x_max-x_min
y_min_relative,y_max_relative=0,y_max-y_min

#axis display
cell_padding_boundary=10

local_spheres=[this_sphere for this_sphere in global_spheres\
               if x_min<=this_sphere.position[0]<=x_max\
               and y_min<=this_sphere.position[1]<=y_max]

'''about consumption'''
spheres=cp.deepcopy(local_spheres)

#fetch the mesh object
that_mesh=C_S_B.SpheresContent(spheres,pixel_step)

#surface_map=C_S_B.SpheresTopMap(spheres,pixel_step) 

img_tag=that_mesh.img_tag

'''effect of smmothing: structural deformation, stress, strain'''

'''effect of boundary extraction: erosion and expansion'''