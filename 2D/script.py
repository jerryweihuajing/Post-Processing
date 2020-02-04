# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:14:09 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

''' 
demand 4:
    add colorbar
    
demand 5:
    comparision as an experiment
'''

from __init__ import *

case_path=r'C:\Users\魏华敬\Desktop\YADE\Data\100-200\input\single'
#output_folder=r'C:\Users\魏华敬\Desktop\extension'

##step 1
#CP.CasePlot(case_path,'XoY',1)
#
##step 2
#CO.CasePostProcessing(case_path,output_folder)

yade_rgb_list=[[0.50,0.50,0.50],
               [1.00,0.00,0.00],
               [0.00,1.00,0.00],
               [1.00,1.00,0.00],
               [0.85,0.85,0.85],
               [0.00,1.00,1.00],
               [1.00,0.00,1.00],
               [0.90,0.90,0.90],
               [0.15,0.15,0.15],
               [0.00,0.00,1.00]]

list_progress=[]

#input txt file names
file_names=NP.FilePathsThisCase(case_path)

#traverse all file to consruct progress
for this_file_name in file_names:
    
    #all lines
    lines=open(this_file_name,'r').readlines()
    
    #correct legnth of each line
    correct_length=len(lines[0].strip('\n').split(','))
    
    list_id=[]
    list_tag=[]
    
    #traverse all lines
    for this_line in lines:
        
        this_list=this_line.strip('\n').split(',')
 
        #judge if total length is OK
        if len(this_list)!=correct_length:
                    
            continue
          
        this_id=int(this_list[0])
        this_rgb=[float(this_str) for this_str in this_list[2:5]]
        this_tag=yade_rgb_list.index(this_rgb)
        
        #collect them
        list_id.append(this_id)
        list_tag.append(this_tag)
    
    #construct map between id and tag
    map_id_tag=dict(zip(list_id,list_tag))
    
    list_set_tag=list(set(list_tag))
        
    #construct map between tag and id list
    map_tag_list_id={}
    
    for this_tag in list_set_tag:
        
        map_tag_list_id[this_tag]=[]
        
    for this_id in list_id:
        
        map_tag_list_id[map_id_tag[this_id]].append(this_id)
    
    print(map_tag_list_id)
    
that_progress=progress()

list_spheres=[]

