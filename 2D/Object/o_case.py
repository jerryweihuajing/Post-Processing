# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:35:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-case
"""

#==============================================================================
#object case to manage data efficiently
#==============================================================================    
class case:
    
    def __init__(self,
                 experiment=None,
                 condition=None,
                 list_progress=None):
        
        self.experiment=experiment
        self.condition=condition
        self.list_progress=list_progress