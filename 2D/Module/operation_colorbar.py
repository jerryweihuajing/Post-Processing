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

import calculation_matrix as C_M
import calculation_global_parameter as C_G_P

from configuration_font import colorbar_font

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
    colorbar_orientation: orientation of colorbar in axes ['horizontal','vertical'] (default: 'horizontal')
    
Returns:
    absolute position of the object [left, bottom, width, height]
"""
def SetColorbar(which_progress,
                post_fix,
                ax_img,
                colorbar_orientation='horizontal'):
    
    figure=plt.gcf()
    
    '''fig.add_axes([left, bottom, width, height]) so as the relative ones'''
    if colorbar_orientation=='vertical':
        
        relative_position=[0.88,0.06,0.03,0.88]
        
    if colorbar_orientation=='horizontal':
        
        if 'compression' in which_progress.path:
            
            relative_position=[0.83,0.73,0.16,0.2]
    
        if 'extension' in which_progress.path:
            
            relative_position=[0.8,0.7,0.17,0.17]
            
    this_colorbar_position=figure.add_axes(PositionInSubplot(relative_position))

    #plot colorbar
    this_colorbar=figure.colorbar(ax_img,cax=this_colorbar_position,orientation=colorbar_orientation)  
        
    if 'Strain' in post_fix:
        
        if '-Cumulative' in post_fix:
            
            this_colorbar.set_ticks([-1,0,1])
            this_colorbar.set_ticklabels(('-1','0','1'))
     
        if '-Periodical' in post_fix:
            
            this_colorbar.set_ticks([-.5,0,.5])
            this_colorbar.set_ticklabels(('-0.5','0','0.5'))
     
        if '-Instantaneous' in post_fix:
            
            this_colorbar.set_ticks([-.1,0,.1])
            this_colorbar.set_ticklabels(('-0.1','0','0.1'))
        
    else:
        
        if which_progress.case==None:
            
            print('--> Local Colorbar')
            
            value_matrix=which_progress.map_matrix[post_fix]
            v_min,v_max=C_M.MinimumWithoutNan(value_matrix),C_M.MaximumWithoutNan(value_matrix)   
            
        else:
            
            print('--> Global Colorbar')
            
            v_min,v_max=C_G_P.GlobalValueRange(which_progress.case,post_fix)
            
        value_ticks=np.linspace(v_min,v_max,5)
    
        #real position
        ticks=list(value_ticks)
        
        if 'Stress' in post_fix:
            
            #str to display
            ticklabels=tuple([str(int(np.round(10e-6*this_tick))) for this_tick in ticks])
            
            #stress unit: MPa
            this_colorbar.set_label('(MPa)',fontdict=colorbar_font)
            
        if 'Velocity' in post_fix:
            
            #str to display
            ticklabels=tuple([str(np.round(this_tick,2)) for this_tick in ticks])
            
            #stress unit: MPa
            this_colorbar.set_label('(m/s)',fontdict=colorbar_font)
          
        if 'Displacement' in post_fix:
            
            #str to display
            ticklabels=tuple([str(int(np.round(this_tick))) for this_tick in ticks])
            
            #stress unit: MPa
            this_colorbar.set_label('(m)',fontdict=colorbar_font)
            
        #major ticks
        this_colorbar.set_ticks(ticks)
        this_colorbar.set_ticklabels(ticklabels)
 
    #set ticks
    this_colorbar.ax.tick_params(labelsize=5)

    #label fonts
    for this_label in this_colorbar.ax.xaxis.get_ticklabels():
        
        this_label.set_fontname('serif')