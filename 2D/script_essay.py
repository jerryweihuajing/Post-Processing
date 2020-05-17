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

def PlotGrid(xpos_grid,
             ypos_grid,
             length_grid,
             length_virtual_grid):

    xpos_grid-=0.5
    ypos_grid-=0.5
    
    #left lower corner point of grid
    
    xpos_virtual_grid,ypos_virtual_grid=xpos_grid-maximum_radius,ypos_grid-maximum_radius
    
    #plt.figure(figsize=(6,6))
    
    #draw a virtual border with a radius of a+r_max
    plt.vlines(xpos_grid,
               ypos_grid,
               ypos_grid+length_grid,
               color='r',
               linestyles="-")
    
    plt.vlines(xpos_grid+length_grid,
               ypos_grid,
               ypos_grid+length_grid,
               color='r',
               linestyles="-")
    
    plt.hlines(ypos_grid,
               xpos_grid,
               xpos_grid+length_grid,
               color='r',
               linestyles="-")
    
    plt.hlines(ypos_grid+length_grid,
               xpos_grid,
               xpos_grid+length_grid,
               color='r',
               linestyles="-")
    
    #draw a concrete border with a radius of a+r_max
    plt.vlines(xpos_virtual_grid,
               ypos_virtual_grid,
               ypos_virtual_grid+length_virtual_grid,
               color='r',
               linestyles="--")
    
    plt.vlines(xpos_virtual_grid+length_virtual_grid,
               ypos_virtual_grid,
               ypos_virtual_grid+length_virtual_grid,
               color='r',
               linestyles="--")
    
    plt.hlines(ypos_virtual_grid,
               xpos_virtual_grid,
               xpos_virtual_grid+length_virtual_grid,
               color='r',
               linestyles="--")
    
    plt.hlines(ypos_virtual_grid+length_virtual_grid,
               xpos_virtual_grid,
               xpos_virtual_grid+length_virtual_grid,
               color='r',
               linestyles="--")
    
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

local_spheres=[this_sphere for this_sphere in global_spheres if 470<=this_sphere.position[0]<=570]

'''about consumption'''
spheres=cp.deepcopy(local_spheres)

#fetch the mesh object
that_mesh=C_S_B.SpheresContent(spheres,pixel_step)

#surface_map=C_S_B.SpheresTopMap(spheres,pixel_step) 

img_tag=that_mesh.img_tag




#PlotGrid(xpos_grid+400,
#         ypos_grid,
#         pixel_step,
#         maximum_radius*2+pixel_step)
#
#plt.axis([450,456,44,50])

'''effect of interplation'''
#plot scatter points in grid


#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_from_data=C_I.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

#have a test to find the ROI
start_index=400
length_ROI=100

plt.figure(figsize=(6,6))

plt.imshow(img_rgb_from_data[:,start_index:start_index+length_ROI])
plt.axis([0,100,0,100])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('rasterization.png',dpi=300,bbox_inches='tight')
plt.close()

#for this_sphere in spheres:
#        
#    plt.plot(this_sphere.position[0],
#             this_sphere.position[1],
#             marker='o',
#             markersize=this_sphere.radius,
#             color=this_sphere.color)     


#plot gird without value

'''effect of smmothing: structural deformation, stress, strain'''

'''effect of boundary extraction: erosion and expansion'''