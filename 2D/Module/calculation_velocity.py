# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 21:50:59 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation of Velocity
"""

import numpy as np

from o_scatter import scatter

#------------------------------------------------------------------------------
"""
Generate velocity scatters

Args:
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX]' displacement in 3 planes
    which_direction: ['x','y','z'] displacement in 3 different direction
    
Returns:
    scatters objects list
"""
def ScattersVelocity(which_spheres,which_plane,which_direction):
    
    print('')
    print('-- Scatters Velocity')
    print('-> plane:',which_plane)
    print('-> direction:',which_direction)
    
    #result list
    scatters=[]
    
    #traverse all spheres
    for this_sphere in which_spheres:
    
        #expire sphere from uplift
        if this_sphere.tag==9:
            
            continue
        
        #new discrete point object
        new_scatter=scatter()
        
        #plane
        list_plane=['XoY','YoZ','ZoX']
        list_position_index=[(0,1),(1,2),(2,0)]
        
        #create index-value map
        map_plane_position_index=dict(zip(list_plane,list_position_index))
        
        new_scatter.pos_x=this_sphere.position[map_plane_position_index[which_plane][0]]
        new_scatter.pos_y=this_sphere.position[map_plane_position_index[which_plane][1]]
        
        #radius
        new_scatter.radius=this_sphere.radius   
        
        #direction
        list_direction=['x','y','z']
        list_velocity_index=[0,1,2]
        
        #create index-value map
        map_direction_velocity_index=dict(zip(list_direction,list_velocity_index))
 
        try:
            
            if which_direction=='resultant':
                
                new_scatter.pos_z=np.sqrt(this_sphere.velocity[0]**2+this_sphere.velocity[1]**2)
                
            else:
                
                new_scatter.pos_z=this_sphere.velocity[map_direction_velocity_index[which_direction]]
              
        except:
            
            continue
        
        scatters.append(new_scatter)
        
    return scatters