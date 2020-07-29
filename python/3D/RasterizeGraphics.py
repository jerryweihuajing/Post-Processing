# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:46:35 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Rasterize Graphics
"""

#==============================================================================   
#计算A和B的交集
def CrossContent(content_A,content_B):
     
    #结果集合
    cross_content=[]
    
    for this_pos in content_A:
        
        if this_pos in content_B:
            
            cross_content.append(this_pos)
            
    return cross_content

#==============================================================================
#圆形和正方形的交集可以通过边界来划分:两种相交算法
def ContentSquareCrossCircle(which_square,which_circle,method=1):
    
    #结果集合
    cross_content=[]
    
    #两种方法
    if method==1:
        
        #角点集合
        square_corners=[which_square.corner_A,
                        which_square.corner_B,
                        which_square.corner_C,
                        which_square.corner_D]
        
        #角点x,y坐标集合
        x_corners=[this_square[0] for this_square in square_corners]
        y_corners=[this_square[1] for this_square in square_corners]
        
        x_min,x_max=min(x_corners),max(x_corners)
        y_min,y_max=min(y_corners),max(y_corners)
        
        #遍历并判断
        for this_pos in which_circle.points_inside:
            
            if x_min<=this_pos[0]<=x_max and y_min<=this_pos[1]<=y_max:
                
                cross_content.append(this_pos)
            
        return cross_content
    
    #交集法
    if method==2:    
         
        return CrossContent(which_square.points_inside,which_circle.points_inside)