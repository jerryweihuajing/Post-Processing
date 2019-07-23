# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:13:18 2019

Created on Mon Jul 15 00:25:15 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Plot in Custom manner
"""

import numpy as np
import matplotlib.pyplot as plt

import sys,os,imageio

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Module import Norm as No
from Module import Path as Pa
from Module import Image as Img
from Module import NewPath as NP
from Module import Decoration as Dec
from Module import SpheresPlot as SP
from Module import AxisBoundary as AB
from Module import NewSpheresGeneration as NSG
from Module import SpheresAttributeMatrix as SAM

#------------------------------------------------------------------------------
"""
Plot different phase image in a custom style

Args:
    which_case_path: load path of all input files
    which_input_mode: 'structural_deformation' 'stress' 'cumulative_strain' 'periodical strain'
    which_output_mode: 'x_normal' 'y_normal' 'shear' 'mean_normal' 'maximal_shear'
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes
    pixel_step: length of single pixel
    index_list: custom index of images
    test: if there is a test with a small amount of spheres
    show: if there is a window display
Returns:
    PNG, TXT, GIF in output folder
"""
def SingleExport(which_case_path,
                 which_input_mode,
                 which_output_mode,
                 which_plane,
                 pixel_step,
                 test=False,
                 show=False):

    #map between index and spheres
    map_all_phase_spheres=NSG.GenerateSpheresMapWithSample(which_case_path)
    
    #list of spheres
    spheres_list=list(map_all_phase_spheres.values())
    
    #通用的axis
    global_axis_boundary=AB.GlobalAxisBoundary(spheres_list)
    
    #file name list in this case
    file_names=NP.FileNamesThisCase(which_case_path)
    
    if which_input_mode=='structural_deformation':
        
        which_output_mode=''
     
    print('input mode:',which_input_mode.replace('_',' '))
    print('output mode:',which_output_mode.replace('_',' '))
    
    '''Medival fold will be generated as well'''
    output_folder=NP.OutputFolder(which_case_path,which_input_mode,which_output_mode)
    
    #Gnenerate this Folder
    Pa.GenerateFold(output_folder)
    
    #construct the map between postfix and colormap
    if which_input_mode=='stress':
        
        #stress colormap
        colormap='gist_rainbow'
        
        #stress norm
        norm=No.StressNorm(spheres_list,which_plane,which_output_mode)
        
    if 'strain' in which_input_mode:
        
        #strain colormap
        colormap='seismic'
        
        #strain norm
        norm=No.StrainNorm()
     
    #计数器
    count=1
    
    #figures to generate GIF
    images=[]
    
    #绘制不同期次的形态
    for k in range(len(map_all_phase_spheres)):    
                   
        print('')
        print('======')
        
        #file name and progress percentage
        this_file_name=file_names[k]
        this_progress=this_file_name.strip('.txt')
        this_percentage=this_progress.strip('progress=')
        
        print(this_progress)
        
        #图片和填充柄
        this_fig=plt.figure(count)
        
        this_ax=plt.subplot()
        
        #give a name
        this_fig_name=this_percentage+'.png'
        
        #this txt name
        this_txt_name=this_percentage+'.txt'
        
        #spheres system
        this_spheres=map_all_phase_spheres[k] 
          
        if test:
            
            this_spheres=map_all_phase_spheres[k][:100]    
        
        if which_input_mode=='structural_deformation':
                       
            #Spheres image
            spheres_grids=SP.SpheresImage(this_spheres,pixel_step)
            
            #图像
            this_img=Img.ImgFlip(spheres_grids.img_color,0)
            this_img_tag=Img.ImgFlip(spheres_grids.img_tag,0)
            
            plt.imshow(this_img)
        
            #save as txt
            np.savetxt(output_folder+this_txt_name,this_img_tag,fmt="%.3f",delimiter=",") 
            
        else:
       
            #final matrix
            this_img=SAM.SpheresValueMatrix(pixel_step,
                                            this_spheres,
                                            which_plane,
                                            which_input_mode,
                                            which_output_mode,
                                            which_interpolation='spheres_in_grid')
             
            plt.imshow(Img.ImgFlip(this_img,0),norm=norm,cmap=colormap) 
            
            #save as txt
            np.savetxt(output_folder+this_txt_name,this_img,fmt="%.3f",delimiter=",")   
                 
        #坐标轴和边
        Dec.TicksAndSpines(this_ax)
        plt.axis(np.array(global_axis_boundary)/pixel_step)
        
        #save this fig
        this_fig.savefig(output_folder+this_fig_name,dpi=300,bbox_inches='tight')
        
        #collect fig to create GIF
        images.append(imageio.imread(output_folder+this_fig_name))
        
        count+=1 
        
        if not show:
            
            plt.close()  
       
    #GIF name
    gif_name=which_input_mode.replace('_',' ')+' '+which_output_mode.replace('_',' ')+'.gif'
    
    #save GIF
    imageio.mimsave(output_folder+'\\'+gif_name,images,duration=0.5)
    
#------------------------------------------------------------------------------   
"""
Total export depending on mode list 

Args:
    which_case_path: load path of all input files
    which_plane: 'XoY' 'YoZ' 'ZoX' displacement in 3 planes 
    pixel_step: length of single pixel
    mode_list: output mode which user need
    test: if there is a test with a small amount of spheres

Returns:
    mass of PNG, TXT, GIF in output folder
"""    
def TotalExport(which_case_path,
                which_plane,
                pixel_step,
                which_mode_list=None,
                test=False):
    
    #posible condition of stress
    stress_mode=['x_normal',
                 'y_normal',
                 'shear',
                 'mean_normal',
                 'maximal_shear']
    
    #posible condition of stain
    strain_mode=['x_normal',
                 'y_normal',
                 'shear',
                 'volumetric',
                 'distortional']
    
    #default: all modes
    if which_mode_list==None:
        
        #structural deformation
        SingleExport(which_case_path,'structural_deformation','',which_plane,pixel_step,test)
                
        #stress
        for this_stress_mode in stress_mode:
            
            SingleExport(which_case_path,'stress',this_stress_mode,which_plane,pixel_step,test)
            
        #strain
        for this_strain_mode in strain_mode:
            
            SingleExport(which_case_path,'cumulative_strain',this_strain_mode,which_plane,pixel_step,test)
            SingleExport(which_case_path,'periodical_strain',this_strain_mode,which_plane,pixel_step,test)
        
    else:
        
        for this_mode in which_mode_list:
            
#            print(this_mode)
            
            #structural deformation
            if this_mode=='structural_deformation':
 
                SingleExport(which_case_path,'structural_deformation','',which_plane,pixel_step,test)
                
            #stress
            if 'stress' in this_mode:
            
                this_stress_mode=this_mode.strip('_stress')
                
                SingleExport(which_case_path,'stress',this_stress_mode,which_plane,pixel_step,test)
            
            #strain
            if 'strain' in this_mode:
                
                this_strain_mode=this_mode.strip('_strain')
                
                SingleExport(which_case_path,'cumulative_strain',this_strain_mode,which_plane,pixel_step,test)
                SingleExport(which_case_path,'periodical_strain',this_strain_mode,which_plane,pixel_step,test)
        