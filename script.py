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
import matplotlib.font_manager as fm

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

#title font
title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=20)

#legend font
annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)

'''
demand 1:
    fracture on stress and deformation figure

demand 2:
    all images from a case path
    
demand 3:
    improve morphorlogy of outline
    
demand 4:
    transform file path into case path
    
demand 5:
    progress of structural deformation,strain,stress 
    
demand 6:
    integral plot of structural deformation,strain,stress 5 or 7 figures
    
demand 7:
    develop with_fracture BUTTON and cumulative or periodical mode BUTTON
    
demand 8:
    Matrix Filter with v-norm proportion
    
demand 9:
    axis and ticks
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
            
            global_norm=GlobalNormFromCase(txt_path)

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
Generate a map between tag and rgb

Args:
    file_path: file path of input file
    
Returns:
    map between tag and rgb
"""
def MapTagRGB(file_path):
    
    #xx.xx%.txt
    post_fix=file_path.split('\\')[-1]

    #re-name
    spheres_path=file_path.replace('output','input')\
                            .replace('\\structural deformation\\values','')\
                            .replace(post_fix,'progress='+post_fix)
                   
    #all lines
    lines=open(spheres_path,'r').readlines()
    
    #exceeding is not allowed
    correct_length=len(lines[0].strip('\n').split(','))
    
    #total color list
    color_list=[]
        
    #build a map
    map_tag_color={}
    map_tag_color[0]=[1.0,1.0,1.0]
    
    for this_line in lines:
      
        this_list=this_line.strip('\n').split(',')
    
        #extract this rgb value
        this_color=[float(this_str) for this_str in this_list[2:5]]
        
        #invalid information line
        if len(this_list)!=correct_length:
            
            continue
        
        #for the same
        this_stress_tensor=np.array([float(this_str) for this_str in this_list[8:]])
        
        #3D tensor length is correct
        if len(this_stress_tensor)!=9:
            
            continue
        
        #judge if there is inf
        if np.inf in this_stress_tensor or -np.inf in this_stress_tensor:
                    
            continue
        
        #judge if there is nan
        for this_element in this_stress_tensor:
        
            if np.isnan(this_element):
      
                continue
            
        #append
        if this_color not in color_list:
            
            color_list.append(this_color)
    
            map_tag_color[len(color_list)]=this_color
            
    return map_tag_color

#------------------------------------------------------------------------------
"""
Transform a tag image to RGB format

Args:
    img_tag: matrix to be processed
    map_tag_rgb: map between tag and rgb
    
Returns:
    RGB Image
"""
def ImageTag2RGB(img_tag,map_tag_rgb):
    
    #shape of rgb image
    img_rgb_shape=(np.shape(img_tag)[0],np.shape(img_tag)[1],3)
    
    #define new matrix
    img_rgb=np.full(img_rgb_shape,1.0)
    
    #给img_rgb矩阵赋值
    for i in range(np.shape(img_rgb)[0]):
        
        for j in range(np.shape(img_rgb)[1]):
            
            img_rgb[i,j]=np.array(map_tag_rgb[img_tag[i,j]])

    return img_rgb





##plot fracture
#fracture_file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\cumulative strain\\distortional\\values\\27.87%.txt'
#
##fracture matrix
#fracture_matrix=ImportMatrixFromTXT(fracture_file_path)
#
##plot background
#background_file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\stress\\mean normal\\values\\27.87%.txt'
#
    
"""regard cumulative distortional strain as fracture"""
##plot main body
#DisplayImageFromTXT(background_file_path)
#DisplayOutlineFromTXT(background_file_path)
#
##filter fracture matrix and plot farcture
#MatrixFilter(fracture_matrix,0.1,1,show=True)

#
#case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89'
#
##standard mode of output
#child_folder_names=['structural deformation',
#                    'stress\\mean normal',
#                    'stress\\maximal shear',
#                    'periodical strain\\volumetric',
#                    'periodical strain\\distortional']
#
##traverse child folder names
#for this_folder_name in child_folder_names:
#
#    #child folder path
#    this_folder_path=case_path+'\\'+this_folder_name+'\\'+'values'
    
#    print(os.listdir(this_folder_path))

'''output as a folder'''

case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\input\\base=10.89'
       
##def f(case_path):
#
##import structural deformation matrix
#structural_deformation_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\structural deformation\\values\\27.87%.txt'
#structural_deformation_img_tag=ImportMatrixFromTXT(structural_deformation_path)
#
##map between tag and rgb in this case
#map_tag_rgb=MapTagRGB(structural_deformation_path)    
#
##transform to RGB format
#structural_deformation_img_rgb=ImageTag2RGB(structural_deformation_img_tag,map_tag_rgb)
#
#plt.imshow(structural_deformation_img_rgb)
#
##calculate global norm
#global_shape=GlobalShapeFromCase(structural_deformation_path)
#
#plt.axis([0,global_shape[1],0,global_shape[0]])

"""
Calculate progress percentage from file path

Args:
    file_path: load path of research case
    
Returns:
    percentage of progress
"""
def ProgressPercentageFromPath(file_path):
    
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
Plot single structural deformation in different progress with fracture

Args:
    file_path: load path of txt file
    subplot_ax: sub ax in progress plot
    with_fracture: (bool) plot fracture or not 
    
Returns:
    None
"""
def SingleStructuralDeformationInProgress(file_path,subplot_ax,with_fracture=True):
    
    print('')
    print('...')
    print('......')
    print('progress='+ProgressPercentageFromPath(file_path))
    
    #map between tag and rgb in this case
    rgb_map=MapTagRGB(file_path)
    
    #percentage of progress
    progress_percentage=ProgressPercentageFromPath(file_path)
    
    #Generate tag image and rgb image
    structural_deformation_img_tag=ImportMatrixFromTXT(file_path)
    
    #transform to RGB format
    structural_deformation_img_rgb=ImageTag2RGB(structural_deformation_img_tag,rgb_map)
    
    #shape of this img
    this_shape=np.shape(structural_deformation_img_rgb)[:2]
    
    plt.imshow(structural_deformation_img_rgb)
    
    """regard cumulative distortional strain as fracture"""
    if with_fracture:
            
        #plot fracture
        fracture_file_path=file_path.replace('structural deformation','cumulative strain\\distortional')
        
        #fracture matrix
        fracture_matrix=ImportMatrixFromTXT(fracture_file_path)
    
        #filter fracture matrix and plot farcture
        MatrixFilter(fracture_matrix,0.23,1,show=True)

    '''revision'''
    #decoration  
    Dec.TicksAndSpines(subplot_ax)

    #sub annotation
    subplot_ax.annotate(progress_percentage,
                         xy=(0,0),
                         xytext=(1.01*this_shape[1],0.25*this_shape[0]),
                         fontproperties=annotation_font)

    
#------------------------------------------------------------------------------
"""
Plot structural deformation progress

Args:
    case_path: load path of input files in a case
    with_fracture: (bool) plot fracture or not 
    
Returns:
    figure series
"""
def ProgressStructuralDeformation(case_path,with_fracture=True):
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)

    #new picture and ax
    figure=plt.subplots(figsize=(12,9))[0]
    
    #subplot index
    index=0
    
    for file_name in file_names:
        
        ProgressPercentageFromPath(file_name)
        #txt file path
        structural_deformation_path=folder_path+file_name
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(file_names),1,index)
 
        #calculate global norm
        global_shape=GlobalShapeFromCase(structural_deformation_path)

        #decoration     
        SingleStructuralDeformationInProgress(structural_deformation_path,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1],0,global_shape[0]])
     
    #figure name
    fig_name='sturctural deformation'
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    #save this fig
    figure.savefig(r'C:\Users\魏华敬\Desktop'+'\\'+fig_name,dpi=300,bbox_inches='tight')
      
 
case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=5.45'

ProgressStructuralDeformation(case_path)

'stress and strain progress'

#file_path=r'D:\Spyder\YADE\StressAndStrain\Data\base detachment\fric=0.0 v=0.5\output\base=10.89\structural deformation\values\0.00%.txt'
#ax=plt.subplot()
#SingleStructuralDeformationInProgress(file_path,ax)


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
