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
#==============================================================================  
class sphere:
    def __init__(self,
                 Id=None,
                 tag=None,
                 area=None,
                 color=None,
                 radius=None,
                 position=None,
                 stress_tensor_3D=None,
                 stress_tensor_2D=None,
                 strain_tensor_3D_periodical=None,
                 strain_tensor_2D_periodical=None,
                 strain_tensor_3D_cumulative=None,
                 strain_tensor_2D_cumulative=None,
                 displacemnet_3D_periodical=None,
                 displacemnet_2D_periodical=None,
                 displacemnet_3D_cumulative=None,
                 displacemnet_2D_cumulative=None,):       
        self.Id=Id
        self.tag=tag
        self.area=area
        self.color=color
        self.radius=radius
        self.position=position
        self.stress_tensor_3D=stress_tensor_3D
        self.stress_tensor_2D=stress_tensor_2D
        self.strain_tensor_3D_periodical=strain_tensor_3D_periodical
        self.strain_tensor_2D_periodical=strain_tensor_2D_periodical
        self.strain_tensor_3D_cumulative=strain_tensor_3D_cumulative
        self.strain_tensor_2D_cumulative=strain_tensor_2D_cumulative
        self.displacemnet_3D_periodical=displacemnet_3D_periodical
        self.displacemnet_2D_periodical=displacemnet_2D_periodical
        self.displacemnet_3D_cumulative=displacemnet_3D_cumulative
        self.displacemnet_2D_cumulative=displacemnet_2D_cumulative
        
    #将张量转化为三维,生成应力二维张量   
    def Init(self):
        
        #stress
        self.stress_tensor_3D=self.stress_tensor_3D.reshape((3,3))
        self.stress_tensor_2D=np.zeros((2,2))
          
        #直接截取
        self.stress_tensor_2D=self.stress_tensor_3D[:2,:2]
        
        #面积计算
        self.area=np.pi*self.radius**2
        
        #judge the type
        #cumulative
        if isinstance(self.strain_tensor_3D_cumulative,list):
            
            self.strain_tensor_3D_cumulative=[float(this_str) for this_str in self.strain_tensor_3D_cumulative.split()]
        
        if isinstance(self.strain_tensor_3D_cumulative,np.matrix):
            
            self.strain_tensor_3D_cumulative=[float(self.strain_tensor_3D_cumulative[i,j]) for i in range(3) for j in range(3)]  
        
        #periodical
        if isinstance(self.strain_tensor_3D_periodical,list):
            
            self.strain_tensor_3D_periodical=[float(this_str) for this_str in self.strain_tensor_3D_periodical.split()]
        
        if isinstance(self.strain_tensor_3D_periodical,np.matrix):
            
            self.strain_tensor_3D_periodical=[float(self.strain_tensor_3D_periodical[i,j]) for i in range(3) for j in range(3)]
            
        #Init displacement
        self.displacemnet_2D_cumulative=self.displacemnet_3D_cumulative[:2]
        self.displacemnet_2D_periodical=self.displacemnet_3D_periodical[:2]
        
        
        