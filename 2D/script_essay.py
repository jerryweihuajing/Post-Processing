# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:59:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay
"""

"""
demand:
    improve the label font
"""

from __init__ import *

case_path=r'E:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single base salt bT=2.4 sT=5 sD=24 sO=200 sW=400'

'''spheres generation'''
pixel_step=1

that_case=case()

that_case.InitCalculation(case_path)

global_spheres=list(that_case.list_A_progress[-1].map_id_spheres.values())

'''local spheres'''
x_spheres=[this_sphere.position[0] for this_sphere in global_spheres]
y_spheres=[this_sphere.position[1] for this_sphere in global_spheres]

#the radius of the maximum and minimum
radius_of_min=global_spheres[x_spheres.index(min(x_spheres))].radius
radius_of_max=global_spheres[y_spheres.index(max(y_spheres))].radius

#x,y boundary
boundary_x=[min(x_spheres)-radius_of_min,max(x_spheres)+radius_of_min]
boundary_y=[min(y_spheres)-radius_of_max,max(y_spheres)+radius_of_max]
    
local_spheres=[this_sphere for this_sphere in global_spheres if 400<=this_sphere.position[0]<=500]

'''about consumption'''
spheres=cp.deepcopy(local_spheres)

#fetch the mesh object
that_mesh=C_S_B.SpheresContent(spheres,pixel_step)

#surface_map=C_S_B.SpheresTopMap(spheres,pixel_step) 

img_tag=that_mesh.img_tag

#'''effect of content'''
###image
#plt.figure(figsize=(6,6))
#
#plt.imshow(np.flip(that_mesh.img_tag,axis=0),cmap='gray_r')
#plt.axis([0,100,0,100])

#ax_showticks=plt.gca()
#x_major_showticks=[this_tick.get_text() for this_tick in ax_showticks.get_xticklabels()]

#graphics
plt.figure(figsize=(6,6))

BETA_C_S_M.SpheresPlot(spheres,6)

plt.axis([400,500,0,100])

#ax_real=plt.gca()
#x_major_realticks=[int(this_tick.get_text()) for this_tick in ax_real.get_xticklabels()]

'''could not get ticklabel'''
#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(400,500,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(0,100,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)

#'''effect of outline'''
##matrix to draw outline image
#outline_matrix=np.full(np.shape(img_tag),np.nan)
#
##outline in all directions
#surface_outline_content=[]
#bottom_outline_content=[]
#right_outline_content=[]
#left_outline_content=[]
#
##surface and bottom
#for j in range(np.shape(outline_matrix)[1]):
#    
#    this_i_list=[]
#    
#    for i in range(np.shape(outline_matrix)[0]):    
#        
#        if img_tag[i,j]:
#            
#            this_i_list.append(i)
#    
#    try:
#        
#        surface_outline_content.append([np.min(this_i_list),j])
#        bottom_outline_content.append([np.max(this_i_list),j])
#        
#    except:
#        
#        pass
#    
##left and right
#for i in range(np.shape(outline_matrix)[0]):
#    
#    this_j_list=[]
#    
#    for j in range(np.shape(outline_matrix)[1]):    
#        
#        if not np.isnan(outline_matrix[i,j]):
#            
#            this_j_list.append(j)
#            
#    try:
#        
#        right_outline_content.append([i,np.max(this_j_list)])
#        left_outline_content.append([i,np.min(this_j_list)])
#    
#    except:
#        
#        pass
#
##total outline content before improvement
#content_outline=surface_outline_content+\
#                bottom_outline_content+\
#                right_outline_content+\
#                left_outline_content
#
#for this_i,this_j in content_outline:
#
#    outline_matrix[this_i,this_j]=1
#
#plt.figure(figsize=(6,6))
#
#plt.imshow(np.flip(outline_matrix,axis=0),cmap='gray')
#plt.axis([0,100,0,100])
#
#'''effect of outline improvement: edge tracing'''
##total outline content after improvement
#content_outline=C_M_O.OutlineImprovement(surface_outline_content)+\
#                C_M_O.OutlineImprovement(bottom_outline_content)+\
#                C_M_O.OutlineImprovement(right_outline_content)+\
#                C_M_O.OutlineImprovement(left_outline_content)
#                    
#for this_i,this_j in content_outline:
#
#    outline_matrix[this_i,this_j]=1
#    
#plt.figure(figsize=(6,6))
#
#plt.imshow(np.flip(outline_matrix,axis=0),cmap='gray')
#plt.axis([0,100,0,100])

'''effect of rasterization'''
#plot boundary box
#plot image
#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_from_data=C_I.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

#have a test to find the ROI
start_index=400
length_ROI=100

plt.figure(figsize=(6,6))

plt.imshow(img_rgb_from_data[:,start_index:start_index+length_ROI])
plt.axis([0,100,0,100])

'''effect of interplation'''
#plot scatter in grid
#plot gird without value

'''effect of smmothing: structural deformation, stress, strain'''

'''effect of boundary extraction: erosion and expansion'''