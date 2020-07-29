# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:33:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Plot Spheres
"""

import copy as cp
import numpy as np
import matplotlib.pyplot as plt

from o_grid import grid
from o_mesh import mesh
from o_square import square
from o_circle import circle

import TransformImage as TI
import ProcessDictionary as PD
import RasterizeGraphics as RG

#------------------------------------------------------------------------------
"""
Construct a granular mapping grid

Args:
    which_spheres: spheres to be operated
    length: length of grid
    show: whether to be plotted (bool)
    
Returns:
    grid object list
"""
def Spheres2Grids(which_spheres,length,show=False):

    #find the grid's coordinate range
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #xy border
    boundary_x=[min(x_spheres),max(x_spheres)]
    boundary_y=[min(y_spheres),max(y_spheres)]
    
    #xy length
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
        
    #number of grids in the xy direction
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))
    
    #number of cross points in the xy direction
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    if show:
        
        #x
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*length,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*length,
                       color='k',
                       linestyles="--")
            
        #y
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*length,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*length,
                       color='k',
                       linestyles="--")
             
    #Initialize grids list
    grids=[]
    
    for k_x in range(amount_grid_x):
        
        for k_y in range(amount_grid_y):
            
            #new grid
            this_grid=grid() 
            
            #assignment
            this_grid.length=length
            this_grid.index_x=k_x
            this_grid.index_y=k_y
            this_grid.index=[this_grid.index_x,this_grid.index_y]
            this_grid.position_x=boundary_x[0]+this_grid.index_x*this_grid.length
            this_grid.position_y=boundary_y[0]+this_grid.index_y*this_grid.length
            this_grid.position=np.array([this_grid.position_x,this_grid.position_y])
            this_grid.spheres_inside=[]
            
            #involved
            grids.append(this_grid)
            
    return grids

#------------------------------------------------------------------------------
"""
Transform spheres into image

Args:
    which_spheres: spheres to be operated
    length: length of grid
    show: whether to be plotted (bool)
    factor: zoom factor very important parameter (default: 1)
    
Returns:
    mesh object
"""
def Spheres2Matrix(which_spheres,length,show=False,factor=1):

    #generate spheres grids
    grids=Spheres2Grids(which_spheres,length)
    
    #restruct
    amount_grid_x=max([this_grid.index_x for this_grid in grids])+1
    amount_grid_y=max([this_grid.index_y for this_grid in grids])+1
    
    #total number and type of color
    color_list=[]
    
    #establish mapping relationship
    map_tag_color={}
    map_tag_color[0]=[1.0,1.0,1.0]
    
    #create the tag_color mapping dictionary
    for this_sphere in which_spheres:
        
        if list(this_sphere.color) not in color_list:
            
            color_list.append(list(this_sphere.color))
    
            map_tag_color[len(color_list)]=list(this_sphere.color)
            
        this_sphere.tag=PD.DictKeyOfValue(map_tag_color,list(this_sphere.color))

    #max radius of spheres
    radius_list=[this_sphere.radius for this_sphere in which_spheres]
    radius_max=max(radius_list)
    
    #traverse the grids
    for this_grid in grids:
            
        #new 2D square 
        new_square=square()
        
        new_square.length=this_grid.length*factor
        new_square.center=this_grid.position+np.array([new_square.length/2,new_square.length/2])
        new_square.Init()

        #virtual grid init
        virtual_grid=cp.deepcopy(this_grid)
        virtual_grid.position_x-=radius_max
        virtual_grid.position_y-=radius_max
        virtual_grid.position=np.array([virtual_grid.position_x,virtual_grid.position_y])
        virtual_grid.length+=2*radius_max
        
        #draw a virtual border
        if show:
                 
            #draw a virtual border with radius a+r_max
            plt.vlines(virtual_grid.position_x,
                       virtual_grid.position_y,
                       virtual_grid.position_y+virtual_grid.length,
                       color='r',
                       linestyles="--")
            
            plt.vlines(virtual_grid.position_x+virtual_grid.length,
                       virtual_grid.position_y,
                       virtual_grid.position_y+virtual_grid.length,
                       color='r',
                       linestyles="--")
            
            plt.hlines(virtual_grid.position_y,
                       virtual_grid.position_x,
                       virtual_grid.position_x+virtual_grid.length,
                       color='r',
                       linestyles="--")
            
            plt.hlines(virtual_grid.position_y+virtual_grid.length,
                       virtual_grid.position_x,
                       virtual_grid.position_x+virtual_grid.length,
                       color='r',
                       linestyles="--")
        
        #determine which centers are in the red box
        for this_sphere in which_spheres:
            
            if virtual_grid.SphereInside(this_sphere):
                
                this_grid.spheres_inside.append(this_sphere)
        
        #calculate total area inside grid
        area_inside_this_grid=0
        
        #tag frequency mapping
        map_tag_area={}
        
        #write within spheres_inside
        if this_grid.spheres_inside!=[]:
                
            for this_sphere in this_grid.spheres_inside:
                
                #2D circle
                new_circle=circle()
                
                new_circle.radius=this_sphere.radius*factor
                new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])
                
                #init the circle
                new_circle.Init()
               
                #different circles represent different areas for the same pixel
                area_this_sphere_in_this_grid=new_circle.area*len(RG.ContentSquareCrossCircle(new_square,new_circle))/len(new_circle.points_inside)
                
                #area sum up
                area_inside_this_grid+=area_this_sphere_in_this_grid

                #exist beforehand
                if this_sphere.tag in map_tag_area.keys():
            
                    map_tag_area[this_sphere.tag]+=area_this_sphere_in_this_grid    
                    
                #to add for the first time
                if this_sphere.tag not in map_tag_area.keys():
            
                    map_tag_area[this_sphere.tag]=area_this_sphere_in_this_grid
                    
            
            this_grid.tag=PD.DictKeyOfValue(map_tag_area,max(list(map_tag_area.values())))
            
            #The color corresponding to it
            this_grid.color=map_tag_color[this_grid.tag] 
    
        #collection is empty
        if this_grid.spheres_inside==[]:
            
            this_grid.tag=0
            this_grid.color=np.array([1.0,1.0,1.0])
        
    #output image
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
    img_color_mesh=np.full((amount_grid_x,amount_grid_y,3),np.array([1.0,1.0,1.0]))
   
    for this_grid in grids:
        
        img_tag_mesh[this_grid.index_x,this_grid.index_y]=this_grid.tag
        img_color_mesh[this_grid.index_x,this_grid.index_y]=this_grid.color
        
    #The mesh object to output
    that_mesh=mesh()
    
    #give it value
    that_mesh.grids=grids
    that_mesh.img_tag=TI.ImgFlip(TI.ImgRotate(cp.deepcopy(img_tag_mesh)),0)
    that_mesh.img_color=TI.ImgFlip(TI.ImgRotate(cp.deepcopy(img_color_mesh)),0)
    
    return that_mesh