# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay
"""

from __init__ import *

def PlotMesh(x_min_relative,
             y_min_relative,
             length_window):
    
    x_lines=list(range(x_min_relative,x_min_relative+length_window))+[x_min_relative+length_window]
    y_lines=list(range(y_min_relative,y_min_relative+length_window))+[y_min_relative+length_window]
    
    x_lines=list(np.array(x_lines)-0.5)
    y_lines=list(np.array(y_lines)-0.5)
    
    for this_x in x_lines:
        
        plt.vlines(this_x,
                   y_min_relative-0.5,
                   y_min_relative-0.5+length_window,
                   color='k',
                   linestyles="-")
    
    for this_y in y_lines:
        
        plt.hlines(this_y,
                   x_min_relative-0.5,
                   x_min_relative-0.5+length_window,
                   color='k',
                   linestyles="-")
        
    plt.axis([x_min_relative-0.5,
              x_min_relative-0.5+length_window,
              y_min_relative-0.5,
              y_min_relative-0.5+length_window])
    
    #change ticks
    ax=plt.gca()
    
    x_major_realticks=np.linspace(x_min_relative-0.5,x_min_relative-0.5+length_window,6)
    x_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]
    y_major_realticks=np.linspace(y_min_relative-0.5,y_min_relative-0.5+length_window,6)
    y_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]
    
    ax.set_xticks(x_major_realticks)
    ax.set_xticklabels(x_major_showticks)
    ax.set_yticks(y_major_realticks)
    ax.set_yticklabels(y_major_showticks)
    
    plt.tick_params(labelsize=10)
    [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]
    
    
def PlotGrid(xpos_grid,
             ypos_grid,
             length_grid,
             style_line='-',
             color_lines='r'):

#    xpos_grid-=0.5
#    ypos_grid-=0.5
    
    #draw a concrete border with a length of a
    plt.plot([xpos_grid,xpos_grid],
             [ypos_grid,ypos_grid+length_grid],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid+length_grid,xpos_grid+length_grid],
             [ypos_grid,ypos_grid+length_grid],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid,xpos_grid+length_grid],
             [ypos_grid,ypos_grid],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid,xpos_grid+length_grid],
             [ypos_grid+length_grid,ypos_grid+length_grid],
             color=color_lines,
             linestyle=style_line)
    
def PlotRectangle(xpos_grid,
                  ypos_grid,
                  width,
                  height,
                  style_line='-',
                  color_lines='r'):

    #draw a concrete border with a length of a
    plt.plot([xpos_grid,xpos_grid],
             [ypos_grid,ypos_grid+height],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid+width,xpos_grid+width],
             [ypos_grid,ypos_grid+height],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid,xpos_grid+width],
             [ypos_grid,ypos_grid],
             color=color_lines,
             linestyle=style_line)
    
    plt.plot([xpos_grid,xpos_grid+width],
             [ypos_grid+height,ypos_grid+height],
             color=color_lines,
             linestyle=style_line)
    
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
x_min,x_max=320,420
y_min,y_max=0,100

'''real boundary box for image'''
x_min_relative,x_max_relative=0,(x_max-x_min)/pixel_step
y_min_relative,y_max_relative=0,(y_max-y_min)/pixel_step

#axis display
cell_padding_boundary=10/pixel_step

local_spheres=[this_sphere for this_sphere in global_spheres\
               if x_min<=this_sphere.position[0]<=x_max\
               and y_min<=this_sphere.position[1]<=y_max]

'''about consumption'''
spheres=cp.deepcopy(local_spheres)

#fetch the mesh object
that_mesh=C_S_B.SpheresContent(spheres,pixel_step)

img_tag=that_mesh.img_tag

#micro view of scatters
length_window=10

window_spheres=[this_sphere for this_sphere in local_spheres\
               if x_min<=this_sphere.position[0]<=x_min+length_window\
               and y_min<=this_sphere.position[1]<=y_min+length_window]

'''effect of smmothing: structural deformation, stress, strain'''

'''effect of boundary extraction: erosion and expansion'''