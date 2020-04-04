# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 21:47:40 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of single figure in a progress
"""

import numpy as np

import matplotlib.pyplot as plt

import operation_path as O_P
import operation_decoration as O_D

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_global_parameter as C_G_P

from configuration_font import annotation_font,title_font,colorbar_font

def MaximumWithoutNan(which_matrix):
    
    return which_matrix.ravel()[np.logical_not(np.isnan(which_matrix.ravel()))].max()

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
Plot single structural deformation in different progress with fracture (do not save)

Args:
    which_progress: progress object
    subplot_ax: subplot axes in progress plot
    x_ticks: (bool) whether there is x ticks (default: True) 
    with_fracture: (bool) plot fracture or not (default: False)  
    with_annotation: (bool) plot progress proportion (default: True) 
    with_title: (bool) plot title which stands for postfix (default: False) 

Returns:
    None
"""
def IndividualStructuralDeformation(which_progress,
                                    subplot_ax,
                                    x_ticks=True,
                                    with_fracture=False,
                                    with_annotation=True,
                                    with_title=False):
    print('')
    print('-- Structural Deformation')
    print('-> progress='+which_progress.percentage)
    
    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    #percentage of progress
    progress_percentage=which_progress.percentage

    #transform to RGB format
    structural_deformation_img_rgb=which_progress.structural_deformation

    #outline matrix
    outline_matrix=which_progress.structural_deformation_outline
    
    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(which_progress.img_tag)
    
    #plot main body
    subplot_ax.imshow(structural_deformation_img_rgb)

    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(C_M.MatrixFilter(fracture_matrix,-1,1,show=True)) is bool:
            
            print('=> WARNING: without fracture')

    #plot outline
    subplot_ax.imshow(outline_matrix,cmap='gray') 
    
    #decoration  
    O_D.TicksAndSpines(subplot_ax,1,1)
    O_D.TicksConfiguration(subplot_ax,which_progress.offset,x_ticks)

    #sub annotation
    if with_annotation:
          
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)

    #sub title
    if with_title:
        
        subplot_ax.annotate('Structural Deformation',
                            xy=(0,0),
                            xytext=(-which_progress.offset+0.008*global_shape[1],0.8*global_shape[0]),
                            fontproperties=title_font)
        
#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture (do not save)

Args:
    which_progress: progress object
    post_fix: post fix of txt file
    subplot_ax: subplot axes in progress plot
    x_ticks: (bool) whether there is x ticks (default: True) 
    with_fracture: (bool) plot fracture or not (default: False) 
    with_annotation: (bool) plot progress proportion (default: True) 
    with_title: (bool) plot title which stands for postfix (default: False) 
    
Returns:
    a matplotlib.image.AxesImage object
"""
def IndividualStressOrStrain(which_progress,
                             post_fix,
                             subplot_ax,
                             x_ticks=True,
                             with_fracture=False,
                             with_annotation=True,
                             with_title=False):
    print('')
    print('-- '+post_fix)
    print('-> progress='+which_progress.percentage)
    
    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    #percentage of progress
    progress_percentage=which_progress.percentage
    
    #stress or strain value matrix to be plotted
    value_matrix=which_progress.map_matrix[post_fix]
    
    #outline matrix
    outline_matrix=which_progress.map_outline[post_fix]

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    if which_progress.case==None:
        
        print('--> Local Norm')
        
        this_ax_img=subplot_ax.imshow(C_I.ImgFlip(value_matrix,0),
                                      cmap=C_G_P.GlobalColormap(post_fix))
            
    else:
        
        print('--> Global Norm')
        
        this_ax_img=subplot_ax.imshow(C_I.ImgFlip(value_matrix,0),
                                      cmap=C_G_P.GlobalColormap(post_fix),
                                      norm=C_G_P.GlobalNorm(which_progress.case,post_fix))
   
    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(C_M.MatrixFilter(fracture_matrix,-1,1,show=True)) is bool:
            
            print('==> WARNING: without fracture')
            
    #plot outline
    subplot_ax.imshow(np.flip(outline_matrix,0),cmap='gray')   
     
    #decoration  
    O_D.TicksAndSpines(subplot_ax,1,1)
    O_D.TicksConfiguration(subplot_ax,which_progress.offset,x_ticks)
    
    #sub annotation
    if with_annotation:
        
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)
        
    #sub title
    if with_title:
        
        subplot_ax.annotate(post_fix,
                            xy=(0,0),
                            xytext=(-which_progress.offset+0.008*global_shape[1],0.8*global_shape[0]),
                            fontproperties=title_font)
        
    return this_ax_img

#------------------------------------------------------------------------------
"""
Plot single figure

Args:
    output_folder: folder to contain result
    which_progress: progress object
    post_fix: post fix of txt file (default: 'Structural Deformation')
    situation: for ['case','progress'] (default: 'case')
    x_ticks: (bool) whether there is x ticks (default: False) 
    with_fracture: (bool) plot fracture or not (default: False) 
    
Returns:
    None
"""        
def Individual(output_folder,
               which_progress,
               post_fix='Structural Deformation',
               situation='case',
               x_ticks=False,
               with_fracture=False):
     
    print('')
    print('-- Single Individual In Progress')
    print('-> '+post_fix)

    #global shape of progress or integral analysis
    global_shape=which_progress.shape 
    
    #new picture and ax
    figure=C_G_P.FigureForSeriesAndIndividual(global_shape)
        
    #new picture and ax
    this_ax=plt.subplot()

    if post_fix=='Structural Deformation':
        
        IndividualStructuralDeformation(which_progress=which_progress,
                                        subplot_ax=this_ax,
                                        x_ticks=x_ticks,
                                        with_fracture=with_fracture,
                                        with_annotation=True,
                                        with_title=True)
    else:
        
        this_ax_img=IndividualStressOrStrain(which_progress=which_progress,
                                             post_fix=post_fix,
                                             subplot_ax=this_ax,
                                             x_ticks=x_ticks,
                                             with_fracture=with_fracture,
                                             with_annotation=True,
                                             with_title=True)

    '''double'''
    plus_offset=-which_progress.offset
    
    if 'double' in output_folder:
        
        if 'diff' in output_folder:
            
            plus_offset-=50
            
        else:
            
            plus_offset-=80
    
    this_ax.axis([plus_offset,plus_offset+global_shape[1]*1.13,0,global_shape[0]])
    
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
            
    #figure path and name    
    if situation=='case':
        
        individual_folder=output_folder+'\\'+post_fix+'\\'
        fig_name=which_progress.percentage
        
    if situation=='progress':

        individual_folder=output_folder+'\\'+which_progress.percentage+'\\'
        fig_name=post_fix
        
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    #generate folder
    O_P.GenerateFolder(individual_folder)
    
    #path of this figure
    this_fig_path=individual_folder+'\\'+fig_name+'.png'
    
    #save this fig
    figure.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
    plt.close()
    
    return this_fig_path