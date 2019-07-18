# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 14:24:46 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

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
   
#    return np.linalg.det(which_tensor-Tensor1stInvariant(which_tensor)/2)
    
    return 0.5*which_tensor[0,1]*which_tensor[1,0]-0.25*np.trace(which_tensor)*np.trace(which_tensor)
