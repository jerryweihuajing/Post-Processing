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

map_post_fix_list['strain-periodical']=['Volumetric Strain-Periodical',
                                        'Distortional Strain-Periodical']
    
map_post_fix_list['strain-periodical']=['Volumetric Strain-Periodical',
                                        'Distortional Strain-Periodical']

map_post_fix_list['velocity']=['X Velocity',
                               'Y Velocity']

#list of integral analysis names
mode_list=list(map_post_fix_list.keys())

#the final output postfix
list_title=[]

for this_key in mode_list:
    
    list_title+=map_post_fix_list[this_key] 