# -*- coding: utf-8 -*-
"""
Created on Sat May 30 15:11:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary for grid
"""

from script_thesis import *

'''erode and expand'''
img_tag=np.zeros((length_window,length_window))

value_content=0.5
value_boundary=0.25

#irregular
# img_tag[1:9,1]=value_content
# img_tag[1:9,2]=value_content
# img_tag[3:9,3]=value_content
# img_tag[3:9,4]=value_content
# img_tag[5:9,5]=value_content
# img_tag[4:9,6]=value_content
# img_tag[2:9,7]=value_content
# img_tag[1:9,8]=value_content

#square
img_tag[1:9,1:9]=value_content

img_boundary=C_B_A.TagBoundaryExtraction(img_tag,tag_foreground=value_content)
img_boundary[img_boundary==1]=value_boundary
plt.figure(figsize=(6,6))

plt.imshow(np.flip(img_tag,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))
plt.imshow(np.flip(img_boundary,axis=0),cmap='gray_r',norm=colors.Normalize(vmin=0,vmax=1))

O_G.PlotMesh(x_min_relative,y_min_relative,length_window)

#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('inlier with mesh.png',dpi=300,bbox_inches='tight')  
plt.close()