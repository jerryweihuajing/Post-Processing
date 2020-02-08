# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 23:35:27 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Global parameters of progress
"""

import os
import numpy as np
from matplotlib import colors

import calculation_matrix as C_M

#------------------------------------------------------------------------------
"""
Calculate global shape from a folder path

Args:
    folder_path: the folder which contain the txt files
    
Returns:
    Global matrix shape
"""
def GlobalShapeFromCase(file_path):
    
    #post fix to delete
    post_fix=file_path.split('\\')[-1]
    
    #folder path of this file path
    folder_path=file_path.strip(post_fix)
    
    #generate txt names
    txt_names=os.listdir(folder_path)
    
    #shapes in this folder
    shapes=[]
      
    #traverse txt names
    for this_txt_name in txt_names:
        
        this_matrix=C_M.ImportMatrixFromTXT(folder_path+this_txt_name)
    
        shapes.append(np.shape(this_matrix))
        
    #matrix shape
    shape_0=np.max([this_shape[0] for this_shape in shapes])
    shape_1=np.max([this_shape[1] for this_shape in shapes])
    
    #global shape in this case
    global_shape=(shape_0,shape_1)
    
    return global_shape

#------------------------------------------------------------------------------
"""
Calculate value norm from a folder path

Args:
    folder_path: the folder which contain the txt files
    
Returns:
    Global value norm
"""
def GlobalNormFromCase(file_path):
    
    #post fix to delete
    post_fix=file_path.split('\\')[-1]
    
    #folder path of this file path
    folder_path=file_path.strip(post_fix)
    
    #generate txt names
    txt_names=os.listdir(folder_path)
  
    #global maximum and minimum of matrix
    values_max=[]
    values_min=[]
    
    #traverse txt names
    for this_txt_name in txt_names:
        
        this_matrix=C_M.ImportMatrixFromTXT(folder_path+this_txt_name)
    
        values_max.append(C_M.MatrixMaximum(this_matrix))
        values_min.append(C_M.MatrixMinimum(this_matrix))
      
    #values maximum and minimum norm
    global_norm=colors.Normalize(vmin=np.min(values_min),vmax=np.max(values_max))
    
    return global_norm
