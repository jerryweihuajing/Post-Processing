# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:15:58 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-collision
"""

from __init__ import *

case_path=r'D:\GitHub\YADEM\Controlling-Simulation\3D\aerolite\Data\input\collision'

'''spheres generation'''
pixel_step=1

that_case=case()

that_case.InitCalculation(case_path)

#the last progress
global_spheres=list(that_case.list_A_progress[-1].map_id_spheres.values())

#roll,pitch,yaw
θ_x=np.pi*10/180
θ_y=np.pi*20/180
θ_z=np.pi*30/180

#sin and cos
c_x,s_x=np.cos(θ_x),np.sin(θ_x)
c_y,s_y=np.cos(θ_y),np.sin(θ_y)
c_z,s_z=np.cos(θ_z),np.sin(θ_z)

#rotation matrix
R_x=np.matrix([[ 1,   0,   0],
              [ 0, c_x, s_x],
              [ 0,-s_x, c_x]])

R_y=np.matrix([[c_y, 0, -s_y],
              [  0, 1,    0],
              [s_y, 0, c_y]])

R_z=np.matrix([[ c_z, s_z, 0],
              [-s_z, c_z, 0],
              [   0, 0,   1]])

M=np.matmul(np.matmul(R_x,R_y),R_z)

#left or right multiply relates to x,y,z rotation order
pos_P=np.matrix([[1],[1],[1]])
pos_U=np.matmul(M,pos_P)

pos_P=np.matrix([[1,1,1]])
pos_V=np.matmul(pos_P,M)

'''traverse and transform'''
for this_sphere in global_spheres:
    
    this_sphere.position=np.array(np.matmul(this_sphere.position,M)).ravel()
    
#depth of spheres
z_spheres=[this_sphere.position[2] for this_sphere in global_spheres]

n_slice=64

#slicing
list_sliced_spheres=[]
list_sliced_spheres_depth=[]

#depth node list
list_nodes_depth_sliced=np.linspace(np.min(z_spheres),np.max(z_spheres),n_slice+1)

count=0

for k in range(n_slice):

    this_sliced_spheres=[this_sphere for this_sphere in global_spheres\
                         if list_nodes_depth_sliced[k]<=this_sphere.position[2]<=list_nodes_depth_sliced[k+1]]

    list_sliced_spheres.append(this_sliced_spheres)
    list_sliced_spheres_depth.append(0.5*(list_nodes_depth_sliced[k]+list_nodes_depth_sliced[k+1]))
    
    count+=len(this_sliced_spheres)

#to restrict boundary
x_min=np.min([this_sphere.position[0] for this_sphere in global_spheres])
x_max=np.max([this_sphere.position[0] for this_sphere in global_spheres])
y_min=np.min([this_sphere.position[1] for this_sphere in global_spheres])
y_max=np.max([this_sphere.position[1] for this_sphere in global_spheres])

#diff in x and y
offset_x=x_max-x_min
offset_y=y_max-y_min

standard_depth=100
maximum_depth=np.max(list_sliced_spheres_depth)

#scale base point
standard_point=[0,0]

list_sliced_spheres_img_tag=[]
list_sliced_spheres_strat_point=[]

#calculate zoom factor
for this_depth in list_sliced_spheres_depth:
    
    k=list_sliced_spheres_depth.index(this_depth)
    
    this_zoom_factor=6
    
    #for scaling
    this_zoom_factor*=(100-maximum_depth)/(100-this_depth)
    
    this_sliced_spheres=list_sliced_spheres[k]
    
    #scaling the coordinates
    for this_sphere in this_sliced_spheres:
        
        #scaling
        this_sphere.position[0]=standard_point[0]+(this_sphere.position[0]-standard_point[0])*this_zoom_factor
        this_sphere.position[1]=standard_point[1]+(this_sphere.position[1]-standard_point[1])*this_zoom_factor
    
        this_sphere.radius*=this_zoom_factor
        
#    #feature map
#    surface_bottom_map=C_S_B.SpheresTopAndBottomMap(this_sliced_spheres,pixel_step)
#
#    #final matrix map
#    map_matrix=C_S_Mat.SpheresValueMatrix(pixel_step,
#                                          this_sliced_spheres,
#                                          'XoY',
#                                          '-Cumulative',
#                                          surface_bottom_map,
#                                          'scatters_in_grid')
#    
#    post_fix='Volumetric Strain-Cumulative'
#    
#    plt.figure(figsize=(8,6))
#    plt.imshow(map_matrix[post_fix],cmap=C_G_P.Colormap(post_fix),vmin=-.05,vmax=.05)
#    # plt.axis([0,6*offset_x,0,6*offset_y])
#    plt.xticks([])
#    plt.yticks([])
#    
#    plt.savefig('frames\\feature_'+str(k)+'.png',dpi=300)
#    plt.close()
#    
#    #feature matrix
#    io.savemat('frames\\feature_'+str(k)+'.mat', {'name': map_matrix[post_fix]})
#    
    #spheres image
    this_spheres_grids=C_S_Mat.SpheresImage(this_sliced_spheres,pixel_step)
#    
#    plt.imshow(this_spheres_grids.img_color)
#    
#    plt.xticks([])
#    plt.yticks([])
#    # plt.axis([0,6*offset_x,0,6*offset_y])
#    plt.savefig('frames\\image_'+str(k)+'.png',dpi=300)
#    plt.close()
#    
#    #feature matrix
#    io.savemat('frames\\image_'+str(k)+'.mat', {'name': this_spheres_grids.img_tag})
    
    #standard point
    this_start_point=[int(np.round(np.min([this_sphere.position[0] for this_sphere in this_sliced_spheres]))),
                      int(np.round(np.min([this_sphere.position[1] for this_sphere in this_sliced_spheres])))]
    
    list_sliced_spheres_img_tag.append(this_spheres_grids.img_tag)
    list_sliced_spheres_strat_point.append(this_start_point)
    
    with open('frames\\point_'+str(k)+'.txt','w') as file: 
        
        file.write('%d'%this_start_point[0])
        file.write(',')
        file.write('%d'%this_start_point[1])


final_frame_tag=np.full((160,230),-1)

#Z Buffering
for k in range(len(list_sliced_spheres_strat_point)):
    
    this_frame=list_sliced_spheres_img_tag[k]
    this_start_point=list_sliced_spheres_strat_point[k]
    
    start_i=this_start_point[0]+20
    start_j=this_start_point[1]+20
    
    final_frame_tag[start_i:start_i+np.shape(this_frame)[0],
                start_j:start_j+np.shape(this_frame)[1]]=this_frame
    
final_frame_color=np.zeros((160,230,3))

from configuration_yade_color import yade_rgb_map

#tag to color
for i in range(np.shape(final_frame_tag)[0]):
    
    for j in range(np.shape(final_frame_tag)[1]):
        
        final_frame_color[i,j,:]=yade_rgb_map[final_frame_tag[i,j]]
        
plt.figure(figsize=(8,6))
plt.imshow(final_frame_color)

plt.xticks([])
plt.yticks([])

plt.savefig('z-buffer frame.png',dpi=300)