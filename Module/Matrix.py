# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:14:43 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculation about matrix
"""

import numpy as np

#============================================================================== 
#calculate the maximum of a matrix
def MatrixMaximum(which_matrix):
    
    total_values=[]
    
    #searching for the maximum
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if np.isnan(which_matrix[i,j]):
                
                continue
            
            total_values.append(which_matrix[i,j])
       
    return np.max(total_values)

#============================================================================== 
#calculate the minimum of a matrix
def MatrixMinimum(which_matrix):
    
    total_values=[]
    
    #searching for the minimum
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if np.isnan(which_matrix[i,j]):
                
                continue
            
            total_values.append(which_matrix[i,j])
       
    return np.min(total_values)

#============================================================================== 
#calculate the average of a matrix
def MatrixAverage(which_matrix):
    
    total_values=[]
    
    #searching for the minimum
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if np.isnan(which_matrix[i,j]):
                
                continue
            
            total_values.append(which_matrix[i,j])
       
    return np.mean(total_values)
