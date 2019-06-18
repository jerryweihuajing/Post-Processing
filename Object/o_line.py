# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:59:22 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-line
"""

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