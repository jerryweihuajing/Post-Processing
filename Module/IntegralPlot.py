# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:25:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Intrgral Plot
"""

'''
demand:
save matrix as txt or other format
'''

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Module import StressPlot as Stress
from Module import StrainPlot as Strain

from Module import Path as Pa
from Module import Image as Img
from Module import NewPath as NP
from Module import Decoration as Dec
from Module import SpheresPlot as SP
from Module import AxisBoundary as AB
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG

#==============================================================================
#Transform Spheres into discrete points
def DiscretePoints(which_spheres,input_mode,output_mode):
    
    #calculate stress
    if 'stress' in input_mode:
        
        #calculate the discrete points
        discrete_points=Stress.DiscreteValueStress(which_spheres,input_mode,output_mode)
    
    #calculater strain
    if 'strain' in input_mode:
    
        #calculate the discrete points
        discrete_points=Strain.DiscreteValueStrain(which_spheres,input_mode,output_mode)
   
    return discrete_points   
  
#==============================================================================
#which_txt and which_vtk will be mapped soon
#which_file stands for the file name input txt or vtk
#scalar: the spheres which take part in calculation
#mode: 'local' or 'global'
def Analysis(which_spheres,input_mode,output_mode,pixel_step,mode='spheres_in_grid'):
    
    #surface to reduce scale of calculation
    surface_map=SB.SpheresTopMap(which_spheres,pixel_step)

    #discrete points to interpolate
    discrete_points=DiscretePoints(which_spheres,input_mode,output_mode)
     
    #global interpolation mass of calculation
    if mode=='global':
    
        return In.GlobalIDWInterpolation(discrete_points,pixel_step,surface_map)
     
    #spheres in grid: grid length is quite larger than spheres 
    if mode=='spheres_in_grid':
        
        return In.SpheresInGridIDW(discrete_points,pixel_step,surface_map)
        
"""
Colormap grey is not recognized. 
Possible values are: 
Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r,BuPu, BuPu_r, CMRmap, CMRmap_r, 
Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, 
PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, 
PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, 
RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, 
Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, 
Vega10, Vega10_r, Vega20, Vega20_r, Vega20b, Vega20b_r, Vega20c, Vega20c_r, 
Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, 
afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, 
cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, 
gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, 
gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, 
gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, 
inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, 
ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, 
seismic, seismic_r, spectral, spectral_r, spring, spring_r, summer, summer_r, 
tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, 
viridis, viridis_r, winter, winter_r
"""
#============================================================================== 
#将文件夹下的所有数据读取并显示构造形态,并显示再output文件夹中
#集中显示
def SubPlot(which_case_path,input_mode,output_mode,pixel_step,test=False):

    print(input_mode)
    print(output_mode)
    
    this_fig=plt.figure()
    
    #输入文件名
    input_file_names=NP.ModeFileNames(which_case_path,input_mode)

    #通用的axis
    global_axis_boundary=AB.GlobalAxisBoundary(which_case_path)
       
    #输出文件夹的名字
    new_output_folder_path=NP.OutputFolderPath(which_case_path,input_mode,output_mode)
    
    #Gnenerate this Folder
    #Medival fold will be generated as well
    Pa.GenerateFold(new_output_folder_path)
    
    #计数器
    number=1
    
    #construct the map between postfix and colormap
    postfix=['.txt','.vtk']
    colormap=['gist_rainbow','seismic'] 
    
    map_postfix_colormap=dict(zip(postfix,colormap))
    
    #绘制不同期次的形态
    for this_new_file_name in input_file_names:
        
        print('')
        print('======')

        #delete the suffix
        for this_postfix in postfix:
 
            if this_postfix in this_new_file_name:
            
                this_percentage=this_new_file_name.strip(this_postfix)
            
                break
       
        print(this_percentage.strip('.')) 
        
        #生成颗粒体系
        if test:
            
            this_spheres=SG.GenerateSpheres(which_case_path,number-1)[:100]
            
        else:
            
            this_spheres=SG.GenerateSpheres(which_case_path,number-1)
        
        #subplot
        this_ax=plt.subplot(len(input_file_names),1,number)
                     
        if output_mode=='structural_deformation':

            #构造形态的绘制
            #图形
#            SpheresPlot(this_spheres)

            #图像版形态
            spheres_grids=SP.SpheresImage(this_spheres,pixel_step)
            spheres_grids.Plot()
            
            #坐标轴和边
            In.TicksAndSpines(this_ax)
            plt.axis(global_axis_boundary)
            
        else:
            
            print(len(this_spheres))
            
            #最终矩阵           
            this_img=Analysis(this_spheres,output_mode,pixel_step)
            
            #select the colormap
            for this_postfix in postfix:
                
                if this_postfix in this_new_file_name:
                
                    plt.imshow(this_img,cmap=map_postfix_colormap[this_postfix]) 
                
                    break    
            
            #坐标轴和边
            Dec.TicksAndSpines(this_ax)
            plt.axis(np.array(global_axis_boundary)/pixel_step)
                  
        #保存一下咯
        this_fig_name='process.png'
        this_fig.savefig(new_output_folder_path+this_fig_name,dpi=300,bbox_inches='tight')
        
        number+=1 
        
    plt.close()   

#============================================================================== 
#将文件夹下的所有数据读取并显示形态或应力,单独显示在output文件夹中
#pixel_step为分辨率
#test为测试按钮
#input_mode: 'stress' 'cumulative strain' 'periodical strain'
#output_mode: 'xx_stress' 'xx_strain' 'structural deformation'
def SinglePlot(which_case_path,input_mode,output_mode,pixel_step,test=False):
    
    print('input_mode:',input_mode.replace('_',' '))
    print('output_mode:',output_mode.replace('_',' '))
    
    #输入文件名
    input_file_names=NP.ModeFileNames(which_case_path,input_mode)

    #通用的axis
    global_axis_boundary=AB.GlobalAxisBoundary(which_case_path)
       
    #输出文件夹的名字
    new_output_folder_path=Pa.OutputFolderPath(which_case_path,input_mode,output_mode)
    
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
            
#==============================================================================    
#outpupt all kinds of plots
def TotalOuput(which_folder_path,pixel_step,which_mode_list=None):
    
    #posible condition of stress
    stress_mode=['x_normal_stress',
                 'y_normal_stress',
                 'shear_stress',
                 'mean_normal_stress',
                 'maximal_shear_stress']
    
    #posible condition of stain
    strain_mode=['x_normal_strain',
                 'y_normal_strain',
                 'shear_strain',
                 'volumetric_strain',
                 'distortional_strain']
    
    #default: all modes
    if which_mode_list==None or which_mode_list==[]:
        
        #structural deformation
        SinglePlot(which_folder_path,'stress','structural_deformation',pixel_step)
        
        #stress
        for this_stress_mode in stress_mode:
            
            SinglePlot(which_folder_path,'stress',this_stress_mode,pixel_step)
            
        #strain
        for this_strain_mode in strain_mode:
            
            SinglePlot(which_folder_path,'cumulative_strain',this_strain_mode,pixel_step)
            SinglePlot(which_folder_path,'periodical_strain',this_strain_mode,pixel_step)
        
    else:
        
        for this_mode in which_mode_list:
            
#            print(this_mode)
            
            #structural deformation
            if this_mode=='structural_deformation':
 
                SinglePlot(which_folder_path,'stress','structural_deformation',pixel_step)
                
            #stress
            if this_mode in stress_mode:
            
                SinglePlot(which_folder_path,'stress',this_mode,pixel_step)
            
            #strain
            if this_mode in strain_mode:
                
                SinglePlot(which_folder_path,'cumulative_strain',this_mode,pixel_step)
                SinglePlot(which_folder_path,'periodical_strain',this_mode,pixel_step)