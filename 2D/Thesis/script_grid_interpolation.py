# -*- coding: utf-8 -*-
"""
Created on Tue May 19 13:24:22 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-grid for interpolation
"""

from script_thesis import *

'''for interpolation'''
plt.figure(figsize=(6,6))

#collate the position
radius_local_spheres=[this_sphere.radius for this_sphere in local_spheres]
radius_maximum=np.max(radius_local_spheres)

for this_sphere in window_spheres:
        
    plt.plot(this_sphere.position[0]-0.3,
             this_sphere.position[1]-0.6,
             marker='o',
             markersize=6,
             color='k')  

x_lines=list(range(x_min,x_min+length_window))+[x_min+length_window]
y_lines=list(range(y_min,y_min+length_window))+[y_min+length_window]

for this_x in x_lines:
    
    plt.vlines(this_x,
               y_min,
               y_min+length_window,
               color='k',
               linestyles="-")

for this_y in y_lines:
    
    plt.hlines(this_y,
               x_min,
               x_min+length_window,
               color='k',
               linestyles="-")
    
plt.axis([x_min,
          x_min+length_window,
          y_min,
          y_min+length_window])

#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(x_min,x_min+length_window,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]
y_major_realticks=np.linspace(y_min,y_min+length_window,6)
y_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)
ax.set_yticks(y_major_realticks)
ax.set_yticklabels(y_major_showticks)

plt.tick_params(labelsize=10)                                             
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('interpolation with mesh.png',dpi=300,bbox_inches='tight')

#value point to calculate
value_point=[x_min+5,y_min+5]

#red grid
PlotGrid(value_point[0],
         value_point[1],
         pixel_step,
         '-')

#blue point
plt.plot(value_point[0]+0.5,
         value_point[1]+0.5,
         marker='o',
         markersize=6,
         color='b')  

plt.savefig('interpolation with mesh and grid.png',dpi=300,bbox_inches='tight')
plt.close()

'''effect of interpolation'''
scatters=C_Stress.ScattersStress(window_spheres,'XoY','xy') 

#generate grid object
that_mesh=C_S_Mesh.ScattersMesh(scatters,pixel_step)

#re-define
img_tag=that_mesh.img_tag
grids=that_mesh.grids

#offset in minus value
offset_x=that_mesh.boundary_x[0]
offset_y=that_mesh.boundary_y[0]

#init grids
for this_grid in grids:
    
    this_grid.scatters_inside=[]
    
for this_scatter in scatters:
    
    index_x=int(np.floor((this_scatter.pos_x-offset_x)/pixel_step))
    index_y=int(np.floor((this_scatter.pos_y-offset_y)/pixel_step))
    
    grids[np.shape(img_tag)[1]*index_x+index_y].scatters_inside.append(this_scatter)  
         
#IDW
for this_grid in grids:

    '''surface is no need: skip the grid which has no discrete point inside'''
    if this_grid.scatters_inside!=[]:
            
        this_pos=this_grid.position+np.array([this_grid.length,this_grid.length])/2
        
        #calculate the weight each point
        this_weight=C_In.InverseDistanceWeight(this_pos,this_grid.scatters_inside)
    
        #vector of z value
        z_scatters=np.array([this_scatter.pos_z for this_scatter in this_grid.scatters_inside])

        #assign the value one by one
        img_tag[this_grid.index_x,this_grid.index_y]=np.dot(z_scatters,this_weight)
   
#comfortable image matrix
z_mesh_points=C_Im.ImgFlip(C_Im.ImgRotate(img_tag),0)

plt.figure(figsize=(6,6))

plt.imshow(np.flip(z_mesh_points,axis=0)[1:,1:],cmap='ocean')
PlotMesh(x_min_relative,y_min_relative,length_window)

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('interpolation effect with mesh.png',dpi=300,bbox_inches='tight')  


#value point to calculate
value_point=[x_min_relative+4-0.5,y_min_relative+5-0.5]

#red grid
PlotGrid(value_point[0],
         value_point[1],
         pixel_step,
         '-')

#red grid virtual
PlotGrid(value_point[0]-pixel_step,
         value_point[1]-pixel_step,
         pixel_step+pixel_step*2,
         '--')

#blue point
plt.plot(value_point[0]+0.5,
         value_point[1]+0.5,
         marker='o',
         markersize=6,
         color='b')  

for this_sphere in window_spheres:
        
    plt.plot(this_sphere.position[0]-0.8-x_min,
             this_sphere.position[1]-1.1,
             marker='o',
             markersize=6,
             color='k')  
    
plt.savefig('interpolation effect with mesh and grid.png',dpi=300,bbox_inches='tight')

plt.close()

'''effect of filling'''
surface_bottom_map=C_S_B.SpheresTopAndBottomMap(window_spheres,pixel_step)

#default: which_surface does not exist
if surface_bottom_map==None:
    
    which_surface_map={}
    
    for k in range(np.shape(z_mesh_points)[0]):
        
        which_surface_map[k]=[0,np.shape(z_mesh_points)[0]]
     
#judge whether which_surface matches mesh_points or not
if len(surface_bottom_map)!=np.shape(z_mesh_points)[1]:
    
    print('ERROR: Incorrect dimension')
    
else:
    
    #check where the nan is
    for j in range(np.shape(z_mesh_points)[1]):
        
        if surface_bottom_map[j]==None:
            
            continue
        
        i_min=surface_bottom_map[j][0]
        i_max=surface_bottom_map[j][1]
        
        for i in range(i_min,i_max+1):
                 
            #fill the nan by interpolation
            if np.isnan(z_mesh_points[i,j]):
                
                this_index=[i,j]
                
                #Initial a pad
                pad=1
                  
                #index of this neighbor
                this_neighbor=C_In.Neighbor(this_index,pad)
                   
                #expire the nan
                this_neighbor_expire_nan=C_In.NanExpire(z_mesh_points,this_neighbor)
              
                #into the loop
                while not len(this_neighbor_expire_nan):
                    
                    pad+=1
      
                    #index of this neighbor
                    this_neighbor=C_In.Neighbor(this_index,pad)
                       
                    #expire the nan
                    this_neighbor_expire_nan=C_In.NanExpire(z_mesh_points,this_neighbor)
                    
                '''interpolate directly with the values on the neighbor grid'''
                #calculate the weight each point
                this_weight=C_In.InverseDistanceWeight(this_index,this_neighbor_expire_nan)
                 
                #vector of z value
                z_this_neighbor=np.array([z_mesh_points[int(this_neighbor_index[0]),
                                                        int(this_neighbor_index[1])]
                                                        for this_neighbor_index in this_neighbor_expire_nan])
                
                #assgin the value one by one
                z_mesh_points[i,j]=np.dot(z_this_neighbor,this_weight)
                
plt.figure(figsize=(6,6))

plt.imshow(np.flip(z_mesh_points,axis=0)[1:,1:],cmap='ocean')
PlotMesh(x_min_relative,y_min_relative,length_window)
    
#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('filled interpolation effect with mesh.png',dpi=300,bbox_inches='tight')  
plt.close()

'''effect of smoothing'''
plt.figure(figsize=(6,6))
              
plt.imshow(np.flip(C_I_S.ImageSmooth(C_M_O.AddBound(z_mesh_points)),axis=0)[1:,1:],cmap='ocean')
PlotMesh(x_min_relative,y_min_relative,length_window)
    
#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('filled interpolation effect with mesh-smoothed.png',dpi=300,bbox_inches='tight')  
plt.close()
