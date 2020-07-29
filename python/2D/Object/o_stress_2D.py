# -*- coding: utf-8 -*-
"""
Created on Wed May  8 15:28:07 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-stress_2D
"""

'''
INPUT:应力张量σ_ij
OUTPUT:
    应力主值σ_max,σ_min,
    剪应力主值τ_max,τ_min,
    应力偏量σ_m,
    差异应力σ_d,

应力张量:
σ_ij=|σ_x  τ_xy|
     |τ_xy σ_y |

平均应力:
σ_m=(σ_x+σ_y)/2=(σ_max+σ_min)/2

差异应力：
σ_d=σ_max-σ_min

最大剪切应力：
τ_max=σ_d/2
'''

import numpy as np

#==============================================================================
#应力张量计算后的相关变量
#σ_x,σ_y:x,y方向上的正应力
#平均应力:σ_m=(σ_x+σ_y)/2=(σ_max+σ_min)/2
#差异应力:σ_d=σ_max-σ_min
#最大剪切应力:τ_max=σ_d/2
#==============================================================================  
class stress_2D:
    def __init__(self,
                 stress_tensor=None,
                 x_normal_stress=None,
                 y_normal_stress=None,                 
                 mean_normal_stress=None,
                 differential_normal_stress=None,
                 maximal_normal_stress=None,
                 minimal_normal_stress=None,                
                 shear_stress=None,
                 maximal_shear_stress=None,
                 minimal_shear_stress=None,                
                 orientation_maximal_normal_stress=None,
                 orientation_minimal_normal_stress=None,
                 orientation_maximal_shear_stress=None,
                 orientation_minimal_shear_stress=None): 
        
        self.stress_tensor=stress_tensor
        self.x_normal_stress=x_normal_stress
        self.y_normal_stress=y_normal_stress
        
        self.mean_normal_stress=mean_normal_stress
        self.differential_normal_stress=differential_normal_stress
        self.maximal_normal_stress=maximal_normal_stress
        self.minimal_normal_stress=minimal_normal_stress
        
        self.shear_stress=shear_stress
        self.maximal_shear_stress=maximal_shear_stress
        self.minimal_shear_stress=minimal_shear_stress
        
        self.orientation_maximal_normal_stress=orientation_maximal_normal_stress
        self.orientation_minimal_normal_stress=orientation_minimal_normal_stress
        self.orientation_maximal_shear_stress=orientation_maximal_shear_stress
        self.orientation_minimal_shear_stress=orientation_minimal_shear_stress
        
    def Init(self,stress_tensor):
        
        #如果是列表改变尺寸
        if isinstance(stress_tensor,list):
            
            stress_tensor=np.array(stress_tensor).reshape((int(np.sqrt(len(stress_tensor))),int(np.sqrt(len(stress_tensor)))))
        
        #张应力
        x_normal_stress=stress_tensor[0,0]
        y_normal_stress=stress_tensor[1,1]
        
        #平均应力
        mean_normal_stress=(x_normal_stress+y_normal_stress)/2
        
        #print(σ_m)
        
        #剪应力
        shear_stress=(stress_tensor[0,1]+stress_tensor[1,0])/2
        
        #计算最大最小主应力
        #剪应力
        maximal_shear_stress=+np.sqrt((x_normal_stress-y_normal_stress)**2+shear_stress**2)
        minimal_shear_stress=-np.sqrt((x_normal_stress-y_normal_stress)**2+shear_stress**2)
        
    #    print(τ_max,τ_min)
        
        #正应力
        maximal_normal_stress=mean_normal_stress+maximal_shear_stress
        minimal_normal_stress=mean_normal_stress+minimal_shear_stress
        
    #    print(σ_max,σ_min)
        
        #差异应力
        differential_normal_stress=maximal_normal_stress-minimal_normal_stress
        
    #    print(σ_m,σ_d)
        
        #正应力对应的主方向
        orientation_maximal_normal_stress=np.arctan(2*shear_stress/(x_normal_stress-y_normal_stress))
        orientation_minimal_normal_stress=orientation_maximal_normal_stress+np.pi/2
        
    #    print(θ_σ_max,θ_σ_min)
        
        #剪应力对应的主方向
        orientation_maximal_shear_stress=orientation_maximal_normal_stress+np.pi/4
        orientation_minimal_shear_stress=orientation_maximal_normal_stress-np.pi/4
    
    #    print(θ_τ_max,θ_τ_min)
               
        #赋值  
        self.stress_tensor=stress_tensor
        self.x_normal_stress=x_normal_stress
        self.y_normal_stress=y_normal_stress
        
        self.mean_normal_stress=mean_normal_stress
        self.differential_normal_stress=differential_normal_stress
        self.maximal_normal_stress=maximal_normal_stress
        self.minimal_normal_stress=minimal_normal_stress
        
        self.shear_stress=shear_stress
        self.maximal_shear_stress=maximal_shear_stress
        self.minimal_shear_stress=minimal_shear_stress
        
        self.orientation_maximal_normal_stress=orientation_maximal_normal_stress
        self.orientation_minimal_normal_stress=orientation_minimal_normal_stress
        self.orientation_maximal_shear_stress=orientation_maximal_shear_stress
        self.orientation_minimal_shear_stress=orientation_minimal_shear_stress
        
    
##应力张量
#σ_ij=[-10,9,9,5]
#
#a=stress_2D()
#
#a.Init(σ_ij)