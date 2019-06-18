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
from Module import Animation as An
from Module import SpheresPlot as SP
from Module import IntegralPlot as IP
from Module import Interpolation as In
from Module import ValueBoundary as VB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

#organize the raw data
folder_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 2'

print(folder_path)

##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

#the mode which I search for
mode_list=['x_normal_strain',
           'y_normal_strain',
           'shear_strain',
           'volumetric_strain',
           'distortional_strain']

#mode_list=['distortional_strain','volumetric_strain','shear_strain','y_normal_strain']

#mode_list=['distortional_strain']
#
#IP.SinglePlot(folder_path,'periodical_strain','y_normal_strain',1)

#load_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 1\output\periodical strain\x normal strain'

#load_path=r'C:\Users\whj\Desktop\operation'
#An.GenerateGIF(load_path)
#
#load_path=r'C:\Users\whj\Desktop\performance'
#An.GenerateGIF(load_path)

#output all images
IP.TotalOuput(folder_path,1,mode_list)

#new format of file organization

'''
demand 1: 
restart with a totally new input data

total folder: input
              output
              
input: case 0 
       case 1 
       case 2 
       case ...
       
case x: stress
        cumulative strain
        periodical strain
        
output: structural deformation
        stress
        cumulative strain
        periodical strain

stress: xx stress
        ......
        
strain: xx strain
        ......     

demand 2:
save matrix as txt or other format

demand 4:
draw surface with stress or strain figure
'''
