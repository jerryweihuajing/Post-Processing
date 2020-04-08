# -*- coding: utf-8 -*-
"""
Created on Sat May  4 15:25:52 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation of Spheres in Image
"""

'''
demand:
    Calculate strain via displacement
'''

"""
Hint:
    Calculation for gradient on y need to add '-' for the geometry of mat and axis is not same
    gradient always comes from larger index to the smaller one
"""

import copy as cp
import numpy as np

import matplotlib.pyplot as plt
    
from o_grid import grid
from o_mesh import mesh
from o_square import square
from o_circle import circle
from o_scatter import scatter

import operation_dictionary as O_D

import calculation_strain as C_Strain
import calculation_stress as C_Stress

import calculation_image as C_Im
import calculation_velocity as C_V
import calculation_rasterization as C_R
import calculation_interpolation as C_In

from configuration_yade_color import yade_rgb_list

#------------------------------------------------------------------------------
"""
Draws all sphere objects via MatplotLib

Args:
    which_spheres: spheres object to be operated
    
Returns:
    None
"""
def SpheresPlot(which_spheres):
    
    for this_sphere in which_spheres:
        
        plt.plot(this_sphere.position[0],
                 this_sphere.position[1],
                 marker='o',
                 markersize=this_sphere.radius,
                 color=this_sphere.color)      
        
#------------------------------------------------------------------------------
"""
Characterization of RGB particle list in structural form

Args:
    which_spheres: spheres object to be operated
    
Returns:
    scatter objects
""" 
def DiscreteValue_rgb(which_spheres):
    
    #result scatter list
    scatters=[]
    
    #traverse all spheres
    for this_sphere in which_spheres:
    
        #create dscatter objects
        new_scatter=scatter()
        
        #define basic attributes
        new_scatter.pos_x=this_sphere.position[0]
        new_scatter.pos_y=this_sphere.position[1]
        new_scatter.pos_z=this_sphere.color
        
        #delete the point with an infinite z value
        if max(new_scatter.pos_z)>1 or min(new_scatter.pos_z)<0:
            
            print(new_scatter.pos_z)
            
            continue
            
        scatters.append(new_scatter)
        
    return scatters

"""
2 methods of putting spheres into the grid:
    A: Area of spheres within the grid
    B: Amount of spheres within the grid

attention: 
    when the mesh is smaller than the particle, the resolution is limited
"""  
#------------------------------------------------------------------------------
"""
Characterization of RGB particle list in structural form

Args:
    which_spheres: spheres object to be operated
    length: length of grid
    show: (bool) whether to show
    
Returns:
    grid objects
"""       
def SpheresGrids(which_spheres,length,show=False):

    print('')
    print('-- Spheres Grids')
    print('-> grid length:',length)
    
    #find out the coordinate range of the grid
    x_spheres=[this_sphere.position[0] for this_sphere in which_spheres]
    y_spheres=[this_sphere.position[1] for this_sphere in which_spheres]
    
    #最大最小值对应的半径
    radius_of_min=which_spheres[x_spheres.index(min(x_spheres))].radius
    radius_of_max=which_spheres[y_spheres.index(max(y_spheres))].radius
    
    #xy边界
    boundary_x=[min(x_spheres)-radius_of_min,max(x_spheres)+radius_of_min]
    boundary_y=[min(y_spheres)-radius_of_max,max(y_spheres)+radius_of_max]
    
    #xy length
    length_x=boundary_x[1]-boundary_x[0]
    length_y=boundary_y[1]-boundary_y[0]
        
    #amount of grids in the xy direction
    amount_grid_x=int(np.ceil(length_x/length))
    amount_grid_y=int(np.ceil(length_y/length))
    
    #amount of grid intersections in the xy direction
    amount_mesh_points_x=amount_grid_x+1
    amount_mesh_points_y=amount_grid_y+1
    
    if show:
        
        #X direction
        for k_x in range(amount_mesh_points_x):
            
            plt.vlines(boundary_x[0]+k_x*length,
                       boundary_y[0],
                       boundary_y[0]+amount_grid_y*length,
                       color='k',
                       linestyles="--")
            
        #Y direction
        for k_y in range(amount_mesh_points_y):
            
            plt.hlines(boundary_y[0]+k_y*length,
                       boundary_x[0],
                       boundary_x[0]+amount_grid_x*length,
                       color='k',
                       linestyles="--")
             
    #initialize grids list
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
    which_spheres: spheres object to be operated
    length: length of grid
    show: (bool) whether to show
    method: fill-in method (default: 'A')
    factor: zoom factor (default: 1)
    
