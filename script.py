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

from Module import Path as Pa
from Module import NewPath as NP
from Module import ColorBar as CB
from Module import Animation as An
from Module import Dictionary as Dict
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG
from Module import NewSpheresGeneration as NSG
from Module import SpheresAttributeMatrix as SAM

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

'''
demand 4:
draw surface with stress or strain figure
'''

#data folder path
case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.3 v=1.0\\input\\base=0.00'

#file_paths=NP.FilePathsThisCase(case_path)

#Generate map between phase index between spheres list 
MAP=NSG.GenerateSpheresMapWithSample(case_path)
 
spheres=MAP[5]  
       
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
    

"""
Plot different phase image in a custom style

"""
def CustomPlot(which_case_path,
               which_input_mode,
               which_output_mode,
               pixel_step,
               test=False,
               show=False):
    
    print('input_mode:',which_input_mode.replace('_',' '))
    print('output_mode:',which_output_mode.replace('_',' '))
    
    #map between index and spheres
    map_all_phase_spheres=NSG.GenerateSpheresMapWithSample(which_case_path)
    
    '''output path'''
    
    #Gnenerate this Folder
    '''Medival fold will be generated as well'''
    Pa.GenerateFold(new_output_folder_path)
    
    #计数器
    count=1
    
    #construct the map between postfix and colormap
    postfix=['.txt','.vtk']
    colormap=['gist_rainbow','seismic'] 
    
    #construct a map between postfix and cmap
    map_postfix_cmap=dict(zip(postfix,colormap))
        
    #stress or strain
    if output_mode!='structural_deformation':
        
        '''generate a norm for stress: global norm'''     
        #stress norm
        zmin,zmax=VB.GlobalValueBoundary(which_case_path,input_mode,output_mode)
        norm_stress=colors.Normalize(vmin=zmin,vmax=zmax)
        
        #strain norm
        norm_strain=colors.Normalize(vmin=-1,vmax=1)
        
        #control the tick of colormap
        norms=[norm_stress,norm_strain]
        
        #construct a map between postfix and norm
        map_postfix_norm=dict(zip(postfix,norms))
    
#    last_time=time.time()
       
    #绘制不同期次的形态
    for this_new_file_name in input_file_names:    
        
#        print(time.time()-last_time)
                
        print('')
        print('======')

        #delete the suffix
        for this_postfix in postfix:
 
            if this_postfix in this_new_file_name:
            
                this_percentage=this_new_file_name.strip(this_postfix)
            
                break
       
        print(this_percentage.strip('.'))
        
        #图片和填充柄
        this_fig=plt.figure(count)

#        print(count)
        
        this_ax=plt.subplot()
        
        #give a name
        this_fig_name=this_percentage.strip('.').strip('progress=')+'.png'
        
        #this txt name
        this_txt_name=this_percentage.strip('.').strip('progress=')+'.txt'
        
        #生成颗粒体系
        if test:
            
            this_spheres=SG.GenerateSpheres(which_case_path,count-1)[:100]
        
        else:
            
            this_spheres=SG.GenerateSpheres(which_case_path,count-1)  
        
        if output_mode=='series':
        
            #构造形态及应力应变系列图
            Stress.StressSeriesPlot(this_spheres,pixel_step)
        
        if output_mode=='structural_deformation':
                       
            #图像版形态
            spheres_grids=SP.SpheresImage(this_spheres,pixel_step)
             
            #构造形态的绘制:图形
#            SpheresPlot(this_spheres)
            
            #图像
            this_img=Img.ImgFlip(spheres_grids.img_color,0)
            plt.imshow(this_img)
            
#            spheres_grids.Plot()
            
            #坐标轴和边
            Dec.TicksAndSpines(this_ax)
            plt.axis(np.array(global_axis_boundary)/pixel_step)
                     
        else:
            
#            print(this_new_file_name)
            
            #最终矩阵
            this_img=Img.ImgFlip(Analysis(this_spheres,input_mode,output_mode,pixel_step),0)
                     
            #select the colormap
            for this_postfix in postfix:
                
                if this_postfix in this_new_file_name:

                    plt.imshow(this_img,
                               norm=map_postfix_norm[this_postfix],
                               cmap=map_postfix_cmap[this_postfix]) 
                   
                    break
                
            #坐标轴和边
            Dec.TicksAndSpines(this_ax)
            
#            print(np.array(global_axis_boundary)/pixel_step)
            
            plt.axis(np.array(global_axis_boundary)/pixel_step)
        
        #save as txt
        np.savetxt(new_output_folder_path+this_txt_name,this_img,fmt="%.3f",delimiter=",")  
        
        #save this fig
        this_fig.savefig(new_output_folder_path+this_fig_name,dpi=300,bbox_inches='tight')
        
#        last_time=time.time()
        
        count+=1 
        plt.close()  
       
##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

#the mode which I search for
#mode_list=['shear_strain',
#           'volumetric_strain',
#           'distortional_strain']

#mode_list=['distortional_strain','volumetric_strain','shear_strain','y_normal_strain']

#mode_list=['distortional_strain']
#
#IP.SinglePlot(folder_path,'periodical_strain','y_normal_strain',1)

#load_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 1\output\periodical strain\x normal strain'

#load_path=r'C:\Users\whj\Desktop\operation'
##An.GenerateGIF(load_path)
##
#load_path=r'C:\魏华敬\Spyder\YADE\Stress Strain\Data\L=1000 v=1.0 r=1.0 layer=10 detachment=0-4\output\2019.6.19\case 4\periodical strain\y normal strain'
#
#An.GenerateGIF(load_path)

#output all images
#IP.TotalOuput(case_path,1)

#which_spheres=SG.GenerateSpheresFromTXT('progress=48.37%.txt')[0]

#pixel_step=1
#
#plt.figure()
#SB.SpheresLeftImg(which_spheres,pixel_step,show=True)
#SB.SpheresRightImg(which_spheres,pixel_step,show=True)
#SB.SpheresBottomImg(which_spheres,pixel_step,show=True)
#SB.SpheresSurfaceImg(which_spheres,pixel_step,show=True)

#plt.figure()
#
#SB.SimpleSpheresBoundary(which_spheres,pixel_step,show=True)

#edge=SB.SpheresEdge(spheres,pixel_step,True)
      
