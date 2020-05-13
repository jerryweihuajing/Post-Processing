# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:57:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Sort folders and files
"""

import os

import operation_dictionary as O_D
 
#==============================================================================
#获取目标路径下所有文件名         
def FileNames(file_dir,post_fix=None):   
    
    #output
    files_names=[]   
    
    for root, dirs, files in os.walk(file_dir):  
        
        #based on post fix
        if post_fix is not None:
            
            for this_file in files: 
                
                if os.path.splitext(this_file)[1]==post_fix: 
                    
                    files_names.append(os.path.join(root,this_file))  
        
        #normal        
        else:
            
            for this_file in files:  
            
                files_names.append(this_file)
            
    return files_names 

#============================================================================== 
#根据文件夹路径生成文件名列表
def GenerateFileNames(folder_path):
    
    #获取目标路径下所有文件名
    file_names=FileNames(folder_path)
    
    #建立进度与文件名的映射列表
    map_progress_file_name={}
    
    #重新排序
    for this_file_name in file_names:
        
    #    print(this_file_name)

        '''refresh from YADE'''
        if '.vtk' in this_file_name:
            
            init=this_file_name.strip('.vtk').strip('progress').strip('=').split('%')
            
        if '.txt' in this_file_name:
                
            init=this_file_name.strip('.txt').strip('progress').strip('=').split('%')
                
    #    print(init[0],'stress')   
        
        #提取出进展
        progress=float(init[0])
        
    #    print(progress)
        
        map_progress_file_name[progress]=this_file_name
        
    #print(map_progress_file_name)
    
    #对file_names进行排序 
    new_map_progress_file_name=O_D.DictSortByIndex(map_progress_file_name,sorted(list(map_progress_file_name.keys())))
    
    #返回新的文件名
    return list(new_map_progress_file_name.values())

#==============================================================================
#construct all stress or all strain
#folder_path: total path
#input_mode: 'stress', 'cumulative_strain', 'periodical_strain'
def ModeFileNames(folder_path,input_mode):
      
    #total input path
    input_folder_path=folder_path+'\input'
    
    #folder name of one mode
    input_mode_name=input_mode.replace('_',' ')
    
    #path for input
    mode_input_folder_path=input_folder_path+'\\'+input_mode_name
    
    #file_names  
    return GenerateFileNames(mode_input_folder_path)

#==============================================================================
#construct the link between stress txt and strain vtk
def MapsModeFileName(folder_path):
    
    maps_mode_file_name=[]
    
    #all types of data
    modes=['stress',
           'cumulative_strain',
           'periodical_strain']
    
    stress_file_names,\
    cumulative_strain_file_names,\
    periodical_strain_file_names=[ModeFileNames(folder_path,this_mode) for this_mode in modes]
    
    for k in range(len(stress_file_names)):
        
        #create the map between mode and file name
        map_mode_file_name={}
        
        map_mode_file_name['stress']=stress_file_names[k]
        map_mode_file_name['cumulative_strain']=cumulative_strain_file_names[k]
        map_mode_file_name['periodical_strain']=periodical_strain_file_names[k]
        
        maps_mode_file_name.append(map_mode_file_name)
        
    return maps_mode_file_name

#============================================================================== 
#calculate output folder path
def OutputFolderPath(which_folder_path,input_mode,output_mode):
    
    #output for structural deformation is particle
    if output_mode=='structural_deformation':
        
        return which_folder_path+'\\output\\structural deformation\\'
    
    else:
        
        #folder name of input mode
        input_mode_name=str(input_mode).replace('_',' ')
        
        #folder name of output mode
        output_mode_name=str(output_mode).replace('_',' ')
        
        #输出路径
        output_folder_path=which_folder_path+'\\output\\'+input_mode_name
        
        #图片输出路径
        return output_folder_path+'\\'+output_mode_name+'\\'