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
import matplotlib.font_manager as fm

import operation_path as O_P
import operation_decoration as O_D

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_global_parameter as C_G_P

#------------------------------------------------------------------------------
"""
Plot single structural deformation in different progress with fracture (do not save)

Args:
    which_progress: progress object
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: (bool) plot progress proportion
    with_title: (bool) plot title which stands for postfix

Returns:
    None
"""
def IndividualStructuralDeformation(which_progress,
                                    subplot_ax,
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

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(which_progress.img_tag)
    
    #plot main body
    plt.imshow(structural_deformation_img_rgb)

    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(C_M.MatrixFilter(fracture_matrix,-1,1,show=True)) is bool:
            
            print('=> WARNING: without fracture')

    #decoration  
    O_D.TicksAndSpines(subplot_ax,1,1)
    O_D.TicksConfiguration(subplot_ax)

    #sub annotation
    if with_annotation:
        
        #annotation font
        annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)
        
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)

    #sub title
    if with_title:
        
        #title font
        title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
        subplot_ax.annotate('Structural Deformation',
                            xy=(0,0),
                            xytext=(0,1.023*global_shape[0]),
                            fontproperties=title_font)
        
#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture (do not save)

Args:
    which_progress: progress object
    post_fix: post fix of txt file
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: (bool) plot progress proportion
    with_title: (bool) plot title which stands for postfix
    
Returns:
    None
"""
def IndividualStressOrStrain(which_progress,
                             post_fix,
                             subplot_ax,
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
        
        plt.imshow(C_I.ImgFlip(value_matrix,0),
                   cmap=C_G_P.GlobalColormap(post_fix))
        
    else:
        
        print('--> Global Norm')
        
        plt.imshow(C_I.ImgFlip(value_matrix,0),
                   cmap=C_G_P.GlobalColormap(post_fix),
                   norm=C_G_P.GlobalNorm(which_progress.case,post_fix))
        
    plt.imshow(np.flip(outline_matrix,0),cmap='gray')
    
    #plot outline
    if 'Stress' in post_fix:
        
        with_fracture=True
        
    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(C_M.MatrixFilter(fracture_matrix,-1,1,show=True)) is bool:
            
            print('==> WARNING: without fracture')
            
    #decoration  
    O_D.TicksAndSpines(subplot_ax,1,1)
    O_D.TicksConfiguration(subplot_ax)
    
    #sub annotation
    if with_annotation:
        
        #annotation font
        annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)
    
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)
        
    #sub title
    if with_title:
        
        #title font
        title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
        subplot_ax.annotate(post_fix,
                            xy=(0,0),
                            xytext=(0,1.023*global_shape[0]),
                            fontproperties=title_font)
        
#------------------------------------------------------------------------------
"""
Plot single figure

Args:
    output_folder: folder to contain result
    which_progress: progress object
    post_fix: post fix of txt file
    with_fracture: (bool) plot fracture or not 
    situation: for 'case' or 'progress'

Returns:
    None
"""        
def Individual(output_folder,
               which_progress,
               post_fix='Structural Deformation',
               with_fracture=False,
               situation='case'):
     
    print('')
    print('-- Single Individual In Progress')
    print('-> '+post_fix)

    #global shape of progress or integral analysis
    global_shape=which_progress.shape 
    
    #100-1000
    if global_shape==(100,1000):
        
        figure=plt.subplots(figsize=(13,13))[0]
        
    #100-500
    if global_shape==(100,500):
    
        figure=plt.subplots(figsize=(7,13))[0]

    #100-500
    if global_shape==(100,350):
    
        figure=plt.subplots(figsize=(5,13))[0]
        
    #new picture and ax
    this_ax=plt.subplot()

    if post_fix=='Structural Deformation':
        
        IndividualStructuralDeformation(which_progress,this_ax,with_fracture,1,1)  
        
    else:
           
        IndividualStressOrStrain(which_progress,post_fix,this_ax,with_fracture,1,1)

    this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
    
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