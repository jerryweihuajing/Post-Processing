# -*- coding: utf-8 -*-
"""
Created on Sat May 30 13:44:29 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-boundary extraction
"""

import numpy as np

def Erode(which_content):
        
    #逆时针遍历邻域内的点
    #领域核
    neighbordict=[(i,j) for i in [-1,0,1] for j in [-1,0,1]]
    
    #腐蚀操作后的结果
    new_content=[]
    
    for pos in which_content:
        
        #8邻域
        neighbor=[]    

        #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
        for item in neighbordict:
                  
            #遍历新的坐标
            new_i=pos[0]+item[0]
            new_j=pos[1]+item[1]
            
            #前提是这个点的位置是有效的
            if [new_i,new_j] in which_content:
                
                neighbor.append(True)          
            else:
                neighbor.append(False)

        #领域值是否都相等        
        if neighbor==len(neighbor)*[True]:
            
            new_content.append(pos)
    
    return new_content
    
#膨胀运算
def Expand(which_content):
  
    #逆时针遍历邻域内的点
    #领域核
    neighbordict=[(i,j) for i in [-1,0,1] for j in [-1,0,1]]
    
    #膨胀操作后的结果
    new_content=[]
    
    for pos in which_content:
        
        #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
        for item in neighbordict:
            
            #遍历新的坐标
            new_i=pos[0]+item[0]
            new_j=pos[1]+item[1]
            
            #增加新的点儿
            if [new_i,new_j] not in which_content:
                
                new_content.append([new_i,new_j])
                        
    return new_content
        
def TagBoundaryExtraction(img_tag_ROI,
                          method='erosion',
                          tag_foreground=None,
                          tag_background=None):
    
    #binary image
    img_binary=np.zeros(np.shape(img_tag_ROI))
    
    if tag_foreground!=None:
        
        img_binary[img_tag_ROI==tag_foreground]=1
    
    if tag_background!=None:
        
        img_binary[img_tag_ROI!=tag_background]=1
        
    content_ROI=[[i,j] for i in range(np.shape(img_binary)[0]) for j in range(np.shape(img_binary)[1]) if img_binary[i,j]==1]
    
    #extraction boundary
    if method=='erosion':
    
        content_boundary=[item for item in content_ROI if item not in Erode(content_ROI)]
    
    if method=='expansion':
        
        content_boundary=[item for item in Expand(content_ROI) if item not in content_ROI]
        
    #new binary image
    img_boundary=np.zeros(np.shape(img_binary))
    
    for i,j in content_boundary:
        
        img_boundary[i,j]=1
    
    for i in range(np.shape(img_boundary)[0]):
        
        for j in range(np.shape(img_boundary)[1]):
            
            if img_boundary[i,j]==0:
                
                img_boundary[i,j]=np.nan
                
    return img_boundary

def NanBoundaryExtraction(img_ROI,method='erosion'):
    
    #binary image
    img_binary=np.zeros(np.shape(img_ROI))
    
    for i in range(np.shape(img_ROI)[0]):
        
        for j in range(np.shape(img_ROI)[1]):
            
            if not np.isnan(img_ROI[i,j]):
                
                img_binary[i,j]=1

    content_ROI=[[i,j] for i in range(np.shape(img_binary)[0]) for j in range(np.shape(img_binary)[1]) if img_binary[i,j]==1]
    
    #extraction boundary
    if method=='erosion':
    
        content_boundary=[item for item in content_ROI if item not in Erode(content_ROI)]
    
    if method=='expansion':
        
        content_boundary=[item for item in Expand(content_ROI) if item not in content_ROI]
        
    #extraction boundary
    content_boundary=[item for item in content_ROI if item not in new_content]
    
    #new binary image
    img_boundary=np.zeros(np.shape(img_binary))
    
    for i,j in content_boundary:
        
        img_boundary[i,j]=1
    
    for i in range(np.shape(img_boundary)[0]):
        
        for j in range(np.shape(img_boundary)[1]):
            
            if img_boundary[i,j]==0:
                
                img_boundary[i,j]=np.nan
                
    return img_boundary