# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 22:35:33 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Scatters to Mesh 
"""

import numpy as np
import matplotlib.pyplot as plt

from o_grid import grid
from o_mesh import mesh
from o_scatter import scatter

#------------------------------------------------------------------------------
"""
Shows 2d scatter

Args:
    ax: axes
    which_scatters: scatters object to be operated
    
Returns:
    scatter objects
"""
def ScatterPlot(ax,which_scatters):
    
    if isinstance(which_scatters[0],scatter):
        
        for this_point in which_scatters:
            
            plt.scatter(this_point.pos_x,this_point.pos_y,color='c') 
            
    if isinstance(which_scatters[0],list) and len(which_scatters[0])==2:
        
        for this_point in which_scatters:
            
            plt.scatter(this_point[0],this_point[1],color='c') 
      
#------------------------------------------------------------------------------
"""
Generate a list of discrete granular objects

Args:
    ax: axes
    width, length: the dimensions of the interpolation region
    m_width, n_length: equal amount of width and length
    show: (bool) whether to show
    
Returns:
    scatter objects
"""
def GeneratePoints(ax,width,length,m_width,n_length,show=False):
    
    #final result
    scatters=[]
    
    for m in range(m_width):
        
        for n in range(n_length):
            
            #new scatter
            this_point=scatter()
            
            #the courtyard has point coordinates on the grid
            original_m=m*width/m_width
            original_n=n*length/n_length
            
            #new point coordinates
            new_m=original_m+np.random.rand()
            new_n=original_n+np.random.rand()
            
            #define attributes of the point
            this_point.pos_x=new_m
            this_point.pos_y=new_n
            
            for k in range(5):
                
                if k*(width/5)<=original_m<=(k+1)*(width/5):
                
                    this_point.pos_z=k
          
            #accumulate them
            scatters.append(this_point)

    if show:
            
        ScatterPlot(ax,scatters)
            
    return scatters

#------------------------------------------------------------------------------
"""
Construct the grid point matrix

Args:
    which_scatters: scatters object to be operated
    step: length of grid
    show: (bool) whether to show
    
Returns:
    mesh points coordinates
"""  
def MeshGrids(which_scatters,step,show=False):
    
    #step in x and y direction
    step_x=step_y=step
    
    #coordinates boundary of mesh
    x_scatters=[this_point.pos_x for this_point in which_scatters]
    y_scatters=[this_point.pos_y for this_point in which_scatters]
    
    #the radius corresponding to the maximum and minimum
    radius_of_min=which_scatters[x_scatters.index(min(x_scatters))].radius
    radius_of_max=which_scatters[y_scatters.index(max(y_scatters))].radius
    
    #xy boundary
    boundary_x=[min(x_scatters)-radius_of_min,max(x_scatters)+radius_of_min]
    boundary_y=[min(y_scatters)-radius_of_max,max(y_scatters)+radius_of_max]
    
    #xy length
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
         
    #amount of grid in x and y respectively
    amount_grid_x=int(np.ceil(length_x/step_x))
    amount_grid_y=int(np.ceil(length_y/step_y))
    
    #amount of mesh cross points in x and y respectively
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    if show:
        
        #x direction
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*step_x,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*step_y,
                       color='k',
                       linestyles="--")
            
        #y direction
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*step_y,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*step_x,
                       color='k',
                       linestyles="--")
     
    #Generate the coordinate matrix of the grid intersection
    mesh_points=[]
    
    for k_x in range(amount_grid_x):
        
        for k_y in range(amount_grid_y):
            
            mesh_points.append([boundary_x[0]+k_x*step_x,boundary_y[0]+k_y*step_y])
                
    return np.array(mesh_points).reshape((amount_grid_x,amount_grid_y,2)) 

#------------------------------------------------------------------------------
"""
Transform scatters into mesh object

Args:
    which_scatters: scatters object to be operated
    grid_length: length of grid
    show: (bool) whether to show
    
Returns:
    mesh object
"""      
def ScattersMesh(which_scatters,grid_length,show=False):

    print('')
    print('-- Scatters Mesh')
    print('-> grid length:',grid_length)
    
    #coordinates boundary of mesh
    x_scatters=[this_scatter.pos_x for this_scatter in which_scatters]
    y_scatters=[this_scatter.pos_y for this_scatter in which_scatters]
    
    #the radius corresponding to the maximum and minimum
    radius_of_min=which_scatters[x_scatters.index(min(x_scatters))].radius
    radius_of_max=which_scatters[y_scatters.index(max(y_scatters))].radius
    
    #xy boundary
    boundary_x=[min(x_scatters)-radius_of_min,max(x_scatters)+radius_of_min]
    boundary_y=[min(y_scatters)-radius_of_max,max(y_scatters)+radius_of_max]
    
    #xy length
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
    
    #amount of grid in x and y respectively
    amount_grid_x=int(np.ceil(length_x/grid_length))
    amount_grid_y=int(np.ceil(length_y/grid_length))
    
    #amount of mesh cross points in x and y respectively
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1

    if show:
        
        #x direction
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*grid_length,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*grid_length,
                       color='k',
                       linestyles="--")
            
        #y direction
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*grid_length,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*grid_length,
                       color='k',
                       linestyles="--")
             
    #initialize grids list
    grids=[]
    
    for k_x in range(amount_grid_x):
        
        for k_y in range(amount_grid_y):
            
            #new grid
            this_grid=grid() 
            
            #assignment
            this_grid.length=grid_length
            this_grid.index_x=k_x
            this_grid.index_y=k_y
            this_grid.index=[this_grid.index_x,this_grid.index_y]
            this_grid.position_x=boundary_x[0]+this_grid.index_x*this_grid.length
            this_grid.position_y=boundary_y[0]+this_grid.index_y*this_grid.length
            this_grid.position=np.array([this_grid.position_x,this_grid.position_y])
            this_grid.spheres_inside=[]
            
            #involved
            grids.append(this_grid)
            
    #output image tag
    img_tag_mesh=np.full((amount_grid_x,amount_grid_y),np.nan) 
    
    #define new mesh object
    that_mesh=mesh()
    
    #assign the value
    that_mesh.grids=grids
    that_mesh.img_tag=img_tag_mesh
    that_mesh.boundary_x=boundary_x
    that_mesh.boundary_y=boundary_y
    
    return that_mesh