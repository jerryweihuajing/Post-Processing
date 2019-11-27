# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:53:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Animation of a progress
"""

import imageio
import matplotlib.pyplot as plt

import Path as Pa

import HPC_IndividualPlot as HPC_IP
import HPC_IntegralAnalysisPlot as HPC_IAP

#------------------------------------------------------------------------------
"""
Plot progress integral analysis animation

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    mode: 'standard' 'all'
    with_fracture: (bool) plot fracture or not 

Returns:
    None
"""
def AnimationIntegralAnalysis(output_folder,
                              which_case,
                              mode='standard',
                              with_fracture=False):
    
    print('')
    print('-- Animation Integral Analysis')

    #figures to generate GIF
    figures=[]
    
    for this_progress in which_case.list_progress:
        
        #path of integral analysis figure
        this_fig_path=HPC_IAP.SingleIntegralAnalysisInProgress(output_folder,this_progress)

        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    #GIF name
    gif_name='integral analysis'
    
    #re-name
    if with_fracture:
        
        gif_name+=' with fracture'

    #animation folder path
    animation_folder=output_folder+'\\animation\\'
    
    Pa.GenerateFolder(animation_folder)
        
    #save GIF
    imageio.mimsave(animation_folder+gif_name+' ('+mode+').gif',figures,duration=0.5)

#------------------------------------------------------------------------------
"""
Plot progress individual animation

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    post_fix: post fix of txt file (default: structural deformation)
    with_fracture: (bool) plot fracture or not 

Returns:
    None
"""   
def AnimationIndividual(output_folder,
                        which_case,
                        post_fix='Structural Deformation',
                        with_fracture=False):
    
    print('')
    print('-- Animation Individual')
    print('-> '+post_fix)
    
    #figures to generate GIF
    figures=[]
       
    #global shape of progress or integral analysis
    global_shape=which_case.list_progress[-1].shape 

    #animation folder path
    post_fix_folder=output_folder+'\\'+post_fix+'\\'
    
    #Generate folder of output figures
    Pa.GenerateFolder(post_fix_folder)
    
    for this_progress in which_case.list_progress:
        
        #100-1000
        if global_shape==(100,1000):
            
            this_figure=plt.subplots(figsize=(13,13))[0]
            
        #100-500
        if global_shape==(100,500):
        
            this_figure=plt.subplots(figsize=(7,13))[0]

        #new picture and ax
        this_ax=plt.subplot()

        if post_fix=='Structural Deformation':
            
            HPC_IP.IndividualStructuralDeformationInProgress(this_progress,this_ax,with_fracture,1,1)  
            
        else:
               
            HPC_IP.IndividualStressOrStrainInProgress(this_progress,post_fix,this_ax,with_fracture,1,1)
    
        this_ax.axis([0,global_shape[1]*1.13,0,global_shape[0]])
        
        #percentage of progress
        fig_name=this_progress.percentage
        
        #re-name
        if with_fracture:
            
            fig_name+=' with fracture'
            
        #path of this figure
        this_fig_path=post_fix_folder+fig_name+'.png'
        
        #save this fig
        this_figure.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        
        plt.close()
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))    
        
    #GIF name
    gif_name=post_fix
    
    #re-name
    if with_fracture:
        
        gif_name+=' with fracture'

    #animation folder path
    animation_folder=output_folder+'\\animation\\'
    
    #Generate folder of output figures
    Pa.GenerateFolder(animation_folder)    
    
    #save GIF
    imageio.mimsave(animation_folder+gif_name+'.gif',figures,duration=0.5)
    
#------------------------------------------------------------------------------
"""
Plot all animations

Args:
    output_folder: folder to contain result
    which_case: case object to be proccessed
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""    
def AnimationAll(output_folder,
                 which_case,
                 with_fracture=False):
    
    print('')
    print('--Animation Analysis Plot')
    
    #structural deformation
    AnimationIndividual(output_folder,which_case)
    
    #all individuals
    list_stress_or_strain=['Mean Normal Stress',
                           'Maximal Shear Stress',
                           'Periodical Volumetric Strain',
                           'Periodical Distortional Strain',
                           'Cumulative Volumetric Strain',
                           'Cumulative Distortional Strain']
        
    #stress and strain
    for this_post_fix in list_stress_or_strain:
        
        AnimationIndividual(output_folder,which_case,this_post_fix)