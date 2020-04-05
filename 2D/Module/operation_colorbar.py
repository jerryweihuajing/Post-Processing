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

import calculation_global_parameter as C_G_P

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
    
Returns:
    absolute position of the object [left, bottom, width, height]
"""
def PositionInSubplot(position_relative):
    
    subplot_ax=plt.gca()
    
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
    which_progress: progress object to calculate
    post_fix: post fix of txt file (default: 'Structural Deformation')
    ax_img: AxesImage object
    orientation: orientation of colorbar
    
Returns:
    absolute position of the object [left, bottom, width, height]
"""
def SetColorbar(which_progress,post_fix,ax_img,orientation='vertical'):
    
    figure=plt.gcf()
    
    if orientation=='vertical':
        
        relative_position=[0.88,0.06,0.03,0.88]
        
    if orientation=='horizontal':
        
        relative_position=[0.84,0.7,0.15,0.2]
    
    '''fig.add_axes([left, bottom, width, height]) so as the relative ones'''
    this_colorbar_position=figure.add_axes(PositionInSubplot(relative_position))

    #plot colorbar
    this_colorbar=figure.colorbar(ax_img,cax=this_colorbar_position,orientation=orientation)  
        
    if 'Strain-Cumulative' in post_fix:
        
        this_colorbar.set_ticks([-1,0,1])
        this_colorbar.set_ticklabels(('-1','0','1'))
 
    if 'Strain-Periodical' in post_fix:
        
        this_colorbar.set_ticks([-.5,0,.5])
        this_colorbar.set_ticklabels(('-0.5','0','0.5'))
     
    if 'Strain-Instantaneous' in post_fix:
        
        this_colorbar.set_ticks([-.1,0,.1])
        this_colorbar.set_ticklabels(('-0.1','0','0.1'))
        
    if 'Stress' in post_fix:

        if which_progress.case==None:
            
            print('--> Local Colorbar')
            
            value_matrix=which_progress.map_matrix[post_fix]
            v_min,v_max=MinimumWithoutNan(value_matrix),MaximumWithoutNan(value_matrix)   
            
        else:
            
            print('--> Global Colorbar')
            
            v_min,v_max=C_G_P.GlobalValueRange(which_progress.case,post_fix)
            
        value_ticks=np.linspace(v_min,v_max,5)

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