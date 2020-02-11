# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 00:25:15 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Generate spheres with displacement(New Version)
"""

import numpy as np

from o_sphere import sphere

import NewPath as NP

#------------------------------------------------------------------------------
"""
Generate sample spheres position

Args:
    case_path: load path of all input files
    
Returns:
    sample spheres position lists
"""
def SamplePos(case_path):

    #path of sample
    sample_path=case_path.split('input')[0]+'sample.txt'
    
    #all lines of sample
    sample_lines=open(sample_path,'r').readlines()[1:]
    
    #position of sample
    sample_pos=[]
    
    for this_line in sample_lines:
        
        this_list=this_line.strip('\n').split('\t')
        
        #position of this sphere
        this_pos=np.array([float(item) for item in this_list[:3]])
    
        #collect pos
        sample_pos.append(this_pos)
        
    return sample_pos

#------------------------------------------------------------------------------
"""
Generate spheres position in a progress

Args:
    file_path: load path of file
    
Returns:
    spheres position list in a progress
"""
def ProgressPos(file_path):
    
    #position of spheres in a progress
    progress_pos=[]
    
    #all lines
    lines=open(file_path,'r').readlines()
    
    #correct legnth of each line
    correct_length=len(lines[0].strip('\n').split(','))
    
    #traverse all lines
    for this_line in lines:
        
        this_list=this_line.strip('\n').split(',')
 
        #judge if total length is OK
        if len(this_list)!=correct_length:
            
            continue
          
        progress_pos.append(np.array([float(this_str) for this_str in this_list[5:8]]))
        
    return progress_pos
        
#------------------------------------------------------------------------------    
"""
Generate spheres position in different progress in a case

Args:
    case_path: load path of all input files
    
Returns:
    list which contain spheres position list of differnet progress
"""
def AllProgressPos(case_path):
    
    #input txt file names
    file_names=NP.FilePathsThisCase(case_path)
    
    return [ProgressPos(this_file_name) for this_file_name in file_names]
      
#------------------------------------------------------------------------------
"""
Generate spheres map in a case with assistance of sample.txt

Args:
    case_path: load path of all input files
    
Returns:
    A map whose values are spheres lists
"""
def GenerateSpheresMapWithSample(case_path):
    
    #Generate sample spheres position
    sample_pos=SamplePos(case_path)
        
    #spheres position in different progresss in a case
    all_progress_pos=AllProgressPos(case_path)

    #all input data in this path
    file_paths=NP.FilePathsThisCase(case_path)
    
    #spheres map in all progress
    map_all_progress_spheres={}
    
    #traverse all file names
    for k in range(len(file_paths)):
    
        file_path_this_progress=file_paths[k]
        
        #all lines
        lines_this_progress=open(file_path_this_progress,'r').readlines()
        
        #list of sphere objects
        spheres_this_progress=[]
            
        #position of spheres in last progress
        #1st progress
        if not k:
            
            spheres_pos_last_progress=all_progress_pos[k]
            
        #from index 1
        if k:
                       
            spheres_pos_last_progress=all_progress_pos[k-1]

        for kk in range(len(spheres_pos_last_progress)):
      
            this_list=lines_this_progress[kk].strip('\n').split(',')
        
            #define new sphere object
            new_sphere=sphere()
            
            new_sphere.Id=float(this_list[0])
            new_sphere.radius=float(this_list[1])
            new_sphere.color=np.array([float(this_str) for this_str in this_list[2:5]])   
            new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
            new_sphere.stress_tensor=np.array([float(this_str) for this_str in this_list[8:]])
         
            #calculate displacement
            new_sphere.cumulative_displacemnet=new_sphere.position-sample_pos[kk]
            new_sphere.periodical_displacemnet=new_sphere.position-spheres_pos_last_progress[kk]
            
            #plane: default XoY
            new_sphere.plane='XoY'
            
            #3D tensor length is correct
            if len(new_sphere.stress_tensor)!=9:
                
                continue
            
            #judge if there is inf
            if np.inf in new_sphere.stress_tensor or -np.inf in new_sphere.stress_tensor:
                     
                continue
            
            #judge if there is nan
            for this_element in new_sphere.stress_tensor:
            
                if np.isnan(this_element):
      
                    continue
            
            new_sphere.Init()
            
            spheres_this_progress.append(new_sphere)
              
        #collect it
        map_all_progress_spheres[k]=spheres_this_progress
        
    return map_all_progress_spheres