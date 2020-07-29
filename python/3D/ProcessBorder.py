# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 19:28:43 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Unified Border
"""

#------------------------------------------------------------------------------       
"""
Define boundaries based on spheres: parameters for a separate phase

Args:
    which_spheres_list: spheres in a list
    which_plane: plane to present
    
Returns:
    single axis boundary
"""
def LocalAxisBoundary(which_spheres,which_plane='XoY'):
    
    #all plane mode
    list_plane=['XoY','YoZ','ZoY']
    list_index=[[0,1],[1,2],[2,0]]
    
    #map between plane and index
    map_plane_index=dict(zip(list_plane,list_index))
    
    #index of 2 dimensions
    index_2D=map_plane_index[which_plane]

    #all two-dimensional coordinates
    X=[this_sphere.position[index_2D[0]] for this_sphere in which_spheres]
    Y=[this_sphere.position[index_2D[1]] for this_sphere in which_spheres]
    R=[this_sphere.radius for this_sphere in which_spheres]
    
    #critical value plus or minus maximum radius
    x_boundary=[min(X)-max(R),max(X)+max(R)]
    y_boundary=[min(Y)-max(R),max(Y)+max(R)]
    
    #output list
    local_axis_boundary=x_boundary+y_boundary
      
    return local_axis_boundary
 
#------------------------------------------------------------------------------       
"""
Global axis boundary in different phase

Args:
    which_spheres_list: spheres list
    which_plane: plane to present
    
Returns:
    axis boundary list
"""
def GlobalAxisBoundary(spheres_list,which_plane):
    
    #all phases LocalAxisBoundary
    total_local_axis_boundary=[]
    
    #draw different forms
    for k in range(len(spheres_list)):
        
        #generate spheres
        this_spheres=spheres_list[k]
        
        #collect them
        total_local_axis_boundary.append(LocalAxisBoundary(this_spheres,which_plane))
        
    #4 vertices
    x_boundary_min=min([this_local_axis_boundary[0] for this_local_axis_boundary in total_local_axis_boundary])
    x_boundary_max=max([this_local_axis_boundary[1] for this_local_axis_boundary in total_local_axis_boundary])
    y_boundary_min=min([this_local_axis_boundary[2] for this_local_axis_boundary in total_local_axis_boundary])
    y_boundary_max=max([this_local_axis_boundary[3] for this_local_axis_boundary in total_local_axis_boundary])
    
    #add some boundaries
    x_padding=(x_boundary_max-x_boundary_min)/100
    y_padding=(y_boundary_max-y_boundary_min)/100
    
    #put them together
    global_axis_boundary=[x_boundary_min-x_padding,
                          x_boundary_max+x_padding,
                          y_boundary_min-y_padding,
                          y_boundary_max+y_padding]
    
    return global_axis_boundary