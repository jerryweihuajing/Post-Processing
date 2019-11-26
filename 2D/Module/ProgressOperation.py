# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:37:12 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Progress Operation
"""

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
    progress_percentage=ProgressPercentageFromTXT(structural_deformation_path)
    
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
                           'Cumulative Volumetric Strain',
                           'Cumulative Distortional Strain']
    
    that_progress.stress_or_strain=dict(zip(list_stress_or_strain,matrix_list))
    
    return that_progress