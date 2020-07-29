# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:25:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Intrgral Plot
"""

'''
demand:
save matrix as txt or other format

'''
import os
import imageio
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import StressPlot as Stress
import StrainPlot as Strain

import Path as Pa
import Image as Img
import NewPath as NP
import Decoration as Dec
import SpheresPlot as SP
import AxisBoundary as AB
import Interpolation as In
import ValueBoundary as VB
import SpheresBoundary as SB
import SpheresGeneration as SG

import operation_path as O_P
import operation_decoration as O_D

import calculation_norm as C_N
import calculation_image as C_I
import calculation_axis_boundary as C_A_B
import calculation_spheres_matrix as C_S_M
import calculation_spheres_boundary as C_S_B

from o_case import case

#------------------------------------------------------------------------------
"""
Generate case object from case path (in calculation)
Args:
    case_path: load path of all input files
    
Returns:
    A case object
"""
def CaseGeneration(case_path):
    
    #final result
    that_case=case()
    
    that_case.InitCalculation(case_path)
                    
    return that_case

#------------------------------------------------------------------------------
"""
Plot different phase image in a custom style
Args:
    which_case_path: load path of all input files
    which_input_mode: ['structural_deformation',
                       'stress',
                       'velocity',
                       'cumulative_strain',
                       'periodical strain',
                       'instantaneous_strain',
                       'cumulative_displacement',
                       'periodical_displacement',
                       'instantaneous_displacement']
    which_output_mode: '[x_normal',
                        'y_normal',
                        'shear',
                        'mean_normal',
                        'maximal_shear,
                        'volumetric',
                        'distortional',
                        'x',
                        'y',
                        'resultant']
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    pixel_step: length of single pixel (int)
    index_list: custom index of images
    test: if there is a test with a small amount of spheres
    values_only: (bool) whether it saves values only (default: True)
    final_only: (bool) whether it calculate the final progress only (default: True)
    
Returns:
    None
