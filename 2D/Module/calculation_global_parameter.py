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
import matplotlib.pyplot as plt

from matplotlib import colors

import calculation_matrix as C_M

#------------------------------------------------------------------------------
"""
Calculate global shape from a folder path (in calculation)

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
Calculate value norm from a folder path (in calculation)

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

    '''vmin and vmax stand for the value which is below and above'''
    if 'Strain' in post_fix:
        
        return colors.Normalize(vmin=-1,vmax=1)
    
    #global maximum and minimum of matrix
    values_max=[]
    values_min=[]
    
    #traverse txt names
    for this_progress in which_case.list_progress:

        this_matrix=this_progress.map_matrix[post_fix]
           
        values_max.append(C_M.MatrixMaximum(this_matrix))
        values_min.append(C_M.MatrixMinimum(this_matrix))
      
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

    if 'Strain' in post_fix:
        
        if 'Volumetric' in post_fix:
            
            return 'RdBu'
        
        if 'Distortional' in post_fix:
            
            return 'BrBG'
        
        if 'Normal' in post_fix:
    
            return 'RdGy'
        
        if 'Shear' in post_fix:
            
            return 'PuOr'
        
    if 'Stress' in post_fix:
        
        if 'Mean Normal' in post_fix:
            
            return 'gist_earth'
        
        if 'Maximal Shear' in post_fix:
            
            return 'terrain'
        
        if 'Normal' in post_fix:
            
            return 'gist_stern'
        
        if 'Shear' in post_fix:
            
            return 'ocean'
        
    if 'Gradient' in post_fix:
        
        if 'Velocity' in post_fix:
            
            return 'Spectral'   
        
        if 'Displacement' in post_fix:
            
            return 'seismic'
        
    if 'Velocity' in post_fix:
        
        return 'hot'
    
    if 'Displacement' in post_fix:
            
        return 'cool'
    
#------------------------------------------------------------------------------
"""
Calculate figure based on global shape (for series and individual)

Args:
    global_shape: global shape of image
    
Returns:
    figure object in plt
"""
def FigureForSeriesAndIndividual(global_shape):
    
    '''compression'''
    #100-1000
    if global_shape==(100,1000):
        
        return plt.subplots(figsize=(13,13))[0]
        
    #100-800
    if global_shape==(100,800):
    
        return plt.subplots(figsize=(10,13))[0]
        
    #100-500
    if global_shape==(100,500):
    
        return plt.subplots(figsize=(7,13))[0]

    '''extension'''
    #100-200
    if global_shape==(100,350):
    
        return plt.subplots(figsize=(5,13))[0]
        
#------------------------------------------------------------------------------
"""
Calculate figure based on global shape (for integral analysis)

Args:
    global_shape: global shape of image
    mode: mode for integral analysis ['all', 'standrad']
    
Returns:
    figure object in plt
"""
def FigureForIntegralAnalysis(global_shape,mode):
    
    if mode=='standard':
        
        '''compression'''
        #100-1000
        if global_shape==(100,1000):
            
            return plt.subplots(figsize=(13,8))[0]
            
        #100-800
        if global_shape==(100,800):
        
            return plt.subplots(figsize=(10,8))[0]
            
        #100-500
        if global_shape==(100,500):
        
            return plt.subplots(figsize=(7,9))[0]
            
        '''extension'''
        #100-200
        if global_shape==(100,350):
        
            return plt.subplots(figsize=(5,9))[0]
            
    if mode=='all':
    
        '''compression'''
        #100-1000
        if global_shape==(100,1000):
            
            return plt.subplots(figsize=(13,13))[0]
        
        #100-800
        if global_shape==(100,800):
        
            return plt.subplots(figsize=(10,13))[0]
        
        #100-500
        if global_shape==(100,500):
            
            return plt.subplots(figsize=(7,13))[0]
            
        '''extension'''
        #100-200
        if global_shape==(100,350):
            
            return plt.subplots(figsize=(5,13))[0]