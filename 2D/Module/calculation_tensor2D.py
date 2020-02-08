# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:24:46 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculate 2D tensor invariant
"""

import numpy as np

#============================================================================== 
def Tensor1stInvariant(which_tensor):

    I_1=np.trace(which_tensor)
    
#    print(I_1)
    
    return I_1

#============================================================================== 
def Tensor2ndInvariant(which_tensor):
   
#    print(0.5*np.sum(np.multiply(which_tensor,which_tensor))-0.25*np.trace(which_tensor)**2)
    
#    print(np.linalg.det(which_tensor-Tensor1stInvariant(which_tensor)/2))
    
#    print(0.5*which_tensor[0,1]*which_tensor[1,0]-0.25*np.trace(which_tensor)*np.trace(which_tensor))

    diff=which_tensor[0,0]-which_tensor[1,1]
    
#    print((diff/2)**2+0.5*(which_tensor[0,1]**2+which_tensor[1,0]**2))
          
    return (diff/2)**2+0.5*(which_tensor[0,1]**2+which_tensor[1,0]**2)

'''
dot: 矩阵相乘
multiply: 对应元素相乘的矩阵
'''

tensor=np.array([[1,3],[3,2]])

Tensor2ndInvariant(tensor)