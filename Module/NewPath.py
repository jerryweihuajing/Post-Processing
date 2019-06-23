# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 23:37:02 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Sort folders and files-new forms and organizations
"""

'''   
demand: 
restart with a totally new input data

total folder: input
              output
              
input: case 0 
       case 1 
       case 2 
       case ...
       
case x: stress
        cumulative strain
        periodical strain
        
output: structural deformation
        stress
        cumulative strain
        periodical strain

stress: xx stress
        ......
        
strain: xx strain
        ......  
'''

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())
    
from Module import Path as Pa

#==============================================================================
#construct all stress or all strain
#folder_path: total path
#input_mode: 'stress', 'cumulative_strain', 'periodical_strain'
def ModeFileNames(which_case_path,input_mode):
    
    #folder name of one mode
    input_mode_name=input_mode.replace('_',' ')
    
    #path for input
    mode_input_folder_path=which_case_path+'\\'+input_mode_name
    
    #file_names  
    return Pa.GenerateFileNames(mode_input_folder_path)

#==============================================================================
#construct the link between stress txt and strain vtk
def MapsModeFileName(which_case_path):
    
    maps_mode_file_name=[]
    
    #all types of data
    modes=['stress',
           'cumulative_strain',
           'periodical_strain']
    
    stress_file_names,\
    cumulative_strain_file_names,\
    periodical_strain_file_names=[ModeFileNames(which_case_path,this_mode) for this_mode in modes]
    
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
def OutputFolderPath(which_case_path,input_mode,output_mode):
    
    #total data file folder
    total_path=which_case_path.split('\input\\')[0]
    
    #which case
    case_str=which_case_path.split('\input\\')[1]
    
    #case output path
    case_output_path=total_path+'\\output\\'+case_str+'\\'
    
    #output for structural deformation is particle
    if output_mode=='structural_deformation':
        
        return case_output_path+'structural deformation\\'
    
    else:
        
        #folder name of input mode
        input_mode_name=str(input_mode).replace('_',' ')
        
        #folder name of output mode
        output_mode_name=str(output_mode).replace('_',' ')
        
        #output path
        return case_output_path+input_mode_name+'\\'+output_mode_name+'\\' 
    
#case_path=r'C:\魏华敬\Spyder\YADE\Stress Strain\Data\L=1000 v=1.0 r=1.0 layer=10 detachment=0-4\input\case 0'
#
#path_A=OutputFolderPath(case_path,'cumulative_strain','volumetric_strain')
#path_B=OutputFolderPath(case_path,'stress','structural_deformation')