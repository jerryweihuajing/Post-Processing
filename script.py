# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：execution script
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Object.o_grid import grid
from Object.o_mesh import mesh
from Object.o_sphere import sphere
from Object.o_strain_2D import strain_2D
from Object.o_discrete_point import discrete_point

from Module import Norm as No
from Module import Path as Pa
from Module import Image as Img
from Module import NewPath as NP
from Module import ColorBar as CB
from Module import Animation as An
from Module import CustomPlot as CP
from Module import Decoration as Dec
from Module import Dictionary as Dict
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import AxisBoundary as AB
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG
from Module import NewSpheresGeneration as NSG
from Module import SpheresAttributeMatrix as SAM

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

'''
demand: fracture on stress and deformation figure

'''

#A experiment
experiment_path=os.getcwd()+'\\Data\\base detachment\\fric=0.3 v=0.2'

CP.ExperimentPlot(experiment_path,'XoY',1,'standard')  

#data folder path
#case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.0 v=0.2\\input\\base=0.00'

#An.GenerateGIF(r'C:\魏华敬\Spyder\YADE\StressAndStrain\Data\base detachment\fric=0.0 v=0.2\output\base=0.00\stress\maximal shear\images')
         

#file_paths=NP.FilePathsThisCase(case_path)

#Generate map between phase index between spheres list 
#MAP=NSG.GenerateSpheresMapWithSample(case_path)
## 
#spheres=MAP[5]  
       
#shear_strain_matrix=SAM.SpheresStrainMatrix(10,spheres,
#                                        which_plane='XoY',
#                                        which_input_mode='periodical',
#                                        which_output_mode='shear')
#plt.figure()
#plt.imshow(shear_strain_matrix)
#    
#shear_stress_matrix=SAM.SpheresStressMatrix(10,spheres,
#                                        which_plane='XoY',
#                                        which_input_mode='stress',
#                                        which_output_mode='shear')
#plt.figure()
#plt.imshow(shear_stress_matrix)

#CP.SingleExport(case_path,'periodical_strain','distortional','XoY',1)

##export all figure
#CP.TotalExport(case_path,'XoY',1)
