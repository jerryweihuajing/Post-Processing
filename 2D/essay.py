# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay
"""

from __init__ import *

import numpy as np
import matplotlib.pyplot as plt

case_path=r'D:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single base uplift bT=2.4 uH=40 uW=100 uO=300'

pixel_step=10

that_case=case()

that_case.InitCalculation(case_path)

spheres=list(that_case.list_A_progress[-1].map_id_spheres.values())

#fetch the mesh object
that_mesh=C_S_B.SpheresContent(spheres,10)


#surface_map=C_S_B.SpheresTopMap(spheres,pixel_step) 

'''effect of rasterization'''
#plot scatter
#plot image

'''effect of interplation'''
#plot scatter in grid
#plot gird without value

'''effect of boundary'''

'''effect of edge tracing'''
