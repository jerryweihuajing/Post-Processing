# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 17:58:55 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculate 3D tensor invariant
"""

import numpy as np

#============================================================================== 
def Tensor1stInvariant(which_tensor):

    I_1=np.trace(which_tensor)
    
#    print(I_1)
    
    return I_1

#============================================================================== 
def Tensor2ndInvariant(which_tensor):
    
    '''where is dimension from'''
    #set of dimension index
    dimensions=[k for k in range(3)]
    
    #second invariant
    I_2=0
    
    another_I_2=0
    
    for k in range(3):
        
        this_dimensions=[this_dimension for this_dimension in dimensions if this_dimension!=k]
        
#        print(this_dimensions)
        
        #define the index
        i,j=this_dimensions
        
        '''another result'''
        this_shear_product=which_tensor[j,i]*which_tensor[i,j]
        this_normal_product=which_tensor[i,i]*which_tensor[j,j]
        
        this_matrix=np.array([[which_tensor[i,i],which_tensor[i,j]],
                              [which_tensor[j,i],which_tensor[j,j]]])
        
        #accumulate result
        I_2+=np.linalg.det(this_matrix)
        another_I_2+=(this_normal_product-this_shear_product)
#    
#    print(I_2)
#    print(another_I_2)
    
    return I_2

#============================================================================== 
def Tensor3rdInvariant(which_tensor):
    
    I_3=np.linalg.det(which_tensor)
    
#    print(I_3)
    
    return I_3

#which_tensor=np.matrix([[-1.6994  ,  3.228751, -5.73405 ],
#        [ 3.228751,  4.17977 , -2.51342 ],
#        [-5.73405 , -2.51342 ,  1.      ]])
#    
#Tensor1stInvariant(which_tensor)
#Tensor2ndInvariant(which_tensor)
#Tensor3rdInvariant(which_tensor)