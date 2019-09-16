# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 14:11:13 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：initialization script
"""

import imageio
import copy as cp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from matplotlib import colors

import sys,os
    
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\Module')
sys.path.append(os.getcwd()+'\\Object')
sys.path=list(set(sys.path)) 

from o_grid import grid
from o_mesh import mesh
from o_sphere import sphere
from o_strain_2D import strain_2D
from o_discrete_point import discrete_point

import Norm as No
import Path as Pa
import Image as Img
import Matrix as Mat
import Global as Glo
import NewPath as NP
import ColorBar as CB
import Animation as An
import Histogram as His
import CustomPlot as CP
import Decoration as Dec
import Dictionary as Dict
import SpheresPlot as SP
import ProgressPlot as PP
import IntegralPlot as IP
import AxisBoundary as AB
import Interpolation as In
import ValueBoundary as VB
import AnimationPlot as AP
import ExperimentPlot as EP
import SpheresBoundary as SB
import SpheresGeneration as SG
import ImageSuperposition as IS
import NewSpheresGeneration as NSG
import IntegralAnalysisPlot as IAP
import SpheresAttributeMatrix as SAM

import StrainPlot as Strain
import StressPlot as Stress