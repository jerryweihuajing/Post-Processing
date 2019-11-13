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
Calculate progress percentage from file path

Args:
    file_path: load path of research case
    
Returns:
    percentage of progress
"""
def ProgressPercentageFromTXT(file_path):
    
    #where is the %
    percentage_index=file_path.index('%')
    
    #start char
    start_char=file_path[percentage_index-5]
    
    if start_char=='\\':
        
        return file_path[percentage_index-4:percentage_index+1]
    
    else:
        
        return file_path[percentage_index-5:percentage_index+1]

#------------------------------------------------------------------------------
"""
Plot structural deformation progress

Args:
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def ProgressStructuralDeformation(case_path,with_fracture=True):
    
    print('')
    print('-- Progress Structural Deformation')
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)

    #new picture and ax
    #100-1000
    if '100-1000' in case_path:
        
        figure=plt.subplots(figsize=(13,13))[0]
        
    #100-500
    if '100-500' in case_path:
    
        figure=plt.subplots(figsize=(7,13))[0]
    
    #subplot index
    index=0
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(file_names),1,index)
 
        #calculate global norm
        global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

        #decoration     
        SingleStructuralDeformationInProgress(structural_deformation_path,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
 
    #figure name
    fig_name='Sturctural Deformation'
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
       
    #animation folder path
    progress_folder=case_path+'\\progress\\'
    
    Pa.GenerateFolder(progress_folder)
    
    #save this fig
    figure.savefig(progress_folder+fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture

Args:
    file_path: load path of txt file
    post_fix: post fix of txt file
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: plot progress proportion

Returns:
    None
"""
def SingleStressOrStrainInProgress(structural_deformation_path,
                                   post_fix,
                                   subplot_ax,
                                   with_fracture=True,
                                   with_annotation=True):
    print('')
    print('-- '+IAP.PostFix2Title(post_fix).strip())
    
    #percentage of progress
    progress_percentage=ProgressPercentageFromTXT(structural_deformation_path)
    
    print('-> progress='+progress_percentage)
    
    #stress and strain itself
    file_path=structural_deformation_path.replace('structural deformation',post_fix)
    
    #plot fracture
    fracture_file_path=structural_deformation_path.replace('structural deformation','cumulative strain\\distortional')
    
    #fracture matrix and smooth
    fracture_matrix=ISm.ImageSmooth(Mat.ImportMatrixFromTXT(fracture_file_path))

    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #show image    
    Mat.DisplayImageFromTXT(file_path,1,1)
    
    #show outline
    Mat.DisplayOutlineFromTXT(file_path,1)
    
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
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def ProgressStressOrStrain(case_path,post_fix,with_fracture=True):
    
    print('')
    print('-- Progress Stress Or Strain')
    print('-> '+IAP.PostFix2Title(post_fix).strip())
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)
    
    #new picture and ax
    #100-1000
    if '100-1000' in case_path:
        
        figure=plt.subplots(figsize=(13,13))[0]
        
    #100-500
    if '100-500' in case_path:
    
        figure=plt.subplots(figsize=(7,13))[0]
            
    #subplot index
    index=0
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(file_names),1,index)
 
        #calculate global norm
        global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

        #decoration     
        SingleStressOrStrainInProgress(structural_deformation_path,post_fix,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
        
    #figure name
    fig_name=IAP.PostFix2Title(post_fix)
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    #animation folder path
    progress_folder=case_path+'\\progress\\'
    
    Pa.GenerateFolder(progress_folder)
    
    #save this fig
    figure.savefig(progress_folder+fig_name+'.png',dpi=300,bbox_inches='tight')
    
    plt.close()
    
#------------------------------------------------------------------------------
"""
Plot all progress

Args:
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    mass of PNGs in output folder
"""
def ProgressAll(case_path,with_fracture=True):

    print('')
    print('-- Progress Plot')
    
    #strucural deformation
    ProgressStructuralDeformation(case_path,with_fracture)
    
    list_post_fix=['stress\\mean normal',
                   'stress\\maximal shear',
                   'periodical strain\\volumetric',
                   'periodical strain\\distortional',
                   'cumulative strain\\volumetric',
                   'cumulative strain\\distortional']

    #stress and strain progress
    for this_post_fix in list_post_fix:        
    
        ProgressStressOrStrain(case_path,this_post_fix,with_fracture)