"""
def ModeCalculation(which_case_path,
                    which_input_mode,
                    which_output_mode,
                    which_plane='XoY',
                    which_interpolation='scatters_in_grid',
                    pixel_step=1,
                    test=False,
                    values_only=True,
                    final_only=True):
    
    print('')
    print('-- Mode Calculation')
    print('-> input mode:',which_input_mode.replace('_',' '))
    print('-> output mode:',which_output_mode.replace('_',' '))
    
    #construct case object
    that_case=CaseGeneration(which_case_path)

    #list of spheres and file name list in this case
    if final_only:
        
        spheres_list=[list(this_progress.map_id_spheres.values()) for this_progress in that_case.list_A_progress[-1:]]
        file_names=O_P.FileNamesAB(which_case_path)[0][-1:]

    else:
        
        spheres_list=[list(this_progress.map_id_spheres.values()) for this_progress in that_case.list_A_progress]
        file_names=O_P.FileNamesAB(which_case_path)[0]

    #global axis
    global_axis_boundary=C_A_B.GlobalAxisBoundary(spheres_list)
    
    if which_input_mode=='structural_deformation':
        
        which_output_mode=''
    
    '''Medival fold will be generated as well'''
    output_folder=O_P.OutputFolder(which_case_path,which_input_mode,which_output_mode)
    
    #images and values folder
    images_folder=output_folder+'images\\'
    values_folder=output_folder+'values\\'
    
    #generate these folder
    O_P.GenerateFolder(images_folder)
    O_P.GenerateFolder(values_folder)
     
    #construct the map between postfix and colormap
    if which_input_mode=='stress':
        
        #stress colormap
        colormap='gist_rainbow'
        
        #stress norm
        norm=C_N.StressNorm(spheres_list,which_plane,which_output_mode)
        
    if 'strain' in which_input_mode:
        
        #strain colormap
        colormap='seismic'
        
        #strain norm
        norm=C_N.StrainNorm()
     
    count=1
    
    #figures to generate GIF
    images=[]
    
    #draws the form of different periods
    for k in range(len(spheres_list)):    
                   
        print('')
        print('======')
        
        #file name and progress percentage
        this_file_name=file_names[k]
        this_progress=this_file_name.strip('.txt').strip('A_')
        this_percentage=this_progress.strip('progress=')
        
        print('-->',this_progress)

        #give a name
        this_fig_name=this_percentage+'.png'
        
        #this txt name
        this_txt_name=this_percentage+'.txt'
        
        #spheres system
        this_spheres=spheres_list[k] 
          
        if test:
            
            pixel_step=23 
            
        if not values_only:
            
            #figure and axe
            this_fig=plt.figure(count)
            
            this_ax=plt.subplot()
            
        if which_input_mode=='structural_deformation':
                       
            #Spheres image
            spheres_grids=C_S_M.SpheresImage(this_spheres,pixel_step)
            
            #image
            this_img=C_I.ImgFlip(spheres_grids.img_color,0)
            this_img_tag=C_I.ImgFlip(spheres_grids.img_tag,0)

            if not values_only:
                
                plt.imshow(this_img)
                
            #save as txt
            np.savetxt(values_folder+this_txt_name,this_img_tag,fmt="%.3f",delimiter=",") 
            
        else:
       
            #final matrix
            this_img=C_S_M.SpheresValueMatrix(pixel_step,
                                              this_spheres,
                                              which_plane,
                                              which_input_mode,
                                              which_output_mode,
                                              which_interpolation)
            
            if not values_only:
                
                plt.imshow(C_I.ImgFlip(this_img,0),norm=norm,cmap=colormap) 

            #save as txt
            np.savetxt(values_folder+this_txt_name,this_img,fmt="%.3f",delimiter=",")   
         
        if not values_only:
            
            #draw outline
            C_S_B.SimpleSpheresBoundary(this_spheres,pixel_step,show=True)
            
            #坐标轴和边
            O_D.TicksAndSpines(this_ax)
            plt.axis(np.array(global_axis_boundary)/pixel_step)
            
            #save this fig
            this_fig.savefig(images_folder+this_fig_name,dpi=300,bbox_inches='tight')
            
            #collect fig to create GIF
            images.append(imageio.imread(images_folder+this_fig_name))
        
            plt.close()  
            
        count+=1
        
    if not values_only:
        
        #GIF name
        gif_name=which_output_mode.replace('_',' ')+' '+which_input_mode.replace('_',' ')+'.gif'
        
        #save GIF
        imageio.mimsave(which_case_path.replace('input','output')+'\\'+gif_name,images,duration=0.5)
    
#------------------------------------------------------------------------------   
"""
Total export depending on mode list 
Args:
    which_case_path: load path of all input files
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes 
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    pixel_step: length of single pixel (int)
    mode_list: output mode which user need
    test: if there is a test with a small amount of spheres
    values_only: (bool) whether it saves values only (default: True)
    final_only: (bool) whether it calculate the final progress only (default: True)
    
Returns:
    None
