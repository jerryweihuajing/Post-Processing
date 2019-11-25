# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 23:57:21 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-High Performance Calculation of Plot of an experiment
"""

import os
import imageio

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import Path as Pa
import Decoration as Dec

import HPC_ProgressPlot as HPC_PP
import HPC_AnimationPlot as HPC_AP
import HPC_IntegralAnalysisPlot as HPC_IAP

#------------------------------------------------------------------------------   
"""
Total export depending on mode list of an experiment which contain a branch of cases

Args:
   experiment_path: load path of all input files cases
   
Returns:
    mass of PNGs, TXTs, GIFs in output folder
""" 
def ExperimentPlotAll(experiment_path):
    
    print('')
    print('-- Experiment Plot All')
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        #with and without fracture
        for this_bool in [True,False]:
            
            #plot everything
            HPC_PP.ProgressAll(this_case_path,with_fracture=this_bool)   
            HPC_AP.AnimationAll(this_case_path,with_fracture=this_bool)
            HPC_IAP.IntegralAnalysisAll(this_case_path,with_fracture=this_bool)
            
#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    
    def __init__(self,
                 case=None,
                 shape=None,
                 outline=None,
                 fracture=None,
                 percentage=None,
                 structural_deformation=None,
                 mean_normal_stress=None,
                 maximal_shear_stress=None,
                 periodical_volumrtric_strain=None,
                 periodical_distortional_strain=None,
                 cumulative_volumrtric_strain=None,
                 cumulative_distortional_strain=None,
                 stress_or_strain=None):
        
        self.case=case
        self.shape=shape
        self.outline=outline
        self.fracture=fracture
        self.percentage=percentage
        self.structural_deformation=structural_deformation
        self.mean_normal_stress=mean_normal_stress
        self.maximal_shear_stress=maximal_shear_stress
        self.periodical_volumrtric_strain=periodical_volumrtric_strain
        self.periodical_distortional_strain=periodical_distortional_strain
        self.cumulative_volumrtric_strain=cumulative_volumrtric_strain
        self.cumulative_distortional_strain=cumulative_distortional_strain
        self.stress_or_strain=stress_or_strain
        
#==============================================================================
#object case to manage data efficiently
#==============================================================================    
class case:
    
    def __init__(self,
                 experiment=None,
                 condition=None,
                 list_progress=None):
        
        self.experiment=experiment
        self.condition=condition
        self.list_progress=list_progress

#==============================================================================
#object experiment to manage data efficiently
#==============================================================================     
class experiment:
    
    def __init__(self,
                 parameter=None,
                 list_case=None):
    
        self.parameter=parameter
        self.list_case=list_case
        
import NewPath as NP
import Matrix as Mat
import Image as Img
import ImageSmoothing as ISm

#------------------------------------------------------------------------------   
"""
Construct a progress object

Args:
   structural_deformation_path: path to construct
   
Returns:
    progress object
""" 
def ProgressConstruction(structural_deformation_path):
    
    #construct a progress object
    that_progress=progress()
    
    if '100-500' in structural_deformation_path:
        
        that_progress.shape=(100,500)
        
    if '100-1000' in structural_deformation_path:
        
        that_progress.shape=(100,1000)    
    
    #map between tag and rgb in this case
    rgb_map=Img.MapTagRGB(structural_deformation_path)
    
    #Generate tag image and rgb image
    structural_deformation_img_tag=Mat.ImportMatrixFromTXT(structural_deformation_path)
    
    #transform to RGB format
    structural_deformation_img_rgb=Img.ImageTag2RGB(structural_deformation_img_tag,rgb_map)

    #percentage of progress
    progress_percentage=HPC_PP.ProgressPercentageFromTXT(structural_deformation_path)
    
    #plot fracture
    fracture_file_path=structural_deformation_path.replace('structural deformation','cumulative strain\\distortional')
    
    #fracture matrix
    fracture_matrix=ISm.ImageSmooth(Mat.ImportMatrixFromTXT(fracture_file_path))
    
    list_post_fix=['stress\\mean normal',
                   'stress\\maximal shear',
                   'periodical strain\\volumetric',
                   'periodical strain\\distortional',
                   'cumulative strain\\volumetric',
                   'cumulative strain\\distortional']
    
    #containing result matrix
    matrix_list=[]
    
    for this_post_fix in list_post_fix:
        
        #stress and strain itself
        file_path=structural_deformation_path.replace('structural deformation',this_post_fix)
        
        matrix_list.append(Mat.ImportMatrixFromTXT(file_path))
        
    that_progress.mean_normal_stress,\
    that_progress.maximal_shear_stress,\
    that_progress.periodical_volumrtric_strain,\
    that_progress.periodical_distortional_strain,\
    that_progress.cumulative_volumrtric_strain,\
    that_progress.cumulative_distortional_strain=matrix_list

    #import outline matrix
    outline_matrix=Img.ImgFlip(Mat.ImportOutlineFromTXT(file_path),0)
    
    that_progress.outline=outline_matrix
    that_progress.fracture=fracture_matrix
    that_progress.percentage=progress_percentage
    that_progress.structural_deformation=structural_deformation_img_rgb

    #construct a map between post fix name and matrix
    list_stress_or_strain=['Mean Normal Stress',
                           'Maximal Shear Stress',
                           'Periodical Volumetric Strain',
                           'Periodical Distortional Strain',
                           'Cumulative Volumrtric Strain',
                           'Cumulative Distortional Strain']
    
    that_progress.stress_or_strain=dict(zip(list_stress_or_strain,matrix_list))
    
    return that_progress

#------------------------------------------------------------------------------   
"""
Construct a case object

