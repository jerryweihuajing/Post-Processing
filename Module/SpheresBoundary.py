# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:50:34 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Calculate boundaries from spheres system
"""

"""
1 Rasterization and calculate the pixels which spheres take up
2 Boundary Tracking: a method in Computer Vision
"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append(r'C:\Users\whj\Desktop\Spyder\YADE\Stress Strain')

from Object import o_mesh

from Module import Interpolation as In
from Module import Rasterization as Ra

#============================================================================== 
#Calculate the pixels up which the spheres take
#length: length of every single grid
#factor: expand ratio
#return: a mesh object presenting content and img
def SpheresContent(which_spheres,length,factor=1,show=False):
    
    #首先找出网格的坐标范围
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #xy边界
    boundary_x=[min(x_spheres),max(x_spheres)]
    boundary_y=[min(y_spheres),max(y_spheres)]
    
    #xy边长
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
        
    #xy方向上的网格数
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))
    
    #xy方向上的网格交点数
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    #total pixels
    spheres_content=[]
                 
    #traverse spheres
    for this_sphere in which_spheres:
            
        #new 2D circle
        new_circle=Ra.circle()
        
        new_circle.radius=this_sphere.radius*factor
        new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])
        
        new_circle.Init()
        
        for this_pos in new_circle.points_inside:
            
            if 0<=this_pos[0]/length<amount_mesh_points_x and 0<=this_pos[1]/length<amount_mesh_points_y:
                    
                if this_pos not in spheres_content:
                    
                    spheres_content.append(this_pos)  

    #check the shape
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
   
#    print(np.shape(img_tag_mesh))
    
    for this_pos in spheres_content:
        
#        print(this_pos)
        
        #restrict the boundary
        this_i=int(this_pos[0]/length)
        this_j=int(this_pos[1]/length)
        
        if 0<=this_i<amount_grid_x and 0<=this_j<amount_grid_y:

            img_tag_mesh[this_i,this_j]=1
     
#        print(this_i,this_j)
               
    #define new mesh
    that_mesh=o_mesh.mesh()
    
    #Rotatation is in need
    that_mesh.img_tag=In.ImgFlip(In.ImgRotate(img_tag_mesh),0)
    that_mesh.content=spheres_content   
    
    if show:
        
        plt.imshow(img_tag_mesh)
    
    return that_mesh

'''
Calculate the elavation
the surface could be calculated, do do the 'left' 'right' 'top' 'bottom'
'''
#============================================================================== 
#Calculate spheres surface from a mesh object
#return: an img tag presenting the elavation
def SpheresSurfaceMap(which_spheres,length,factor=1):

    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,show)
 
    #地表的列表
    map_j_i_surface={}
    
    #img tag
    for j in range(np.shape(that_mesh.img_tag)[1]):
        
        map_j_i_surface[j]=np.shape(that_mesh.img_tag)[0]
        
        for i in range(np.shape(that_mesh.img_tag)[0]):

            if that_mesh.img_tag[i,j]!=0:
                
#                print(np.shape(that_mesh.img_tag)[0]-i)
                
                map_j_i_surface[j]=i
                
                break
            
    return map_j_i_surface  
 
#==============================================================================     
#img to map
#convenient to plot
def SpheresSurfaceImg(which_spheres,length,factor=1,show=False):
    
    #fetch the mesh object
    that_mesh=SpheresContent(which_spheres,length,factor)
    
    #img to present the elavation
    that_img_tag=np.full(np.nan,np.shape(that_mesh.img_tag))    
    
    #surface map to img tag
    for k in range(len(map_j_i_surface)):
        
        this_j=list(map_j_i_surface.keys())[k]
        this_i=list(map_j_i_surface.values())[k]
    
        that_img_tag[this_i,this_j]=1
    
    #show or not
    if show:   
        
        plt.imshow(that_img_tag)
      
    return that_img_tag
        
#txt_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 0'
#ax=plt.subplot()
#this_mesh=SP.SpheresGrids(ax,spheres,1)
#
#plt.figure()
#plt.imshow(this_mesh.img_tag)