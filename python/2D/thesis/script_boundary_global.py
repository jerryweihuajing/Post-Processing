# -*- coding: utf-8 -*-
"""
Created on Mon May 25 15:59:21 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary for global
"""

from script_thesis import *
        
folder_path=os.getcwd()+'\\boundary-global\\'
O_P.GenerateFolder(folder_path)

'''outline'''
#plot image
#import matrix from txt
case_path_global=r'E:\GitHub\YADEM\Controlling-Simulation\2D\compression 100-800\Data\input\single'

progress_path=case_path.replace('input','output')+'\\Structural Deformation\\30.01%.txt'
# progress_path=case_path_global.replace('input','output')+'\\Structural Deformation\\30.01%.txt'

img_tag_from_data=C_M_O.AddBound(C_I_S.TagImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path),bound_value=-1)),bound_value=-1)
img_rgb_from_data=C_Im.ImageTag2RGB(img_tag_from_data,yade_rgb_map)

img_strain=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Strain-Cumulative'))))),axis=0)
img_stress=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Shear Stress'))))),axis=0)
img_velocity=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Resultant Velocity'))))),axis=0)
img_displacement=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','Resultant Displacement-Cumulative'))))),axis=0)
img_gradient_velocity=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','X Gradient of Y Velocity'))))),axis=0)
img_gradient_displacement=np.flip(C_M_O.AddBound(C_I_S.ImageSmooth(C_M_O.AddBound(C_M.ImportMatrixFromTXT(progress_path.replace('Structural Deformation','X Gradient of Y Displacement-Cumulative'))))),axis=0)

img_boundary=C_B_A.TagBoundaryExtraction(img_tag_from_data,tag_foreground=1)
# img_boundary=C_B_A.TagBoundaryExtraction(img_tag_from_data,tag_foreground=4)        

'''strain for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_strain,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromMatrix(img_strain),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('strain-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''stress for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_stress,cmap='ocean')
plt.imshow(img_boundary,cmap='gray_r')
plt.imshow(C_M_O.OutlineFromMatrix(img_stress),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('stress-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''velocity for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_velocity,cmap='hot')
plt.imshow(img_boundary,cmap='gray_r')
plt.imshow(C_M_O.OutlineFromMatrix(img_velocity),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('velocity-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''displacement for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_displacement,cmap='cool')
plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromMatrix(img_displacement),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('displacement-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''gradient velocity for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_gradient_velocity,cmap='Spectral',norm=colors.Normalize(vmin=-0.25,vmax=0.25))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromMatrix(img_gradient_velocity),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('gradient velocity-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''gradient displacement for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_gradient_displacement,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromMatrix(img_gradient_displacement),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('gradient displacement-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''boundary for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_boundary,cmap='gray')
plt.imshow(C_M_O.OutlineFromImgTag(img_tag_from_data),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('boundary-global.png',dpi=300,bbox_inches='tight')
plt.close()

'''structrual deformation for global'''
plt.figure(figsize=(10,13))

plt.imshow(img_rgb_from_data)
# plt.imshow(C_M_O.OutlineFromImgTag(img_tag_from_data),cmap='gray')

plt.axis([0,np.shape(img_tag_from_data)[1],0,np.shape(img_tag_from_data)[0]])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('structural deformation-global.png',dpi=300,bbox_inches='tight')
plt.close()