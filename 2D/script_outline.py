# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:48:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-outline
"""

from script_essay import *

'''effect of outline'''
#matrix to draw outline image
outline_matrix=np.full(np.shape(img_tag),np.nan)

#outline in all directions
surface_outline_content=[]
bottom_outline_content=[]
right_outline_content=[]
left_outline_content=[]

#surface and bottom
for j in range(np.shape(outline_matrix)[1]):
    
    this_i_list=[]
    
    for i in range(np.shape(outline_matrix)[0]):    
        
        if img_tag[i,j]:
            
            this_i_list.append(i)
    
    try:
            
        if 0<=np.min(this_i_list)-1<np.shape(outline_matrix)[0]:
            
            surface_outline_content.append([np.min(this_i_list)-1,j])
            
        else:
            
            surface_outline_content.append([np.min(this_i_list),j])
            
        if 0<=np.max(this_i_list)+1<np.shape(outline_matrix)[0]:
            
            bottom_outline_content.append([np.max(this_i_list)+1,j])
            
        else:
            
            bottom_outline_content.append([np.max(this_i_list),j])
        
    except:
        
        pass
    
#left and right
for i in range(np.shape(outline_matrix)[0]):
    
    this_j_list=[]
    
    for j in range(np.shape(outline_matrix)[1]):    
        
        if img_tag[i,j]:
            
            this_j_list.append(j)
 
    try:
        
        if 0<=np.max(this_j_list)+1<np.shape(outline_matrix)[1]:
            
            right_outline_content.append([i,np.max(this_j_list)+1])
            
        else:
            
            right_outline_content.append([i,np.max(this_j_list)])
        
        if 0<=np.min(this_j_list)-1<np.shape(outline_matrix)[1]:
            
            left_outline_content.append([i,np.min(this_j_list)-1])
            
        else:
        
            left_outline_content.append([i,np.min(this_j_list)])
    
    except:
        
        pass
        
#total outline content before improvement
content_outline=surface_outline_content+\
                bottom_outline_content+\
                right_outline_content+\
                left_outline_content

for this_i,this_j in content_outline:

    outline_matrix[this_i,this_j]=1

plt.figure(figsize=(6,6))

plt.imshow(np.flip(outline_matrix,axis=0),cmap='gray')
plt.axis([-10,110,-10,110])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('outline.png',dpi=300,bbox_inches='tight')
plt.close()

'''effect of outline improvement: edge tracing'''
#total outline content after improvement
content_outline_improvement=C_M_O.OutlineImprovement(surface_outline_content)+\
                            C_M_O.OutlineImprovement(bottom_outline_content)+\
                            right_outline_content+\
                            left_outline_content

for this_i,this_j in content_outline_improvement:

    outline_matrix[this_i,this_j]=1
    
plt.figure(figsize=(6,6))

plt.imshow(np.flip(outline_matrix,axis=0),cmap='gray')
plt.axis([-10,110,-10,110])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('outline improvement.png',dpi=300,bbox_inches='tight')
plt.close()