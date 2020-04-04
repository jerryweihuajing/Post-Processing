# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:01:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculation about colorbar
"""

import Path as Pa
import IntegralPlot as IP
import SpheresGeneration as SG

'''global shape would change the scale of sxes'''
#colorbar position of stress and strain 
if post_fix!='Structural Deformation':
    
    '''fig.add_axes([left, bottom, width, height]) so as the relative ones'''
    this_colorbar_position=figure.add_axes(PositionInSubplot([0.84,0.72,0.15,0.22],this_ax))

    #plot colorbar
    this_colorbar=figure.colorbar(this_ax_img,cax=this_colorbar_position,orientation='horizontal')
    
    if 'Strain' in post_fix:
        
        this_colorbar.set_ticks([-1,0,1])
        this_colorbar.set_ticklabels(('-1','0','1'))
 
    if 'Stress' in post_fix:
        
        #value matrix to be plotted
        value_matrix=which_progress.map_matrix[post_fix]
        
        value_ticks=np.linspace(MinimumWithoutNan(value_matrix),MaximumWithoutNan(value_matrix),5)
        
        #real position
        ticks=list(value_ticks)
        
        #str to display
        ticklabels=tuple([str(int(np.round(10e-6*this_tick))) for this_tick in ticks])

        this_colorbar.set_ticks(ticks)
        this_colorbar.set_ticklabels(ticklabels)

        #stress unit: MPa
        this_colorbar.set_label('(MPa)',fontdict=colorbar_font)
        
    #set ticks
    this_colorbar.ax.tick_params(labelsize=6)

    #label fonts
    for this_label in this_colorbar.ax.xaxis.get_ticklabels():
        
        this_label.set_fontname('serif')