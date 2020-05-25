# -*- coding: utf-8 -*-
"""
Created on Mon May 25 21:03:35 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-smoothing
"""

from script_thesis import *

#plot image
#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_I_S.TagImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path),bound_value=-1))
img_rgb_from_data=C_Im.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

img_strain=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Strain-Cumulative'))))
img_stress=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Stress'))))

#have a test to find the ROI
start_index=x_min
length_ROI=x_max-x_min

img_tag_ROI=img_tag_from_data[:,start_index:start_index+length_ROI]
img_strain_ROI=np.flip(img_strain[:,start_index:start_index+length_ROI],axis=0)
img_stress_ROI=np.flip(img_strain[:,start_index:start_index+length_ROI],axis=0)

plt.figure(figsize=(6,6))

plt.imshow(C_I_S.ImageSmooth(C_M_O.AddBound(z_mesh_points))),cmap='ocean')
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('filled interpolation effect.png',dpi=300,bbox_inches='tight') 
plt.close()