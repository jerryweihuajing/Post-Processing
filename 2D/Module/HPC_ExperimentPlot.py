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

import copy as cp
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
            
        
import NewPath as NP
import Matrix as Mat
import Image as Img
import ImageSmoothing as ISm

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
        
case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=0.00'

#A experiment
#experiment_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2'

a_case=CaseConstruction(case_path)

#structural_deformation_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=10.87\structural deformation\values\27.87%.txt'

#a_progress=ProgressConstruction(structural_deformation_path)

#install its original case
#a_progress.case=a_case

#ExperimentConstruction(experiment_path)

#ax=plt.subplot()   
#SingleStressOrStrainInProgress(a_progress,'Periodical Volumetric Strain',ax)
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
#AnimationIndividual(output_folder,a_case,'Cumulative Distortional Strain')

#AnimationAll(output_folder,a_case)

#ProgressStructuralDeformation(output_folder,a_case)
#
#ProgressStressOrStrain(output_folder,a_case,'Mean Normal Stress')
#ProgressStressOrStrain(output_folder,a_case,'Maximal Shear Stress')
#ProgressStressOrStrain(output_folder,a_case,'Periodical Volumetric Strain')
#ProgressStressOrStrain(output_folder,a_case,'Periodical Distortional Strain')
#ProgressStressOrStrain(output_folder,a_case,'Cumulative Volumetric Strain')
#ProgressStressOrStrain(output_folder,a_case,'Cumulative Distortional Strain')


ProgressAll(output_folder,a_case)   
AnimationAll(output_folder,a_case)
IntegralAnalysisAll(output_folder,a_case)
            