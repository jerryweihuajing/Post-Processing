# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:37:12 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Progress Operation
"""

from o_progress import progress

import Image as Img
import Matrix as Mat
import ImageSmoothing as ISm

import HPC_IndividualPlot as HPC_IP

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
    
    #construct a progress object
    that_progress=progress()
    
    if '100-500' in progress_path:
        
        that_progress.shape=(100,500)
        
    if '100-1000' in progress_path:
        
        that_progress.shape=(100,1000)    
    
    #map between tag and rgb in this case
    rgb_map=Img.MapTagRGB(progress_path)
    
    #Generate tag image and rgb image
    structural_deformation_img_tag=Mat.ImportMatrixFromTXT(progress_path)
    
    #transform to RGB format
    structural_deformation_img_rgb=Img.ImageTag2RGB(structural_deformation_img_tag,rgb_map)

    #percentage of progress
    progress_percentage=ProgressPercentageFromTXT(progress_path)
    
    #plot fracture
    fracture_file_path=progress_path.replace('structural deformation','cumulative strain\\distortional')
    
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
        file_path=progress_path.replace('structural deformation',this_post_fix)
        
        matrix_list.append(ISm.ImageSmooth(Mat.ImportMatrixFromTXT(file_path)))
        
    that_progress.mean_normal_stress,\
    that_progress.maximal_shear_stress,\
    that_progress.periodical_volumrtric_strain,\
    that_progress.periodical_distortional_strain,\
    that_progress.cumulative_volumrtric_strain,\
    that_progress.cumulative_distortional_strain=matrix_list

    stress_path=file_path.replace('structural deformation','stress\\mean normal')
    strain_path=file_path.replace('structural deformation','periodical strain\\volumetric')
    
    #import outline matrix
    outline_stress=Img.ImgFlip(Mat.ImportOutlineFromTXT(stress_path),0)
    outline_strain=Img.ImgFlip(Mat.ImportOutlineFromTXT(strain_path),0)
    
    that_progress.rgb_map=rgb_map
    that_progress.fracture=fracture_matrix
    that_progress.outline_stress=outline_stress
    that_progress.outline_strain=outline_strain
    that_progress.percentage=progress_percentage
    that_progress.img_tag=structural_deformation_img_tag
    that_progress.structural_deformation=structural_deformation_img_rgb

    #construct a map between post fix name and matrix
    list_post_fix=['Mean Normal Stress',
                   'Maximal Shear Stress',
                   'Volumetric Strain-Periodical',
                   'Distortional Strain-Periodical',
                   'Volumetric Strain-Cumulative',
                   'Distortional Strain-Cumulative']
    
    that_progress.stress_or_strain=dict(zip(list_post_fix,matrix_list))
    
    return that_progress

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
def ProgressPostProcessing(progress_path,output_folder,with_fracture=False):
    
    #construct a progress
    that_progress=ProgressConstruction(progress_path)
    
    #output folder of this progress
    progress_folder=output_folder+'\\'+that_progress.percentage
    
    #imaging and output
    HPC_IP.AllIndividualsInProgress(progress_folder,that_progress,with_fracture)