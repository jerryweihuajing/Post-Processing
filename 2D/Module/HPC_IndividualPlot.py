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

import operation_path_v1 as O_P_1
import Image as Img
import Matrix as Mat
import Decoration as Dec

import HPC_Global as HPC_Glo

#------------------------------------------------------------------------------
"""
Plot single structural deformation in different progress with fracture

Args:
    which_progress: progress object
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: (bool) plot progress proportion
    with_title: (bool) plot title which stands for postfix

Returns:
    None
"""
def IndividualStructuralDeformationInProgress(which_progress,
                                              subplot_ax,
                                              with_fracture=False,
                                              with_annotation=True,
                                              with_title=False):
    print('')
    print('-- Structural Deformation')

    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    #percentage of progress
    progress_percentage=which_progress.percentage
    
    print('-> progress='+progress_percentage)

    #transform to RGB format
    structural_deformation_img_rgb=which_progress.structural_deformation

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    plt.imshow(structural_deformation_img_rgb)

    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(Mat.MatrixFilter(fracture_matrix,0.23,1,show=True)) is bool:
            
            print('=> WARNING: without fracture')
                           
    '''revision'''
    #decoration  
    Dec.TicksAndSpines(subplot_ax,1,1)
    Dec.TicksConfiguration(subplot_ax)
    
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
Plot single stress of strain in different progress with fracture

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
def IndividualStressOrStrainInProgress(which_progress,
                                       post_fix,
                                       subplot_ax,
                                       with_fracture=False,
                                       with_annotation=True,
                                       with_title=False):
    print('')
    print('-- '+post_fix)

    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    #percentage of progress
    progress_percentage=which_progress.percentage
    
    print('-> progress='+progress_percentage)
    
    #stress or strain value matrix to be plotted
    value_matrix=which_progress.stress_or_strain[post_fix]

    #outline matrix
    outline_stress=which_progress.outline_stress
    outline_strain=which_progress.outline_strain

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    if which_progress.case==None:
        
        print('--> Local Norm')
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=HPC_Glo.GlobalColormap(post_fix))
        
    else:
        
        print('--> Global Norm')
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=HPC_Glo.GlobalColormap(post_fix),
                   norm=HPC_Glo.GlobalNorm(which_progress.case,post_fix))
    
    #plot outline
    if 'Stress' in post_fix:
        
        plt.imshow(outline_stress,cmap='gray')
    
    if 'Strain' in post_fix:
        
        plt.imshow(outline_strain,cmap='gray')
        
    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(Mat.MatrixFilter(fracture_matrix,0.23,1,show=True)) is bool:
            
            print('==>WARNING: without fracture')
            
    '''revision'''
    #decoration  
    Dec.TicksAndSpines(subplot_ax,1,1)
    Dec.TicksConfiguration(subplot_ax)
    
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
    
Returns:
    None
"""        
def IndividualInProgress(output_folder,
                         which_progress,
                         post_fix='Structural Deformation',
                         with_fracture=False):
     
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

    #new picture and ax
    this_ax=plt.subplot()

    if post_fix=='Structural Deformation':
        
        IndividualStructuralDeformationInProgress(which_progress,this_ax,with_fracture,1,1)  
        
    else:
           
        IndividualStressOrStrainInProgress(which_progress,post_fix,this_ax,with_fracture,1,1)

    this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
    
    #percentage of progress
    fig_name=post_fix
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    #generate folder
    O_P_1.GenerateFolder(output_folder)
    
    #path of this figure
    this_fig_path=output_folder+'\\'+fig_name+'.png'
    
    #save this fig
    figure.savefig(this_fig_path,dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot single figure

Args:
    output_folder: folder to contain result
    which_progress: progress object
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""     
def AllIndividualsInProgress(output_folder,
                             which_progress,
                             with_fracture=False):  
    
    list_post_fix=['Structural Deformation',
                   'Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
    
    #plot all postfix mode
    for this_post_fix in list_post_fix:
        
        IndividualInProgress(output_folder,which_progress,this_post_fix,with_fracture)