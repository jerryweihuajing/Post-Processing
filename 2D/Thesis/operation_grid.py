# -*- coding: utf-8 -*-
"""
Created on Sat May 30 13:43:31 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot
"""

import numpy as np

import matplotlib.pyplot as plt

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
    
    num_ticks=6
    
    x_major_realticks=np.linspace(x_min_relative-0.5,x_min_relative-0.5+length_window,num_ticks)
    x_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,num_ticks))]
    y_major_realticks=np.linspace(y_min_relative-0.5,y_min_relative-0.5+length_window,num_ticks)
    y_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,num_ticks))]
    
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