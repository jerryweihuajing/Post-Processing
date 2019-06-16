# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：execution script
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import colors

import sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())

from Object import o_grid
from Object import o_mesh

from Module import Path as Pa
from Module import ColorBar as CB
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

#organize the raw data
#total path
#对所有路径进行读取与处理
folder_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 0'

pixel_step=1

print(folder_path)

##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

#the mode which I search for
mode_list=['structural_deformation',
           'mean_normal_stress',
           'maximal_shear_stress',
           'volumetric_strain',
           'distortional_strain']

#IP.SinglePlot(folder_path,'cumulative_strain','volumetric_strain',10,1)

#Histogram of stress or strain 
def ValueHistogram(which_spheres,input_mode,output_mode):
    
    return

#output all images
IP.TotalOuput(folder_path,pixel_step)

