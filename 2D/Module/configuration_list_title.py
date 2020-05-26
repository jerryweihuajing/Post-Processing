# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 20:58:59 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-name of postfix list
"""

flag_all=False

#list post fix in individual
list_standard=['Structural Deformation',
               'Mean Normal Stress',
               'Maximal Shear Stress',
               'Volumetric Strain-Cumulative',
               'Distortional Strain-Cumulative']

list_extra=['Volumetric Strain-Periodical',
            'Distortional Strain-Periodical',
            'Volumetric Strain-Instantaneous',
            'Distortional Strain-Instantaneous']

#list_extra=[]

#list post fix in integral analysis
map_post_fix_list={}

map_post_fix_list['dynamics']=['Structural Deformation',
                               'Mean Normal Stress',
                               'Maximal Shear Stress',
                               'Volumetric Strain-Cumulative',
                               'Distortional Strain-Cumulative']
            
map_post_fix_list['kinematics']=['Structural Deformation',
                                 'X Velocity',
                                 'Y Velocity',
                                 'X Displacement-Cumulative',
                                 'Y Displacement-Cumulative']

map_post_fix_list['strain-cumulative']=['X Normal Strain-Cumulative',
                                        'Y Normal Strain-Cumulative',
                                        'Diff Normal Strain-Cumulative',
                                        'Mean Normal Strain-Cumulative',
                                        'Minimal Normal Strain-Cumulative',
                                        'Maximal Normal Strain-Cumulative',
                                        'Shear Strain-Cumulative',
                                        'Minimal Shear Strain-Cumulative',
                                        'Maximal Shear Strain-Cumulative',
                                        'Volumetric Strain-Cumulative',
                                        'Distortional Strain-Cumulative']

map_post_fix_list['strain-periodical']=['X Normal Strain-Periodical',
                                        'Y Normal Strain-Periodical',
                                        'Diff Normal Strain-Periodical',
                                        'Mean Normal Strain-Periodical',
                                        'Minimal Normal Strain-Periodical',
                                        'Maximal Normal Strain-Periodical',
                                        'Shear Strain-Periodical',
                                        'Minimal Shear Strain-Periodical',
                                        'Maximal Shear Strain-Periodical',
                                        'Volumetric Strain-Periodical',
                                        'Distortional Strain-Periodical']
    
map_post_fix_list['strain-instantaneous']=['X Normal Strain-Instantaneous',
                                           'Y Normal Strain-Instantaneous',
                                           'Diff Normal Strain-Instantaneous',
                                           'Mean Normal Strain-Instantaneous',
                                           'Minimal Normal Strain-Instantaneous',
                                           'Maximal Normal Strain-Instantaneous',
                                           'Shear Strain-Instantaneous',
                                           'Minimal Shear Strain-Instantaneous',
                                           'Maximal Shear Strain-Instantaneous',
                                           'Volumetric Strain-Instantaneous',
                                           'Distortional Strain-Instantaneous']

map_post_fix_list['velocity']=['Resultant Velocity',
                               'X Velocity',
                               'Y Velocity',
                               'X Gradient of X Velocity',
                               'Y Gradient of Y Velocity']

map_post_fix_list['displacement-cumulative']=['Resultant Displacement-Cumulative',
                                              'X Displacement-Cumulative',
                                              'Y Displacement-Cumulative',
                                              'X Gradient of X Displacement-Cumulative',
                                              'Y Gradient of Y Displacement-Cumulative']

map_post_fix_list['displacement-periodical']=['Resultant Displacement-Periodical',
                                              'X Displacement-Periodical',
                                              'Y Displacement-Periodical',
                                              'X Gradient of X Displacement-Periodical',
                                              'Y Gradient of Y Displacement-Periodical']

map_post_fix_list['displacement-instantaneous']=['Resultant Displacement-Instantaneous',
                                                 'X Displacement-Instantaneous',
                                                 'Y Displacement-Instantaneous',
                                                 'X Gradient of X Displacement-Instantaneous',
                                                 'Y Gradient of Y Displacement-Instantaneous']

#list of integral analysis names
mode_list=['dynamics',
           'kinematics',
           'velocity',
           'displacement-cumulative',
           'displacement-periodical',
           'displacement-instantaneous']

#the final output postfix
list_title=[]

for this_key in mode_list:
    
    list_title+=map_post_fix_list[this_key] 