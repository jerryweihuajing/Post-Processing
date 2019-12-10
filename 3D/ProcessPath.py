# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:38:19 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Process Path
"""

import os

import ProcessDictionary as PD

#------------------------------------------------------------------------------
"""
Gets all filenames under the target path

Args:
    file_dir: load path of folder
    post_fix: postfix of file names
    
Returns:
    file names under the target path
"""   
def FileNames(file_dir,post_fix=None):   
    
    #output
    files_names=[]   
    
    for root, dirs, files in os.walk(file_dir):  
        
        #based on post fix
        if post_fix is not None:
            
            for this_file in files: 
                
                if os.path.splitext(this_file)[1]==post_fix: 
                    
                    files_names.append(os.path.join(root,this_file))  
        
        #normal        
        else:
            
            for this_file in files:  
            
                files_names.append(this_file)
            
    return files_names 

#------------------------------------------------------------------------------
"""
Generate file names in this case path in the order of progress

Args:
    which_case_path: load path of this case
    
Returns:
    file names list in this case path in the order of progress
"""
def FileNamesThisCase(which_case_path):
    
    #获取目标路径下所有文件名
    file_names=FileNames(which_case_path)

    #建立进度与文件名的映射列表
    map_progress_file_name={}
    
    #重新排序
    for this_file_name in file_names:
        
    #    print(this_file_name)
              
        init=this_file_name.strip('.txt').strip('progress').strip('=').split('%')
                
    #    print(init[0],'stress')   
        
        #提取出进展
        progress=float(init[0])
        
    #    print(progress)
        
        map_progress_file_name[progress]=this_file_name
        
    #print(map_progress_file_name)
    
    #对file_names进行排序 
    new_map_progress_file_name=PD.DictSortByIndex(map_progress_file_name,sorted(list(map_progress_file_name.keys())))
    
    #返回新的文件名
    return list(new_map_progress_file_name.values())

#------------------------------------------------------------------------------
"""
Generate file paths in this case path in the order of progress

Args:
    which_case_path: load path of this case
    
Returns:
    file paths list in this case path in the order of progress
"""
def FilePathsThisCase(which_case_path):
    
    #Generate file names in this case path in the order of progress
    file_names=FileNamesThisCase(which_case_path)

    return [which_case_path+'\\'+this_file_name for this_file_name in file_names]