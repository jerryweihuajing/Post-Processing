# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:03:43 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Rasterization of several geometric figures
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

#==============================================================================
#Line
#orientation: direction of a line object
#points_above: pixels or points on the boundary
#==============================================================================
class line:
    def __Init__(self,
                 Id=None,
                 value=None,
                 center=None,
                 length=None,                 
                 orientation=None,
                 points_above=None):
        self.Id=Id
        self.value=value
        self.center=center
        self.length=length
        self.orientation=orientation
        self.points_above=points_above
        
    #初始化线段坐标值
    def Init(self):
        
        if self.orientation=='V':
            
            self.value=self.center[0]
        
        if self.orientation=='H':
            
            self.value=self.center[1]
    
    #判断点是否在线段上
    def Below(self,which_point):
        
        if self.center[0]==which_point[0] and self.center[1]-self.length/2<=which_point[1]<=self.center[1]+self.length/2 or\
           self.center[1]==which_point[1] and self.center[0]-self.length/2<=which_point[0]<=self.center[0]+self.length/2:
                
           return True      
        else:
            return False
            
#==============================================================================
#圆形
#==============================================================================
class circle:
    def __Init__(self,
                 Id=None,
                 area=None,
                 radius=None,
                 center=None,
                 points_above=None,
                 points_inside=None):      
        self.Id=Id
        self.area=area
        self.radius=radius
        self.center=center
        self.points_above=points_above
        self.points_inside=points_inside
        
    #初始化内部点points_above和points_inside
    def Init(self,method=2):
        
        self.area=np.pi*self.radius**2
        self.center=np.array(self.center)
        self.points_above=[]  
        self.points_inside=[] 
        
        #方向角
        alpha=np.linspace(-np.pi,np.pi,num=500)
           
        #圆上点         
        for this_alpha in alpha:
            
            this_pos=self.center+np.array([self.radius*np.cos(this_alpha),self.radius*np.sin(this_alpha)])
            
            #判断应不应该加入
            if list(this_pos.astype(int)) not in self.points_above:
                
                self.points_above.append(list(this_pos.astype(int)))
        
        '''1 极坐标填充法：计算量可能较大，会有大量重复'''
        if method==1:
            
            #填充点
            for this_radius in range(self.radius):
                
                for this_alpha in alpha:
                    
                    this_pos=self.center+np.array([this_radius*np.cos(this_alpha),this_radius*np.sin(this_alpha)])
                    
                    #判断应不应该加入
                    if list(this_pos.astype(int)) not in self.points_inside:
                        
                        self.points_inside.append(list(this_pos.astype(int)))        
                
        '''边界求内容：该方法要求points_above是个连通域，若非连通可用膨胀腐蚀解决''' 
        if method==2:
            
            Boundary2Content(self)
            
    #画出位置
    def Plot(self,which_canvas):
        
        GraphicPlot(self,which_canvas)
        
    #填充图形
    def Fill(self,which_canvas):
        
        GraphicFill(self,which_canvas)
        
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
        top_line=line()
        left_line=line()
        right_line=line()
        bottom_line=line()
        
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
        Boundary2Content(self)
        
    #画出位置
    def Plot(self,which_canvas):
        
        GraphicPlot(self,which_canvas)
        
    #填充图形
    def Fill(self,which_canvas):
        
        GraphicFill(self,which_canvas)
        
