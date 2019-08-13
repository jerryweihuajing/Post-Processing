# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 14:41:32 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Value Boundary: for imshow Norm
"""

import numpy as np

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

import NewPath as NP
import IntegralPlot as IP
import SpheresGeneration as SG

#==============================================================================
#stress norm: single norm
def LocalValueBoundary(which_spheres,input_mode,output_mode):
     
    if 'structural_deformation' in output_mode:
    
        print('ERROR:You idiot')
    
        return 
    
    else:
                           
        #calculate the discrete points
        discrete_points=IP.DiscretePoints(which_spheres,input_mode,output_mode)
        
        #z_value
        z_values=[this_discrete_point.pos_z for this_discrete_point in discrete_points]    
            
        #maximum and minimum
        z_values_min=np.min(z_values)
        z_values_max=np.max(z_values)
        
        return z_values_min,z_values_max
        
#==============================================================================
#stress norm: every stage share the same norm
def GlobalValueBoundary(which_folder_path,input_mode,output_mode):
     
    list_z_values_min=[]
    list_z_values_max=[]

    #traverse all files
    '''index 0 is invalid'''
    for k in range(1,len(NP.ModeFileNames(which_folder_path,input_mode))):
             
#            print(k)
        
        #generate spheres from file      
        this_spheres=SG.GenerateSpheres(which_folder_path,k)
        
        #local values boundary
        this_z_values_min,this_z_values_max=LocalValueBoundary(this_spheres,input_mode,output_mode)
        
        #collect
        list_z_values_min.append(this_z_values_min)
        list_z_values_max.append(this_z_values_max)
        
    #pos_z maximum and minimum
    z_values_min=np.min(list_z_values_min)
    z_values_max=np.max(list_z_values_max)
    
#        print(z_values_min,z_values_max)
    
    return z_values_min,z_values_max
