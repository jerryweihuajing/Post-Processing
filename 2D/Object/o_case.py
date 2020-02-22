# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:35:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Object-case
"""

import operation_path as O_P

import visualization_progress as V_P

from o_progress import progress

#==============================================================================
#object case to manage data efficiently
#==============================================================================    
class case:
    def __init__(self,
                 experiment=None,
                 condition=None,
                 list_progress=None,
                 list_A_progress=None,
                 list_B_progress=None):
        
        self.experiment=experiment
        self.condition=condition
        self.list_progress=list_progress
        self.list_A_progress=list_A_progress
        self.list_B_progress=list_B_progress

    def InitCalculation(self,case_path):
        
        self.list_A_progress=[]
        self.list_B_progress=[]
        
        self.list_surface_map=[]
        
        #input txt file names
        file_paths_A,file_paths_B=O_P.FilePathsAB(case_path)
    
        #traverse all file to consruct progress
        for this_file_path in file_paths_A:
            
            that_progress_A=progress()
            
            that_progress_A.InitCalculation(this_file_path)
            
            #case collect progress
            self.list_A_progress.append(that_progress_A)
            
        #traverse all file to consruct progress
        for this_file_path in file_paths_B:
            
            that_progress_B=progress()
            
            that_progress_B.InitCalculation(this_file_path)
            
            #case collect progress
            self.list_B_progress.append(that_progress_B)
            
        if len(self.list_A_progress)!=len(self.list_B_progress):
            
            print('-> ERROR: Incorrect progress amount')
            
            return
    
        amount_progress=len(self.list_A_progress)
        
        #traverse all progress to calculate displacement
        for k in range(amount_progress):
        
            #progress object
            that_progress_A=self.list_A_progress[k]
            that_progress_B=self.list_B_progress[k]
    
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
                    for this_progress in self.list_A_progress[k-1::-1]+self.list_A_progress[k:]:
                
                        if this_tag in list(this_progress.map_tag_list_id.keys()):
                                
                            last_list_id_this_tag=this_progress.map_tag_list_id[this_tag]
                            last_list_spheres_this_tag=[this_progress.map_id_spheres[this_id] for this_id in last_list_id_this_tag]
                            last_map_id_spheres_this_tag=dict(zip(last_list_id_this_tag,last_list_spheres_this_tag))
                    
                            break
                    
                    #find 1st progress with this tag
                    for this_progress in self.list_A_progress[:k+1]:
                        
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

    def InitVisualization(self,case_path):
        
        self.list_progress=[]
        
        self.experiment=case_path.split('\\')[-3]
        self.condition=case_path.split('\\')[-1]
        
        #strutrual deformation path
        folder_path=case_path+'\\Structural Deformation'
        
        #file names in pogress order
        file_names=O_P.FileNamesThisCase(folder_path)
        
        for file_name in file_names:
            
            #txt file path
            structural_deformation_path=folder_path+'\\'+file_name
           
            self.list_progress.append(V_P.ProgressConstruction(structural_deformation_path,lite=False))
        
        #give them house
        for this_progress in self.list_progress:
            
            this_progress.case=self