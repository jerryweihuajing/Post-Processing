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

from Object.o_grid import grid
from Object.o_mesh import mesh
from Object.o_sphere import sphere

from Module import Path as Pa
from Module import NewPath as NP
from Module import ColorBar as CB
from Module import Animation as An
from Module import Dictionary as Dict
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

#data folder path
case_path=os.getcwd()+'\\Data\\base detachment\\fric=0.3 v=1.0\\input\\base=0.00'

#file_names=FileNamesThisCase(case_path)
file_paths=NP.FilePathsThisCase(case_path)

#Generate spheres
#
#for this_file in file_paths:
#    
#    print(len(SG.GenerateSpheresFromFile(this_file)))

#displacement cumulative periodical
 
#spheres_start=SG.GenerateSpheresFromFile(file_paths[0])
#
#spheres_now=SG.GenerateSpheresFromFile(file_paths[-1])


#------------------------------------------------------------------------------
"""
Generate sample spheres position

Args:
    case_path: load path of all input files
    
Returns:
    sample spheres position lists
"""
def SamplePos(case_path):
    
    #path of sample
    sample_path=case_path.split('input')[0]+'sample.txt'
    
    #all lines of sample
    sample_lines=open(sample_path,'r').readlines()[1:]
    
    #position of sample
    sample_pos=[]
    
    for this_line in sample_lines:
        
        this_list=this_line.strip('\n').split('\t')
        
        #position of this sphere
        this_pos=np.array([float(item) for item in this_list[:3]])
    
        #collect pos
        sample_pos.append(this_pos)
        
    return sample_pos

#------------------------------------------------------------------------------
"""
Generate spheres position in a phase

Args:
    file_path: load path of file
    
Returns:
    spheres position list in a phase
"""
def PhasePos(file_path):
    
    #position of spheres in a phase
    phase_pos=[]
    
    #all lines
    lines=open(file_path,'r').readlines()
    
    #correct legnth of each line
    correct_length=len(lines[0].strip('\n').split(','))
    
    #traverse all lines
    for this_line in lines:
        
        this_list=this_line.strip('\n').split(',')
 
        #judge if total length is OK
        if len(this_list)!=correct_length:
            
            continue
          
        phase_pos.append(np.array([float(this_str) for this_str in this_list[5:8]]))
        
    return phase_pos
        
#------------------------------------------------------------------------------    
"""
Generate spheres position in different phases in a case

Args:
    case_path: load path of all input files
    
Returns:
    list which contain spheres position list of differnet phase
"""
def AllPhasepos(case_path):
    
    #input txt file names
    file_names=NP.FilePathsThisCase(case_path)
    
    return [PhasePos(this_file_name) for this_file_name in file_names]
      
#------------------------------------------------------------------------------
"""
Generate spheres map in a case with assistance of sample.txt

Args:
    case_path: load path of all input files
    
Returns:
    A map whose values are spheres lists
"""
def GenerateSpheresMapWithSample(case_path):
    
    #Generate sample spheres position
    sample_pos=SamplePos(case_path)
        
    #spheres position in different phases in a case
    all_phase_pos=AllPhasepos(case_path)

#    print(len(all_phase_pos[0]))
#    print(len(sample_pos))
    
    for k in range(len(all_phase_pos[0])):
        
#        print(all_phase_pos[0][0]-sample_pos[0])
#        
    
GenerateSpheresMapWithSample(case_path)
#------------------------------------------------------------------------------
"""
Generate cumulative displacement of spheres

Args:
    
    
Returns:
    
"""
def SpheresCumulativeDisplacement(spheres_start,spheres_now):
    
    return


#------------------------------------------------------------------------------
"""
Generate cumulative strain of spheres

Args:
    spheres_start: original spheres (from file_names[0])
    spheres_now: spheres to be processed (from file_names[k])
    
Returns:
    spheres list with cumulative strain
"""
def SpheresCumulativeStrain(spheres_start,spheres_now):
    
    return
"""
Generate periodical strain of spheres

Args:
    spheres_last: spheres in last period (from file_names[k-1])
    spheres_now: spheres to be processed (from file_names[k])
    
Returns:
    spheres list with cumulative strain
"""
def SpheresPeriodicalStrain(spheres_last,spheres_now):
    
    return

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

#which_spheres=SG.GenerateSpheresFromTXT('progress=48.37%.txt')[0]

#pixel_step=1
#
#plt.figure()
#SB.SpheresLeftImg(which_spheres,pixel_step,show=True)
#SB.SpheresRightImg(which_spheres,pixel_step,show=True)
#SB.SpheresBottomImg(which_spheres,pixel_step,show=True)
#SB.SpheresSurfaceImg(which_spheres,pixel_step,show=True)

#plt.figure()
#
#SB.SimpleSpheresBoundary(which_spheres,pixel_step,show=True)

#edge=SB.SpheresEdge(spheres,pixel_step,True)
      
