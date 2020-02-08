# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:28 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Case Operation
"""

import numpy as np

from o_case import case
from o_sphere import sphere
from o_progress import progress

import operation_path as O_Pa
import operation_progress as O_Pro

import HPC_ProgressPlot as HPC_PP
import HPC_AnimationPlot as HPC_AP
import HPC_IndividualPlot as HPC_IP
import HPC_IntegralAnalysisPlot as HPC_IAP

from data_yade_color import yade_rgb_list

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
    
    that_case.list_progress=[]
    
    #input txt file names
    file_names=O_Pa.FilePathsThisCase(case_path)
    
    #traverse all file to consruct progress
    for this_file_name in file_names:
        
        that_progress=progress()
        
        #all lines
        lines=open(this_file_name,'r').readlines()
        
        #correct legnth of each line
        correct_length=len(lines[0].strip('\n').split(','))
    
        list_spheres=[]
        
        #traverse all lines
        for this_line in lines:
            
            this_list=this_line.strip('\n').split(',')
            
            #judge if total length is OK
            if len(this_list)!=correct_length:
                        
                continue
        
            #define new sphere object
            new_sphere=sphere()
            
            new_sphere.Id=int(this_list[0])
            new_sphere.radius=float(this_list[1])
            new_sphere.color=[float(this_str) for this_str in this_list[2:5]] 
            new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
            new_sphere.stress_tensor=np.array([float(this_str) for this_str in this_list[8:]])
         
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
               
            list_spheres.append(new_sphere)
                
        #id and tag list
        list_id=[this_sphere.Id for this_sphere in list_spheres]
        list_tag=[yade_rgb_list.index(this_sphere.color) for this_sphere in list_spheres]
        
        #construct map between id and tag
        map_id_tag=dict(zip(list_id,list_tag))
        
        list_set_tag=list(set(list_tag))
            
        #construct map between tag and id list
        that_progress.map_tag_list_id={}
        
        for this_tag in list_set_tag:
            
            that_progress.map_tag_list_id[this_tag]=[]
            
        for this_id in list_id:
            
            that_progress.map_tag_list_id[map_id_tag[this_id]].append(this_id)
        
        #construct map between id and spheres
        that_progress.map_id_spheres=dict(zip(list_id,list_spheres))
        
        #case collect progress
        that_case.list_progress.append(that_progress)
        
    #traverse all progress to calculate displacement
    for k in range(len(that_case.list_progress)):
    
        #progress object
        that_progress=that_case.list_progress[k]
        
        #init spheres list    
        that_progress.list_spheres=[]
        
        all_tag=list(that_progress.map_tag_list_id.keys())
        all_id_list=list(that_progress.map_tag_list_id.values())
        
        #first progress
        if k==0:
            
            for this_id in list(that_progress.map_id_spheres.keys()):
                
                current_position=that_progress.map_id_spheres[this_id].position
                
                #give value to displacement
                that_progress.map_id_spheres[this_id].cumulative_displacement=current_position-current_position
                that_progress.map_id_spheres[this_id].periodical_displacement=current_position-current_position
        
                that_progress.map_id_spheres[this_id].Init()
    
        #then
        if k>0:
            
            for kk in range(len(that_progress.map_tag_list_id)):
                
                this_tag=all_tag[kk]
                
                current_list_id_this_tag=all_id_list[kk]
                current_list_spheres_this_tag=[that_progress.map_id_spheres[this_id] for this_id in current_list_id_this_tag]
                current_map_id_spheres_this_tag=dict(zip(current_list_id_this_tag,current_list_spheres_this_tag))
                
                #find last progress with this tag
                for this_progress in that_case.list_progress[k-1::-1]+that_case.list_progress[k:]:
            
                    if this_tag in list(this_progress.map_tag_list_id.keys()):
                            
                        last_list_id_this_tag=this_progress.map_tag_list_id[this_tag]
                        last_list_spheres_this_tag=[this_progress.map_id_spheres[this_id] for this_id in last_list_id_this_tag]
                        last_map_id_spheres_this_tag=dict(zip(last_list_id_this_tag,last_list_spheres_this_tag))
                
                        break
                
                #find 1st progress with this tag
                for this_progress in that_case.list_progress[:k+1]:
                    
                    if this_tag in list(this_progress.map_tag_list_id.keys()):
                        
                        first_list_id_this_tag=this_progress.map_tag_list_id[this_tag]
                        first_list_spheres_this_tag=[this_progress.map_id_spheres[this_id] for this_id in first_list_id_this_tag]
                        first_map_id_spheres_this_tag=dict(zip(first_list_id_this_tag,first_list_spheres_this_tag))
                
                        break
                
                #traverse and calculate displacement
                for this_id in current_list_id_this_tag:
                     
                    current_position=current_map_id_spheres_this_tag[this_id].position
                    first_position=first_map_id_spheres_this_tag[this_id].position
                    last_position=last_map_id_spheres_this_tag[this_id].position
                    
                    #give value to displacement
                    that_progress.map_id_spheres[this_id].cumulative_displacement=current_position-first_position
                    that_progress.map_id_spheres[this_id].periodical_displacement=current_position-last_position
            
                    that_progress.map_id_spheres[this_id].Init()
                
#        for this_sphere in list(that_progress.map_id_spheres.values()):
#            
#            print(this_sphere.cumulative_dispalcement)
#            print(this_sphere.periodical_dispalcement)
#            print(this_sphere.stress_tensor)
    
    return that_case

#------------------------------------------------------------------------------   
"""
Construct a case object (in visualization)

Args:
   case_path: path to construct
   
Returns:
    case object
""" 
def CaseConstruction(case_path):
    
    print('')
    print('-- Case Construction')
    
    #construct case object to save the image data
    that_case=case()
    
    that_case.list_progress=[]
    that_case.condition=case_path.split('\\')[-1]
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=O_Pa.FileNamesThisCase(folder_path)
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
   
        that_case.list_progress.append(O_Pro.ProgressConstruction(structural_deformation_path))
    
    #give them house
    for this_progress in that_case.list_progress:
        
        this_progress.case=that_case
        
    return that_case

#------------------------------------------------------------------------------   
"""
Construct a case object and visualize

Args:
   case_path: path to construct
   output_folder: folder to contain result
   with_farcture: (bool) plot fracture and interface or not 
   
Returns:
    None
""" 
def CaseVisualization(case_path,output_folder,with_fracture=False):
    
    print('')
    print('-- Case Visualization')
    
    #construct a case
    that_case=CaseConstruction(case_path)
    
    #output folder of this case
    case_folder=output_folder+'\\'+that_case.condition
    
    HPC_PP.ProgressAll(case_folder,that_case,with_fracture)   
    HPC_AP.AnimationAll(case_folder,that_case,with_fracture)
    HPC_IAP.IntegralAnalysisAll(case_folder,that_case,with_fracture)
    
    #Individual figures
    for this_progress in that_case.list_progress:
        
        #output folder of this progress
        progress_folder=case_folder+'\\'+this_progress.percentage
        
        #imaging and output
        HPC_IP.AllIndividualsInProgress(progress_folder,this_progress,with_fracture)