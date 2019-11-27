# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:28 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Case Operation
"""

from o_case import case

import NewPath as NP
import ProgressOperation as PO

import HPC_ProgressPlot as HPC_PP
import HPC_AnimationPlot as HPC_AP
import HPC_IndividualPlot as HPC_IP
import HPC_IntegralAnalysisPlot as HPC_IAP

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
   
        that_case.list_progress.append(PO.ProgressConstruction(structural_deformation_path))
    
    #give them house
    for this_progress in that_case.list_progress:
        
        this_progress.case=that_case
        
    return that_case

#------------------------------------------------------------------------------   
"""
Construct a case object and post processing

Args:
   case_path: path to construct
   output_folder: folder to contain result
   with_farcture: (bool) plot fracture and interface or not 
   
Returns:
    None
""" 
def CasePostProcessing(case_path,output_folder,with_fracture=False):
    
    #construct a case
    that_case=CaseConstruction(case_path)
    
    #output folder of this case
    case_folder=output_folder+'\\'+that_case.condition
    
    HPC_PP.ProgressAll(case_folder,that_case,with_fracture)   
    HPC_AP.AnimationAll(case_folder,that_case,with_fracture)
    HPC_IAP.IntegralAnalysisAll(case_folder,that_case,with_fracture)
    
    #Individual figures
    for this_progress in that_case.list_progress:
        
        #output folder of this progress
        progress_folder=case_folder+'\\'+this_progress.percentage
        
        #imaging and output
        HPC_IP.AllIndividualsInProgress(progress_folder,this_progress,with_fracture)