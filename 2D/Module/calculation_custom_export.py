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
import copy as cp
import numpy as np
import operation_path as O_P

import calculation_image as C_I
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
    which_mode_list: ['structural_deformation',
                      'stress',
                      'velocity',
                      'cumulative_strain',
                      'periodical strain',
                      'instantaneous_strain']
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    pixel_step: length of single pixel (int)
    test: if there is a test with a small amount of spheres
    final_only: (bool) whether it calculate the final progress only (default: True)
    
Returns:
    None
"""
def CaseCalculation(which_case_path,
                    which_mode_list=None,
                    which_plane='XoY',
                    which_interpolation='scatters_in_grid',
                    pixel_step=1,
                    test=False,
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
    
    #standard mode of output
    standard_mode=['structural_deformation',
                   'stress',
                   'velocity',
                   'cumulative_strain',
                   'periodical_strain',
                   'instantaneous_strain']
    
    #default: all modes
    if which_mode_list==None:
        
        which_mode_list=cp.deepcopy(standard_mode)
        
    if test:
            
        pixel_step=23 
            
    #construct case object
    that_case=CaseGeneration(which_case_path)

    #list of surface map
    list_surface_map=[C_S_B.SpheresTopMap(list(this_progress_A.map_id_spheres.values()),pixel_step) for this_progress_A in that_case.list_A_progress]
    
    #list of spheres and file name list in this case
    if final_only:
        
        spheres_list=[list(this_progress.map_id_spheres.values()) for this_progress in that_case.list_A_progress[-1:]]
        file_names=O_P.FileNamesAB(which_case_path)[0][-1:]

    else:
        
        spheres_list=[list(this_progress.map_id_spheres.values()) for this_progress in that_case.list_A_progress]
        file_names=O_P.FileNamesAB(which_case_path)[0]
    
    '''Medival fold will be generated as well'''
    output_folder=which_case_path.replace('input','output')
    
    #draws the form of different periods
    for k in range(len(spheres_list)):    
                   
        #file name and progress percentage
        this_file_name=file_names[k]
        this_progress=this_file_name.strip('.txt').strip('A_')
        this_percentage=this_progress.strip('progress=')
        this_surface_map=list_surface_map[k]
        
        print('')
        print('-->',this_progress)
        print('======')
        
        #this txt name
        this_txt_name=this_percentage+'.txt'
        
        #spheres system
        this_spheres=spheres_list[k] 
            
        for this_mode in which_mode_list:

            print('')
            print('---> input mode:',this_mode.replace('_',' '))
                
            if this_mode=='structural_deformation':
                
                values_folder=output_folder+'\\structural deforamtion'
                
                O_P.GenerateFolder(values_folder)
                
                #Spheres image
                spheres_grids=C_S_M.SpheresImage(this_spheres,pixel_step)
                
                #image
                this_img=C_I.ImgFlip(spheres_grids.img_color,0)
                this_img_tag=C_I.ImgFlip(spheres_grids.img_tag,0)
    
                #save as txt
                np.savetxt(values_folder+'\\'+this_txt_name,this_img_tag,fmt="%.3f",delimiter=",") 
    
            else:
           
                #final matrix map
                map_matrix=C_S_M.SpheresValueMatrix(pixel_step,
                                                    this_spheres,
                                                    which_plane,
                                                    this_mode,
                                                    this_surface_map,
                                                    which_interpolation)
                
                for kk in range(len(map_matrix)):
                    
                    #folder name and matrix
                    this_name,this_img=list(map_matrix.items())[kk]
                    
                    values_folder=output_folder+'\\'+this_name
                    
                    O_P.GenerateFolder(values_folder)
                    
                    #save as txt
                    np.savetxt(values_folder+'\\'+this_txt_name,this_img,fmt="%.3f",delimiter=",")   
                
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
                          final_only=True):
    
    #traverse
    for this_case_name in os.listdir(which_experiment_path+'\\input'):
        
        this_case_path=which_experiment_path+'\\input\\'+this_case_name

        CaseCalculation(this_case_path,
                        which_mode_list,
                        which_plane,
                        which_interpolation,
                        pixel_step,
                        test,
                        final_only)        