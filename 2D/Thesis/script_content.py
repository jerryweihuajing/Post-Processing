# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:44:06 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-content
"""

from script_thesis import *

folder_path=os.getcwd()+'\\content\\'
O_P.GenerateFolder(folder_path)

'''effect of content'''
##image
plt.figure(figsize=(6,6))

plt.imshow(np.flip(that_mesh.img_tag,axis=0),'terrain_r')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary,])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig(folder_path+'content.png',dpi=300,bbox_inches='tight')

#image boundary
image_x_min,image_x_max=0,np.shape(that_mesh.img_tag)[1]
image_y_min,image_y_max=0,np.shape(that_mesh.img_tag)[0]

#plot boundary box
O_G.PlotRectangle(image_x_min-1,
                  image_y_min-1,
                  image_x_max-image_x_min+2,
                  image_y_max-image_y_min+2,
                  '--',
                  'k')
    
plt.savefig(folder_path+'content with boundary box.png',dpi=300,bbox_inches='tight')
plt.close()

