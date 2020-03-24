# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay
"""

from __init__ import *

case_path=r'D:\GitHub\YADE\Controlling-Simulation\2D\extension 100-200\input\single'

pixel_step=10

that_case=case()

that_case.InitCalculation(case_path)

spheres=list(that_case.list_A_progress[-1].map_id_spheres.values())

surface_map=C_S_B.SpheresTopMap(spheres,pixel_step) 

'''effect of rasterization'''
#plot scatter
#plot image

'''effect of interplation'''
#plot scatter in grid
#plot gird without value

'''effet of boundary'''

'''effect of edge tracing'''