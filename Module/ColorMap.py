# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:20:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculation about colormap
"""

#============================================================================== 
#filter the value of img
def Filter(which_img,ratio):
    
    new_img=cp.deepcopy(which_img)
    
    #get the maximum and minimum
    maximum_new_img=MatrixMaximum(which_img)
    minimum_new_img=MatrixMinimum(which_img)
#    average_new_img=np.mean(total_values)
    
    #print(maximum_new_img)
    #print(average_new_img)
    
    #check scalar in the array
    #print(len(new_img[np.where(np.abs(new_img)>maximum_new_img*0.1)]))
    #print(np.sum(new_img!=new_img))
    #print(np.sum(new_img==new_img)) 
    
    new_img[np.where(abs(new_img)>(maximum_new_img+minimum_new_img))]=np.nan

    #print(len(new_img[np.where(np.abs(new_img)>maximum_new_img*0.5)]))
    #print(np.sum(new_img!=new_img))
    #print(np.sum(new_img==new_img))
        
    return new_img

#==============================================================================
#fold the colomap: for performance    
def FoldColorMap(which_img):
    
    #get the maximum and minimum
    maximum_new_img=MatrixMaximum(which_img)
    minimum_new_img=MatrixMinimum(which_img)
    
    #get the average
#    average_new_img=MatrixAverage(which_img)
#    average_new_img=(maximum_new_img+minimum_new_img)/2
#    average_new_img=0
    
    #manual adjust
    ratio=0.8
    
    average_new_img=minimum_new_img+(maximum_new_img-minimum_new_img)*ratio
    
    new_img=cp.deepcopy(which_img)
    
    #fold the colormap
    for i in range(np.shape(which_img)[0]):
        
        for j in range(np.shape(which_img)[1]):   
            
            if which_img[i,j]>average_new_img:
                
                new_img[i,j]=maximum_new_img-(which_img[i,j]-average_new_img)
            
            if which_img[i,j]<average_new_img:
                
                new_img[i,j]=minimum_new_img+(average_new_img-which_img[i,j])
                
    return new_img  