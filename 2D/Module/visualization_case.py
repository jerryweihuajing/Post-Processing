# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:28 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Case Operationin visualization
"""

from o_case import case

import operation_path as O_Pa

import visualization_series as V_S
import visualization_progress as V_P
import visualization_animation as V_A
import visualization_integral_analysis as V_I_A

#------------------------------------------------------------------------------   
"""
Construct a case object (in visualization)

Args:
   case_path: path to construct
   
Returns:
    case object
""" 
def CaseConstruction(case_path):
    
    print('')
    print('-- Case Construction')
    
    #construct case object to save the image data
    that_case=case()
    
    that_case.list_progress=[]
    that_case.condition=case_path.split('\\')[-1]
    that_case.experiment=case_path.split('\\')[-3]

    #strutrual deformation path
    folder_path=case_path+'\\structural deformation\\values\\'
    
    #file names in pogress order
    file_names=O_Pa.FileNamesThisCase(folder_path)

    for file_name in file_names:
        
        #txt file path
        structural_deformation_path=folder_path+file_name
   
        that_case.list_progress.append(V_P.ProgressConstruction(structural_deformation_path))
    
    #give them house
    for this_progress in that_case.list_progress:
        
        this_progress.case=that_case
        
    return that_case

#------------------------------------------------------------------------------   
"""
Construct a case object and visualize

Args:
   case_path: path to construct
   output_folder: folder to contain result
   with_farcture: (bool) plot fracture and interface or not 
   
Returns:
    None
""" 
def CaseVisualization(case_path,output_folder=None,with_fracture=False):
    
    print('')
    print('-- Case Visualization')
    
    #construct a case
    that_case=CaseConstruction(case_path)
    
    #output folder of this case
    if output_folder!=None:
        
        case_folder=output_folder+'\\'+that_case.condition
    
    if output_folder==None:
        
        case_folder=case_path.replace('output','Figures')
        
#    V_S.SeriesAll(case_folder,that_case,with_fracture)   
#    V_A.AnimationAll(case_folder,that_case,with_fracture)
#    V_I_A.IntegralAnalysisAll(case_folder,that_case,with_fracture)
    
    #figures in different progress
    for this_progress in that_case.list_progress:
        
        #imaging and output
        V_P.ProgressAllIndividuals(case_folder,this_progress,with_fracture)
        
        #integral analysis
        for this_mode in ['standard','all']:
            
            V_I_A.SingleIntegralAnalysis(case_folder,
                                         this_progress,
                                         this_mode,
                                         with_fracture,
                                         situation='progress')