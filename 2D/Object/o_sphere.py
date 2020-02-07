# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:54:11 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-sphere
"""

import numpy as np

#==============================================================================
#pos表示离散点的三维坐标
#X,Y,Z: discrete point 3 attributes
#==============================================================================  
class sphere:
    def __init__(self,
                 Id=None,
                 tag=None,
                 area=None,
                 color=None,
                 plane=None,
                 radius=None,
                 position=None,
                 stress_tensor=None,             
                 periodical_strain_tensor=None,
                 cumulative_strain_tensor=None,        
                 periodical_displacement=None,            
                 cumulative_displacement=None):     
       
        self.Id=Id
        self.tag=tag
        self.area=area
        self.color=color
        self.plane=plane
        self.radius=radius
        self.position=position
        self.stress_tensor=stress_tensor         
        self.periodical_strain_tensor=periodical_strain_tensor
        self.cumulative_strain_tensor=periodical_strain_tensor  
        self.periodical_displacement=periodical_displacement      
        self.cumulative_displacement=cumulative_displacement
        
    #将张量转化为三维,生成应力二维张量   
    def Init(self):
        
        print('-- sphere.Init')
        
        #Area Calculation
        self.area=np.pi*self.radius**2
        
        #stress
        self.stress_tensor=self.stress_tensor.reshape((3,3))

        #judge the type
        #cumulative
        if isinstance(self.cumulative_strain_tensor,list):
            
            self.self.cumulative_strain_tensor=[float(this_str) for this_str in self.cumulative_strain_tensor.split()]
        
        if isinstance(self.cumulative_strain_tensor,np.matrix):
            
            self.cumulative_strain_tensor=[float(self.cumulative_strain_tensor[i,j]) for i in range(3) for j in range(3)]  
        
        #periodical
        if isinstance(self.periodical_strain_tensor,list):
            
            self.periodical_strain_tensor=[float(this_str) for this_str in self.periodical_strain_tensor.split()]
        
        if isinstance(self.periodical_strain_tensor,np.matrix):
            
            self.periodical_strain_tensor=[float(self.periodical_strain_tensor[i,j]) for i in range(3) for j in range(3)]
             