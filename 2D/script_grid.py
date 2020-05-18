# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:51:56 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-grid
"""

"""
demand:
    boundary box of interpolation and rasterization
"""

from script_essay import *

length_window=10

window_spheres=[this_sphere for this_sphere in local_spheres\
               if x_min<=this_sphere.position[0]<=x_min+length_window\
               and y_min<=this_sphere.position[1]<=y_min+length_window]

'''for rasterization'''
plt.figure(figsize=(6,6))

BETA_C_S_M.SpheresPlot(window_spheres,60)

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

x_lines=list(range(x_min,x_min+length_window))+[x_min+length_window]
y_lines=list(range(y_min,y_min+length_window))+[y_min+length_window]

#plot mesh
for this_x in x_lines:
    
    plt.plot([this_x,this_x],
             [y_min,y_min+length_window],
             color='k',
             linestyle='-')
    
for this_y in y_lines:
    
    plt.plot([x_min,x_min+length_window],
             [this_y,this_y],
             color='k',
             linestyle='-')
    
plt.savefig('scatters with mesh.png',dpi=300,bbox_inches='tight')

#plot concrete boundary box
PlotGrid(x_min+4,
         y_min+4,
         pixel_step,
         '-')

#plot virtual boundary box
PlotGrid(x_min+4-maximum_radius,
         y_min+4-maximum_radius,
         maximum_radius*2+pixel_step,
         '--')

plt.savefig('scatters with grid.png',dpi=300,bbox_inches='tight')
plt.close()

#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_from_data=C_I.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

#have a test to find the ROI
start_j=x_min
start_i=y_min

length_ROI=length_window

plt.figure(figsize=(6,6))

#grid image for display
img_grid=img_rgb_from_data[start_i:start_i+length_ROI,
                           start_j:start_j+length_ROI]

img_rgb_1=img_grid[0,0]
img_rgb_2=img_grid[5,0]
img_rgb_3=img_grid[9,0]

new_img_grid=cp.deepcopy(img_grid)

#fakeh hhhhhhhhh
new_img_grid[:2,:]=img_rgb_1
new_img_grid[2:5,:]=img_rgb_2
new_img_grid[5:,:]=img_rgb_3
new_img_grid[5,7]=img_rgb_2
new_img_grid[1,6]=img_rgb_2

plt.imshow(new_img_grid)

x_lines=list(range(x_min_relative,x_min_relative+length_window))+[x_min_relative+length_window]
y_lines=list(range(y_min_relative,y_min_relative+length_window))+[y_min_relative+length_window]

x_lines=list(np.array(x_lines)-0.5)
y_lines=list(np.array(y_lines)-0.5)

for this_x in x_lines:
    
    plt.vlines(this_x,
               y_min_relative-0.5,
               y_min_relative-0.5+length_window,
               color='k',
               linestyles="-")

for this_y in y_lines:
    
    plt.hlines(this_y,
               x_min_relative-0.5,
               x_min_relative-0.5+length_window,
               color='k',
               linestyles="-")
    
plt.axis([x_min_relative-0.5,
          x_min_relative-0.5+length_window,
          y_min_relative-0.5,
          y_min_relative-0.5+length_window])

#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(x_min_relative-0.5,x_min_relative-0.5+length_window,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]
y_major_realticks=np.linspace(y_min_relative-0.5,y_min_relative-0.5+length_window,6)
y_major_showticks=[str(int(item)) for item in list(np.linspace(0,length_window,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)
ax.set_yticks(y_major_realticks)
ax.set_yticklabels(y_major_showticks)

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]
    
plt.savefig('rasterization with mesh.png',dpi=300,bbox_inches='tight')
plt.close()
    
'''for interpolation'''
plt.figure(figsize=(6,6))

for this_sphere in local_spheres:
        
    plt.plot(this_sphere.position[0],
             this_sphere.position[1],
             marker='o',
             markersize=6,
             color='b')  

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
plt.close()
