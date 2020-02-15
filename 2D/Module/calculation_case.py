# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:49:19 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Case Operation in calculation
"""

import numpy as np

from o_case import case
from o_sphere import sphere
from o_progress import progress

import operation_path as O_P

from variable_yade_color import yade_rgb_list

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
    file_paths_A,file_paths_B=O_P.FilePathsAB(case_path)

    #traverse all file to consruct progress
    for this_file_path in file_paths_A:
        
        that_progress_A=progress()
        
        that_progress_A.Init(this_file_path)
        
        #case collect progress
        that_case.list_A_progress.append(that_progress_A)
        
    #traverse all file to consruct progress
    for this_file_path in file_paths_B:
        
        that_progress_B=progress()
        
        that_progress_B.Init(this_file_path)
        
        #case collect progress
        that_case.list_B_progress.append(that_progress_B)
        
    if len(that_case.list_A_progress)!=len(that_case.list_B_progress):
        
        print('-> ERROR: Incorrect progress amount')
        
        return

    amount_progress=len(that_case.list_A_progress)
    
    #traverse all progress to calculate displacement
    for k in range(amount_progress):
    
        #progress object
        that_progress_A=that_case.list_A_progress[k]
        that_progress_B=that_case.list_B_progress[k]

        all_tag=list(that_progress_A.map_tag_list_id.keys())
        all_id_list=list(that_progress_A.map_tag_list_id.values())
        
        '''instantaneous displacement'''
        for this_id in list(that_progress_A.map_id_spheres.keys()):
        
            #A: start, B: end
            position_A=that_progress_A.map_id_spheres[this_id].position
            position_B=that_progress_B.map_id_spheres[this_id].position
            
            try:
                
                #give value to displacement
                that_progress_A.map_id_spheres[this_id].instantaneous_displacement=position_A-position_B

            except:
                
                pass
            
        '''cumulative and periodical displacement'''
        #first progress
        if k==0:
            
            for this_id in list(that_progress_A.map_id_spheres.keys()):
                
                current_position=that_progress_A.map_id_spheres[this_id].position
                
                #give value to displacement
                that_progress_A.map_id_spheres[this_id].cumulative_displacement=current_position-current_position
                that_progress_A.map_id_spheres[this_id].periodical_displacement=current_position-current_position
    
        #then
        if k>0:
            
            for kk in range(len(that_progress_A.map_tag_list_id)):
                
                this_tag=all_tag[kk]
                
                current_list_id_this_tag=all_id_list[kk]
                current_list_spheres_this_tag=[that_progress_A.map_id_spheres[this_id] for this_id in current_list_id_this_tag]
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
                    
                    #give value to displacement
                    try:
                        
                        first_position=first_map_id_spheres_this_tag[this_id].position
                        that_progress_A.map_id_spheres[this_id].cumulative_displacement=current_position-first_position
                    
                    except:
                        
                        pass
                    
                    try:
                        
                        last_position=last_map_id_spheres_this_tag[this_id].position
                        that_progress_A.map_id_spheres[this_id].periodical_displacement=current_position-last_position
                    
                    except:
                        
                        pass
                    
    return that_case