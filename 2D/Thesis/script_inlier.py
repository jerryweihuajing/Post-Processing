# -*- coding: utf-8 -*-
"""
Created on Wed May 20 18:24:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary
"""

from script_thesis import *

folder_path=os.getcwd()+'\\inlier\\'
O_P.GenerateFolder(folder_path)

#plot image
#import matrix from txt
progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_I_S.TagImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path),bound_value=-1))
img_rgb_from_data=C_Im.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

img_strain=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Strain-Cumulative'))))
img_stress=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Stress'))))
img_velocity=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Resultant Velocity'))))
img_displacement=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Resultant Displacement-Cumulative'))))
img_gradient_velocity=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','X Gradient of Y Velocity'))))
img_gradient_displacement=C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','X Gradient of Y Displacement-Cumulative'))))

#have a test to find the ROI
start_index=x_min
length_ROI=x_max-x_min

img_tag_ROI=img_tag_from_data[:,start_index:start_index+length_ROI]
img_strain_ROI=np.flip(img_strain[:,start_index:start_index+length_ROI],axis=0)
img_stress_ROI=np.flip(img_strain[:,start_index:start_index+length_ROI],axis=0)
img_velocity_ROI=np.flip(img_velocity[:,start_index:start_index+length_ROI],axis=0)
img_displacement_ROI=np.flip(img_displacement[:,start_index:start_index+length_ROI],axis=0)
img_gradient_velocity_ROI=np.flip(img_gradient_velocity[:,start_index:start_index+length_ROI],axis=0)
img_gradient_displacement_ROI=np.flip(img_gradient_displacement[:,start_index:start_index+length_ROI],axis=0)

img_boundary=C_B_A.TagBoundaryExtraction(img_tag_ROI,tag_foreground=1)

'''ROI strain'''
plt.figure(figsize=(6,6))

plt.imshow(img_strain_ROI,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
# plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_B_A.NanBoundaryExtraction(img_strain_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig(folder_path+'strain ROI.png',dpi=300,bbox_inches='tight')
plt.close()

# '''ROI stress'''
# plt.figure(figsize=(6,6))

# plt.imshow(img_stress_ROI,cmap='ocean')
# plt.imshow(img_boundary,cmap='gray_r')
# plt.imshow(C_B_A.NanBoundaryExtraction(img_stress_ROI),cmap='gray')

# plt.axis([x_min_relative-cell_padding_boundary,
#           x_max_relative+cell_padding_boundary,
#           y_min_relative-cell_padding_boundary,
#           y_max_relative+cell_padding_boundary])

# ax=plt.gca()

# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'stress ROI.png',dpi=300,bbox_inches='tight')
# plt.close()

# '''ROI velocity'''
# plt.figure(figsize=(6,6))

# plt.imshow(img_velocity_ROI,cmap='hot')
# plt.imshow(img_boundary,cmap='gray_r')
# plt.imshow(C_B_A.NanBoundaryExtraction(img_velocity_ROI),cmap='gray')

# plt.axis([x_min_relative-cell_padding_boundary,
#           x_max_relative+cell_padding_boundary,
#           y_min_relative-cell_padding_boundary,
#           y_max_relative+cell_padding_boundary])

# ax=plt.gca()

# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'velocity ROI.png',dpi=300,bbox_inches='tight')
# plt.close()

# '''ROI displacement'''
# plt.figure(figsize=(6,6))

# plt.imshow(img_displacement_ROI,cmap='cool')
# plt.imshow(img_boundary,cmap='gray')
# plt.imshow(C_B_A.NanBoundaryExtraction(img_displacement_ROI),cmap='gray')

# plt.axis([x_min_relative-cell_padding_boundary,
#           x_max_relative+cell_padding_boundary,
#           y_min_relative-cell_padding_boundary,
#           y_max_relative+cell_padding_boundary])

# ax=plt.gca()

# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig('displacement ROI.png',dpi=300,bbox_inches='tight')
# plt.close()

# '''ROI gradient velocity'''
# plt.figure(figsize=(6,6))

# plt.imshow(img_gradient_velocity_ROI,cmap='Spectral',norm=colors.Normalize(vmin=-0.25,vmax=0.25))
# plt.imshow(img_boundary,cmap='gray')
# plt.imshow(C_B_A.NanBoundaryExtraction(img_gradient_velocity_ROI),cmap='gray')

# plt.axis([x_min_relative-cell_padding_boundary,
#           x_max_relative+cell_padding_boundary,
#           y_min_relative-cell_padding_boundary,
#           y_max_relative+cell_padding_boundary])

# ax=plt.gca()

# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'gradient velocity ROI.png',dpi=300,bbox_inches='tight')
# plt.close()

# '''ROI gradient displacement'''
# plt.figure(figsize=(6,6))

# plt.imshow(img_gradient_displacement_ROI,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))
# plt.imshow(img_boundary,cmap='gray')
# plt.imshow(C_B_A.NanBoundaryExtraction(img_gradient_displacement_ROI),cmap='gray')

# plt.axis([x_min_relative-cell_padding_boundary,
#           x_max_relative+cell_padding_boundary,
#           y_min_relative-cell_padding_boundary,
#           y_max_relative+cell_padding_boundary])

# ax=plt.gca()

# plt.tick_params(labelsize=10)
# [label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

# plt.savefig(folder_path+'gradient displacement ROI.png',dpi=300,bbox_inches='tight')
# plt.close()

'''ROI boundary'''
plt.figure(figsize=(6,6))

plt.imshow(img_boundary,cmap='gray')
# plt.imshow(C_B_A.TagBoundaryExtraction(img_tag_ROI,tag_background=-1),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig(folder_path+'ROI boundary.png',dpi=300,bbox_inches='tight')
plt.close()
