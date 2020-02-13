# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 16:30:07 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Image smooth
"""

import copy as cp
import numpy as np

#------------------------------------------------------------------------------
"""
Gaussian convolution kernel

Args:
    miu: mathematical expectation of gaussian distribution
    sigma: standard deviation of the gaussian distribution
    kernel_size: size of kernel (n*n)
        
Returns:
    gaussian convolution kernel matrix
"""
def GaussianKernel(miu,sigma,kernel_size):
      
    #kernel_size must be odd
    if kernel_size%2!=1:
        
        print('--ERROR: please redefine the window_size')
        
        return

    #define void kernel
    kernel=np.zeros((kernel_size,kernel_size))
    
    #wingspan
    wingspan=kernel_size//2
    
    #relative_coordinate of guassian kernel
    relative_coordinates=list(np.linspace(-wingspan,wingspan,kernel_size))

    for x in relative_coordinates:
        
        j=int(x+wingspan)
        
        for y in relative_coordinates:

            i=int(y+wingspan)
            
            #value assignment
            kernel[i,j]=np.exp(-(x**2+y**2)/2*sigma**2)/(2*np.pi*sigma**2)
            
    return kernel
        
#------------------------------------------------------------------------------
"""
window matrix

Args:
    which_image: image matrix to be smoothed
    i,j: index if image
    window_size: size of window (n*n)
        
Returns:
    window matrix
"""    
def Window(which_image,i,j,window_size):
    
    #wingspan
    wingspan=window_size//2
    
    #relative_coordinate of window
    relative_coordinates=list(np.linspace(-wingspan,wingspan,window_size))

    #define void window
    window=np.zeros((window_size,window_size))
    
    if wingspan<=i<np.shape(which_image)[0]-wingspan and wingspan<=j<np.shape(which_image)[1]-wingspan:

        for x in relative_coordinates:
            
            this_j=int(x+wingspan)
            
            for y in relative_coordinates:
    
                this_i=int(y+wingspan)

                #value assignment
                window[this_i,this_j]=which_image[i+int(x),j+int(y)]
                
    else:
        
        print('->IndexError: index out of bound')
        
        window[:,:]=window[i,j]
        
    return window

#------------------------------------------------------------------------------
"""
Convolution calculation between window and kernel

Args:
    which_window: matrix with nan
    which_kernel: matrix with weight
        
Returns:
    convolution result (float)
"""
def Convolution(which_window,which_kernel):
    
    if not np.shape(which_window)==np.shape(which_kernel):
        
        print('-- ERROR: Incorrect dimensions')
        
        return
    
    else:
        
        #invalid index list
        list_invalid_index=[]
        
        for i in range(np.shape(which_window)[0]):
            
            for j in range(np.shape(which_window)[1]):
                
                '''expire nan'''
                if np.isnan(which_window[i,j]):
                    
                    list_invalid_index.append([i,j])
                    
        #generate valid index
        for this_i,this_j in list_invalid_index:
            
            opposite_index=[np.shape(which_window)[0]-1-this_i,np.shape(which_window)[1]-1-this_j]
            
            if opposite_index not in list_invalid_index:
                
                list_invalid_index.append(opposite_index)
            
        #valid index list
        list_valid_index=[]
        
        for i in range(np.shape(which_window)[0]):
            
            for j in range(np.shape(which_window)[1]):
                
                this_index=[i,j]
                
                if this_index not in list_invalid_index:
                    
                    list_valid_index.append(this_index)
                    
        if list_valid_index==[]:
            
            return which_window[np.shape(which_window)[0]//2,np.shape(which_window)[1]//2]
        
        else:
            
            real_window=np.zeros(np.shape(which_window))
            real_kernel=np.zeros(np.shape(which_kernel))

            for i,j in list_valid_index:
                
                real_kernel[i,j]=which_kernel[i,j]
                real_window[i,j]=which_window[i,j]
                
            factor=1/np.sum(real_kernel)

            #expand and shrink in a ratio
            for i,j in list_valid_index:
                
                real_kernel[i,j]*=factor
            
            return np.sum(real_window*real_kernel)

#------------------------------------------------------------------------------
"""
Smooth image

Args:
    which_image: image matrix to be smoothed
    smooth_operator: operator which performs (default: Gaussian)
    wingspan: half size of kernel and window    
    
Returns:
    image matrix which has been smoothed
"""
def ImageSmooth(which_image,smooth_operator='Gaussian',wingspan=1):
    
    print('')
    print('-- Image Smooth')
    
    #result image
    smooth_image=cp.deepcopy(which_image)
    
    if smooth_operator=='Gaussian':
        
        #image boundary length
        window_size=2*wingspan+1
        
        #kernel default to be (0,1)
        kernel=GaussianKernel(0,1,window_size)
        
        for i in range(wingspan,np.shape(which_image)[0]-wingspan):
            
            for j in range(wingspan,np.shape(which_image)[1]-wingspan):
                
                smooth_image[i,j]=Convolution(Window(which_image,i,j,window_size),kernel)
    
    return smooth_image[wingspan:-wingspan,wingspan:-wingspan]