# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 14:13:18 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Plot in Custom manner
"""

'''
demand:
draw surface with stress or strain figure
'''

import os
import imageio
import copy as cp
import numpy as np
import matplotlib.pyplot as plt

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
                   'distortional_cumulative_strain']
      
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
                    
                if 'displacement' in this_mode:
                    
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