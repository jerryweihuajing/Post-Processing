# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:52:05 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Integral Analysis in a progress
"""

import matplotlib.pyplot as plt

import operation_path as O_P
import operation_colorbar as O_C
import operation_decoration as O_D

import visualization_animation as V_A
import visualization_individual as V_I

import calculation_global_parameter as C_G_P

from configuration_list_title import map_post_fix_list

#------------------------------------------------------------------------------
"""
Plot integral analysis of a progress

Args:
    output_folder: folder to contain result
    which_progress: progress object
    mode: mode for integral analysis ['standard' 'all']
    situation: mode for visualization ['case','progress']
    with_farcture: (bool) plot fracture and interface or not (default: False)
    
Returns:
    Figure path
"""
def SingleIntegralAnalysis(output_folder,
                           which_progress,
                           mode='dynamics',
                           situation='case',
                           with_fracture=False):
    
    print('')
    print('-- Single Integral Analysis')
    print('-> progress='+which_progress.percentage)
    print('-> mode:',mode)
    
    #from configuration
    list_post_fix=map_post_fix_list[mode]
    
    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    #new picture and ax
    figure=C_G_P.FigureForIntegralAnalysis(global_shape,mode)
     
    #subplot index
    index=0
    
    #whether to plot x ticks
    x_ticks=False
    
    for this_post_fix in list_post_fix:
        
        #iter
        index+=1
        
        #only the last one need it
        if index==len(list_post_fix):
            
            x_ticks=True
            
        plt.subplot(len(list_post_fix),1,index)
        
        if this_post_fix=='Structural Deformation':
            
            #structural deformation
            V_I.IndividualStructuralDeformation(which_progress,
                                                x_ticks,
                                                with_annotation=True,
                                                with_title=True)

        else:
                  
            #stress and strain
            this_ax_img=V_I.IndividualCloudImage(which_progress,
                                                 this_post_fix,
                                                 x_ticks=x_ticks,
                                                 with_annotation=True,
                                                 with_title=True)    
            
        #set global axis
        O_D.AxisLimit(output_folder,-which_progress.offset,global_shape)
            
        '''global shape would change the scale of axes'''
        #colorbar position of stress and strain 
        if this_post_fix!='Structural Deformation':
        
            O_C.SetColorbar(which_progress,this_post_fix,this_ax_img)
        
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
    with_fracture: (bool) plot fracture or not (default: False)
    
Returns:
    None
"""   
def IntegralAnalysisAll(output_folder,
                        which_case,
                        with_fracture=False):
    
    print('')
    print('-- Integral Analysis All')
    
    #integral analysis
    list_mode=['dynamics','kinematics']
    
    for this_mode in list_mode:
        
        V_A.AnimationIntegralAnalysis(output_folder=output_folder,
                                      which_case=which_case,
                                      mode=this_mode,
                                      with_fracture=with_fracture)
