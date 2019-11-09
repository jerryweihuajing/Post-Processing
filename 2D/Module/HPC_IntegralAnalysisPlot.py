# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:52:05 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Integral Analysis in a progress
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import Path as Pa
import Matrix as Mat
import Global as Glo
import HPC_ProgressPlot as HPC_PP
import HPC_AnimationPlot as HPC_AP

#------------------------------------------------------------------------------
"""
Translate file name post fix to title string

Args:
    which_post_fix: post fix of file name 

Returns:
    None
"""
def PostFix2Title(which_post_fix):
    
    temp_str=which_post_fix.split('\\')
    
    #S+C to C+S
    temp_str.reverse()

    #output str
    title_str=''
    
    #strain mode
    if 'strain' in temp_str[-1]:
        
        title_str_list=[temp_str[-1].split(' ')[0],
                        temp_str[0],
                        temp_str[-1].split(' ')[1]]
        
    #stress and deformation    
    else:
        
        title_str_list=temp_str[0].split(' ')+[temp_str[-1]]

    for this_str in title_str_list:
        
        title_str+=' '+this_str[0].upper()+this_str[1:]
       
    return title_str
    
#------------------------------------------------------------------------------
"""
Plot integral analysis of a progress

Args:
    file_path: load path of txt file
    mode: 'standard' 'all'
    with_fracture: (bool) plot fracture or not 

Returns:
    Figure path
"""
def SingleIntegralAnalysisInProgress(file_path,mode='standard',with_fracture=True):
    
    print('')
    print('Single Integral Analysis In Progress')

    #title font
    title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
    #annotation font
    annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)

    #plot structural deformation
    structural_deformation_path=cp.deepcopy(file_path)
    
    #percentage of progress
    progress_percentage=PP.ProgressPercentageFromTXT(file_path) 
    
    #plot fracture
    fracture_file_path=file_path.replace('structural deformation','cumulative strain\\distortional')
    
    #fracture matrix
    fracture_matrix=Mat.ImportMatrixFromTXT(fracture_file_path)
        
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    if mode=='standard':
    
        list_post_fix=['structural deformation',
                       'stress\\mean normal',
                       'stress\\maximal shear',
                       'periodical strain\\volumetric',
                       'periodical strain\\distortional']
    
        #new picture and ax
        #100-1000
        if '100-1000' in file_path:
            
            figure=plt.subplots(figsize=(13,10))[0]
            
        #100-500
        if '100-500' in file_path:
        
            figure=plt.subplots(figsize=(7,10))[0]
    
    if mode=='all':
        
        list_post_fix=['structural deformation',
                       'stress\\mean normal',
                       'stress\\maximal shear',
                       'periodical strain\\volumetric',
                       'cumulative strain\\volumetric',
                       'periodical strain\\distortional',
                       'cumulative strain\\distortional']
    
        #new picture and ax
        #100-1000
        if '100-1000' in file_path:
            
            figure=plt.subplots(figsize=(13,14))[0]
        
        #100-500
        if '100-500' in file_path:
            
            figure=plt.subplots(figsize=(7,14))[0]
        
    #calculate global norm
    global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

    #subplot index
    index=0
    
    for this_post_fix in list_post_fix:
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(list_post_fix),1,index)
        
        #title str
        this_title=PostFix2Title(this_post_fix)
        
        if index==1:
            
            #sturctural deformation   
            PP.SingleStructuralDeformationInProgress(structural_deformation_path,
                                                     this_ax,
                                                     with_fracture,
                                                     0)

        if index>1:
            
            #stress and strain
            PP.SingleStressOrStrainInProgress(structural_deformation_path,
                                              this_post_fix,
                                              this_ax,
                                              with_fracture,
                                              0)
     
        #sub annotation
        this_ax.annotate(progress_percentage,
                         xy=(0,0),
                         xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                         fontproperties=annotation_font)
    
        #sub title
        this_ax.annotate(this_title,
                         xy=(0,0),
                         xytext=(0,1.023*global_shape[0]),
                         fontproperties=title_font)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
     
    #figure name
    fig_name=progress_percentage

    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    output_folder=file_path.split('structural deformation')[0]+'integral analysis\\'
    
    #generate folder
    Pa.GenerateFolder(output_folder)
    
    #figure path
    fig_path=output_folder+fig_name+' ('+mode+').png'
    
    #save this fig
    figure.savefig(fig_path,dpi=300,bbox_inches='tight')
        
    plt.close()
    
    return fig_path

#------------------------------------------------------------------------------
"""
Plot all integral analysis

Args:
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    mass of PNGs, GIFs in output folder
"""    
def IntegralAnalysisAll(case_path,with_fracture=True):
    
    print('')
    print('--Integral Analysis Plot')
    
    #integral analysis
    list_mode=['standard','all']
    
    for this_mode in list_mode:
        
        AP.AnimationIntegralAnalysis(case_path,this_mode,with_fracture)