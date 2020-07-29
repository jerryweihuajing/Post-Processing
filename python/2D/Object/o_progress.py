# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:34:04 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Object-progress
"""

import os
import copy as cp
import numpy as np

import operation_path as O_P

import calculation_image as C_I
import calculation_matrix as C_M
import calculation_matrix_outline as C_M_O
import calculation_image_smoothing as C_I_S

from o_sphere import sphere

from configuration_list_title import list_title,flag_all
from configuration_yade_color import yade_rgb_list,yade_rgb_map

#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    def __init__(self,
                 path=None,
                 map_tag_id=None,
                 map_id_spheres=None,
                 list_spheres=None,
                 case=None,
                 shape=None,
                 offset=None,
                 percentage=None,
                 rgb_map=None,
                 img_tag=None,
                 structural_deformation=None,
                 structural_deformation_outline=None,
                 fracture=None,
                 map_matrix=None,
                 map_outline=None):
        
        self.path=path
        self.map_tag_id=map_tag_id
        self.map_id_spheres=map_id_spheres
        self.list_spheres=list_spheres
        self.case=case
        self.shape=shape
        self.offset=offset
        self.percentage=percentage
        self.rgb_map=rgb_map
        self.img_tag=img_tag
        self.structural_deformation=structural_deformation
        self.structural_deformation_outline=structural_deformation_outline
        self.fracture=fracture
        self.map_matrix=map_matrix
        self.map_outline=map_outline
        
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
        
            #exception: '-' in the list
            if '-' in this_list:
                
                continue
            
            #define new sphere object
            new_sphere=sphere()
            
            new_sphere.Id=int(this_list[0])
            new_sphere.radius=float(this_list[1])
            new_sphere.color=[float(this_str) for this_str in this_list[2:5]] 
            new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
            new_sphere.velocity=np.array([float(this_str) for this_str in this_list[8:11]])
            new_sphere.stress_tensor=np.array([float(this_str) for this_str in this_list[11:]])
         
            #rgb represent with tag
            new_sphere.tag=yade_rgb_list.index(new_sphere.color)
            
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
        
    def InitOffset(self,progress_path):
        
        #calculate offset
        self.InitCalculation(progress_path)
        
        x_spheres=[this_sphere.position[0] for this_sphere in list(self.map_id_spheres.values())]
        
        self.offset=np.min(x_spheres)
        
    def InitVisualization(self,progress_path,lite):
        
        print('')
        print('-- Init Visualization')
        
        self.path=progress_path
        
        '''compression'''
        if '100-500' in progress_path:
        
            self.shape=(100,500)
            
        if '100-800' in progress_path:
        
            self.shape=(100,800) 
            
        if '100-1000' in progress_path:
            
            self.shape=(100,1000)   
            
        '''extension'''
        if '100-500' in progress_path:
            
            self.shape=(100,500) 
            
        #map between tag and YADE rgb
        self.rgb_map=yade_rgb_map
        
        #progress percentage
        self.percentage=O_P.ProgressPercentageFromTXT(progress_path)
        
        #img tag and img rgb of structural deformation
        self.img_tag=C_M_O.AddBound(C_I_S.TagImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path),bound_value=-1)),bound_value=-1)
        self.structural_deformation=C_I.ImageTag2RGB(self.img_tag,self.rgb_map)
        self.structural_deformation_outline=C_M_O.OutlineFromImgTag(self.img_tag)
        
        if not lite:

            case_path=progress_path.split('\\Structural Deformation')[0]
           
            #init map of matrix and outline
            self.map_matrix={}
            self.map_outline={}
            
            if flag_all:
                
                real_list_title=os.listdir(case_path)

            else:
                
                real_list_title=list_title
                
            for this_title in os.listdir(case_path):
                
                if this_title in real_list_title:
                    
                    if this_title=='Structural Deformation':
                    
                        continue
                    
                    this_matrix_path=progress_path.replace('Structural Deformation',this_title)
                    
                    print('->',this_title)
                    
                    #add bound before smoothing
                    self.map_matrix[this_title]=C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(this_matrix_path))))
                    self.map_outline[this_title]=C_M_O.OutlineFromMatrix(self.map_matrix[this_title])         

            try:
                
                #fracture matrix
                self.fracture=cp.deepcopy(self.map_matrix['Distortional Strain-Cumulative'])
            
            except:
                
                pass
            
            '''outlines are different for the existence of gradient calculation'''