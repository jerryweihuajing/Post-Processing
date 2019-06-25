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
from Module import ContentBoundary as CB
from Module import SpheresBoundary as SB
from Module import SpheresGeneration as SG

from Module import StrainPlot as Strain
from Module import StressPlot as Stress

'''
demand 4:
draw surface with stress or strain figure
'''

#organize the raw data
case_path=r'C:\魏华敬\Spyder\YADE\Stress Strain\Data\L=1000 v=1.0 r=1.0 layer=10 detachment=0-4\input\case 0'

#print(folder_path)

##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

#the mode which I search for
#mode_list=['shear_strain',
#           'volumetric_strain',
#           'distortional_strain']

#mode_list=['distortional_strain','volumetric_strain','shear_strain','y_normal_strain']

#mode_list=['distortional_strain']
#
#IP.SinglePlot(folder_path,'periodical_strain','y_normal_strain',1)

#load_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 1\output\periodical strain\x normal strain'

#load_path=r'C:\Users\whj\Desktop\operation'
##An.GenerateGIF(load_path)
##
#load_path=r'C:\魏华敬\Spyder\YADE\Stress Strain\Data\L=1000 v=1.0 r=1.0 layer=10 detachment=0-4\output\2019.6.19\case 4\periodical strain\y normal strain'
#
#An.GenerateGIF(load_path)

#output all images
#IP.TotalOuput(case_path,1)

which_spheres=SG.GenerateSpheresFromTXT('progress=48.37%.txt')[0]

pixel_step=1
#
#plt.figure()
#SB.SpheresLeftImg(which_spheres,pixel_step,show=True)
#SB.SpheresRightImg(which_spheres,pixel_step,show=True)
#SB.SpheresBottomImg(which_spheres,pixel_step,show=True)
#SB.SpheresSurfaceImg(which_spheres,pixel_step,show=True)

plt.figure()
SB.SimpleSpheresBoundary(which_spheres,pixel_step,show=True)

#edge=SB.SpheresEdge(spheres,pixel_step,True)
      
#new format of file organization
