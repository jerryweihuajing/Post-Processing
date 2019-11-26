# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:28 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Case Operation
"""

#------------------------------------------------------------------------------   
"""
Construct a case object

Args:
   case_path: path to construct
   
Returns:
    case object
""" 
def CaseConstruction(case_path):
    
    #construct case object to save the image data
    that_case=case()
    
    that_case.list_progress=[]
    that_case.condition=case_path.split('\\')[-1]
    
    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=NP.FileNamesThisCase(folder_path)
    
    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
   
        that_case.list_progress.append(ProgressConstruction(structural_deformation_path))
    
    #give them house
    for this_progress in that_case.list_progress:
        
        this_progress.case=that_case
        
    return that_case