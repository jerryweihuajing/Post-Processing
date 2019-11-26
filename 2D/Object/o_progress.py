# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 22:34:04 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Object-progress
"""

#==============================================================================
#object progress to manage data efficiently
#==============================================================================            
class progress:
    
    def __init__(self,
                 case=None,
                 shape=None,
                 outline=None,
                 fracture=None,
                 percentage=None,
                 structural_deformation=None,
                 mean_normal_stress=None,
                 maximal_shear_stress=None,
                 periodical_volumrtric_strain=None,
                 periodical_distortional_strain=None,
                 cumulative_volumrtric_strain=None,
                 cumulative_distortional_strain=None,
                 stress_or_strain=None):
        
        self.case=case
        self.shape=shape
        self.outline=outline
        self.fracture=fracture
        self.percentage=percentage
        self.structural_deformation=structural_deformation
        self.mean_normal_stress=mean_normal_stress
        self.maximal_shear_stress=maximal_shear_stress
        self.periodical_volumrtric_strain=periodical_volumrtric_strain
        self.periodical_distortional_strain=periodical_distortional_strain
        self.cumulative_volumrtric_strain=cumulative_volumrtric_strain
        self.cumulative_distortional_strain=cumulative_distortional_strain
        self.stress_or_strain=stress_or_strain