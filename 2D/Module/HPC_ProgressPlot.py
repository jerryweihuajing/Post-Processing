# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:49:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Progress plot
"""

import matplotlib.pyplot as plt

import Path as Pa

import HPC_IndividualPlot as HPC_IP

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
 
        HPC_IP.IndividualStructuralDeformationInProgress(this_progress,this_ax,with_fracture)
        
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
        
        HPC_IP.IndividualStressOrStrainInProgress(this_progress,post_fix,this_ax,with_fracture)
        
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
                   'Volumetric Strain (Periodical)',
                   'Distortional Strain (Periodical)',
                   'Volumetric Strain (Cumulative)',
                   'Distortional Strain (Cumulative)']
    
    #stress and strain progress
    for this_post_fix in list_post_fix:        
        
        ProgressStressOrStrain(output_folder,which_case,this_post_fix)