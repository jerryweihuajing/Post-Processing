# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:55:07 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-strain_2D
"""


import numpy as np

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())


import Tensor2D as Ts2D

#==============================================================================
#应力张量计算后的相关变量
#==============================================================================  
class strain_2D:
    def __init__(self,
                 strain_tensor=None,                
                 x_normal_strain=None,
                 y_normal_strain=None,
                 shear_strain=None,                 
                 volumetric_strain=None,
                 distortional_strain=None):   
        
        self.strain_tensor=strain_tensor
        self.x_normal_strain=x_normal_strain
        self.y_normal_strain=y_normal_strain
        self.shear_strain=shear_strain      
        self.volumetric_strain=volumetric_strain
        self.distortional_strain=distortional_strain
        
    def Init(self,which_strain_tensor):
        
        which_strain_tensor=np.array(which_strain_tensor)

        #如果是列表改变尺寸
        if isinstance(which_strain_tensor,list):
                
            which_strain_tensor=np.array(which_strain_tensor).reshape((int(np.sqrt(len(which_strain_tensor))),
                               int(np.sqrt(len(which_strain_tensor)))))
        
        else:
            
            #scalar of all elements
            product=np.shape(which_strain_tensor)[0]*np.shape(which_strain_tensor)[1]
                
            which_strain_tensor=which_strain_tensor.reshape((int(np.sqrt(product)),int(np.sqrt(product))))
        
    #    print(which_strain_tensor)
        
        x_normal_strain=which_strain_tensor[0,0]
        y_normal_strain=which_strain_tensor[1,1]
        shear_strain=which_strain_tensor[0,1]+which_strain_tensor[1,0]
        
    #    shear_strain=np.sqrt(which_strain_tensor[0,1]**2+\
    #                         which_strain_tensor[0,2]**2+\
    #                         which_strain_tensor[1,2]**2)
            
        volumetric_strain=Ts2D.Tensor1stInvariant(which_strain_tensor)
        distortional_strain=Ts2D.Tensor2ndInvariant(which_strain_tensor)
             
        #赋值  
        self.strain_tensor=which_strain_tensor
        self.x_normal_strain=x_normal_strain
        self.y_normal_strain=y_normal_strain
        self.shear_strain=shear_strain      
        self.volumetric_strain=volumetric_strain
        self.distortional_strain=distortional_strain
           
##应变张量
#tensor=np.array([[-0.0178654 , -0.00645549,  0.02125459],
#        [-0.00645549,  0.00176057, -0.2979786 ],
#        [ 0.02125459, -0.2979786 ,  0.318659  ]])
#    
#b=Strain2D(tensor)
#
#print(b.strain_tensor,b.volumetric_strain,b.shear_strain)