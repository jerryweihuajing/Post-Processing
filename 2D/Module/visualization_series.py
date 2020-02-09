# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:49:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Progress plot
"""

import matplotlib.pyplot as plt

import operation_path as O_P

import visualization_individual as V_I

#------------------------------------------------------------------------------
"""
Plot structural deformation series

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def SeriesStructuralDeformation(output_folder,
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

    #100-500
    if global_shape==(100,350):
    
        figure=plt.subplots(figsize=(5,13))[0]
        
    #subplot index
    index=0
    
    for this_progress in which_case.list_progress:
              
        #iter
        index+=1
        
        this_ax=plt.subplot(len(which_case.list_progress),1,index)
 
        V_I.IndividualStructuralDeformation(this_progress,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
 
    #animation folder path
    series_folder=output_folder+'\\series\\'
    post_fix_folder=output_folder+'\\Structural Deformation\\'
    
    O_P.GenerateFolder(series_folder)
    O_P.GenerateFolder(post_fix_folder)
    
    #figure name
    series_fig_name='Structural Deformation'
    post_fix_fig_name='series'
    
    #re-name
    if with_fracture:
        
        series_fig_name+=' with fracture'
        series_fig_name+=' with fracture'
    
    #save this fig
    figure.savefig(series_folder+series_fig_name+'.png',dpi=300,bbox_inches='tight')
    figure.savefig(post_fix_folder+post_fix_fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
        
#------------------------------------------------------------------------------
"""
Plot stress or strain series

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    post_fix: post fix of txt file
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def SeriesStressOrStrain(output_folder,
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

    #100-500
    if global_shape==(100,350):
    
        figure=plt.subplots(figsize=(5,13))[0]
        
    #subplot index
    index=0

    for this_progress in which_case.list_progress:
              
        #iter
        index+=1
        
        this_ax=plt.subplot(len(which_case.list_progress),1,index)
        
        V_I.IndividualStressOrStrain(this_progress,post_fix,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
        
    #animation folder path
    series_folder=output_folder+'\\series\\'
    post_fix_folder=output_folder+'\\'+post_fix+'\\'
    
    O_P.GenerateFolder(series_folder)
    O_P.GenerateFolder(post_fix_folder)
    
    #figure name
    series_fig_name=post_fix
    post_fix_fig_name='series'
    
    #re-name
    if with_fracture:
        
        series_fig_name+=' with fracture'
        series_fig_name+=' with fracture'
    
    #save this fig
    figure.savefig(series_folder+series_fig_name+'.png',dpi=300,bbox_inches='tight')
    figure.savefig(post_fix_folder+post_fix_fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot stress or strain series

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    post_fix: post fix of txt file
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def Series(output_folder,
           which_case,
           post_fix,
           with_fracture=False):
    
    if post_fix=='Structural Deformation':
        
        SeriesStructuralDeformation(output_folder,which_case,with_fracture) 
        
    else:
           
        SeriesStressOrStrain(output_folder,which_case,post_fix,with_fracture)
        
#------------------------------------------------------------------------------
"""
Plot all series

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def SeriesAll(output_folder,
              which_case,
              with_fracture=False):

    print('')
    print('-- Progress Plot')
    
    list_post_fix=['Structural Deformation',
                   'Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
    
    #stress and strain progress
    for this_post_fix in list_post_fix:        
        
        Series(output_folder,which_case,this_post_fix)