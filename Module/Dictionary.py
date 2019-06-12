# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 20:59:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Utilizing dictionary
"""

#============================================================================== 
#字典按value搜索key
def DictKeyOfValue(dictionary,value):
    
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    
    #要查询的值为value
    key=keys[values.index(value)]
    
    return key

#============================================================================== 
#让字典索引以某列表的顺序排列
def DictSortByIndex(which_dict,which_keys):
    
    #结果
    that_dict={}
    
    #遍历新列表，并填充字典
    for this_key in which_keys:
        
        that_dict[this_key]=which_dict[this_key]
        
    return that_dict