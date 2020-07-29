# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:27:36 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

import os
import ImportSpheres as IS
import PlotSpheres as PS
import TransformImage as TI

import matplotlib.pyplot as plt

#Import a case
case_path=os.getcwd()+'\\Data\\salt detachment\\fric=0.3 v=0.2\\input\\salt=0.00'


#map between index and spheres
map_all_phase_spheres=IS.GenerateSpheresMapWithSample(case_path)

#%%
#take index 11 as example
spheres=map_all_phase_spheres[11]

#slice operation
list_plane=['XoY','YoZ','ZoX']

#index of a plane
list_plane_index=[[0,1],[1,2],[2,0]]

#another dimension
list_slice_index=[2,0,1]

plane='YoZ'

import numpy as np

#all 3-dimensional coordinates
X=[this_sphere.position[0] for this_sphere in spheres]
Y=[this_sphere.position[1] for this_sphere in spheres]
Z=[this_sphere.position[2] for this_sphere in spheres]

#and radius
R=[this_sphere.radius for this_sphere in spheres]

#critical value plus or minus maximum radius
x_boundary=[min(X)-max(R),max(X)+max(R)]
y_boundary=[min(Y)-max(R),max(Y)+max(R)]
z_boundary=[min(Z)-max(R),max(Z)+max(R)]

#amount of slice
pos_slice=(min(X)+max(X))/2

#threshold of slice
slice_threshold=[pos_slice-np.mean(R),pos_slice+np.mean(R)]

#filter to get spheres in this threshold
spheres_this_slice=[this_sphere for this_sphere in spheres if slice_threshold[0]<=this_sphere.position[0]<=slice_threshold[1]]

#Spheres image
spheres_grids=PS.Spheres2Matrix(spheres_this_slice,1)

#Image
this_img=TI.ImgFlip(spheres_grids.img_color,0)
this_img_tag=TI.ImgFlip(spheres_grids.img_tag,0)

plt.imshow(this_img)