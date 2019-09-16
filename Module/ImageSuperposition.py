# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 16:53:27 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Combination of PNG images
"""

'''
png format with RGBA 4 channels: alpha stands for opacity

demand:
combine 2 images on transparency
'''

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------   
"""
Modify opacity of an PNG image and save it

Args:
   which_img: image whose opacity will be modified
   opacity_value: opacity value which will be given
   
Returns:
    modified PNG image
""" 
def ModifyOpacity(which_img,opacity_value):
    
    that_img=cp.deepcopy(which_img)
    
    for i in range(np.shape(that_img)[0]):
        
        for j in range(np.shape(that_img)[1]):
            
            that_img[i,j,3]=opacity_value
    
    return that_img

#------------------------------------------------------------------------------   
"""
Superpose 2 images with a certain opacity

Args:
   image_background: image matrix of background
   image_attachment: image matrix of attachment
       
Returns:
    modified PNG image
""" 
def SuperposeImages(image_background,image_attachment):
    
    plt.subplots()
    plt.imshow(image_background)
    plt.imshow(ModifyOpacity(image_attachment,0.5))