Returns:
    a mesh object
"""  
def SpheresImage(which_spheres,length,show=False,method='A',factor=1):

    print('')
    print('-- Spheres Image')
    print('-> grid length:',length)
    
    #generate spheres grids
    grids=SpheresGrids(which_spheres,length)
    
    #restruct
    amount_grid_x=max([this_grid.index_x for this_grid in grids])+1
    amount_grid_y=max([this_grid.index_y for this_grid in grids])+1
    
    #create a tag_color mapping dictionary
    for this_sphere in which_spheres:

        this_sphere.tag=yade_rgb_list.index(this_sphere.color)

    if method=='B':
        
        tag_list=[k for k in range(len(yade_rgb_list))]
        
        #put spheres into grid
        for this_sphere in which_spheres:
            
            for this_grid in grids:
                
                #judge if it is inside grid
                if this_grid.position_x<=this_sphere.position[0]<this_grid.position_x+this_grid.length and\
                   this_grid.position_y<=this_sphere.position[1]<this_grid.position_y+this_grid.length:
                    
                    this_grid.spheres_inside.append(this_sphere)  
                    
        #dictionary of each tag and amount
        grid_map_tag_color=dict(zip(tag_list,len(tag_list)*[0]))
             
        #calculate the number of certain colors           
        for this_grid in grids:     
            
            #每个grid都会有的
            this_grid.map_tag_color=cp.deepcopy(grid_map_tag_color)
            
            #grid内的所有sphere
            for this_sphere_inside in this_grid.spheres_inside:
                
                this_grid.map_tag_color[this_sphere_inside.tag]+=1
             
            #tag of the most amount
            this_grid.tag=O_D.DictKeyOfValue(this_grid.map_tag_color,max(list(this_grid.map_tag_color.values())))
            
            #its rgb
            this_grid.color=yade_rgb_list[this_grid.tag]       
            
    '''A'''
    if method=='A':
        
        #max radius in spheres
        radius_list=[this_sphere.radius for this_sphere in which_spheres]
        radius_max=max(radius_list)
        
        #traverse the grids
        for this_grid in grids:
                
            #new 2D square 
            new_square=square()
            
            new_square.length=this_grid.length*factor
            new_square.center=(this_grid.position+np.array([new_square.length/2,new_square.length/2]))*factor
            new_square.Init()
    
            #construct virtual grid
            virtual_grid=cp.deepcopy(this_grid)
            
            virtual_grid.position_x-=radius_max
            virtual_grid.position_y-=radius_max
            virtual_grid.position=np.array([virtual_grid.position_x,virtual_grid.position_y])
            virtual_grid.length+=2*radius_max
            
            #draw a virtual border
            if show:
                     
                #draw a virtual border with a radius of a+r_max
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
            
            #calculate total area
            area_inside_this_grid=0
            
            #map between tag and its area
            map_tag_area={}
            
            #work on spheres_inside
            if this_grid.spheres_inside!=[]:
                    
                for this_sphere in this_grid.spheres_inside:
                    
                    #2d circle object
                    new_circle=circle()
                    
                    new_circle.radius=this_sphere.radius*factor
                    new_circle.center=np.array([this_sphere.position[0],this_sphere.position[1]])*factor
                    
                    new_circle.Init()
                    
                    #circles with the same pixel represent different areas
                    area_this_sphere_in_this_grid=new_circle.area*len(C_R.ContentSquareCrossCircle(new_square,new_circle))/len(new_circle.points_inside)
                    
                    #accumulate area
                    area_inside_this_grid+=area_this_sphere_in_this_grid

                    #it exists already
                    if this_sphere.tag in map_tag_area.keys():
                
                        map_tag_area[this_sphere.tag]+=area_this_sphere_in_this_grid    
                        
                    #add for the 1st time
                    if this_sphere.tag not in map_tag_area.keys():
                
                        map_tag_area[this_sphere.tag]=area_this_sphere_in_this_grid
                        
                this_grid.tag=O_D.DictKeyOfValue(map_tag_area,max(list(map_tag_area.values())))
              
                #its rgb
                this_grid.color=yade_rgb_list[this_grid.tag] 
        
            #void set
            if this_grid.spheres_inside==[]:
                
                this_grid.tag=-1
                this_grid.color=np.array([1.0,1.0,1.0])
        
    #output image
    img_tag_mesh=np.zeros((amount_grid_x,amount_grid_y))
    img_color_mesh=np.full((amount_grid_x,amount_grid_y,3),np.array([1.0,1.0,1.0]))
   
    for this_grid in grids:
        
        img_tag_mesh[this_grid.index_x,this_grid.index_y]=this_grid.tag
        img_color_mesh[this_grid.index_x,this_grid.index_y]=this_grid.color
        
    #output mesh object
    that_mesh=mesh()
    
    #assign the value
    that_mesh.grids=grids
    that_mesh.img_tag=C_Im.ImgFlip(C_Im.ImgRotate(cp.deepcopy(img_tag_mesh)),0)
    that_mesh.img_color=C_Im.ImgFlip(C_Im.ImgRotate(cp.deepcopy(img_color_mesh)),0)
    
    return that_mesh

#------------------------------------------------------------------------------
"""
Velocity interpolation image (mesh points)

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_surface_bottom_map: to save computation time by not directly participating in interpolation calculation
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Displacement matrix in one direction
"""
def SpheresVelocityMatrix(pixel_step,
                          which_spheres,
                          which_plane,
                          which_surface_bottom_map,
                          which_interpolation):
    
    print('')
    print('-- Spheres Velocity Matrix')
    print('-> plane:',which_plane)
    
    #scatter objects: components of velocity
    scatters_velocity_x=C_V.ScattersVelocity(which_spheres,which_plane,'x')    
    scatters_velocity_y=C_V.ScattersVelocity(which_spheres,which_plane,'y')  
    
    #matrix of velocity components
    if which_interpolation=='scatters_in_grid':
        
        X=C_In.ScattersInGridIDW(scatters_velocity_x,pixel_step,which_surface_bottom_map)
        Y=C_In.ScattersInGridIDW(scatters_velocity_y,pixel_step,which_surface_bottom_map)

    #axis=0 x gradient, axis=1 y gradient
    X_x=+np.gradient(X,axis=1)
    X_y=-np.gradient(X,axis=0)
    Y_x=+np.gradient(Y,axis=1)
    Y_y=-np.gradient(Y,axis=0)

    #resultant displacement
    V=np.sqrt(X**2+Y**2) 
    V_x=+np.gradient(V,axis=1)
    V_y=-np.gradient(V,axis=0)
    
    #make sure shape is same
    if not (np.shape(X)==\
            np.shape(Y)==\
            np.shape(V)==\
            np.shape(V_x)==\
            np.shape(V_y)==\
            np.shape(X_y)==\
            np.shape(Y_y)==\
            np.shape(X_x)==\
            np.shape(Y_x)):
        
        print('=> ERROR: Incorrect dimension')
        
        return
    
    #map between name and strain
    map_velocity={}
    
    map_velocity['X']=X
    map_velocity['Y']=Y
    map_velocity['X Gradient of X']=X_x
    map_velocity['Y Gradient of X']=X_y
    map_velocity['X Gradient of Y']=Y_x
    map_velocity['Y Gradient of Y']=Y_y
    
    map_velocity['Resultant']=V  
    map_velocity['X Gradient of Resultant']=V_x
    map_velocity['Y Gradient of Resultant']=V_y
    
    map_velocity['Resultant Gradient of X']=np.sqrt(X_x**2+X_y**2)
    map_velocity['Resultant Gradient of Y']=np.sqrt(Y_x**2+Y_y**2)
    map_velocity['Resultant Gradient of Resultant']=np.sqrt(V_x**2+V_y**2)
    
    return dict(zip([this_key+' Velocity' for this_key in list(map_velocity.keys())],list(map_velocity.values())))
    
#------------------------------------------------------------------------------
"""
Displacement interpolation image (mesh points)

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_direction: ['x','y','z'] displacement in 3 different direction
    which_input_mode: ['periodical','cumulative','instantaneous'] dispalcement mode
    which_surface_bottom_map: to save computation time by not directly participating in interpolation calculation
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Displacement matrix in one direction
"""
def SpheresDisplacementMatrix(pixel_step,
                              which_spheres,
                              which_plane,
                              which_direction,
                              which_input_mode,
                              which_surface_bottom_map,
                              which_interpolation):
    
    print('')
    print('-- Spheres Displacement Matrix')
    print('-> plane:',which_plane)
    print('-> direction:',which_direction)
    print('-> input mode:',which_input_mode)
    
    #scatter objects
    scatters=C_Strain.ScattersDisplacement(which_spheres,
                                           which_plane,
                                           which_direction,
                                           which_input_mode.split('_')[0])
    
    if which_interpolation=='scatters_in_grid':
        
        return C_In.ScattersInGridIDW(scatters,pixel_step,which_surface_bottom_map)
    
#------------------------------------------------------------------------------
"""
Spheres strain objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_input_mode: ['periodical','cumulative','instantaneous'] dispalcement mode
    which_surface_bottom_map: to save computation time by not directly participating in interpolation calculation
    which_interpolation: ['scatters_in_grid','grids_in_scatter]
    
Returns:
    Spheres strain values matrix
"""   
def SpheresStrainMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_input_mode,
                        which_surface_bottom_map,
                        which_interpolation):
    
    print('')
    print('-- Spheres Strain Matrix')
    print('-> plane:',which_plane)
    print('-> input mode:',which_input_mode)
    
    #displacemnt in x direction
    X=SpheresDisplacementMatrix(pixel_step,
                                which_spheres,
                                which_plane,
                                'x',
                                which_input_mode,
                                which_surface_bottom_map,
                                which_interpolation)
    
    #displacemnt in y direction
    Y=SpheresDisplacementMatrix(pixel_step,
                                which_spheres,
                                which_plane,
                                'y',
                                which_input_mode,
                                which_surface_bottom_map,
                                which_interpolation)

    #axis=0 x gradient(+), axis=1 y gradient(-)
    ε_xx=+np.gradient(X,axis=1)
    ε_yy=-np.gradient(Y,axis=0)
    γ_xy=+np.gradient(Y,axis=1)-np.gradient(X,axis=0)

    #make sure shape is same
    if not (np.shape(ε_xx)==\
            np.shape(ε_yy)==\
            np.shape(γ_xy)):
        
        print('=> ERROR: Incorrect dimension')
        
        return
    
    #map between name and strain
    map_strain={}
    
    map_strain['X Normal']=ε_xx
    map_strain['Y Normal']=ε_yy
    map_strain['Shear']=γ_xy
    map_strain['Mean Normal']=0.5*(ε_xx+ε_yy)
    map_strain['Diff Normal']=0.5*(ε_xx-ε_yy)
    
    map_strain['Maximal Normal']=0.5*(ε_xx+ε_yy)+np.sqrt((0.5*(ε_xx-ε_yy))**2+(0.5*γ_xy)**2)
    map_strain['Minimal Normal']=0.5*(ε_xx+ε_yy)-np.sqrt((0.5*(ε_xx-ε_yy))**2+(0.5*γ_xy)**2)
    map_strain['Maximal Shear']=+np.sqrt((0.5*(ε_xx-ε_yy))**2+(0.5*γ_xy)**2)
    map_strain['Minimal Shear']=-np.sqrt((0.5*(ε_xx-ε_yy))**2+(0.5*γ_xy)**2)
    
    map_strain['Volumetric']=ε_xx+ε_yy
    map_strain['Distortional']=(0.5*(ε_xx-ε_yy))**2+(0.5*γ_xy)**2
 
    #x, y gradient of X, Y
    X_x=+np.gradient(X,axis=1)
    X_y=-np.gradient(X,axis=0)
    Y_x=+np.gradient(Y,axis=1)
    Y_y=-np.gradient(Y,axis=0)
    
    #resultant displacement
    D=np.sqrt(X**2+Y**2) 
    D_x=+np.gradient(D,axis=1)
    D_y=-np.gradient(D,axis=0)
    
    #make sure shape is same
    if not (np.shape(X)==\
            np.shape(Y)==\
            np.shape(D)==\
            np.shape(D_x)==\
            np.shape(D_y)==\
            np.shape(X_y)==\
            np.shape(Y_y)==\
            np.shape(X_x)==\
            np.shape(Y_x)):
        
        print('=> ERROR: Incorrect dimension')
        
        return
    
    #map between name and displacement
    map_displacement={}
    
    map_displacement['X']=X
    map_displacement['Y']=Y
    map_displacement['X Gradient of X']=X_x
    map_displacement['Y Gradient of X']=X_y
    map_displacement['X Gradient of Y']=Y_x
    map_displacement['Y Gradient of Y']=Y_y
    
    map_displacement['Resultant']=D  
    map_displacement['X Gradient of Resultant']=D_x
    map_displacement['Y Gradient of Resultant']=D_y
    
    map_displacement['Resultant Gradient of X']=np.sqrt(X_x**2+X_y**2)
    map_displacement['Resultant Gradient of Y']=np.sqrt(Y_x**2+Y_y**2)
    map_displacement['Resultant Gradient of Resultant']=np.sqrt(D_x**2+D_y**2)
    
    #add the mode to the tail of title
    map_strain=dict(zip([this_key+' Strain'+which_input_mode for this_key in list(map_strain.keys())],list(map_strain.values())))
    map_displacement=dict(zip([this_key+' Displacement'+which_input_mode for this_key in list(map_displacement.keys())],list(map_displacement.values())))
    
    '''{**Dict_A,**Dict_B}: merge the dict'''
    return  {**map_strain,**map_displacement}
    
#------------------------------------------------------------------------------
"""
Spheres stress values matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_surface_bottom_map: to save computation time by not directly participating in interpolation calculation
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Spheres stress value matrix
"""   
def SpheresStressMatrix(pixel_step,
                        which_spheres,
                        which_plane,
                        which_surface_bottom_map,
                        which_interpolation):

    print('')
    print('-- Spheres Stress Matrix')
    print('-> plane:',which_plane)
    
    #component of stress scatters object
    scatters_σ_xx=C_Stress.ScattersStress(which_spheres,which_plane,'xx')   
    scatters_σ_yy=C_Stress.ScattersStress(which_spheres,which_plane,'yy')  
    scatters_τ_xy=C_Stress.ScattersStress(which_spheres,which_plane,'xy') 
    
    #matrix of stress components
    if which_interpolation=='scatters_in_grid':
    
        σ_xx=C_In.ScattersInGridIDW(scatters_σ_xx,pixel_step,which_surface_bottom_map)
        σ_yy=C_In.ScattersInGridIDW(scatters_σ_yy,pixel_step,which_surface_bottom_map)
        τ_xy=C_In.ScattersInGridIDW(scatters_τ_xy,pixel_step,which_surface_bottom_map)
    
    #mao between name and stress
    map_stress={}
    
    map_stress['X Normal']=σ_xx
    map_stress['Y Normal']=σ_yy
    map_stress['Shear Stress']=τ_xy
    
    map_stress['Mean Normal']=0.5*(σ_xx+σ_yy)
    map_stress['Diff Normal']=0.5*(σ_xx-σ_yy)
    
    map_stress['Maximal Normal']=0.5*(σ_xx+σ_yy)+np.sqrt((0.5*(σ_xx-σ_yy))**2+τ_xy**2)
    map_stress['Minimal Normal']=0.5*(σ_xx+σ_yy)-np.sqrt((0.5*(σ_xx-σ_yy))**2+τ_xy**2)
    map_stress['Maximal Shear']=+np.sqrt((0.5*(σ_xx-σ_yy))**2+τ_xy**2)
    map_stress['Minimal Shear']=-np.sqrt((0.5*(σ_xx-σ_yy))**2+τ_xy**2)

    return dict(zip([this_key+' Stress' for this_key in list(map_stress.keys())],list(map_stress.values())))
    
#------------------------------------------------------------------------------
"""
Spheres values objects matrix throughout args such as pixel step

Args:
    pixel_step: length of single pixel (int)
    which_spheres: input sphere objects list
    which_plane: ['XoY','YoZ','ZoX'] displacement in 3 planes
    which_input_mode: ['stress','velocity','cumulative_strain','periodical strain','instantaneous_strain']
    which_surface_bottom_map: to save computation time by not directly participating in interpolation calculation
    which_interpolation: ['scatters_in_grid','grids_in_scatter'] interpolation algorithm
    
Returns:
    Spheres value matrix
"""   
def SpheresValueMatrix(pixel_step,
                       which_spheres,
                       which_plane,
                       which_input_mode,
                       which_surface_bottom_map,
                       which_interpolation):
    
    print('')
    print('-> Spheres Value Matrix')
    print('-> grid length:',pixel_step)
    print('-> plane:',which_plane)
    print('-> input mode:',which_input_mode)
    
    if '-' in which_input_mode:
        
        return SpheresStrainMatrix(pixel_step,
                                   which_spheres,
                                   which_plane,
                                   which_input_mode,
                                   which_surface_bottom_map,
                                   which_interpolation)
        
    if which_input_mode=='Stress':
        
        return SpheresStressMatrix(pixel_step,
                                   which_spheres,
                                   which_plane,
                                   which_surface_bottom_map,
                                   which_interpolation)
    
    if which_input_mode=='Velocity':
        
        return SpheresVelocityMatrix(pixel_step,
                                     which_spheres,
                                     which_plane,
                                     which_surface_bottom_map,
                                     which_interpolation)