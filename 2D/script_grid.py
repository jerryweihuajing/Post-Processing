# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:51:56 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-grid
"""

"""
demand:
    boundary box of interpolation and rasterization
"""

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
    
#plot boundary box
PlotGrid(xpos_grid+400,
         ypos_grid,
         pixel_step,
         maximum_radius*2+pixel_step)

plt.axis([450,456,44,50])