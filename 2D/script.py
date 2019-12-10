# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

''' 
demand 4:
    add colorbar
    
demand 5:
    comparision as an experiment
'''

from __init__ import *

#A experiment
#experiment_path=os.getcwd()+'\\Data\\100-500\\base detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

#HPC_EP.ExperimentPlotAll(experiment_path)

#experiment_folder=os.getcwd()+'\\Data\\100-500\\base detachment'
#
#for this_experiment in os.listdir(experiment_folder):
#    
#    #concat data path
#    this_experiment_path=experiment_folder+'\\'+this_experiment
#    
#    print(this_experiment_path)
#    
#    CP.ExperimentPlot(this_experiment_path,'XoY',1,'standard')
#
#    EP.ExperimentPlotAll(this_experiment_path)

case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=2.72'

#A experiment
#experiment_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2'

#a_case=CO.CaseConstruction(case_path)

structural_deformation_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\2D\Data\100-500\base detachment\fric=0.0 v=0.2\output\base=5.43\structural deformation\values\27.87%.txt'

a_progress=PO.ProgressConstruction(structural_deformation_path) 

output_folder=r'C:\Users\whj\Desktop\fig'

#CO.CasePostProcessing(case_path,output_folder)

import Image as Img

img_rgb=Img.ImgFlip(a_progress.structural_deformation,0)
img_tag=Img.ImgFlip(a_progress.img_tag,0)

import numpy as np
import matplotlib.pyplot as plt

#import cv2
#laplacian=cv2.Laplacian(img_tag,cv2.CV_64F)
#
#gradient_x=np.gradient(img_tag)[0]
#gradient_y=np.gradient(img_tag)[1]

#sobel=cv2.Sobel(img_tag,cv2.CV_64F,1,1,ksize=3)
#sobelx=cv2.Sobel(img_tag,cv2.CV_64F,1,0,ksize=3)
#sobely=cv2.Sobel(img_tag,cv2.CV_64F,0,1,ksize=3)
#
#plt.figure()
#plt.subplot(221),plt.imshow(laplacian)
#plt.subplot(222),plt.imshow(sobel)
#plt.subplot(223),plt.imshow(sobelx)
#plt.subplot(224),plt.imshow(sobelx)
#
#'''ok!'''
#plt.figure()
#plt.subplot(211),plt.imshow(img_rgb)
#plt.subplot(212),plt.imshow(laplacian)
#
#
#plt.figure()
#plt.subplot(211),plt.imshow(gradient_x)
#plt.subplot(212),plt.imshow(gradient_y)
#
#np.where(laplacian!=0)

def SimpleGradient(which_matrix,axis=0):
    
    simple_gradient=np.zeros(np.shape(which_matrix))
    
    if axis==0:
        
        simple_gradient[1:,:]=which_matrix[1:,:]-which_matrix[:-1,:]
        
    if axis==1:
        
        simple_gradient[:,1:]=which_matrix[:,1:]-which_matrix[:,:-1]
        
    return simple_gradient

#RGB channel

#surface outline show some similarity

#find element whose tag


'''content to add algorithm'''

'''
1 erosion and expand-cv2: no good
2 tracing based on gradient
'''

def AllStrataSurface(which_progress,show=False):
    
    #Calculate gradient
    manual_gradient_x=SimpleGradient(img_tag,0)
    manual_gradient_y=SimpleGradient(img_tag,1)
    manual_gradient=manual_gradient_x+manual_gradient_y
    
    #surface of all strata
    strata_surface=np.full(np.shape(manual_gradient),np.nan)
    strata_surface[np.where(manual_gradient!=0)]=1
    
    if show:
        
        plt.imshow(strata_surface,cmap='gray')
        
    return strata_surface
    
def DetachmentSurfaceBasedOnTag(which_progress,which_tag,show=False):
    
    #Calculate gradient
    manual_gradient_x=SimpleGradient(img_tag,0)
    manual_gradient_y=SimpleGradient(img_tag,1)
    manual_gradient=manual_gradient_x+manual_gradient_y
    
    #surface of all strata
    strata_surface=np.full(np.shape(manual_gradient),np.nan)
    strata_surface[np.where(manual_gradient!=0)]=1
    
    #detachment surface which is intersection of surface and detachment 
    detachment_surface=np.full(np.shape(manual_gradient),np.nan)
    
    for i in range(np.shape(detachment_surface)[0]):
        
        for j in range(np.shape(detachment_surface)[1]):
            
            if strata_surface[i,j]==1 and img_tag[i,j]==which_tag:
                
                detachment_surface[i,j]=1

    if show:
        
        plt.imshow(detachment_surface,cmap='gray')  
        
    return detachment_surface