Args:
   case_path: path to construct
   
Returns:
    case object
""" 
def CaseConstruction(case_path):
    
    #construct case object to save the image data
    that_case=case()
    
    that_case.list_progress=[]
    that_case.condition=case_path.split('\\')[-1]
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
   
        that_case.list_progress.append(ProgressConstruction(structural_deformation_path))
    
    return that_case

#------------------------------------------------------------------------------   
"""
Construct an experiment object

Args:
   experiment_path: path to construct
   
Returns:
    experiment object
""" 
def ExperimentConstruction(experiment_path):
    
    that_experiment=experiment()
    
    that_experiment.parameter=experiment_path.split('\\')[-1]
    that_experiment.list_case=[]
    
    #cases folder
    folder_path=experiment_path+'\\output'
    
    #traverse all case
    for this_case_name in os.listdir(folder_path):
        
        this_case_path=folder_path+'\\'+this_case_name
        
        that_experiment.list_case.append(CaseConstruction(this_case_path))
        
    return that_experiment

#------------------------------------------------------------------------------
"""
Plot single structural deformation in different progress with fracture

Args:
    which_progress: progress object
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: plot progress proportion

Returns:
    None
"""
def SingleStructuralDeformationInProgress(which_progress,
                                          subplot_ax,
                                          with_fracture=False,
                                          with_annotation=True):
    print('')
    print('-- Structural Deformation')

    #percentage of progress
    progress_percentage=which_progress.percentage
    
    print('-> progress='+progress_percentage)

    #transform to RGB format
    structural_deformation_img_rgb=which_progress.structural_deformation

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    plt.imshow(structural_deformation_img_rgb)

    """regard cumulative distortional strain as fracture"""
    if with_fracture:

        #filter fracture matrix and plot farcture
        if type(Mat.MatrixFilter(fracture_matrix,0.23,1,show=True)) is bool:
            
            print('=> WARNING: without fracture')
                           
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

from matplotlib import colors

#------------------------------------------------------------------------------
"""
Calculate value norm from a case object

Args:
    which_case: case object
    post_fix: post fix of value type
    
Returns:
    value norm
"""
def GlobalNorm(which_case,post_fix):

    if 'Strain' in post_fix:
        
        return colors.Normalize(vmin=-1,vmax=1)
    
    #global maximum and minimum of matrix
    values_max=[]
    values_min=[]
    
    #traverse txt names
    for this_progress in which_case.list_progress:
        
        if 'Mean Normal' in post_fix:
            
            this_matrix=this_progress.mean_normal_stress
        
        if 'Maximal Shear' in post_fix:
            
            this_matrix=this_progress.maximal_shear_stress
            
        values_max.append(Mat.MatrixMaximum(this_matrix))
        values_min.append(Mat.MatrixMinimum(this_matrix))
      
    #values maximum and minimum norm
    return colors.Normalize(vmin=np.min(values_min),vmax=np.max(values_max))

#------------------------------------------------------------------------------
"""
Calculate colormap

Args:
    post_fix: post fix of value type
    
Returns:
    colormap
"""
def GlobalColormap(post_fix):

    if 'Volumetric' in post_fix:
        
        return 'RdBu'
    
    if 'Distortional' in post_fix:
        
        return 'BrBG'
    
    if 'Normal' in post_fix:
        
        return 'gist_earth'
    
    if 'Shear' in post_fix:
        
        return 'terrain'

#------------------------------------------------------------------------------
"""
Plot single stress of strain in different progress with fracture

Args:
    which_progress: progress object
    post_fix: post fix of txt file
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    with_annotation: plot progress proportion

Returns:
    None
