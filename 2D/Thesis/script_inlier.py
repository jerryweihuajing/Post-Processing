# -*- coding: utf-8 -*-
"""
Created on Wed May 20 18:24:03 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-boundary
"""

from script_thesis import *

def Erode(which_content):
        
    #逆时针遍历邻域内的点
    #领域核
    neighbordict=[(i,j) for i in [-1,0,1] for j in [-1,0,1]]
    
    #腐蚀操作后的结果
    new_content=[]
    
    for pos in which_content:
        
        #8邻域
        neighbor=[]    

        #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
        for item in neighbordict:
                  
            #遍历新的坐标
            new_i=pos[0]+item[0]
            new_j=pos[1]+item[1]
            
            #前提是这个点的位置是有效的
            if [new_i,new_j] in which_content:
                
                neighbor.append(True)          
            else:
                neighbor.append(False)

        #领域值是否都相等        
        if neighbor==len(neighbor)*[True]:
            
            new_content.append(pos)
    
    return new_content
    
#膨胀运算
def Expand(which_content):
  
    #逆时针遍历邻域内的点
    #领域核
    neighbordict=[(i,j) for i in [-1,0,1] for j in [-1,0,1]]
    
    #膨胀操作后的结果
    new_content=[]
    
    for pos in which_content:
        
        #[i,j-1],[i+1,j-1],[i+1,j],[i+1,j+1],[i,j+1],[i-1,j+1],[i-1,j],[i-1,j-1]
        for item in neighbordict:
            
            #遍历新的坐标
            new_i=pos[0]+item[0]
            new_j=pos[1]+item[1]
            
            #增加新的点儿
            if [new_i,new_j] not in which_content:
                
                new_content.append([new_i,new_j])
                        
    return new_content
        
def TagBoundaryExtraction(img_tag_ROI,tag_foreground=None,tag_background=None):
    
    #binary image
    img_binary=np.zeros(np.shape(img_tag_ROI))
    
    if tag_foreground!=None:
        
        img_binary[img_tag_ROI==tag_foreground]=1
    
    if tag_background!=None:
        
        img_binary[img_tag_ROI!=tag_background]=1
        
    content_ROI=[[i,j] for i in range(np.shape(img_binary)[0]) for j in range(np.shape(img_binary)[1]) if img_binary[i,j]==1]
    
    new_content=Erode(content_ROI)
    
    #extraction boundary
    content_boundary=[item for item in content_ROI if item not in new_content]
    
    #new binary image
    img_boundary=np.zeros(np.shape(img_binary))
    
    for i,j in content_boundary:
        
        img_boundary[i,j]=1
    
    for i in range(np.shape(img_boundary)[0]):
        
        for j in range(np.shape(img_boundary)[1]):
            
            if img_boundary[i,j]==0:
                
                img_boundary[i,j]=np.nan
                
    return img_boundary
        
def NanBoundaryExtraction(img_ROI):
    
    #binary image
    img_binary=np.zeros(np.shape(img_ROI))
    
    for i in range(np.shape(img_ROI)[0]):
        
        for j in range(np.shape(img_ROI)[1]):
            
            if not np.isnan(img_ROI[i,j]):
                
                img_binary[i,j]=1

    content_ROI=[[i,j] for i in range(np.shape(img_binary)[0]) for j in range(np.shape(img_binary)[1]) if img_binary[i,j]==1]
    
    new_content=Erode(content_ROI)
    
    #extraction boundary
    content_boundary=[item for item in content_ROI if item not in new_content]
    
    #new binary image
    img_boundary=np.zeros(np.shape(img_binary))
    
    for i,j in content_boundary:
        
        img_boundary[i,j]=1
    
    for i in range(np.shape(img_boundary)[0]):
        
        for j in range(np.shape(img_boundary)[1]):
            
            if img_boundary[i,j]==0:
                
                img_boundary[i,j]=np.nan
                
    return img_boundary

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

img_boundary=TagBoundaryExtraction(img_tag_ROI,tag_foreground=1)

'''ROI strain'''
plt.figure(figsize=(6,6))

plt.imshow(img_strain_ROI,cmap='PuOr',norm=colors.Normalize(vmin=-1,vmax=1))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(NanBoundaryExtraction(img_strain_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('strain ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI stress'''
plt.figure(figsize=(6,6))

plt.imshow(img_stress_ROI,cmap='ocean')
plt.imshow(img_boundary,cmap='gray_r')
plt.imshow(NanBoundaryExtraction(img_stress_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('stress ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI velocity'''
plt.figure(figsize=(6,6))

plt.imshow(img_velocity_ROI,cmap='hot')
plt.imshow(img_boundary,cmap='gray_r')
plt.imshow(NanBoundaryExtraction(img_velocity_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('velocity ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI displacement'''
plt.figure(figsize=(6,6))

plt.imshow(img_displacement_ROI,cmap='cool')
plt.imshow(img_boundary,cmap='gray')
plt.imshow(NanBoundaryExtraction(img_displacement_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('displacement ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI gradient velocity'''
plt.figure(figsize=(6,6))

plt.imshow(img_gradient_velocity_ROI,cmap='Spectral',norm=colors.Normalize(vmin=-0.25,vmax=0.25))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(NanBoundaryExtraction(img_gradient_velocity_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('gradient velocity ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI gradient displacement'''
plt.figure(figsize=(6,6))

plt.imshow(img_gradient_displacement_ROI,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))
plt.imshow(img_boundary,cmap='gray')
plt.imshow(NanBoundaryExtraction(img_gradient_displacement_ROI),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('gradient displacement ROI.png',dpi=300,bbox_inches='tight')
plt.close()

'''ROI boundary'''
plt.figure(figsize=(6,6))

plt.imshow(img_boundary,cmap='gray')
plt.imshow(TagBoundaryExtraction(img_tag_ROI,tag_background=-1),cmap='gray')

plt.axis([x_min_relative-cell_padding_boundary,
          x_max_relative+cell_padding_boundary,
          y_min_relative-cell_padding_boundary,
          y_max_relative+cell_padding_boundary])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('ROI boundary.png',dpi=300,bbox_inches='tight')
plt.close()
