# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:27:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot Decoration
"""

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
def TicksAndSpines(ax,
                   ticks=False,
                   spines=False,
                   style='scaled'):
    
    #拉长形态
    ax.axis(style)
    
    #去掉坐标轴
    if not ticks:

        ax.set_xticks([])
        ax.set_yticks([])
        
     #去掉上下左右边框
    if not spines:

        ax.spines['top'].set_visible(False) 
        ax.spines['bottom'].set_visible(False) 
        ax.spines['left'].set_visible(False) 
        ax.spines['right'].set_visible(False)
        
#------------------------------------------------------------------------------
"""
Configure ticks on ax

Args:
    which_ax: axes to be plotted
    
Returns:
    None
"""        
def TicksConfiguration(which_ax):
    
    #major locator
    which_ax.xaxis.set_major_locator(MultipleLocator(100))
    which_ax.yaxis.set_major_locator(MultipleLocator(50))
    
    #minor locator
    which_ax.xaxis.set_minor_locator(MultipleLocator(20))
    which_ax.yaxis.set_minor_locator(MultipleLocator(10))
    
    plt.tick_params(labelsize=10)
    labels = which_ax.get_xticklabels() + which_ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
        