'''cv2 erosion: no good'''
def CV2ErosionBasedOnTag(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),np.nan)
    this_strata[np.where(img_tag==which_tag)]=1
        
    #construct kernel parameter to make erosion operation
    erosion_kernel=np.ones((5, 5),np.uint8)
    erosion=cv2.erode(this_strata,erosion_kernel,iterations=1)
    
    #nan 2 float
    this_strata=np.nan_to_num(this_strata)
    erosion=np.nan_to_num(erosion)
    
    #subduction operation
    this_strata_surface=this_strata-erosion
    
    #fill 0 with np.nan
    this_strata_surface[np.where(this_strata_surface==0)]=np.nan
    
    if show:
            
        plt.figure()
        
        plt.subplot(311),plt.imshow(this_strata,cmap='gray')
        plt.subplot(312),plt.imshow(erosion,cmap='gray')
        plt.subplot(313),plt.imshow(this_strata_surface,cmap='gray')
    
'''cv2 dilation: no good'''
def CV2DilationBasedOnTag(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),np.nan)
    this_strata[np.where(img_tag==which_tag)]=1

    #construct kernel parameter to make erosion operation
    dilation_kernel=np.ones((5, 5),np.uint8)
    dilation=cv2.erode(this_strata,dilation_kernel,iterations=1)

    #nan 2 float
    this_strata=np.nan_to_num(this_strata)
    dilation=np.nan_to_num(dilation)
    
    #subduction operation
    this_strata_surface=dilation-this_strata
    
    #fill 0 with np.nan
    this_strata_surface[np.where(this_strata_surface==0)]=np.nan
    
    if show:
        
        plt.figure()
        
        plt.subplot(311),plt.imshow(this_strata,cmap='gray')
        plt.subplot(312),plt.imshow(dilation,cmap='gray')
        plt.subplot(313),plt.imshow(this_strata_surface,cmap='gray')

