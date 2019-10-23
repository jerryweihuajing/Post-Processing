# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 16:19:07 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Image
"""

'''Rotation and Flipping of an image'''

import numpy as np

#============================================================================== 
#Flip
def ImgFlip(which_img,axis):
      
    #获取img的第三维度   
    if isinstance(which_img[0,0],float):
        
        new_img=np.zeros((np.shape(which_img)[0],np.shape(which_img)[1]))
        
    else:
           
        new_img=np.full((np.shape(which_img)[0],np.shape(which_img)[1],3),np.array(len(which_img[0,0])*[0.0]))
    
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
#Rotate
def ImgRotate(which_img):
      
    #获取img的第三维度   
    if isinstance(which_img[0,0],float):
        
        new_img=np.zeros((np.shape(which_img)[1],np.shape(which_img)[0]))
        
    else:
           
        new_img=np.full((np.shape(which_img)[1],np.shape(which_img)[0],3),np.array(len(which_img[0,0])*[0.0]))
        
    #赋值
    for k in range(np.shape(new_img)[0]):
        
        new_img[k,:]=which_img[:,k]
    
    return new_img

#------------------------------------------------------------------------------
"""
Generate a map between tag and rgb

Args:
    file_path: file path of input file
    
Returns:
    map between tag and rgb
"""
def MapTagRGB(file_path):
    
    #xx.xx%.txt
    post_fix=file_path.split('\\')[-1]

    #re-name
    spheres_path=file_path.replace('output','input')\
                            .replace('\\structural deformation\\values','')\
                            .replace(post_fix,'progress='+post_fix)
                   
    #all lines
    lines=open(spheres_path,'r').readlines()
    
    #exceeding is not allowed
    correct_length=len(lines[0].strip('\n').split(','))
    
    #total color list
    color_list=[]
        
    #build a map
    map_tag_color={}
    map_tag_color[0]=[1.0,1.0,1.0]
    
    for this_line in lines:
      
        this_list=this_line.strip('\n').split(',')
        
        #invalid information line
        if len(this_list)!=correct_length:
            
            continue

        #extract this rgb value
        this_color=[float(this_str) for this_str in this_list[2:5]]
        
        #for the same
        this_stress_tensor=np.array([float(this_str) for this_str in this_list[8:]])
        
        #3D tensor length is correct
        if len(this_stress_tensor)!=9:
            
            continue
        
        #judge if there is inf
        if np.inf in this_stress_tensor or -np.inf in this_stress_tensor:
                    
            continue
        
        #judge if there is nan
        for this_element in this_stress_tensor:
        
            if np.isnan(this_element):
      
                continue
            
        #append
        if this_color not in color_list:
            
            color_list.append(this_color)
    
            map_tag_color[len(color_list)]=this_color
            
    return map_tag_color

#------------------------------------------------------------------------------
"""
Transform a tag image to RGB format

Args:
    img_tag: matrix to be processed
    map_tag_rgb: map between tag and rgb
    
Returns:
    RGB Image
"""
def ImageTag2RGB(img_tag,map_tag_rgb):
    
    #shape of rgb image
    img_rgb_shape=(np.shape(img_tag)[0],np.shape(img_tag)[1],3)
    
    #define new matrix
    img_rgb=np.full(img_rgb_shape,1.0)
    
    #give value to img_rgb
    for i in range(np.shape(img_rgb)[0]):
        
        for j in range(np.shape(img_rgb)[1]):
            
            img_rgb[i,j]=np.array(map_tag_rgb[img_tag[i,j]])

    return img_rgb