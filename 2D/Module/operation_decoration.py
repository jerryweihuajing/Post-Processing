# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:27:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot Decoration
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.pyplot import MultipleLocator

#==============================================================================
#用新字体表示中文图名
def ChineseTitle(which_title):
    
    #动态修改字体，需要在可视化参数中添加fontproperties=font
    font=FontProperties(fname=r"C:\Windows\Fonts\Simsun.ttc",size=12)
    
    #标题与细节
    plt.title(which_title,fontproperties=font)
    
#============================================================================== 
#坐标轴和边框
def TicksAndSpines(ticks=False,
                   spines=False,
                   style='scaled'):
    
    which_ax=plt.gca()
    
    #拉长形态
    which_ax.axis(style)

    #去掉坐标轴
    if not ticks:

        which_ax.set_xticks([])
        which_ax.set_yticks([])
     
     #去掉上下左右边框
    if not spines:

        which_ax.spines['top'].set_visible(False) 
        which_ax.spines['bottom'].set_visible(False) 
        which_ax.spines['left'].set_visible(False) 
        which_ax.spines['right'].set_visible(False)
        
#------------------------------------------------------------------------------
"""
Configure ticks on ax

Args:
    x_offset: translate distance in x axis (toward right)
    x_ticks: (bool) whether there is x ticks (default: True) 
    
Returns:
    None
"""        
def TicksConfiguration(x_offset,x_ticks=True):
      
    which_ax=plt.gca()
    
    #x locator
    x_major_interval=100
    x_minor_interval=int(x_major_interval/5)
    
    x_min=-500
    x_max=1500
    
    x_major_realticks=np.array(list(range(x_min,x_max,x_major_interval)))-x_offset
    x_minor_realticks=np.array(list(range(x_min,x_max,x_minor_interval)))-x_offset
    
    if x_ticks:
        
        x_major_showticks=(x_major_realticks+x_offset).astype(int)
        
    else:
        
        x_major_showticks=len(x_major_realticks)*['']
        
    x_minor_showticks=len(x_minor_realticks)*['']
    
    which_ax.set_xticks(x_major_realticks)
    which_ax.set_xticklabels(x_major_showticks)
    which_ax.set_xticks(x_minor_realticks,minor=True)
    which_ax.set_xticklabels(x_minor_showticks,minor=True)

    #y locator
    y_major_interval=50
    y_minor_interval=int(y_major_interval/5)
    
    which_ax.yaxis.set_major_locator(MultipleLocator(y_major_interval))
    which_ax.yaxis.set_minor_locator(MultipleLocator(y_minor_interval))

    plt.tick_params(labelsize=10)
    labels = which_ax.get_xticklabels() + which_ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]

#------------------------------------------------------------------------------
"""
Call plt.axis on different case

Args:
    output_folder: folder to get case name
    plus_offset: translate distance in x axis (toward right)
    global_shape: global shape of all progress
 
Returns:
    None
"""      
def AxisLimit(output_folder,plus_offset,global_shape):
    
    subplot_ax=plt.gca()
    
    if 'double' in output_folder:
        
        if 'diff' in output_folder:
            
            plus_offset-=50
            
        else:
            
            plus_offset-=80
    
    subplot_ax.axis([plus_offset,plus_offset+global_shape[1]*1.13,0,global_shape[0]])
    
#------------------------------------------------------------------------------
"""
Calculate offset about title position

Args:
    which_progress: progress object to be calculated

Returns:
    None
""" 
def TitleOffset(which_progress):
    
    if 'compression' in which_progress.path:
        
        vertical_offset=-20
        
    if 'extension' in which_progress.path:
        
        vertical_offset=1
        
    horizontal_offset=-which_progress.offset
    
    if 'double' in which_progress.path:
        
        if 'diff' in which_progress.path:
            
            horizontal_offset-=50
            
        else:
            
            horizontal_offset-=80
        
    return horizontal_offset,vertical_offset