#==============================================================================
#正方形
#points_above为周长上的点
#points_above为正方形内部的点
#==============================================================================
class square:
    def __Init__(self,
                 Id=None,
                 area=None,
                 length=None,
                 center=None,
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
        self.length=length
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
        
        self.area=(self.length+1)**2
        self.center=np.array(self.center)
        self.points_above=[]
        self.points_inside=[]
        
        #定义四条边
        top_line=line()
        left_line=line()
        right_line=line()
        bottom_line=line()
        
        #定义走向
        top_line.orientation='H'
        left_line.orientation='V'
        right_line.orientation='V'
        bottom_line.orientation='H'
        
        #定义边长
        top_line.length=self.length
        left_line.length=self.length
        right_line.length=self.length 
        bottom_line.length=self.length
        
        #定义中点
        top_line.center=self.center+np.array([0,+self.length/2])
        left_line.center=self.center+np.array([-self.length/2,0])
        right_line.center=self.center+np.array([+self.length/2,0]) 
        bottom_line.center=self.center+np.array([0,-self.length/2])

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
        self.corner_A=self.center+np.array([+self.length/2,+self.length/2])
        self.corner_B=self.center+np.array([-self.length/2,-self.length/2])
        self.corner_C=self.center+np.array([+self.length/2,-self.length/2])
        self.corner_D=self.center+np.array([-self.length/2,+self.length/2])
       
        #矩形上的点
        for k in range(self.length+1):
            
            this_pos_A=self.center+np.array([-self.length/2,-self.length/2+k])
            this_pos_B=self.center+np.array([+self.length/2,-self.length/2+k])
            this_pos_C=self.center+np.array([-self.length/2+k,-self.length/2])
            this_pos_D=self.center+np.array([-self.length/2+k,+self.length/2])
            
            self.points_above.append(list(this_pos_A.astype(int)))
            self.points_above.append(list(this_pos_B.astype(int)))
            self.points_above.append(list(this_pos_C.astype(int)))
            self.points_above.append(list(this_pos_D.astype(int)))
            
        #填充content
        Boundary2Content(self)
            
    #画出位置
    def Plot(self,which_canvas):
        
        GraphicPlot(self,which_canvas)
        
    #填充图形
    def Fill(self,which_canvas):
        
        GraphicFill(self,which_canvas)
    
#==============================================================================
#计算圆和水平线的交点
#水平线：y确定
def HLineCrossCircle(which_y,which_circle):
    
    delta=which_circle.radius**2-(which_y-which_circle.center[1])**2
    
    #会有两个根
    if delta>0:
        
        return [[which_circle.center[0]+np.sqrt(delta),which_y],\
                [which_circle.center[0]-np.sqrt(delta),which_y]]
    
    #一个根
    if delta==0:
        
        return [[which_circle.center[0],which_y]]
    
#==============================================================================
#计算圆和垂直线的交点
#水平线：x确定
def VLineCrossCircle(which_x,which_circle):
    
    delta=which_circle.radius**2-(which_x-which_circle.center[0])**2
    
    #会有两个根
    if delta>0:
        
        return [[which_x,which_circle.center[1]+np.sqrt(delta)],\
                [which_x,which_circle.center[1]-np.sqrt(delta)]]
    
    #一个根
    if delta==0:
        
        return [[which_x,which_circle.center[1]]]
    
#==============================================================================
#计算圆和直线的交点
def LineCrossCircle(orientation,which_value,which_circle):
    
    #垂直
    if orientation=='V':
        
        return VLineCrossCircle(which_value,which_circle)
    
    #水平
    if orientation=='H':
        
        return HLineCrossCircle(which_value,which_circle)
    
#==============================================================================
#计算直线与圆形两个交点的弦长
def ChordLength(orientation,which_value,which_circle):
    
    #只有在有两个交点时才有结果
    if len(LineCrossCircle(orientation,which_value,which_circle)):
        
        return abs(LineCrossCircle(orientation,which_value,which_circle)[1]-LineCrossCircle(orientation,which_value,which_circle)[0])

#==============================================================================
#计算直线与圆形两个交点的弦与圆形围城的三角形面积
def ChordTriangleArea(orientation,which_value,which_circle):
    
    #高
    if orientation=='V':
        
        height=abs(which_value-which_circle.center[0])
    
    if orientation=='H':
        
        height=abs(which_value-which_circle.center[1])
        
    return height*ChordLength(orientation,which_value,which_circle)/2

#==============================================================================
#计算直线与圆形两个交点的弦与圆形围成的扇形面积
def ChordSectorArea(orientation,which_value,which_circle):
    
    #弧度大小
    alpha=2*np.arcsin(ChordLength(orientation,which_value,which_circle)/(2*which_circle.radius))
    
#    print(alpha)
    
    return 0.5*alpha*which_circle.radius**2

#==============================================================================
#计算正方形与圆形的交点:多种相交情况
def PointsSquareCrossCircle(which_square,which_circle):
    
    #先初始化一波
    which_square.Init()
    which_square.points_above=[]

    #正方形边列表
    square_boundaries=[which_square.top_boundary,
                       which_square.left_boundary,
                       which_square.right_boundary,
                       which_square.bottom_boundary]
    #那个边
    that_boundary=None
    
    #分别计算交点
    for this_boundary in square_boundaries:
        
        #初始化边上点
        this_boundary.points_above=[]
        
        this_cross_points=LineCrossCircle(this_boundary.orientation,this_boundary.value,which_circle)
      
#        print(this_cross_points)
        
        #只要不是None
        if this_cross_points!=None:
            
            for this_cross_point in this_cross_points:
                
                if this_boundary.Below(this_cross_point):
                    
                    this_boundary.points_above.append(this_cross_point)

                    if this_cross_point not in which_square.points_above:
                        
                        which_square.points_above.append(this_cross_point)
                        
#                        print(this_cross_point)
                        
#        print(this_boundary.points_above)     
                    
        #交点数为2直接研究
        if len(this_boundary.points_above)==2:   
            
            that_boundary=cp.deepcopy(this_boundary)
            
            print(that_boundary.points_above)
            
    print(which_square.points_above)
    
    #不存在这样一个双点边
    if that_boundary==None:
        
        for this_boundary in square_boundaries:
            
            print(this_boundary.points_above)
        
#==============================================================================
#又边界点计算内部的点:只适合简单图形
def Boundary2Content(which_graphic):
    
    #计算坐标集合及其最值
    x_points_above=[this_pos[0] for this_pos in which_graphic.points_above]
    y_points_above=[this_pos[1] for this_pos in which_graphic.points_above]
    
    x_min,x_max=min(x_points_above),max(x_points_above)
    y_min,y_max=min(y_points_above),max(y_points_above)
    
#    print(x_min,x_max)
#    print(y_min,y_max)
    
    #遍历找出边界上的值
    map_x_y={}
    
    for this_x in range(x_min,x_max+1):
        
        map_x_y[this_x]=[]
        
        for this_y in range(y_min,y_max+1):
            
            if [this_x,this_y] in which_graphic.points_above:
                
                map_x_y[this_x].append(this_y)
                
    #    print(len(map_x_y[this_x]))
        
        for this_Y in range(min(map_x_y[this_x]),max(map_x_y[this_x])+1):
            
            if [this_x,this_Y] not in which_graphic.points_inside:
                
                which_graphic.points_inside.append([this_x,this_Y])
                
#==============================================================================
#图形边界显示
def GraphicPlot(which_graphic,which_canvas):
    
    #在画布上显示 
    for this_pos in which_graphic.points_above:
    
        which_canvas[int(this_pos[0]),int(this_pos[1])]=1    
        
    plt.imshow(which_canvas,cmap='rainbow')
    
#==============================================================================
#图形填充显示
def GraphicFill(which_graphic,which_canvas):
    
    #在画布上显示 
    for this_pos in which_graphic.points_inside:
    
        which_canvas[int(this_pos[0]),int(this_pos[1])]=1    
        
    plt.imshow(which_canvas,cmap='rainbow')

#==============================================================================
#在某个画布canvas当中显示像素点集合
def Show(which_content,which_canvas):
    
    #在画布上显示 
    for this_pos in which_content:
    
        which_canvas[int(this_pos[0]),int(this_pos[1])]=1    
        
    plt.imshow(which_canvas,cmap='rainbow')
    
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

##canvas的尺寸
#width=300
#height=300
#
##canvas=np.full((width,height,3),np.array([255,255,255],dtype=np.uint8) )
#
#canvas=np.zeros((height,width)) 
#
#cir=circle()
#cir.radius=50
#cir.center=np.array([100,150]) 
#cir.Init()
#
#sq=square()
#sq.length=100
#sq.center=np.array([150,200])
#sq.Init()
#
##sq.Fill(canvas)
##cir.Fill(canvas) 
#
#import time
#
#time_start=time.time()
#
#a=ContentSquareCrossCircle(sq,cir,method=1)
#           
#time_end=time.time()
#
#print(time_end-time_start)
# 
#time_start=time.time()
#
#b=ContentSquareCrossCircle(sq,cir,method=2)
#
#time_end=time.time()
#
#print(time_end-time_start)
#
##计算相交面积
#
##Show(a,canvas)
##Show(b,canvas)
