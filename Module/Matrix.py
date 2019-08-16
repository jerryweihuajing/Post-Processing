# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:14:43 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation about matrix
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

import Image as Img
import Global as Glo

#------------------------------------------------------------------------------
"""
Generate image matrix from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    image matrix oject
"""
def ImportMatrixFromTXT(txt_path):
    
    #read lines
    lines=open(txt_path).readlines()
    
    value_lines=[]
    
    for this_line in lines:
        
        value_lines.append(this_line.strip('\n').split(','))  
        
    #check if length every single line is equal
    for this_value_line in value_lines:
        
        if len(this_value_line)!=len(value_lines[0]):
            
            print('ERROR: Incorrect length!')
            
            break
        
    value_matrix=np.zeros((len(value_lines),len(value_lines[0])))
    
    for i in range(np.shape(value_matrix)[0]):
        
        for j in range(np.shape(value_matrix)[1]):
            
            value_matrix[i,j]=float(value_lines[i][j])
              
    return value_matrix
  
#------------------------------------------------------------------------------
"""
Display image matrix from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    None
"""
def DisplayImageFromTXT(txt_path,global_norm=None):
    
    #image matrix
    matrix=ImportMatrixFromTXT(txt_path)
    
    #strain
    if 'strain' in txt_path:
        
        colormap='seismic'
        
        if global_norm==None:
            
            global_norm=colors.Normalize(vmin=-1,vmax=1)
   
    #stress
    if 'stress' in txt_path:
        
        colormap='gist_rainbow'
        
        if global_norm==None:
            
            global_norm=Glo.GlobalNormFromCase(txt_path)

    plt.imshow(matrix,cmap=colormap,norm=global_norm)
    
    #structural deformation
    if 'structural_deformation' in txt_path:
        
        plt.imshow(matrix)
        
#------------------------------------------------------------------------------
"""
Calculate outline from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    Outline matrix
"""
def ImportOutlineFromTXT(txt_path):
        
    #image matrix
    which_matrix=ImportMatrixFromTXT(txt_path)
    
    #matrix to draw outline image
    outline_matrix=np.full(np.shape(which_matrix),np.nan)
    
    #top and bottom
    for j in range(np.shape(which_matrix)[1]):
        
        for i in range(np.shape(which_matrix)[0]):    
            
            if not np.isnan(which_matrix[i,j]):
                 
                outline_matrix[i,j]=1
                outline_matrix[-1,j]=1
                
                break

    #left and right
    for j in [0,-1]:
        
        for i in range(np.shape(which_matrix)[0]): 
            
            if not np.isnan(which_matrix[i,j]):
                
                outline_matrix[i:,j]=1          
               
    return outline_matrix

#------------------------------------------------------------------------------
"""
Display outline from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    None
"""
def DisplayOutlineFromTXT(txt_path):
    
    #outline matrix
    outline_matrix=ImportOutlineFromTXT(txt_path)
    
    plt.imshow(outline_matrix,cmap='gray') 
      
#------------------------------------------------------------------------------
"""
Calculate maximum of a matrix

Args:
    which_matrix: matrix to be calculated
    
Returns:
    Maximum of a matrix
"""
def MatrixMaximum(which_matrix):
    
    #figure in this matrix
    content=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                content.append(which_matrix[i,j])   
            
    return np.max(content)
     
#------------------------------------------------------------------------------
"""
Calculate minimum of a matrix

Args:
    which_matrix: matrix to be calculated
    
Returns:
    Minimum of a matrix
"""
def MatrixMinimum(which_matrix):
    
    #figure in this matrix
    content=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                content.append(which_matrix[i,j])
            
    return np.min(content)

#------------------------------------------------------------------------------
"""
Matrix values list except nan

Args:
    which_matrix: matrix to be calculated
    
Returns:
    value list
"""
def MatrixValues(which_matrix):
    
    #value list
    values=[]
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                values.append(which_matrix[i,j])
                
    return values

#------------------------------------------------------------------------------
"""
Filter the matrix value between low value and high value

Args:
    which_matrix: matrix to be calculated
    lower_value: lower threshold
    upper_value: upper threshold
    show: Display or not
    
Returns:
    New matrix with the position whose value between low value and high value present 1
"""
def MatrixFilter(which_matrix,lower_value,upper_value,show=False):
    
    #if valid
    if MatrixMinimum(which_matrix)>lower_value or MatrixMaximum(which_matrix)<upper_value:
    
        print('=>')
        print('WARNING: without fracture')
        
        return
        
    #result matrix
    new_matrix=np.full(np.shape(which_matrix),np.nan)
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                if lower_value<=which_matrix[i,j]<=upper_value:
                    
                    new_matrix[i,j]=which_matrix[i,j]
    
    if show:
        
        plt.imshow(Img.ImgFlip(new_matrix,0),cmap='gray')
            
    return new_matrix