# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 10:46:56 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Norm
"""

import numpy as np

from matplotlib import colors

import calculation_stress as C_S

#------------------------------------------------------------------------------ 
"""
Calculate stress norm object depending on spheres list

Args:
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_Spheres_list: spheres list
    which_output_mode: which attriutes value to be calculated
    
Returns:
    stress norm object
"""
def StressNorm(which_spheres_list,which_plane,which_output_mode):
    
    if 'structural_deformation' in which_output_mode:
    
        print('ERROR:You idiot')
    
        return 
    
    list_z_values_min=[]
    list_z_values_max=[]
    
    for k in range(1,len(which_spheres_list)):
        
        #spheres this phase
        this_spheres=which_spheres_list[k]
        
        #scatters
        scatters=C_S.ScattersStress(this_spheres,which_plane,'stress',which_output_mode)
        
        #z_values
        z_values=[this_discrete_point.pos_z for this_discrete_point in scatters]  
        
        #maximum and minimum
        z_values_min=np.min(z_values)
        z_values_max=np.max(z_values)
        
        #collect
        list_z_values_min.append(z_values_min)
        list_z_values_max.append(z_values_max)
          
    #pos_z maximum and minimum
    z_values_min=np.min(list_z_values_min)
    z_values_max=np.max(list_z_values_max)
    
#    print(z_values_min,z_values_max)
    
    return colors.Normalize(vmin=z_values_min,vmax=z_values_max)

#------------------------------------------------------------------------------
"""
Calculate strain norm object depending on spheres list

Args:
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_Spheres_list: spheres list
    which_output_mode: which attriutes value to be calculated
    
Returns:
    strain norm object (defualt: -1:1)
"""
def StrainNorm(which_spheres_list=None,which_plane=None,which_output_mode=None):
    
    return colors.Normalize(vmin=-1,vmax=1)