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
import operation_colorbar as O_C
import operation_decoration as O_D

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_global_parameter as C_G_P

from configuration_font import annotation_font,title_font
from configuration_circumstance import title_position

#------------------------------------------------------------------------------
"""
Plot single structural deformation in different progress with fracture (do not save)

Args:
    which_progress: progress object
    x_ticks: (bool) whether there is x ticks (default: True) 
    with_fracture: (bool) plot fracture or not (default: False)  
    with_annotation: (bool) plot progress proportion (default: True) 
    with_title: (bool) plot title which stands for postfix (default: False) 

Returns:
    None
"""
def IndividualStructuralDeformation(which_progress,
                                    x_ticks=True,
                                    with_fracture=False,
                                    with_annotation=True,
                                    with_title=False):
    print('')
    print('-- Structural Deformation')
    print('-> progress='+which_progress.percentage)
    
    subplot_ax=plt.gca()
    
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
    O_D.TicksAndSpines(1,1)
    O_D.TicksConfiguration(which_progress.offset,x_ticks)

    #sub annotation
    if with_annotation:
          
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)

    #sub title
    if with_title:
        
        if title_position=='exterior':
            
            vertical_offset=1.3
            
        if title_position=='interior':
            
            vertical_offset=-20
            
        subplot_ax.annotate('Structural Deformation',
                            xy=(0,0),
                            xytext=(which_progress.offset+0.008*global_shape[1],vertical_offset+global_shape[0]),
                            fontproperties=title_font)
        
#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture (do not save)

Args:
    which_progress: progress object
    post_fix: post fix of txt file
    x_ticks: (bool) whether there is x ticks (default: True) 
    with_fracture: (bool) plot fracture or not (default: False) 
    with_annotation: (bool) plot progress proportion (default: True) 
    with_title: (bool) plot title which stands for postfix (default: False) 
    
Returns:
    a matplotlib.image.AxesImage object
"""
def IndividualCloudImage(which_progress,
                         post_fix,
                         x_ticks=True,
                         with_fracture=False,
                         with_annotation=True,
                         with_title=False):
    print('')
    print('-- Individual Cloud Image')
    print('-> '+post_fix)
    print('-> progress='+which_progress.percentage)
    
    subplot_ax=plt.gca()
    
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
    this_shape=np.shape(value_matrix)
    
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
    O_D.TicksAndSpines(1,1)
    O_D.TicksConfiguration(which_progress.offset,x_ticks)
    
    #sub annotation
    if with_annotation:
        
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)
        
    #sub title
    if with_title:
        
        if title_position=='exterior':
            
            vertical_offset=1.3
            
        if title_position=='interior':
            
            vertical_offset=-20
            
        subplot_ax.annotate(post_fix,
                            xy=(0,0),
                            xytext=(which_progress.offset+0.008*global_shape[1],vertical_offset+global_shape[0]),
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
    title_position: sub title is inside the axis or not ['exterior','interior'] (default: 'interior')
    
Returns:
    None
"""        
def Individual(output_folder,
               which_progress,
               post_fix='Structural Deformation',
               situation='case',
               x_ticks=False,
               with_fracture=False,
               title_position='exterior'):
     
    print('')
    print('-- Individual')
    print('-> '+post_fix)

    #global shape of progress or integral analysis
    global_shape=which_progress.shape 
    
    #new picture and ax
    figure=C_G_P.FigureForSeriesAndIndividual(global_shape)
        
    #new picture and ax
    plt.subplot()

    if post_fix=='Structural Deformation':
        
        IndividualStructuralDeformation(which_progress=which_progress,
                                        x_ticks=x_ticks,
                                        with_fracture=with_fracture,
                                        with_annotation=True,
                                        with_title=True)
    else:
        
        this_ax_img=IndividualCloudImage(which_progress=which_progress,
                                         post_fix=post_fix,
                                         x_ticks=x_ticks,
                                         with_fracture=with_fracture,
                                         with_annotation=True,
                                         with_title=True)

    #set global axis
    O_D.AxisLimit(output_folder,-which_progress.offset,global_shape)
    
    '''global shape would change the scale of axes'''
    #colorbar position of stress and strain 
    if post_fix!='Structural Deformation':
    
        O_C.SetColorbar(which_progress,post_fix,this_ax_img)
            
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