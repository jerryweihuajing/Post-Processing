# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:49:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Progress plot
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import Path as Pa
import Image as Img
import Matrix as Mat
import Global as Glo
import NewPath as NP
import Decoration as Dec
import ImageSmoothing as ISm
import HPC_IntegralAnalysisPlot as HPC_IAP

#------------------------------------------------------------------------------
"""
Plot single structural deformation in different progress with fracture

Args:
    which_progress: progress object
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: plot progress proportion

Returns:
    None
"""
def SingleStructuralDeformationInProgress(which_progress,
                                          subplot_ax,
                                          with_fracture=False,
                                          with_annotation=True):
    print('')
    print('-- Structural Deformation')

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
        annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)
        
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)

       
#------------------------------------------------------------------------------
"""
Plot structural deformation progress

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def ProgressStructuralDeformation(output_folder,
                                  which_case,
                                  with_fracture=False):
    
    print('')
    print('-- Progress Structural Deformation')
    
    #global shape of progress or integral analysis
    global_shape=which_case.list_progress[-1].shape 
    
    #new picture and ax
    #100-1000
    if global_shape==(100,1000):
        
        figure=plt.subplots(figsize=(13,13))[0]
        
    #100-500
    if global_shape==(100,500):
    
        figure=plt.subplots(figsize=(7,13))[0]

    #subplot index
    index=0
    
    for this_progress in which_case.list_progress:
              
        #iter
        index+=1
        
        this_ax=plt.subplot(len(which_case.list_progress),1,index)
 
        SingleStructuralDeformationInProgress(this_progress,
                                              this_ax,
                                              with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
 
    #figure name
    fig_name='Sturctural Deformation'
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
       
    #animation folder path
    progress_folder=output_folder+'\\progress\\'
    
    Pa.GenerateFolder(progress_folder)
    
    #save this fig
    figure.savefig(progress_folder+fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture

Args:
    which_progress: progress object
    post_fix: post fix of txt file
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: plot progress proportion

Returns:
    None
"""
def SingleStressOrStrainInProgress(which_progress,
                                   post_fix,
                                   subplot_ax,
                                   with_fracture=False,
                                   with_annotation=True):
    print('')
    print('-- '+post_fix)

    #percentage of progress
    progress_percentage=which_progress.percentage
    
    print('-> progress='+progress_percentage)
    
    #stress or strain value matrix to be plotted
    value_matrix=ISm.ImageSmooth((which_progress.stress_or_strain[post_fix]))

    #outline matrix
    outline_matrix=which_progress.outline

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    if which_progress.case==None:
        
        print('--> Local Norm')
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=GlobalColormap(post_fix))
        
    else:
        
        print('--> Global Norm')
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=GlobalColormap(post_fix),
                   norm=GlobalNorm(which_progress.case,post_fix))
    
    #plot outline
    plt.imshow(outline_matrix,cmap='gray')
    
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
        annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)
    
        subplot_ax.annotate(progress_percentage,
                            xy=(0,0),
                            xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                            fontproperties=annotation_font)
        
#------------------------------------------------------------------------------
"""
Plot stress or strain progress

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    post_fix: post fix of txt file
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def ProgressStressOrStrain(output_folder,
                           which_case,
                           post_fix,
                           with_fracture=False):
    
    print('')
    print('-- Progress Structural Deformation')
    
    #global shape of progress or integral analysis
    global_shape=which_case.list_progress[-1].shape 
    
    #new picture and ax
    #100-1000
    if global_shape==(100,1000):
        
        figure=plt.subplots(figsize=(13,13))[0]
        
    #100-500
    if global_shape==(100,500):
    
        figure=plt.subplots(figsize=(7,13))[0]

    #subplot index
    index=0

    for this_progress in which_case.list_progress:
              
        #iter
        index+=1
        
        this_ax=plt.subplot(len(which_case.list_progress),1,index)
        
        SingleStressOrStrainInProgress(this_progress,
                                       post_fix,
                                       this_ax,
                                       with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
  
    #figure name
    fig_name=post_fix
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
       
    #animation folder path
    progress_folder=output_folder+'\\progress\\'
    
    Pa.GenerateFolder(progress_folder)
    
    #save this fig
    figure.savefig(progress_folder+fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot all progress

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def ProgressAll(output_folder,
                which_case,
                with_fracture=False):

    print('')
    print('-- Progress Plot')
    
    #strucural deformation
    ProgressStructuralDeformation(output_folder,which_case,with_fracture)
    
    list_post_fix=['Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Periodical Volumetric Strain',
                   'Periodical Distortional Strain',
                   'Cumulative Volumetric Strain',
                   'Cumulative Distortional Strain']
    
    #stress and strain progress
    for this_post_fix in list_post_fix:        
        
        ProgressStressOrStrain(output_folder,which_case,this_post_fix)