# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:52:05 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Integral Analysis in a progress
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import operation_path as O_P

import visualization_animation as V_A
import visualization_individual as V_I

#------------------------------------------------------------------------------
"""
Plot integral analysis of a progress

Args:
    output_folder: folder to contain result
    which_progress: progress object
    mode: 'standard' 'all'
    with_farcture: (bool) plot fracture and interface or not 
    situation: for 'case' or 'progress'

Returns:
    Figure path
"""
def SingleIntegralAnalysis(output_folder,
                           which_progress,
                           mode='standard',
                           with_fracture=False,
                           situation='case'):
    
    print('')
    print('-- Single Integral Analysis In Progress')
    print('-> progress='+which_progress.percentage)
    
    #title font
    title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
    #annotation font
    annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)
    
    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    if mode=='standard':
    
        list_post_fix=['Structural Deformation',
                       'Mean Normal Stress',
                       'Maximal Shear Stress',
                       'Volumetric Strain-Cumulative',
                       'Distortional Strain-Cumulative']

        #new picture and ax
        #100-1000
        if global_shape==(100,1000):
            
            figure=plt.subplots(figsize=(13,9))[0]
            
        #100-500
        if global_shape==(100,500):
        
            figure=plt.subplots(figsize=(7,9))[0]
    
        #100-200
        if global_shape==(100,350):
        
            figure=plt.subplots(figsize=(5,9))[0]
            
    if mode=='all':
        
        list_post_fix=['Structural Deformation',
                       'Mean Normal Stress',
                       'Maximal Shear Stress',
                       'Volumetric Strain-Cumulative',
                       'Distortional Strain-Cumulative'
                       'Volumetric Strain-Periodical',
                       'Distortional Strain-Periodical']
    
        #new picture and ax
        #100-1000
        if global_shape==(100,1000):
            
            figure=plt.subplots(figsize=(13,14))[0]
        
        #100-500
        if global_shape==(100,500):
            
            figure=plt.subplots(figsize=(7,14))[0]
            
        #100-200
        if global_shape==(100,350):
            
            figure=plt.subplots(figsize=(5,14))[0]
     
    #shape of this img
    this_shape=np.shape(which_progress.fracture)
    
    #subplot index
    index=0
    
    for this_post_fix in list_post_fix:
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(list_post_fix),1,index)
        
        if this_post_fix=='Structural Deformation':
            
            #structural deformation
            V_I.IndividualStructuralDeformation(which_progress,this_ax)

        else:
                  
            #stress and strain
            V_I.IndividualStressOrStrain(which_progress,this_post_fix,this_ax)    
        
        '''double'''
        plus_offset=-which_progress.offset
        
        if 'double' in output_folder:
            
            if 'diff' in output_folder:
                
                plus_offset-=50
                
            else:
                
                plus_offset-=80
        
        this_ax.axis([plus_offset,plus_offset+global_shape[1]*1.13,0,global_shape[0]])
        
        #sub annotation
        this_ax.annotate(which_progress.percentage,
                         xy=(0,0),
                         xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                         fontproperties=annotation_font)
    
        #sub title
        this_ax.annotate(this_post_fix,
                         xy=(0,0),
                         xytext=(plus_offset,1.023*global_shape[0]),
                         fontproperties=title_font)
     
    #figure path and name    
    if situation=='case':
        
        integral_analysis_folder=output_folder+'\\integral analysis\\'
        fig_name=which_progress.percentage
        
    if situation=='progress':

        integral_analysis_folder=output_folder+'\\'+which_progress.percentage+'\\'
        fig_name='integral analysis'
        
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'    
        
    #generate folder
    O_P.GenerateFolder(integral_analysis_folder)
    
    #figure path
    fig_path=integral_analysis_folder+fig_name+' ('+mode+').png'
    
    #save this fig
    figure.savefig(fig_path,dpi=300,bbox_inches='tight')
        
    plt.close()
    
    return fig_path

#------------------------------------------------------------------------------
"""
Plot all integral analysis

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""   
def IntegralAnalysisAll(output_folder,
                        which_case,
                        with_fracture=False):
    
    print('')
    print('-- Integral Analysis Plot')
    
    #integral analysis
    list_mode=['standard','all'][:1]
    
    for this_mode in list_mode:
        
        V_A.AnimationIntegralAnalysis(output_folder,
                                      which_case,
                                      this_mode,
                                      with_fracture)