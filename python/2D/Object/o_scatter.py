# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:55:26 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-scatter

for xyz format
"""

#==============================================================================
#pos表示离散点的三维坐标
#==============================================================================  
class scatter:
    
    def __init__(self,
                 pos_x=None,
                 pos_y=None,
                 pos_z=None,
                 radius=None):
        
        self.pos_x=pos_x
        self.pos_y=pos_y
        self.pos_z=pos_z
        self.radius=radius