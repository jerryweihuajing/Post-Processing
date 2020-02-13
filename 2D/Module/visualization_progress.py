# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:37:12 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Progress Operation
"""

import copy as cp

from o_progress import progress

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_matrix_outline as C_M_O
import calculation_image_smoothing as C_I_S

import visualization_individual as V_I
import visualization_integral_analysis as V_I_A

from data_yade_color import yade_rgb_map

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
Construct a progress object

Args:
   progress_path: path to construct
   
Returns:
    progress object
""" 
def ProgressConstruction(progress_path):
    
    print('')
    print('-- Progress Construction')
    
    #construct a progress object
    that_progress=progress()
    
    if '100-500' in progress_path:
        
        that_progress.shape=(100,500)
        
    if '100-1000' in progress_path:
        
        that_progress.shape=(100,1000)   
        
    if '100-200' in progress_path:
        
        that_progress.shape=(100,350) 

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
        file_path=progress_path.replace('structural deformation',this_post_fix)
        
        matrix_list.append(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(file_path))))
        
    that_progress.mean_normal_stress,\
    that_progress.maximal_shear_stress,\
    that_progress.periodical_volumrtric_strain,\
    that_progress.periodical_distortional_strain,\
    that_progress.cumulative_volumrtric_strain,\
    that_progress.cumulative_distortional_strain=matrix_list
    
    #construct a map between post fix name and matrix
    list_post_fix=['Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
    
    #stress and strain map
    that_progress.stress_or_strain=dict(zip(list_post_fix,matrix_list))

    #map between tag and YADE rgb
    that_progress.rgb_map=yade_rgb_map
    
    #img tag and img rgb of structural deformation
    that_progress.img_tag=C_M.ImportMatrixFromTXT(progress_path)
    that_progress.structural_deformation=C_I.ImageTag2RGB(that_progress.img_tag,that_progress.rgb_map)
    
    #fracture matrix
    that_progress.fracture=cp.deepcopy(that_progress.stress_or_strain['Distortional Strain-Cumulative'])
    
    '''they are different for the existence of gradient calculation'''
    #stress outline
    that_progress.outline_stress=C_M_O.OutlineFromMatrix(that_progress.stress_or_strain['Mean Normal Stress'])
 
    #stress outline
    that_progress.outline_strain=C_M_O.OutlineFromMatrix(that_progress.stress_or_strain['Volumetric Strain-Periodical'])
    
    #progress percentage
    that_progress.percentage=ProgressPercentageFromTXT(progress_path)
    
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
    
    #plot all postfix mode
    for this_post_fix in list_post_fix:
        
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