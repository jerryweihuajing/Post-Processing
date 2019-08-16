# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 23:45:48 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Progress plot
"""

'''
demand:
1 show axis and ticks
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import Matrix as Mat
import Image as Img
import Global as Glo
import NewPath as NP
import Decoration as Dec

#title font
title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=20)

#annotation font
annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)

#------------------------------------------------------------------------------
"""
Calculate progress percentage from file path

Args:
    file_path: load path of research case
    
Returns:
    percentage of progress
"""
def ProgressPercentageFromTXT(file_path):
    
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
    
    #map between tag and rgb in this case
    rgb_map=Img.MapTagRGB(file_path)
    
    #percentage of progress
    progress_percentage=ProgressPercentageFromTXT(file_path)
    
    print('progress='+progress_percentage)
    
    #Generate tag image and rgb image
    structural_deformation_img_tag=Mat.ImportMatrixFromTXT(file_path)
    
    #transform to RGB format
    structural_deformation_img_rgb=Img.ImageTag2RGB(structural_deformation_img_tag,rgb_map)
    
    #shape of this img
    this_shape=np.shape(structural_deformation_img_rgb)[:2]
    
    plt.imshow(structural_deformation_img_rgb)
    
    """regard cumulative distortional strain as fracture"""
    if with_fracture:
            
        #plot fracture
        fracture_file_path=file_path.replace('structural deformation','cumulative strain\\distortional')
        
        #fracture matrix
        fracture_matrix=Mat.ImportMatrixFromTXT(fracture_file_path)
    
        #filter fracture matrix and plot farcture
        Mat.MatrixFilter(fracture_matrix,0.23,1,show=True)

    '''revision'''
    #decoration  
    Dec.TicksAndSpines(subplot_ax,1,1)

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
    figure=plt.subplots(figsize=(13,9.6))[0]
    
    #subplot index
    index=0
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
        
        #iter
        index+=1
        
        this_ax=plt.subplot(len(file_names),1,index)
 
        #calculate global norm
        global_shape=Glo.GlobalShapeFromCase(structural_deformation_path)

        #decoration     
        SingleStructuralDeformationInProgress(structural_deformation_path,this_ax,with_fracture)
        
        this_ax.axis([0,global_shape[1]*1.1,0,global_shape[0]])
     
    #figure name
    fig_name='sturctural deformation'
    
    #re-name
    if with_fracture:
        
        fig_name+=' with fracture'
        
    #save this fig
    figure.savefig(r'C:\Users\魏华敬\Desktop'+'\\'+fig_name,dpi=300,bbox_inches='tight')