# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:02:22 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-rectangle
"""

import numpy as np

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())
    
import o_line

import Rasterization as Ra

#==============================================================================
#Rectangle
#==============================================================================
class rectangle:
    def __Init__(self,
                 Id=None,
                 area=None,
                 width=None,
                 height=None,
                 center=None,
                 content=None,
                 points_above=None,
                 points_inside=None,
                 top_boundary=None,
                 left_boundary=None,
                 right_boundary=None,
                 bottom_boundary=None,
                 corner_A=None,
                 corner_B=None,
                 corner_C=None,
                 corner_D=None):  
        self.Id=Id
        self.area=area
        self.width=width
        self.height=height
        self.center=center
        self.points_above=points_above
        self.points_inside=points_inside
        self.top_boundary=top_boundary
        self.left_boundary=left_boundary
        self.right_boundary=right_boundary
        self.bottom_boundary=bottom_boundary
        self.corner_A=corner_A
        self.corner_B=corner_B
        self.corner_C=corner_C
        self.corner_D=corner_D
        
    #初始化
    def Init(self):
        
        self.area=(self.height+1)*(self.width+1)
        self.center=np.array(self.center)
        self.points_above=[]
        self.points_inside=[]
        
        #定义四条边
        top_line=o_line.line()
        left_line=o_line.line()
        right_line=o_line.line()
        bottom_line=o_line.line()
        
        #定义走向
        top_line.orientation='H'
        left_line.orientation='V'
        right_line.orientation='V'
        bottom_line.orientation='H'
        
        #定义边长
        top_line.length=self.width
        left_line.length=self.height
        right_line.length=self.height
        bottom_line.length=self.width
        
        #定义中点
        top_line.center=self.center+np.array([0,+self.height/2])
        left_line.center=self.center+np.array([-self.width/2,0])
        right_line.center=self.center+np.array([+self.width/2,0]) 
        bottom_line.center=self.center+np.array([0,-self.height/2])

        #定义value属性
        top_line.Init()
        left_line.Init()
        right_line.Init()
        bottom_line.Init()
        
        #赋值到属性
        self.top_boundary=top_line
        self.left_boundary=left_line
        self.right_boundary=right_line
        self.bottom_boundary=bottom_line
        
        #定义四个角点
        self.corner_A=self.center+np.array([+self.width/2,+self.height/2])
        self.corner_B=self.center+np.array([-self.width/2,-self.height/2])
        self.corner_C=self.center+np.array([+self.width/2,-self.height/2])
        self.corner_D=self.center+np.array([-self.width/2,+self.height/2])
       
        #矩形上的点
        for k in range(self.length+1):
            
            this_pos_A=self.center+np.array([-self.width/2,-self.height/2+k])
            this_pos_B=self.center+np.array([+self.width/2,-self.height/2+k])
            this_pos_C=self.center+np.array([-self.width/2+k,-self.height/2])
            this_pos_D=self.center+np.array([-self.width/2+k,+self.height/2])
            
            self.points_above.append(list(this_pos_A.astype(int)))
            self.points_above.append(list(this_pos_B.astype(int)))
            self.points_above.append(list(this_pos_C.astype(int)))
            self.points_above.append(list(this_pos_D.astype(int)))
            
        #填充content
        Ra.Boundary2Content(self)
        
    #画出位置
    def Plot(self,which_canvas):
        
        Ra.GraphicPlot(self,which_canvas)
        
    #填充图形
    def Fill(self,which_canvas):
        
        Ra.GraphicFill(self,which_canvas)