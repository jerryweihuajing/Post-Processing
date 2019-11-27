# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 18:29:24 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Module-High Performance Calculation of Global affairs
"""

import numpy as np
from matplotlib import colors

import Matrix as Mat

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