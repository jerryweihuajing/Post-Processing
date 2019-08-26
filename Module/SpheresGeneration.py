# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 21:01:27 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Generate spheres
"""

import numpy as np

from o_sphere import sphere

import NewPath as NP

"""
Generate spheres objects from file (txt)

Args:
    which_file: particle file (txt) from YADE
    
Returns:
    list which containg sphere objects
"""
def GenerateSpheresFromFile(which_file):
    
#    print(this_pos)
    
    #all lines
    lines=open(which_file,'r').readlines()
    
#    print(len(lines))
    
    #list of sphere objects
    spheres=[]
    
    #correct legnth of each line
    correct_length=len(lines[0].strip('\n').split(','))
    
    for this_line in lines:

        this_list=this_line.strip('\n').split(',')
               
        #judge if total length is OK
        if len(this_list)!=correct_length:
            
            continue
        
        #define new sphere object
        new_sphere=sphere()
        
        new_sphere.Id=float(this_list[0])
        new_sphere.radius=float(this_list[1])
        new_sphere.color=np.array([float(this_str) for this_str in this_list[2:5]])       
        new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
        new_sphere.stress_tensor_3D=np.array([float(this_str) for this_str in this_list[8:]])
     
        #3D tensor length is correct
        if len(new_sphere.stress_tensor_3D)!=9:
            
            continue
        
        #judge if there is inf
        if np.inf in new_sphere.stress_tensor_3D or -np.inf in new_sphere.stress_tensor_3D:
                 
#            print(new_sphere.stress_tensor_3D)
     
            continue
        
        #judge if there is nan
        for this_element in new_sphere.stress_tensor_3D:
        
            if np.isnan(this_element):
  
                continue
        
        new_sphere.Init()
        
        spheres.append(new_sphere)

    return spheres

#============================================================================== 
#根据路径生成颗粒体系
def GenerateSpheresFromTXT(which_txt):
    
    #所有的行
    lines=open(which_txt,'r').readlines()
    
    #颗粒体系
    spheres=[]
    
    #正确的长度
    correct_length=len(lines[0].strip('\n').split(','))
    
    #deleter invalid
    id_to_delete=[]
    
    this_id=-1
    
    for this_line in lines:
        
        this_id+=1
        
        this_list=this_line.strip('\n').split(',')
        
    #    print(len(this_list))    
       
        #判断有没有缺漏值
        if len(this_list)!=correct_length:
            
            id_to_delete.append(this_id)
            
            continue
        
        #定义新的颗粒
        new_sphere=sphere()
        
        new_sphere.Id=float(this_list[0])
        new_sphere.radius=float(this_list[1])
        new_sphere.color=np.array([float(this_str) for this_str in this_list[2:5]])       
        new_sphere.position=np.array([float(this_str) for this_str in this_list[5:8]])
        new_sphere.stress_tensor_3D=np.array([float(this_str) for this_str in this_list[8:]])
 
        #判断最后一项的长度是正常的就ok
        if len(new_sphere.stress_tensor_3D)!=9:
            
            id_to_delete.append(this_id)
            
            continue
        
#        print(new_sphere.stress_tensor_3D)
#        print(new_sphere.Id)
        
        #判断有没有无穷项,若有就抛弃它咯
        if np.inf in new_sphere.stress_tensor_3D or -np.inf in new_sphere.stress_tensor_3D:
            
            id_to_delete.append(this_id)
            
            continue
        
        new_sphere.Init()
        
#        print(new_sphere.color)
#        print(new_sphere.stress_tensor_2D)
        
        spheres.append(new_sphere)

    return spheres,id_to_delete

"which_vtk is file name to be processed"
#==============================================================================
def GenerateSpheresFromVTK(which_vtk):
      
    end = open(which_vtk,"r+")
    
    segment = 0
    
    #point positions
    list2 = [] 
    
    #strain matrices
    list3 = [] 
    
    #strain deviator
    list4 = [] 
        
    for line in end:
        
        #marking the starts of each segments, segment 0 is put in list2, segment 2 is put in list3
        if "CELLS" in line:
            
            segment = 1
            
        if "POINT_DATA" in line:
            
            segment = 2
            
        if "SCALARS" in line:
            
            segment = 3
        
        if segment == 0:
            
            list2.append(line)
            
        elif segment == 2:
            
            list3.append(line)
            
        elif segment == 3:
            
            list4.append(line)
          
    end.close()
    
    entries = []
    EvList = ["SCALARS Volumetric_strain float 1", "LOOKUP_TABLE default"]
    EsList = ["SCALARS Shear_strain float 1", "LOOKUP_TABLE default"]
    strain_tensors=[]
    
    for line in list3[2:-1]:
        
        if line != '\n':
            
            l = line.split()
            
            for i in range(len(l)):
                
                l[i] = float(l[i])
                
            entries.append(l)
    	
        else:
            
            DispGrad = np.mat(entries)
            StrainTensor = 0.5*(DispGrad + DispGrad.T)
            #print StrainTensor, '\n'
            
            Ev = np.trace(StrainTensor)
            EvList.append(Ev)
            
            Es = np.sqrt(StrainTensor[0,1]**2 + StrainTensor[0,2]**2 + StrainTensor[1,2]**2)
            EsList.append(Es)
            
            entries = []
            strain_tensors.append(StrainTensor)
        
#    spheres_positions=list2[6:-1]
#    volumetric_strain=EvList[2:]
#    shear_strain=EsList[2:]
#    
#    strain_tensors=[]
#    
#    real_tensors=list3[2:-1]
#    
#    for k in range(int(len(real_tensors)/4)):
#        
#        this_matrix=real_tensors[4*k:4*k+3]
#        
#        this_strain_tensor=[]
#        
#        for kk in range(len(this_matrix)):
#            
#            this_strain_tensor+=this_matrix[kk].split()
#            
#        strain_tensors.append(this_strain_tensor)
#    
#    spheres=[]
#    
#    for k in range(len(spheres_positions)):
#        
#        #define new sphere
#        new_sphere=sphere()
#
#        new_sphere.strain_tensor_3D=strain_tensors[k]
#    
#        #collect new sphere
#        spheres.append(new_sphere)
        
    return strain_tensors

#==============================================================================
#Generate spheres systematically
#number: which period
def GenerateSpheres(which_folder_path,number):
    
    map_mode_file_name=NP.MapsModeFileName(which_folder_path)[number]
    
#    print(map_mode_file_name)
    
    #different file path
    stress_path=which_folder_path+'\\stress'+'\\'+map_mode_file_name['stress']
    cumulative_strain_path=which_folder_path+'\\cumulative strain'+'\\'+map_mode_file_name['cumulative_strain']
    periodical_strain_path=which_folder_path+'\\periodical strain'+'\\'+map_mode_file_name['periodical_strain']

    #different spheres
    spheres_stress=GenerateSpheresFromTXT(stress_path)[0]
    strain_tensors_cumulative=GenerateSpheresFromVTK(cumulative_strain_path)
    strain_tensors_periodical=GenerateSpheresFromVTK(periodical_strain_path)
    
    #delete some spheres
    id_to_delete=GenerateSpheresFromTXT(stress_path)[1]
    
#    print(len(id_to_delete))
#    print(len(spheres_stress))
#    print(len(spheres_cumulative_strain))
#    print(len(spheres_periodical_strain))
#    
#    print(id_to_delete)
    
    if len(strain_tensors_periodical)==len(strain_tensors_cumulative):
        
        scalar=len(strain_tensors_periodical)
        
    else:
        
        print('ERROR:Incorrect scalar')
        
        return
    
    #delete the invalid sphere
    for k in range(scalar):
        
        #delter invalid sphere
        if k in id_to_delete:
            
#            print(k)
            
            strain_tensors_cumulative.pop(k)
            strain_tensors_periodical.pop(k)   
            
    #define final output spheres
    new_spheres=[]

#    print(len(spheres_cumulative_strain))
#    print(len(spheres_periodical_strain))
    
    #information fusion
    for k in range(scalar-len(id_to_delete)):
        
        new_sphere=sphere()
        
        #re-define
        new_sphere.Id=spheres_stress[k].Id
        new_sphere.radius=spheres_stress[k].radius
        new_sphere.color=spheres_stress[k].color
        new_sphere.position=spheres_stress[k].position
        new_sphere.stress_tensor_3D=spheres_stress[k].stress_tensor_3D
        
        new_sphere.strain_tensor_3D_cumulative=strain_tensors_cumulative[k]
        new_sphere.strain_tensor_3D_periodical=strain_tensors_periodical[k]
        
        #Initialize
        new_sphere.Init()
        
        new_spheres.append(new_sphere)
    
#    print(len(new_spheres))  
   
    return new_spheres