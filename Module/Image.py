# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:19:07 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Image Transformation
"""

'''Rotation and Flipping of an image'''

import numpy as np

#============================================================================== 
#翻转
def ImgFlip(which_img,axis):
    
#    print(which_img)
#    print(which_img[0,0])
#    print(type(which_img[0,0]))
#    print(which_img[0,0].dtype)
    
    #获取img的第三维度   
    if isinstance(which_img[0,0],float):
        
        new_img=np.zeros((np.shape(which_img)[0],np.shape(which_img)[1]))
        
    else:
           
        new_img=np.full((np.shape(which_img)[0],np.shape(which_img)[1],3),np.array(len(which_img[0,0])*[0.0]))
    
#    print(np.shape(new_img))  
#    print(np.shape(which_img)) 
    
    #沿x轴翻转
    if axis==0 or axis=='x':
        
        for i in range(np.shape(which_img)[0]):
                        
            new_img[i,:]=which_img[-(1+i),:]
            
    #沿x轴翻转
    if axis==1 or axis=='y':
        
        for j in range(np.shape(which_img)[1]):
                        
            new_img[:,j]=which_img[:,-(1+j)]  
                
    return new_img

#==============================================================================     
#旋转：
def ImgRotate(which_img):
    
#    print(which_img[0,0])

#    print(type(which_img[0,0]))
#    print(which_img[0,0].dtype)
    
    #获取img的第三维度   
    if isinstance(which_img[0,0],float):
        
        new_img=np.zeros((np.shape(which_img)[1],np.shape(which_img)[0]))
        
    else:
           
        new_img=np.full((np.shape(which_img)[1],np.shape(which_img)[0],3),np.array(len(which_img[0,0])*[0.0]))
    
#    print(new_img)
#    print(np.shape(new_img))  
#    print(np.shape(which_img)) 
    
    #赋值
    for k in range(np.shape(new_img)[0]):
        
        new_img[k,:]=which_img[:,k]
    
    return new_img