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

#------------------------------------------------------------------------------
"""
To arrange the dictionary index in the order of a list

Args:
    which_dict: dictionary object to be arranged
    which_keys: keys list of new dictionary
    
Returns:
    new dictionary object
"""
def DictSortByIndex(which_dict,which_keys):
    
    #The results of operation
    that_dict={}
    
    #Traverse the new list and populate the dictionary
    for this_key in which_keys:
        
        that_dict[this_key]=which_dict[this_key]
        
    return that_dict

#============================================================================== 
#获取字典子集的函数，从索引start到索引stop,不包括索引stop
def DictSlice(dictionary,start,stop):
    
    keys=list(dictionary.keys())
    values=list(dictionary.values())  
    
    new_dict={}
    
    for i in range(start,stop):
        
        new_dict[keys[i]]=values[i]
        
    return new_dict

#============================================================================== 
#以start为起始索引，将字典重新排序
def DictSortFromStart(dictionary,start):
    
    #两个字典切片
    new_dict_1=DictSlice(dictionary,start,len(dictionary))
    new_dict_2=DictSlice(dictionary,0,start)
    
    #建立新的索引列表
    keys=[]
    
    for item in list(new_dict_1.items()):
        
        keys.append(item[0])
        
    for item in list(new_dict_2.items()):
        
        keys.append(item[0])
        
    #建立新的值列表 
    values=[]
    
    for item in list(new_dict_1.items()):
        
        values.append(item[1])
        
    for item in list(new_dict_2.items()):
        
        values.append(item[1])
        
    #建立新的字典
    new_dict={}
    
    for k in range(len(dictionary)):
        
        new_dict[keys[k]]=values[k]
        
    return new_dict