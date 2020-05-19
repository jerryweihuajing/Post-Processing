# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:00:21 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-interpolation
"""

from script_essay import *

'''samples of interplation'''
#plot scatter points in grid

plt.figure(figsize=(6,6))

#plot gird without value
for this_sphere in spheres:
        
    plt.plot(this_sphere.position[0],
             this_sphere.position[1],
             marker='o',
             markersize=1,
             color='k')  
    
plt.axis([x_min-cell_padding_boundary,
          x_max+cell_padding_boundary,
          y_min-cell_padding_boundary,
          y_max+cell_padding_boundary])   
    
#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(x_min,x_max,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(x_min_relative,x_max_relative,6))]
y_major_realticks=np.linspace(y_min,y_max,6)
y_major_showticks=[str(int(item)) for item in list(np.linspace(y_min_relative,y_max_relative,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)
ax.set_yticks(y_major_realticks)
ax.set_yticklabels(y_major_showticks)

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('interpolation samples.png',dpi=300,bbox_inches='tight')  
plt.close()

'''effect of interpolation'''
scatters=C_Stress.ScattersStress(spheres,'XoY','xy') 

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
plt.imshow(np.flip(z_mesh_points,axis=0),cmap='ocean')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   
    
#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('interpolation effect.png',dpi=300,bbox_inches='tight')  
plt.close()

'''effect of filling'''
surface_bottom_map=C_S_B.SpheresTopAndBottomMap(spheres,pixel_step)

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
plt.imshow(np.flip(z_mesh_points,axis=0),cmap='ocean')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   
        
#change ticks
ax=plt.gca()


#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('filled interpolation effect.png',dpi=300,bbox_inches='tight')  
plt.close()