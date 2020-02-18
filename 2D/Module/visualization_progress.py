# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:37:12 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Progress Operation
"""

from o_progress import progress

import visualization_individual as V_I
import visualization_integral_analysis as V_I_A

#------------------------------------------------------------------------------   
"""
Construct a progress object

Args:
   progress_path: path to construct
   lite: (bool) whether only structural deformation (defualt: True)
   
Returns:
    progress object
""" 
def ProgressConstruction(progress_path,lite=True):
    
    print('')
    print('-- Progress Construction')
    
    #construct a progress object
    that_progress=progress()
    
    that_progress.InitVisualization(progress_path,lite)
    
    print('-> progress='+that_progress.percentage)
    
    return that_progress

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
def ProgressAllIndividuals(output_folder,
                           which_progress,
                           with_fracture=False):  
    
    print('')
    print('-- Progress All Individuals')
    print('-> progress='+which_progress.percentage)
    
    list_post_fix=['Structural Deformation',
                   'Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
    
    list_title=['Structural Deformation',
                'Mean Normal Stress',
                'Maximal Shear Stress',
                'Volumetric Strain-Cumulative',
                'Distortional Strain-Cumulative',
                'Resultant Velocity',
                'Resultant Displacement-Cumulative',
                'Volumetric Strain-Instantaneous',
                'Distortional Strain-Instantaneous']
    
    #plot all postfix mode
    for this_post_fix in list_title:
        
        V_I.Individual(output_folder,
                       which_progress,
                       this_post_fix,
                       with_fracture,
                       situation='progress')
        
#------------------------------------------------------------------------------   
"""
Construct a progress object and post processing

Args:
   progress_path: path to construct
   output_folder: folder to contain result
   with_farcture: (bool) plot fracture and interface or not 
   
Returns:
    None
""" 
def ProgressVisualization(progress_path,output_folder,with_fracture=False):
    
    print('')
    print('-- Progress Visualization')
    
    #construct a progress
    that_progress=ProgressConstruction(progress_path)
    
    #output folder of this progress
    progress_folder=output_folder+'\\'+that_progress.percentage
    
    #imaging and output
    ProgressAllIndividuals(progress_folder,that_progress,with_fracture)
    
    #integral analysis
    for this_mode in ['standard','all']:
        
        V_I_A.SingleIntegralAnalysis(output_folder,
                                     that_progress,
                                     this_mode,
                                     with_fracture,
                                     situation='progress')