"""
def SingleStressOrStrainInProgress(which_progress,
                                   post_fix,
                                   subplot_ax,
                                   with_fracture=False,
                                   with_annotation=True):
    print('')
    print('-- '+post_fix)

    #percentage of progress
    progress_percentage=which_progress.percentage
    
    print('-> progress='+progress_percentage)
    
    #stress or strain value matrix to be plotted
    value_matrix=ISm.ImageSmooth((which_progress.stress_or_strain[post_fix]))

    #outline matrix
    outline_matrix=which_progress.outline

    #fracture matrix
    fracture_matrix=which_progress.fracture
    
    #shape of this img
    this_shape=np.shape(fracture_matrix)
    
    #plot main body
    if 'Stress' in post_fix and which_progress.case==None:
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=GlobalColormap(post_fix))
        
    else:
        
        plt.imshow(Img.ImgFlip(value_matrix,0),
                   cmap=GlobalColormap(post_fix),
                   norm=GlobalNorm(which_progress.case,post_fix))
    
    #plot outline
    plt.imshow(outline_matrix,cmap='gray')
    
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
Plot integral analysis of a progress

Args:
    output_folder: folder to contain result
    which_progress: progress object
    mode: 'standard' 'all'
    with_farcture: (bool) plot fracture and interface or not 

Returns:
    Figure path
"""
def SingleIntegralAnalysisInProgress(output_folder,
                                     which_progress,
                                     mode='standard',
                                     with_fracture=True):
    
    print('')
    print('Single Integral Analysis In Progress')

    #title font
    title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
    #annotation font
    annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)
    
    #global shape of progress or integral analysis
    global_shape=which_progress.shape
    
    if mode=='standard':
    
        list_stress_or_strain=['Structural Deformation',
                               'Mean Normal Stress',
                               'Maximal Shear Stress',
                               'Periodical Volumetric Strain',
                               'Periodical Distortional Strain']
        
        #new picture and ax
        #100-1000
        if global_shape==(100,1000):
            
            figure=plt.subplots(figsize=(13,10))[0]
            
        #100-500
        if global_shape==(100,500):
        
            figure=plt.subplots(figsize=(7,10))[0]
    
    if mode=='all':
        
        list_stress_or_strain=['Mean Normal Stress',
                               'Maximal Shear Stress',
                               'Periodical Volumetric Strain',
                               'Periodical Distortional Strain',
                               'Cumulative Volumrtric Strain',
                               'Cumulative Distortional Strain']
    
        #new picture and ax
        #100-1000
        if global_shape==(100,1000):
            
            figure=plt.subplots(figsize=(13,14))[0]
        
        #100-500
        if global_shape==(100,500):
            
            figure=plt.subplots(figsize=(7,14))[0]
     
    #shape of this img
    this_shape=np.shape(which_progress.fracture)
    
    #subplot index
    index=0
    
    for this_post_fix in list_stress_or_strain:
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(list_stress_or_strain),1,index)
        
        if index==1:
            
            #structural deformation
            SingleStructuralDeformationInProgress(which_progress,this_ax,0,0)

        if index>1:
            
            #stress and strain
            SingleStressOrStrainInProgress(which_progress,this_post_fix,this_ax,0,0)    
            
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
        
        #sub annotation
        this_ax.annotate(which_progress.percentage,
                         xy=(0,0),
                         xytext=(1.01*this_shape[1],0.23*this_shape[0]),
                         fontproperties=annotation_font)
    
        #sub title
        this_ax.annotate(this_post_fix,
                         xy=(0,0),
                         xytext=(0,1.023*global_shape[0]),
                         fontproperties=title_font)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
     
    #figure name
    fig_name=which_progress.percentage

    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    integral_analysis_folder=output_folder+'\\integral analysis\\'
    
    #generate folder
    Pa.GenerateFolder(integral_analysis_folder)
    
    #figure path
    fig_path=integral_analysis_folder+fig_name+' ('+mode+').png'
    
    #save this fig
    figure.savefig(fig_path,dpi=300,bbox_inches='tight')
        
    plt.close()
    
    return fig_path

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
        this_fig_path=SingleIntegralAnalysisInProgress(output_folder,this_progress)

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
 
        SingleStructuralDeformationInProgress(this_progress,
                                              this_ax,
                                              with_fracture,
                                              with_annotation=False)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
 
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
        
        SingleStressOrStrainInProgress(this_progress,
                                       post_fix,
                                       this_ax,
                                       with_fracture,
                                       with_annotation=False)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])

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
    


case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=0.00'

#A experiment
#experiment_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2'

a_case=CaseConstruction(case_path)

structural_deformation_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=10.87\structural deformation\values\27.87%.txt'

a_progress=ProgressConstruction(structural_deformation_path)

#install its original case
#a_progress.case=a_case

#ExperimentConstruction(experiment_path)


#ax=plt.subplot()   
#SingleStressOrStrainInProgress(a_progress,'Periodical Distortional Strain',ax)
#SingleStressOrStrainInProgress(a_progress,'Periodical Volumetric Strain',ax)

#SingleStressOrStrainInProgress(a_progress,'Maximal Shear Stress',ax)
#SingleStressOrStrainInProgress(a_progress,'Mean Normal Stress',ax)

#global shape of progress or integral analysis
#global_shape=(100,500)
#
#ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])

output_folder=r'C:\Users\whj\Desktop\fig'
#
#SingleIntegralAnalysisInProgress(output_folder,a_progress)    
#AnimationIntegralAnalysis(output_folder,a_case)

#ProgressStructuralDeformation(output_folder,a_case)

ProgressStressOrStrain(output_folder,a_case,'Periodical Distortional Strain')
