# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:11:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary for grid
"""

from script_thesis import *

# method_boundary_extraction='expansion'
method_boundary_extraction='erosion'

# mode_img_content='square'
mode_img_content='irregular'
    
folder_path=os.getcwd()+'\\boundary-grid\\'+method_boundary_extraction+'\\'+mode_img_content+'\\'
O_P.GenerateFolder(folder_path)

if method_boundary_extraction=='erosion':

    value_point=[2-0.5,2-0.5]
    
if method_boundary_extraction=='expansion':

    value_point=[1-0.5,1-0.5]
    
'''erode and expand'''
img_content=np.zeros((length_window,length_window))

value_content=0.31
value_boundary=0.13

#square
if mode_img_content=='square':
    
    img_content[1:9,1:9]=value_content
    
#irregular
if mode_img_content=='irregular':

    img_content[1:9,1]=value_content
    img_content[1:9,2]=value_content
    img_content[3:9,3]=value_content
    img_content[3:9,4]=value_content
    img_content[5:9,5]=value_content
    img_content[4:9,6]=value_content
    img_content[2:9,7]=value_content
    img_content[1:9,8]=value_content

def SimpleOutlier(img_content):
    
    img_outlier=np.zeros(np.shape(img_content))
    
    #outline in all directions
    surface_outlier_content=[]
    bottom_outlier_content=[]
    right_outlier_content=[]
    left_outlier_content=[]
    
    for j in range(np.shape(img_content)[0]):
        
        i_list_this_j=[]
        
        for i in range(np.shape(img_content)[1]):
            
            if img_content[i,j]>0:
                
                i_list_this_j.append(i)
            
        try:
            
            surface_outlier_content.append([np.min(i_list_this_j),j])
            bottom_outlier_content.append([np.max(i_list_this_j),j])
        
        except:
            
            pass
        
    for i in range(np.shape(img_content)[1]):
        
        j_list_this_i=[]
        
        for j in range(np.shape(img_content)[0]):
            
            if img_content[i,j]>0:
                
                j_list_this_i.append(j)
                
        try:
            
            right_outlier_content.append([i,np.min(j_list_this_i)])
            left_outlier_content.append([i,np.max(j_list_this_i)])
        
        except:
            
            pass
        
    for this_i,this_j in surface_outlier_content+bottom_outlier_content+right_outlier_content+left_outlier_content:
        
        img_outlier[int(this_i),int(this_j)]=value_boundary
         
    return img_outlier
 
img_outlier=SimpleOutlier(img_content)

'''simple outlier'''
plt.figure(figsize=(6,6))

plt.imshow(np.flip(img_outlier,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]
plt.savefig(os.getcwd()+'\\inlier-grid\\simple outlier with mesh.png',dpi=300,bbox_inches='tight')  
plt.close()

'''fine outlier'''
plt.figure(figsize=(6,6))

#red grid
O_G.PlotGrid(3.5,5.5,pixel_step,'-')

#red grid virtual
O_G.PlotGrid(3.5-pixel_step,5.5-pixel_step,pixel_step+pixel_step*2,'--')

plt.imshow(np.flip(img_outlier,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]
plt.savefig(os.getcwd()+'\\inlier-grid\\simple outlier with grid and mesh.png',dpi=300,bbox_inches='tight')  
plt.close()

'''fine outlier'''
plt.figure(figsize=(6,6))

img_outlier[2,3]=value_content
img_outlier[4,5]=value_content
img_outlier[3,7]=value_content

plt.imshow(np.flip(img_outlier,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]
plt.savefig(os.getcwd()+'\\inlier-grid\\fine outlier and mesh.png',dpi=300,bbox_inches='tight')  
plt.close()

img_boundary=C_B_E.TagBoundaryExtraction(img_content,
                                         method=method_boundary_extraction,
                                         tag_foreground=value_content)
img_boundary[img_boundary==1]=value_boundary

# '''original'''
# plt.figure(figsize=(6,6))

# plt.imshow(np.flip(img_content,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
# O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

# #change ticks
# ax=plt.gca()
    
# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'content with mesh.png',dpi=300,bbox_inches='tight')  

# #red grid
# O_G.PlotGrid(value_point[0],
#               value_point[1],
#               pixel_step,
#               '-')

# #red grid virtual
# O_G.PlotGrid(value_point[0]-pixel_step,
#               value_point[1]-pixel_step,
#               pixel_step+pixel_step*2,
#               '--')
    
# plt.savefig(folder_path+'content with mesh and grid.png',dpi=300,bbox_inches='tight')  
# plt.close()

# '''inlier and original'''
# plt.figure(figsize=(6,6))

# plt.imshow(np.flip(img_content,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
# plt.imshow(np.flip(img_boundary,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))

# O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

# #change ticks
# ax=plt.gca()
    
# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'content and boundary with mesh.png',dpi=300,bbox_inches='tight')  

# #red grid
# O_G.PlotGrid(value_point[0],
#               value_point[1],
#               pixel_step,
#               '-')

# #red grid virtual
# O_G.PlotGrid(value_point[0]-pixel_step,
#               value_point[1]-pixel_step,
#               pixel_step+pixel_step*2,
#               '--')

# plt.savefig(folder_path+'boundary with mesh and grid.png',dpi=300,bbox_inches='tight')  
# plt.close()

# '''only inlier'''
# plt.figure(figsize=(6,6))

# plt.imshow(np.flip(img_boundary,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))

# O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

# #change ticks
# ax=plt.gca()
    
# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'boundary with mesh.png',dpi=300,bbox_inches='tight')  
# plt.close()

# '''content without figure'''
# plt.figure(figsize=(6,6))

# if method_boundary_extraction=='erosion':

#     img_boundary[img_boundary==value_boundary]=0
    
# if method_boundary_extraction=='expansion':
    
#     img_boundary[img_boundary==value_boundary]=value_content
    
# plt.imshow(np.flip(img_content,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
# plt.imshow(np.flip(img_boundary,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))

# O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

# #change ticks
# ax=plt.gca()
    
# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'content without boundary with mesh.png',dpi=300,bbox_inches='tight')  
# plt.close()