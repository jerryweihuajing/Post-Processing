# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:01:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculation about colorbar
"""

import numpy as np
import matplotlib.pyplot as plt

from configuration_font import colorbar_font

#------------------------------------------------------------------------------
"""
Calculate the maximum in a matrix regardless of nan

Args:
    which_matrix: matrix to calculate
    
Returns:
    matrix maximum
"""
def MaximumWithoutNan(which_matrix):
    
    return which_matrix.ravel()[np.logical_not(np.isnan(which_matrix.ravel()))].max()

#------------------------------------------------------------------------------
"""
Calculate the minimum in a matrix regardless of nan

Args:
    which_matrix: matrix to calculate
    
Returns:
    matrix minimum
"""
def MinimumWithoutNan(which_matrix):
    
    return which_matrix.ravel()[np.logical_not(np.isnan(which_matrix.ravel()))].min()

#------------------------------------------------------------------------------
"""
Convert relative position of subplot to global figure

Args:
    position_relative: relative [left, bottom, width, height] in colorbar
    subplot_ax: subplot axes to plot
    
Returns:
    absolute position of the object [left, bottom, width, height]
"""
def PositionInSubplot(position_relative,subplot_ax):
    
    #relative [left, bottom, width, height] in colorbar
    left_in_ax,bottom_in_ax,width_in_ax,height_in_ax=position_relative
    
    #absolute position of axes
    x_min,y_min,x_max,y_max=np.array(subplot_ax.get_position()).ravel()

    #absolute position of colorbar
    left=x_min+left_in_ax*(x_max-x_min)
    bottom=y_min+bottom_in_ax*(y_max-y_min)
    width=width_in_ax*(x_max-x_min)
    height=height_in_ax*(y_max-y_min)
    
    return [left,bottom,width,height]

#------------------------------------------------------------------------------
"""
Set Colorbar based on

Args:
    value_matrix: matrix to describe
    post_fix: post fix of txt file (default: 'Structural Deformation')
    ax_img: AxesImage object
    
Returns:
    absolute position of the object [left, bottom, width, height]
"""
def SetColorbar(value_matrix,post_fix,ax_img):
    
    this_ax=plt.gca()
    figure=plt.gcf()
    
    '''fig.add_axes([left, bottom, width, height]) so as the relative ones'''
    this_colorbar_position=figure.add_axes(PositionInSubplot([0.84,0.7,0.15,0.2],this_ax))

    #plot colorbar
    this_colorbar=figure.colorbar(ax_img,cax=this_colorbar_position,orientation='horizontal')  
        
    if 'Strain' in post_fix:
        
        this_colorbar.set_ticks([-1,0,1])
        this_colorbar.set_ticklabels(('-1','0','1'))
 
    if 'Stress' in post_fix:
        
        value_ticks=np.linspace(MinimumWithoutNan(value_matrix),MaximumWithoutNan(value_matrix),5)

        #real position
        ticks=list(value_ticks)

        #str to display
        ticklabels=tuple([str(int(np.round(10e-6*this_tick))) for this_tick in ticks])

        #major ticks
        this_colorbar.set_ticks(ticks)
        this_colorbar.set_ticklabels(ticklabels)
        
        #stress unit: MPa
        this_colorbar.set_label('(MPa)',fontdict=colorbar_font)
        
    #set ticks
    this_colorbar.ax.tick_params(labelsize=5)

    #label fonts
    for this_label in this_colorbar.ax.xaxis.get_ticklabels():
        
        this_label.set_fontname('serif')