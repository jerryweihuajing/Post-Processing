# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 19:04:51 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Operation of List
"""

#------------------------------------------------------------------------------   
"""
Delete repetition in list

Args:
   which_list: list to be operated
   
Returns:
    list without repetition
""" 
def Set(which_list):
    
    new_list=[]
    
    for item in which_list:
        
        if item not in new_list:
            
            new_list.append(item)
            
    return new_list
    