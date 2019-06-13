# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:55:03 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-grid
"""

#============================================================================== 
#定义网格类
#[position_x,position_x]为grid左上角点的坐标
#spheres_inside为grid内部sphere的数量
#map_tag_amount为grid内部不同tag的sphere数量
#============================================================================== 
class grid:
    def __Init__(self,
                 Id=None,
                 tag=None,
                 color=None,
                 length=None,
                 index=None,
                 index_x=None,
                 index_y=None,
                 position=None,
                 position_x=None,
                 position_y=None,
                 map_tag_amount=None,
                 spheres_inside=None,
                 discreto_points_inside=None):       
        self.Id=Id
        self.tag=tag
        self.color=color
        self.length=length
        self.index=index
        self.index_x=index_x
        self.index_y=index_y
        self.position=position
        self.position_x=position_x
        self.position_y=position_y
        self.map_tag_amount=map_tag_amount
        self.spheres_inside=spheres_inside
        self.discreto_points_inside=discreto_points_inside
        
    #判断sphere是否在grid虚拟边框内部的函数
    def SphereInside(self,which_sphere):
        
        if self.position[0]<=which_sphere.position[0]<self.position[0]+self.length and\
           self.position[1]<=which_sphere.position[1]<self.position[1]+self.length:
            
            return True   
        else:
            return False
        
    #判断discrete point是否在grid虚拟边框内部的函数
    def DiscretePointInside(self,which_discrete_point):
        
        if self.position[0]<=which_discrete_point.pos_x<self.position[0]+self.length and\
           self.position[1]<=which_discrete_point.pos_y<self.position[1]+self.length:
            
            return True   
        else:
            return False