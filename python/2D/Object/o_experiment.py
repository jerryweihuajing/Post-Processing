# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:35:36 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-experiment
"""

#==============================================================================
#object experiment to manage data efficiently
#==============================================================================     
class experiment:
    
    def __init__(self,
                 parameter=None,
                 list_case=None):
    
        self.parameter=parameter
        self.list_case=list_case