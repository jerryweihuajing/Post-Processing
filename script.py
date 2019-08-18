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
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path)) 

from o_grid import grid
from o_mesh import mesh
from o_sphere import sphere
from o_strain_2D import strain_2D
from o_discrete_point import discrete_point

import Norm as No
import Path as Pa
import Image as Img
import Matrix as Mat
import Global as Glo
import NewPath as NP
import ColorBar as CB
import Animation as An
import Histogram as His
import CustomPlot as CP
import Decoration as Dec
import Dictionary as Dict
import SpheresPlot as SP
import ProgressPlot as PP
import IntegralPlot as IP
import AxisBoundary as AB
import Interpolation as In
import ValueBoundary as VB
import SpheresBoundary as SB
import SpheresGeneration as SG
import NewSpheresGeneration as NSG
import SpheresAttributeMatrix as SAM

import StrainPlot as Strain
import StressPlot as Stress

#title font
title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=20)

#annotation font
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
    progress of structural deformation, strain, stress 
    
demand 6:
    integral plot of structural deformation,strain,stress 5 or 7 figures
    
demand 7:
    develop with_fracture BUTTON and cumulative or periodical mode BUTTON
    
demand 8:
    Matrix Filter with v-norm proportion
    
'''

case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89'

#PP.ProgressStructuralDeformation(case_path)

'stress and strain progress'

file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\structural deformation\\values\\27.87%.txt'

def PostFix2Title(which_post_fix):
    
    temp_str=which_post_fix.split('\\')
    
    #S+C to C+S
    temp_str.reverse()

    title_str=''
    
    for this_part in temp_str:
        
        for this_str in this_part.split(' '):

            title_str+=this_str[0].upper()+this_str[1:]+' '
         
    return title_str

#------------------------------------------------------------------------------
"""
Plot integral analysis of a progress

Args:
    file_path: load path of txt file
    mode: 'standard'

Returns:
    None
"""
def SingleIntegralAnalysisInProgress(file_path,mode='standard'):
    
    print('')
    print('integral analysis')

    #title font
    title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)
    
    #annotation font
    annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=13)

    #plot structural deformation
    structural_deformation_path=cp.deepcopy(file_path)
    
    #percentage of progress
    progress_percentage=PP.ProgressPercentageFromTXT(file_path)
    
    #Generate tag image and rgb image
    structural_deformation_img_tag=Mat.ImportMatrixFromTXT(file_path)
    
    #shape of this img
    this_shape=np.shape(structural_deformation_img_tag)
    
    list_post_fix=['stress\\mean normal',
                   'stress\\maximal shear',
                   'periodical strain\\volumetric',
                   'periodical strain\\distortional']

    #new picture and ax
    figure=plt.subplots(figsize=(10,6))[0]
    
    first_ax=plt.subplot(len(list_post_fix)+1,1,1)
    
    #calculate global norm
    global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

    #decoration     
    PP.SingleStructuralDeformationInProgress(structural_deformation_path,first_ax,1,0)
    
    #sub annotation
    first_ax.annotate(progress_percentage,
                      xy=(0,0),
                      xytext=(1.01*this_shape[1],0.25*this_shape[0]),
                      fontproperties=annotation_font)
        
    #sub title
    first_ax.annotate('Structural Deformation',
                      xy=(0,0),
                      xytext=(0.01*global_shape[1],1.06*global_shape[0]),
                      fontproperties=title_font)
        
    first_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
        
    #subplot index
    index=1
    
    for this_post_fix in list_post_fix:
        
        #path of this mode
        this_path=file_path.replace('structural deformation',this_post_fix)
            
        #title str
        this_title=PostFix2Title(this_post_fix)
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(list_post_fix)+1,1,index)
 
        #calculate global norm
        global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

        #show image    
        Mat.DisplayImageFromTXT(this_path,1)
        
        #oshow utline
        Mat.DisplayOutlineFromTXT(this_path,1)
        
        #sub annotation
        this_ax.annotate(progress_percentage,
                         xy=(0,0),
                         xytext=(1.01*this_shape[1],0.25*this_shape[0]),
                         fontproperties=annotation_font)
    
        #sub title
        this_ax.annotate(this_title,
                         xy=(0,0),
                         xytext=(0.01*global_shape[1],1.06*global_shape[0]),
                         fontproperties=title_font)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
     
    #figure name
    fig_name=progress_percentage+' integral analysis'

    #save this fig
    figure.savefig(r'C:\Users\魏华敬\Desktop'+'\\'+fig_name+'.png',dpi=300,bbox_inches='tight')
    
SingleIntegralAnalysisInProgress(file_path)


##plot fracture
#fracture_file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\cumulative strain\\distortional\\values\\27.87%.txt'
#
##fracture matrix
#fracture_matrix=ImportMatrixFromTXT(fracture_file_path)
#
##plot background
#background_file_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\output\\base=10.89\\stress\\mean normal\\values\\27.87%.txt'
#
    
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
