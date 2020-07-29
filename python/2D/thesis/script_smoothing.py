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

#original img
img_tag_original=C_M.ImportMatrixFromTXT(progress_path)
img_rgb_original=C_Im.ImageTag2RGB(img_tag_original,yade_rgb_map)
img_strain_original=C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Strain-Cumulative'))
img_stress_original=C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Stress'))
              
#smoothed img
img_tag_smoothed=C_I_S.TagImageSmooth(C_M_O.AddBound(img_tag_original,bound_value=-1))
img_rgb_smoothed=C_Im.ImageTag2RGB(img_tag_smoothed,yade_rgb_map)
img_strain_smoothed=C_I_S.ImageSmooth(C_M_O.AddBound(img_strain_original))
img_stress_smoothed=C_I_S.ImageSmooth(C_M_O.AddBound(img_stress_original))

#have a test to find the ROI
start_index=x_min
length_ROI=x_max-x_min

#original img ROI
img_rgb_original_ROI=img_rgb_original[:,start_index:start_index+length_ROI]
img_strain_original_ROI=np.flip(img_strain_original[:,start_index:start_index+length_ROI],axis=0)
img_stress_original_ROI=np.flip(img_strain_original[:,start_index:start_index+length_ROI],axis=0)

#smoothed img ROI
img_rgb_smoothed_ROI=img_rgb_smoothed[:,start_index:start_index+length_ROI]
img_strain_smoothed_ROI=np.flip(img_strain_smoothed[:,start_index:start_index+length_ROI],axis=0)
img_stress_smoothed_ROI=np.flip(img_strain_smoothed[:,start_index:start_index+length_ROI],axis=0)

'''stress-original'''
plt.figure(figsize=(6,6))

plt.imshow(img_stress_original_ROI,cmap='ocean')
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('stress-original.png',dpi=300,bbox_inches='tight') 
plt.close()

'''stress-smoothed'''
plt.figure(figsize=(6,6))

plt.imshow(img_stress_smoothed_ROI,cmap='ocean')
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('stress-smoothed.png',dpi=300,bbox_inches='tight') 
plt.close()

'''strain-original'''
plt.figure(figsize=(6,6))

plt.imshow(img_strain_original_ROI,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('strain-original.png',dpi=300,bbox_inches='tight') 
plt.close()

'''strain-smoothed'''
plt.figure(figsize=(6,6))

plt.imshow(img_strain_smoothed_ROI,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('strain-smoothed.png',dpi=300,bbox_inches='tight') 
plt.close()

'''structural deformation-original'''
plt.figure(figsize=(6,6))

plt.imshow(img_rgb_original_ROI)
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('structural deformation-original.png',dpi=300,bbox_inches='tight') 
plt.close()

'''structural deformation-smoothed'''
plt.figure(figsize=(6,6))

plt.imshow(img_rgb_smoothed_ROI)
    
plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])   

#change ticks
ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('structural deformation-smoothed.png',dpi=300,bbox_inches='tight') 
plt.close()