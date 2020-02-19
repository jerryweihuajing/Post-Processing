# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:34:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Object-progress
"""

import copy as cp
import numpy as np

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_matrix_outline as C_M_O
import calculation_image_smoothing as C_I_S

import operation_path as O_P

from o_sphere import sphere

from variable_yade_color import yade_rgb_list,yade_rgb_map

#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    
    def __init__(self,
                 map_tag_id=None,
                 map_id_spheres=None,
                 list_spheres=None,
                 case=None,
                 shape=None,
                 percentage=None,
                 
                 rgb_map=None,
                 img_tag=None,
                 structural_deformation=None,
                 fracture=None,
                 outline_stress=None,
                 outline_strain=None,
                 outline_velocity=None,
                 outline_displacement=None,
                 map_stress_or_strain=None,
                 map_velocity_or_displacement=None):
        
        self.map_tag_id=map_tag_id
        self.map_id_spheres=map_id_spheres
        self.list_spheres=list_spheres
        self.case=case
        self.shape=shape
        self.percentage=percentage
        
        self.rgb_map=rgb_map
        self.img_tag=img_tag
        self.structural_deformation=structural_deformation
        self.fracture=fracture
        
        self.outline_stress=outline_stress
        self.outline_strain=outline_strain
        self.outline_velocity=outline_velocity
        self.outline_displacement=outline_displacement
        
        self.map_stress_or_strain=map_stress_or_strain
        self.map_velocity_or_displacement=map_velocity_or_displacement
        
    def InitCalculation(self,file_path):
        
        #all lines
        lines=open(file_path,'r').readlines()
        
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
            new_sphere.velocity=np.array([float(this_str) for this_str in this_list[8:11]])
            new_sphere.stress_tensor=np.array([float(this_str) for this_str in this_list[11:]])
         
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
            
            list_spheres.append(new_sphere)
                
        #id and tag list
        list_id=[this_sphere.Id for this_sphere in list_spheres]
        list_tag=[yade_rgb_list.index(this_sphere.color) for this_sphere in list_spheres]
        
        #construct map between id and tag
        map_id_tag=dict(zip(list_id,list_tag))
        
        list_set_tag=list(set(list_tag))
            
        #construct map between tag and id list
        self.map_tag_list_id={}
        
        for this_tag in list_set_tag:
            
            self.map_tag_list_id[this_tag]=[]
            
        for this_id in list_id:
            
            self.map_tag_list_id[map_id_tag[this_id]].append(this_id)
        
        #construct map between id and spheres
        self.map_id_spheres=dict(zip(list_id,list_spheres))
        
    def InitVisualization(self,progress_path,lite):
        
        if '100-500' in progress_path:
        
            self.shape=(100,500)
            
        if '100-1000' in progress_path:
            
            self.shape=(100,1000)   
            
        if '100-200' in progress_path:
            
            self.shape=(100,350) 
            
        #map between tag and YADE rgb
        self.rgb_map=yade_rgb_map
        
        #progress percentage
        self.percentage=O_P.ProgressPercentageFromTXT(progress_path)
        
        #img tag and img rgb of structural deformation
        self.img_tag=C_M.ImportMatrixFromTXT(progress_path)
        self.structural_deformation=C_I.ImageTag2RGB(self.img_tag,self.rgb_map)
        
        if not lite:
            
            list_post_fix=['stress\\mean normal',
                           'stress\\maximal shear',
                           'cumulative strain\\volumetric',
                           'cumulative strain\\distortional',
                           'velocity\\resultant',
                           'cumulative displacement\\resultant',
                           'instantaneous strain\\volumetric',
                           'instantaneous strain\\distortional']
            
            #containing result matrix
            matrix_list=[]
            
            for this_post_fix in list_post_fix:
                
                #stress and strain itself
                file_path=progress_path.replace('structural deformation',this_post_fix)
                
                matrix_list.append(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(file_path))))
                
            self.mean_normal_stress,\
            self.maximal_shear_stress,\
            self.cumulative_volumrtric_strain,\
            self.cumulative_distortional_strain,\
            self.resultant_velocity,\
            self.cumulative_resultant_displacement,\
            self.instantaneous_distortional_strain,\
            self.instantaneous_volumrtric_strain=matrix_list
            
            '''None list to present'''
            #construct a map between post fix name and matrix
            list_title=['Mean Normal Stress',
                        'Maximal Shear Stress',
                        'Volumetric Strain-Cumulative',
                        'Distortional Strain-Cumulative',
                        'Resultant Velocity',
                        'Resultant Displacement-Cumulative',
                        'Volumetric Strain-Instantaneous',
                        'Distortional Strain-Instantaneous']
            
            #stress and strain map
            self.map_stress_or_strain=dict(zip(list_title,matrix_list))
        
            #fracture matrix
            self.fracture=cp.deepcopy(self.map_stress_or_strain['Distortional Strain-Cumulative'])
            
            '''they are different for the existence of gradient calculation'''
            #stress outline
            self.outline_stress=C_M_O.OutlineFromMatrix(self.map_stress_or_strain['Mean Normal Stress'])
         
            #stress outline
            self.outline_strain=C_M_O.OutlineFromMatrix(self.map_stress_or_strain['Volumetric Strain-Cumulative'])
        