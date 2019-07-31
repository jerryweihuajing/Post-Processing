# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：execution script
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Object.o_grid import grid
from Object.o_mesh import mesh
from Object.o_sphere import sphere
from Object.o_strain_2D import strain_2D
from Object.o_discrete_point import discrete_point

from Module import Norm as No
from Module import Path as Pa
from Module import Image as Img
from Module import NewPath as NP
from Module import ColorBar as CB
from Module import Animation as An
from Module import Histogram as His
from Module import CustomPlot as CP
from Module import Decoration as Dec
from Module import Dictionary as Dict
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import AxisBoundary as AB
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG
from Module import NewSpheresGeneration as NSG
from Module import SpheresAttributeMatrix as SAM

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

'''
demand 1:
    fracture on stress and deformation figure

demand 2:
    all images from a case path
    
demand 3:
    improve morphorlogy of outline
'''


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
Calculate global shape from a folder path

Args:
    folder_path: the folder which contain the txt files
    
Returns:
    Global matrix shape
"""
def GlobalShapeFromCase(folder_path):
    
    #generate txt names
    txt_names=os.listdir(folder_path)
    
    #shapes in this folder
    shapes=[]
      
    #traverse txt names
    for this_txt_name in txt_names:
        
        this_matrix=ImportMatrixFromTXT(folder_path+this_txt_name)
    
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
def GlobalNormFromCase(folder_path):
    
    #generate txt names
    txt_names=os.listdir(folder_path)
  
    #global maximum and minimum of matrix
    values_max=[]
    values_min=[]
    
    #traverse txt names
    for this_txt_name in txt_names:
        
        this_matrix=ImportMatrixFromTXT(folder_path+this_txt_name)
    
        values_max.append(MatrixMaximum(this_matrix))
        values_min.append(MatrixMinimum(this_matrix))
      
    #values maximum and minimum norm
    global_norm=colors.Normalize(vmin=np.min(values_min),vmax=np.max(values_max))
    
    return global_norm

#------------------------------------------------------------------------------
"""
Display image matrix from txt file

Args:
    txt_path: file path which contains values matrix
    
Returns:
    None
"""
def DisplayImageFromTXT(txt_path):
    
    #image matrix
    matrix=ImportMatrixFromTXT(txt_path)
    
    #strain
    if 'strain' in txt_path:
        
        colormap='seismic'
        global_norm=colors.Normalize(vmin=-1,vmax=1)
   
    #stress
    if 'stress' in txt_path:
        
        colormap='gist_rainbow'
        global_norm=GlobalNormFromCase(txt_path)

    plt.imshow(matrix,cmap=colormap,norm=global_norm)

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
    
    #result matrix
    new_matrix=np.full(np.shape(which_matrix),np.nan)
    
    for i in range(np.shape(which_matrix)[0]):
        
        for j in range(np.shape(which_matrix)[1]):
            
            if not np.isnan(which_matrix[i,j]):
                
                if lower_value<=which_matrix[i,j]<=upper_value:
                    
                    new_matrix[i,j]=1
    
    if show:
        
        plt.imshow(new_matrix,cmap='gray')
            
    return new_matrix
    
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

file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\cumulative strain\\distortional\\values\\27.87%.txt'

#post fix to delete
post_fix=file_path.split('\\')[-1]

#folder path of this file path
folder_path=file_path.strip(post_fix)

matrix=ImportMatrixFromTXT(file_path)  

DisplayImageFromTXT(file_path)

DisplayOutlineFromTXT(file_path)

"""regard cumulative distortional strain as fracture"""


#His.ValueHistogram(MatrixValues(matrix),0.01,show=True)
#plt.xlim([0,0.5])

#A experiment
#experiment_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.5\\input'
#
#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')  

#data folder path
#case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\input\\base=0.00'

#An.GenerateGIF(r'C:\魏华敬\Spyder\YADE\StressAndStrain\Data\base detachment\fric=0.0 v=0.2\output\base=0.00\stress\maximal shear\images')

#file_paths=NP.FilePathsThisCase(case_path)

#Generate map between phase index between spheres list 
#MAP=NSG.GenerateSpheresMapWithSample(case_path)
## 
#spheres=MAP[5]  
       
#shear_strain_matrix=SAM.SpheresStrainMatrix(10,spheres,
#                                        which_plane='XoY',
#                                        which_input_mode='periodical',
#                                        which_output_mode='shear')
#plt.figure()
#plt.imshow(shear_strain_matrix)
#    
#shear_stress_matrix=SAM.SpheresStressMatrix(10,spheres,
#                                        which_plane='XoY',
#                                        which_input_mode='stress',
#                                        which_output_mode='shear')
#plt.figure()
#plt.imshow(shear_stress_matrix)

#CP.SingleExport(case_path,'periodical_strain','distortional','XoY',1)

##export all figure
#CP.TotalExport(case_path,'XoY',1)