"""    
def CaseCalculation(which_case_path,
                    which_plane='XoY',
                    which_interpolation='scatters_in_grid',
                    pixel_step=1,
                    which_mode_list=None,
                    test=False,
                    values_only=True,
                    final_only=True):
    
    #argument information
    argument_str=''
    
    for this_str in which_case_path.split('\\input\\'):
        
        argument_str+='\\'
        argument_str+=this_str.split('\\')[-1]
        
    print('')
    print('-- Case Calculation')
    print('-> case:',argument_str.strip('\\'))
    
    print('')
    print('...')
    print('......')
     
    #posible condition of stress
    stress_mode=['x_normal',
                 'y_normal',
                 'shear',
                 'mean_normal',
                 'maximal_shear']
    
    #posible condition of strain
    strain_mode=['x_normal',
                 'y_normal',
                 'shear',
                 'volumetric',
                 'distortional']  
    
    #posible condition of velocity
    velocity_mode=['x',
                   'y',
                   'resultant']

    #posible condition of displacement
    displacement_mode=['x',
                       'y',
                       'resultant']
    
    #standard mode of output
    standard_mode=['structural_deformation',
                   'mean_normal_stress',
                   'maximal_shear_stress',
                   'volumetric_cumulative_strain',
                   'distortional_cumulative_strain',
                   'volumetric_instantaneous_strain',
                   'distortional_instantaneous_strain',
                   'resultant_velocity',
                   'resultant_cumulative_displacement']
      
    list_output_mode=['cumulative',
                      'periodical',
                      'instantaneous']
    
    #default: all modes
    if which_mode_list==None:
        
        #structural deformation
        ModeCalculation(which_case_path,
                        'structural_deformation',
                        '',
                        which_plane,
                        which_interpolation,
                        pixel_step,
                        test,
                        values_only,
                        final_only)
                
        #stress
        for this_input_mode in stress_mode:
            
            ModeCalculation(which_case_path,
                            'stress',
                            this_input_mode,
                            which_plane,
                            which_interpolation,
                            pixel_step,
                            test,
                            values_only,
                            final_only)
            
        #strain
        for this_input_mode in strain_mode:
                
            for this_output_mode in list_output_mode:
                
                ModeCalculation(which_case_path,
                                this_output_mode+'_strain',
                                this_input_mode,
                                which_plane,
                                which_interpolation,
                                pixel_step,
                                test,
                                values_only,
                                final_only)
                
        #velocity
        for this_input_mode in velocity_mode:
                
            ModeCalculation(which_case_path,
                            'velocity',
                            this_input_mode,
                            which_plane,
                            which_interpolation,
                            pixel_step,
                            test,
                            values_only,
                            final_only)
            
        #displacement
        for this_input_mode in displacement_mode:
                
            for this_output_mode in list_output_mode:
                
                ModeCalculation(which_case_path,
                                this_output_mode+'_displacement',
                                this_input_mode,
                                which_plane,
                                which_interpolation,
                                pixel_step,
                                test,
                                values_only,
                                final_only)

    else:
        
        #standard for resaerch    
        if which_mode_list=='standard':
                   
            which_mode_list=cp.deepcopy(standard_mode)
       
        #custom and standard mode
        for this_mode in which_mode_list:
            
            #structural deformation
            if this_mode=='structural_deformation':
 
                ModeCalculation(which_case_path,
                                'structural_deformation',
                                '',
                                which_plane,
                                which_interpolation,
                                pixel_step,
                                test,
                                values_only,
                                final_only)
            else:
                
                if 'stress' in this_mode:
                    
                    this_input_mode=this_mode.split('_')[2]
                    this_output_mode=this_mode.split('_')[0]+'_'+this_mode.split('_')[1]
                    
                if 'strain' in this_mode:
                    
                    this_input_mode=this_mode.split('_')[1]+'_'+this_mode.split('_')[2]
                    this_output_mode=this_mode.split('_')[0]
                      
                if 'displacement' in this_mode:
                    
                    this_input_mode=this_mode.split('_')[1]+'_'+this_mode.split('_')[2]
                    this_output_mode=this_mode.split('_')[0]
                    
                if 'velocity' in this_mode:
                    
                    this_input_mode=this_mode.split('_')[1]
                    this_output_mode=this_mode.split('_')[0]
                    
                ModeCalculation(which_case_path,
                                this_input_mode,
                                this_output_mode,
                                which_plane,
                                which_interpolation,
                                pixel_step,
                                test,
                                values_only,
                                final_only)

#------------------------------------------------------------------------------   
"""
Total export depending on mode list of an experiment which contain a branch of cases
Args:
    which_experiment_path: load path of all input files cases
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes 
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    pixel_step: length of single pixel (int)
    mode_list: output mode which user need
    test: if there is a test with a small amount of spheres
    values_only: (bool) whether it saves values only (default: True)
    final_only: (bool) whether it calculate the final progress only (default: True)
    
Returns:
    None
""" 
def ExperimentCalculation(which_experiment_path,
                          which_plane='XoY',
                          which_interpolation='scatters_in_grid',
                          pixel_step=1,
                          which_mode_list=None,
                          test=False,
                          values_only=True,
                          final_only=True):
    
    #traverse
    for this_case_name in os.listdir(which_experiment_path+'\\input'):
        
        this_case_path=which_experiment_path+'\\input\\'+this_case_name
        
        CaseCalculation(this_case_path,
                        which_plane,
                        which_interpolation,
                        pixel_step,
                        which_mode_list,
                        test,
                        values_only,
                        final_only)  
        
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