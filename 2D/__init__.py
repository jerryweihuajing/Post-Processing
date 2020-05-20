# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 14:11:13 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：initialization script
"""

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path)) 

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

import operation_path as O_P

import calculation_stress as C_Stress

import calculation_matrix as C_M
import calculation_image as C_Im
import calculation_interpolation as C_In
import calculation_custom_export as C_C_E
import calculation_spheres_matrix as C_S_Mat
import calculation_scatters_mesh as C_S_Mesh
import calculation_matrix_outline as C_M_O
import calculation_image_smoothing as C_I_S
import calculation_spheres_boundary as C_S_B

import visualization_case as V_C
import visualization_progress as V_P
import visualization_individual as V_I

from o_case import case

import BETA_calculation_spheres_matrix as BETA_C_S_M

from configuration_yade_color import yade_rgb_map