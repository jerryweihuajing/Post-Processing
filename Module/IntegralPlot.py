# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:25:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Intrgral Plot
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(r'C:\Users\whj\Desktop\Spyder\YADE\Stress Strain')

from Module import StressPlot as Stress
from Module import StrainPlot as Strain
from Module import Path as Pa
from Module import Image as Img
from Module import Decoration as Dec
from Module import SpheresPlot as SP
from Module import AxisBoundary as AB
from Module import Interpolation as In
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG

#==============================================================================
#which_txt and which_vtk will be mapped soon
#which_file stands for the file name input txt or vtk
#scalar: the spheres which take part in calculation
def Analysis(which_spheres,input_mode,output_mode,pixel_step):
    
    #surface to reduce scale of calculation
    surface_map=SB.SpheresSurfaceMap(which_spheres,pixel_step)

    #calculate stress
    if 'stress' in input_mode:
        
        #calculate the discrete points
        discrete_points=Stress.DiscreteValueStress(which_spheres,input_mode,output_mode)
    
    #calculater strain
    if 'strain' in input_mode:
    
        #calculate the discrete points
        discrete_points=Strain.DiscreteValueStrain(which_spheres,input_mode,output_mode)
        
    return Img.ImgFlip(Img.ImgRotate(In.GlobalIDWInterpolation(discrete_points,pixel_step,surface_map)),0)

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
def SubPlot(which_folder_path,input_mode,output_mode,pixel_step,test=False):
    
    this_fig=plt.figure()
    
    #输入文件名
    input_file_names=Pa.ModeFileNames(which_folder_path,input_mode)

    #通用的axis
    global_axis_boundary=AB.GlobalAxisBoundary(which_folder_path)
       
    #输出文件夹的名字
    new_output_folder_path=Pa.OutputFolderPath(which_folder_path,input_mode,output_mode)
    
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
            
            this_spheres=SG.GenerateSpheres(which_folder_path,number-1)[:100]
            
        else:
            
            this_spheres=SG.GenerateSpheres(which_folder_path,number-1)
        
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
def SinglePlot(which_folder_path,input_mode,output_mode,pixel_step,test=False):
     
    #输入文件名
    input_file_names=Pa.ModeFileNames(which_folder_path,input_mode)

    #通用的axis
    global_axis_boundary=AB.GlobalAxisBoundary(which_folder_path)
       
    #输出文件夹的名字
    new_output_folder_path=Pa.OutputFolderPath(which_folder_path,input_mode,output_mode)
    
    #Gnenerate this Folder
    #Medival fold will be generated as well
    Pa.GenerateFold(new_output_folder_path)
    
    #计数器
    count=1
    
    #construct the map between postfix and colormap
    postfix=['.txt','.vtk']
    colormap=['gist_rainbow','seismic'] 
    
    map_postfix_colormap=dict(zip(postfix,colormap))
    
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
        
        #生成颗粒体系
        if test:
            
            this_spheres=SG.GenerateSpheres(which_folder_path,count-1)[:100]
        
        else:
            
            this_spheres=SG.GenerateSpheres(which_folder_path,count-1)  
        
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
                
                    plt.imshow(this_img,cmap=map_postfix_colormap[this_postfix]) 
                
                    break
                
            #坐标轴和边
            Dec.TicksAndSpines(this_ax)
            
#            print(np.array(global_axis_boundary)/pixel_step)
            
            plt.axis(np.array(global_axis_boundary)/pixel_step)
            
        #save this fig
        this_fig.savefig(new_output_folder_path+this_fig_name,dpi=300,bbox_inches='tight')
        
#        last_time=time.time()
        
        count+=1 
        plt.close()  