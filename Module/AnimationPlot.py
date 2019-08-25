# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 22:29:18 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Animation of a progress
"""

import imageio
import matplotlib.pyplot as plt

import Path as Pa
import Global as Glo
import NewPath as NP
import ProgressPlot as PP
import IntegralAnalysisPlot as IAP

#------------------------------------------------------------------------------
"""
Plot progress integral analysis animation

Args:
    case_path: load path of case
    mode: 'standard' 'all'
    with_fracture: (bool) plot fracture or not 

Returns:
    None
"""
def AnimationIntegralAnalysis(case_path,mode='standard',with_fracture=True):
    
    print('')
    print('-- Animation Integral Analysis')
    
    folder_path=case_path+'\\structural deformation\\values'

    #figures to generate GIF
    figures=[]
    
    for this_file_name in NP.FileNamesThisCase(folder_path):
        
        #join file path
        this_file_path=folder_path+'\\'+this_file_name
        
        #path of integral analysis figure
        this_fig_path=IAP.SingleIntegralAnalysisInProgress(this_file_path,mode,with_fracture)

        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
        #GIF name
        gif_name='integral analysis'
        
        #re-name
        if with_fracture:
            
            gif_name+=' with fracture'

        #animation folder path
        animation_folder=case_path+'\\animation\\'
        
        Pa.GenerateFolder(animation_folder)
        
    #save GIF
    imageio.mimsave(animation_folder+gif_name+' ('+mode+').gif',figures,duration=0.5)

#------------------------------------------------------------------------------
"""
Plot progress individual animation

Args:
    case_path: load path of case
    post_fix: post fix of txt file (default: structural deformation)
    with_fracture: (bool) plot fracture or not 

Returns:
    None
"""   
def AnimationIndividual(case_path,post_fix='structural deformation',with_fracture=True):
    
    print('')
    print('-- Animation Individual')
    print('-> '+IAP.PostFix2Title(post_fix).strip())
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #figures to generate GIF
    figures=[]
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)

    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
        
        #new picture and ax
        this_figure=plt.subplots(figsize=(13,11))[0]
        this_ax=plt.subplot()
    
        #calculate global norm
        global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)
        
        if post_fix=='structural deformation':
            
            PP.SingleStructuralDeformationInProgress(structural_deformation_path,
                                                     this_ax,
                                                     with_fracture)
            
        else:
               
            PP.SingleStressOrStrainInProgress(structural_deformation_path,
                                              post_fix,
                                              this_ax,
                                              with_fracture)
    
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
        
        #percentage of progress
        fig_name=PP.ProgressPercentageFromTXT(structural_deformation_path)
        
        #re-name
        if with_fracture:
            
            fig_name+=' with fracture'
            
        #output path of this fig
        this_fig_path=case_path+'\\'+post_fix+'\\'+fig_name+'.png'
        
        #save this fig
        this_figure.savefig(this_fig_path,dpi=300,bbox_inches='tight')
        
        #collect fig to create GIF
        figures.append(imageio.imread(this_fig_path))
        
        plt.close()
        
    #GIF name
    gif_name=IAP.PostFix2Title(post_fix)
    
    #re-name
    if with_fracture:
        
        gif_name+=' with fracture'

    #animation folder path
    animation_folder=case_path+'\\animation\\'
    
    Pa.GenerateFolder(animation_folder)    
    
    #save GIF
    imageio.mimsave(animation_folder+gif_name+'.gif',figures,duration=0.5)
    
#------------------------------------------------------------------------------
"""
Plot all animations

Args:
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    mass of GIFs in output folder
"""    
def AnimationAll(case_path,with_fracture=True):
    
    print('')
    print('--Animation Analysis Plot')
    
    #all individuals
    list_post_fix=['structural deformation',
                   'stress\\mean normal',
                   'stress\\maximal shear',
                   'periodical strain\\volumetric',
                   'periodical strain\\distortional',
                   'cumulative strain\\volumetric',
                   'cumulative strain\\distortional']
        
    for this_post_fix in list_post_fix:
        
        AnimationIndividual(case_path,this_post_fix,with_fracture)