'''cv2 finding contours: no good'''
def CV2FindContours(img_tag,which_tag,show=False):
    
    this_strata=np.full(np.shape(img_tag),0,np.uint8)
    this_strata[np.where(img_tag==which_tag)]=255    
     
    #find contour
    image, contours, hierarchy = cv2.findContours(this_strata, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    print("contours size: ", len(contours))
    
    #draw contours
    cv2.drawContours(this_strata, contours, -1, (0, 0, 255), 3)
    
    if show:
        
        cv2.imshow("img", this_strata)
        cv2.waitKey(0)

#==============================================================================  
#定义像素点类:横纵坐标和值
#neighbor表示邻域里的8个像素点点
#==============================================================================  
class pixel:
    def __int__(self,
                xpos=None,
                ypos=None,
                value=None,
                neighbor=None):
        
        self.xpos=xpos
        self.ypos=ypos
        self.value=value
        self.neighbor=neighbor
    
    #找到合适的点之后生成他的邻域
    def GenerateNeighbor(self,img_tag):
  
        self.neighbor=[]    
        
        #逆时针遍历邻域内的点
        neighbordict={0:(0,-1),
                      1:(1,-1),
                      2:(1,0),
                      3:(1,1),
                      4:(0,1),
                      5:(-1,1),
                      6:(-1,0),
                      7:(-1,-1)}
        
        #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
        for item in list(neighbordict.values()):

            #遍历新的坐标
            new_y=self.ypos+item[0]
            new_x=self.xpos+item[1]
            
            if 0<=new_y<np.shape(img_tag)[0] and 0<=new_x<np.shape(img_tag)[1]:
                
                self.neighbor.append(img_tag[new_y,new_x])      
                
            else:
                
                self.neighbor.append(None)

"""
以下情况需要特殊处理：
1 S[k-1]邻域内的第一个点已在边缘集合当中，则访问下一个点 OK
2 S[k]邻域内只有一个边缘点，即上一个点S[k-1],则访问S[k-1]邻域内下一个点 OK  
3 S[K]从上一个目标点是S[k-1]逆时针进行遍历 OK
""" 

#============================================================================== 
#寻找自己的第一个符合要求的邻居像素,要追踪的像素值为tag
#第一个满足tag的pixel对象
def Find1stNeighbor(tag,flag_stop,edge,img_tag,index):
    
    #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
    #邻域的索引和横纵坐标的索引（绝对索引）
    neighbordict={0:(0,-1),
                  1:(1,-1),
                  2:(1,0),
                  3:(1,1),
                  4:(0,1),
                  5:(-1,1),
                  6:(-1,0),
                  7:(-1,-1)}
    
    #以最后一个edge点为指针进行检索
    first_pixel=pixel()
    first_pixel.ypos=edge[-1][0]
    first_pixel.xpos=edge[-1][1]
    first_pixel.neighbor=[]
    
    #3 S[K]从上一个目标点是S[k-1]逆时针进行遍历
    #重新规划索引new_index后一个索引和前一个索引呈对角关系
    #若索引大于4，归化

    if index<4:
        
        new_index=index+4
        
    else:
        
        new_index=index-4
        
    new_neighbordict=Dict.DictSortFromStart(neighbordict,new_index)
    
    #生成邻居列表,起始迭代邻居的索引
    first_pixel.GenerateNeighbor(img_tag)
    
    #邻域内邻居数量
    count=0

    for i in range(len(new_neighbordict)):
        
        #获取目标点的索引,转化为绝对索引
        index=list(new_neighbordict.keys())[i]
        
        #符合tag的点计数
        if first_pixel.neighbor[index]==tag:
            
            count+=1
            
            #建立新的pixel对象
            temp_pixel=pixel()
            temp_pixel.ypos=first_pixel.ypos+new_neighbordict[index][0]
            temp_pixel.xpos=first_pixel.xpos+new_neighbordict[index][1]
            pos=[temp_pixel.ypos,temp_pixel.xpos]
   
            #判断目标点和起点是否相同,不能是第一个点
            if i>0 and pos==edge[0]:
               
                flag_stop=True
                edge.append(pos)
                
                break
            
            #1 S[k-1]邻域内的第一个点已在边缘集合当中，则访问下一个点    
            if pos not in edge:
                
                edge.append(pos)
                
                break  
            
            #*2 S[k]邻域内只有一个边缘点，即上一个点S[k-1],则访问S[k-1]邻域内下一个点
            if len(edge)>1 and pos==edge[-2] and count==1 and i==7:
               
                edge.append(pos)
                
                break
                   
    return edge,index,flag_stop

#==============================================================================  
#在img_tag中根据edge[0]追踪边界,要追踪的像素标签值为tag
def EdgeTracing(tag,edge,img_tag):
    
    #初始化循环中止判别标志
    flag_stop=False
    
    #初始化绝对索引
    index=-4
    
    #进行第一次邻居搜索
    edge,index,flag_stop=Find1stNeighbor(tag,flag_stop,edge,img_tag,index) 
    
    while len(edge)>1 and flag_stop is False:
        
        edge,index,flag_stop=Find1stNeighbor(tag,flag_stop,edge,img_tag,index) 
    
    return edge

import cv2 
import Dictionary as Dict

which_tag=1 
  
#plt.figure()
#plt.imshow(img_rgb)
#AllStrataSurface(a_progress,1)
detachment_surface=DetachmentSurfaceBasedOnTag(a_progress,6)

'''Edge tracing based on gradients'''

import copy as cp

def OutlineNextRound(outline_matrix,outline_content,edge_content,show=False):
    
    outline_rest_matrix=cp.deepcopy(outline_matrix)
    outline_rest_content=[]
    
    for this_pos in outline_content:
        
        if this_pos not in edge_content:
            
            outline_rest_content.append(this_pos)
            
        else:
            
            outline_rest_matrix[this_pos[0],this_pos[1]]=np.nan
            
    print(len(outline_rest_content))
    
    if show:

        plt.imshow(outline_rest_matrix,cmap='gray')

    return outline_rest_matrix

def EdgeThisRound(outline_original,show=False):
    
    x_outline=np.where(outline_original==1)[0]
    y_outline=np.where(outline_original==1)[1]
    
    outline_content=[[x_outline[k],y_outline[k]] for k in range(len(x_outline))]
    
    start_point=[x_outline[0],y_outline[0]]
    
    print(len(outline_content))
    
    #先求梯度是为了缩小检索范围，避免全局搜索
    edge_content=EdgeTracing(6,[start_point],img_tag)
    
    edge_matrix=np.full(np.shape(img_tag),np.nan)
    
    for this_pos in edge_content:
        
        edge_matrix[this_pos[0],this_pos[1]]=1
        
    if show:
        
        plt.figure()
        
        #original outline
        plt.subplot(311)
        plt.imshow(img_rgb)
        plt.imshow(outline_original,cmap='gray')  
        
        #edge
        plt.subplot(312)
        plt.imshow(img_rgb)
        plt.imshow(edge_matrix,cmap='gray')  
        
        #outline rest
        plt.subplot(313)
        plt.imshow(img_rgb)
         
    return OutlineNextRound(detachment_surface,outline_content,edge_content,show=show)  

outline_rest_matrix=EdgeThisRound(detachment_surface,show=1)

'''could not find the next neighbor whose tag is the same'''
outline_rest_matrix=EdgeThisRound(outline_rest_matrix,show=1)