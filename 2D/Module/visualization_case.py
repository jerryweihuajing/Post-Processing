# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:38:28 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Case Operationin visualization
"""

from o_case import case

import visualization_series as V_S
import visualization_progress as V_P
import visualization_animation as V_A
import visualization_integral_analysis as V_I_A

from configuration_list_title import mode_list

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
    
    that_case.InitOffset(case_path.replace('output','input'))
    that_case.InitVisualization(case_path)
    
    print('')
    print('-> experiment:',that_case.experiment)
    print('-> condition:',that_case.condition)
        
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
def CaseVisualization(case_path,
                      output_folder=None,
                      with_fracture=False):
    
    print('')
    print('-- Case Visualization')
    
    #construct a case
    that_case=CaseConstruction(case_path)
    
    #output folder of this case
    if output_folder!=None:
        
        case_folder=output_folder+'\\'+that_case.condition
    
    if output_folder==None:
        
        case_folder=case_path.replace('output','Figure')
        
#    V_S.SeriesAll(case_folder,that_case)   
#    V_A.AnimationAll(case_folder,that_case)
#    V_I_A.IntegralAnalysisAll(case_folder,that_case)
    
    #figures in different progress
    for this_progress in that_case.list_progress:

        #imaging and output
        V_P.ProgressAllIndividuals(output_folder=case_folder,
                                   which_progress=this_progress,
                                   with_fracture=with_fracture)
        
        #integral analysis
        for this_mode in mode_list:
            
            V_I_A.SingleIntegralAnalysis(output_folder=case_folder,
                                         which_progress=this_progress,
                                         mode=this_mode,
                                         situation='progress',
                                         with_fracture=with_fracture)
            