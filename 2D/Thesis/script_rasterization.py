# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:53:45 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-outline
"""

from script_thesis import *

folder_path=os.getcwd()+'\\rasterization\\'
O_P.GenerateFolder(folder_path)

'''effect of rasterization'''
#plot image
#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_from_data=C_Im.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

#have a test to find the ROI
start_index=x_min
length_ROI=x_max-x_min

plt.figure(figsize=(6,6))

plt.imshow(img_rgb_from_data[:,start_index:start_index+length_ROI])
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig(folder_path+'rasterization.png',dpi=300,bbox_inches='tight')

#plot boundary box
O_G.PlotRectangle(-1,
                  -1,
                  spheres_x_max-spheres_x_min+2,
                  spheres_y_max-spheres_y_min+2,
                  '--',
                  'k')

plt.savefig(folder_path+'rasterization with boundary box.png',dpi=300,bbox_inches='tight')
plt.close()

