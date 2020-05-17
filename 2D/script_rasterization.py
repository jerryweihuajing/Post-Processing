# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:53:45 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-outline
"""

from script_essay import *

'''effect of rasterization'''
#plot image
#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_from_data=C_I.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

#have a test to find the ROI
start_index=400
length_ROI=100

plt.figure(figsize=(6,6))

plt.imshow(img_rgb_from_data[:,start_index:start_index+length_ROI])
plt.axis([-10,110,-10,110])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('rasterization.png',dpi=300,bbox_inches='tight')
plt.close()