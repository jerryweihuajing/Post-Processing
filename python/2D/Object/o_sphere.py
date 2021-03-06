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
                 velocity=None,
                 stress_tensor=None,             
                 periodical_displacement=None,            
                 cumulative_displacement=None,
                 instantaneous_displacement=None):     
        self.Id=Id
        self.tag=tag
        self.area=area
        self.color=color
        self.plane=plane
        self.radius=radius
        self.position=position
        self.velocity=velocity
        self.stress_tensor=stress_tensor         
        self.periodical_displacement=periodical_displacement      
        self.cumulative_displacement=cumulative_displacement
        self.instantaneous_displacement=instantaneous_displacement
  
    def Init(self):

        #area Calculation
        self.area=np.pi*self.radius**2
        
        #stress
        self.stress_tensor=self.stress_tensor.reshape((3,3))
