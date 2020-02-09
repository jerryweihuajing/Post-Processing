# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:53:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Animation of a progress
"""

import imageio

import operation_path as O_P

import visualization_individual as V_I
import visualization_integral_analysis as V_I_A

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
        this_fig_path=V_I_A.SingleIntegralAnalysis(output_folder,this_progress,mode,with_fracture)

        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
    #GIF name
    gif_name='integral analysis'
    
    #re-name
    if with_fracture:
        
        gif_name+=' with fracture'

    #animation folder path
    animation_folder=output_folder+'\\animation\\'
    
    O_P.GenerateFolder(animation_folder)
        
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

    #animation folder path
    post_fix_folder=output_folder+'\\'+post_fix+'\\'
    
    #Generate folder of output figures
    O_P.GenerateFolder(post_fix_folder)
    
    for this_progress in which_case.list_progress:
        
        this_fig_path=V_I.Individual(output_folder,this_progress,post_fix,with_fracture)
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))    
        
    #animation folder path
    animation_folder=output_folder+'\\animation\\'
    post_fix_folder=output_folder+'\\'+post_fix+'\\'
    
    #Generate folder of output figures
    O_P.GenerateFolder(animation_folder)    
    O_P.GenerateFolder(animation_folder) 
    #GIF name
    animation_gif_name=post_fix
    post_fix_gif_name='animation'
    
    #re-name
    if with_fracture:
        
        animation_gif_name+=' with fracture'
        post_fix_gif_name+=' with fracture'
        
    #save GIF
    imageio.mimsave(animation_folder+animation_gif_name+'.gif',figures,duration=0.5)
    imageio.mimsave(post_fix_folder+post_fix_gif_name+'.gif',figures,duration=0.5)
    
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
    print('-- Animation Analysis Plot')

    #all individuals
    list_post_fix=['Structural Deformation',
                   'Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
        
    #stress and strain
    for this_post_fix in list_post_fix:
        
        AnimationIndividual(output_folder,which_case,this_post_fix,with_fracture)