# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:56:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-mesh
"""

import matplotlib.pyplot as plt

#============================================================================== 
#grid集合对象为mesh
#============================================================================== 
class mesh:
    def __Init__(self,
                 grids=None,
                 img_tag=None,
                 img_color=None,
                 content=None):      
        self.grids=grids
        self.img_tag=img_tag
        self.img_color=img_color
        self.content=content
        
    def Plot(self):
        
#        print(np.shape(self.img_tag))
        
        plt.imshow(self.img_color)