# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:43:10 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Process Dictionary
"""

#------------------------------------------------------------------------------
"""
To arrange the dictionary index in the order of a list

Args:
    which_dict: dict to be arranged
    which_keys: index list to command
    
Returns:
    new dict in the order of index list
"""  
def DictSortByIndex(which_dict,which_keys):
    
    #result dictionary
    that_dict={}
    
    #Iterate through the new list and populate the dictionary
    for this_key in which_keys:
        
        that_dict[this_key]=which_dict[this_key]
        
    return that_dict