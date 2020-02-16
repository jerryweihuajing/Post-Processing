"""
Created on Fri Jun 21 23:37:02 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Sort folders and files-new forms and organizations
"""

'''   
demand: 
restart with a totally new input data: new format of file organization
total folder: input
              output
              
input: case 0 
       case 1 
       case 2 
       case ...
       
case x: progress=xx%.txt
        ......
        
output: structural deformation
        stress
        cumulative strain
        periodical strain

stress: xx stress
        ......
        
strain: xx strain
        ......  
'''
    
import os

import BETA_operation_path as B_O_P
import operation_dictionary as O_D

#============================================================================== 
#在某路径下判断并创建文件夹
def GenerateFolder(path):

    #去除首位空格
    path=path.strip()
    
    #去除尾部\符号
    path=path.rstrip("\\")
 
    #判断路径是否存在(True/False)
    Exist=os.path.exists(path)
 
    #判断结果
    if not Exist:
        
        #如果不存在则创建目录
        #创建目录操作函数
        os.makedirs(path)  
        
#------------------------------------------------------------------------------
#construct all stress or all strain
#folder_path: total path
#input_mode: 'stress', 'cumulative_strain', 'periodical_strain'
def ModeFileNames(which_case_path,input_mode):
    
    #folder name of one mode
    input_mode_name=input_mode.replace('_',' ')
    
    #path for input
    mode_input_folder_path=which_case_path+'\\'+input_mode_name
    
    #file_names  
    return B_O_P.GenerateFileNames(mode_input_folder_path)

#------------------------------------------------------------------------------
#construct the link between stress txt and strain vtk
def MapsModeFileName(which_case_path):
    
    maps_mode_file_name=[]
    
    #all types of data
    modes=['stress',
           'cumulative_strain',
           'periodical_strain']
    
    stress_file_names,\
    cumulative_strain_file_names,\
    periodical_strain_file_names=[ModeFileNames(which_case_path,this_mode) for this_mode in modes]
    
    for k in range(len(stress_file_names)):
        
        #create the map between mode and file name
        map_mode_file_name={}
        
        map_mode_file_name['stress']=stress_file_names[k]
        map_mode_file_name['cumulative_strain']=cumulative_strain_file_names[k]
        map_mode_file_name['periodical_strain']=periodical_strain_file_names[k]
        
        maps_mode_file_name.append(map_mode_file_name)
        
    return maps_mode_file_name

#------------------------------------------------------------------------------
#calculate output folder path
def OutputFolderPath(which_case_path,input_mode,output_mode):
    
    #total data file folder
    total_path=which_case_path.split('\input\\')[0]
    
    #which case
    case_str=which_case_path.split('\input\\')[1]
    
    #case output path
    case_output_path=total_path+'\\output\\'+case_str+'\\'
    
    #output for structural deformation is particle
    if output_mode=='structural_deformation':
        
        return case_output_path+'structural deformation\\'
    
    else:
        
        #folder name of input mode
        input_mode_name=str(input_mode).replace('_',' ')
        
        #folder name of output mode
        output_mode_name=str(output_mode).replace('_',' ')
        
        #output path
        return case_output_path+input_mode_name+'\\'+output_mode_name+'\\' 
 
#------------------------------------------------------------------------------
"""
Generate file names in this case path in the order of progress

Args:
    which_case_path: load path of this case
    
Returns:
    file names list in this case path in the order of progress
"""
def FileNamesThisCase(which_case_path):
    
    #获取目标路径下所有文件名
    file_names=B_O_P.FileNames(which_case_path)
    
    #建立进度与文件名的映射列表
    map_progress_file_name={}
    
    #重新排序
    for this_file_name in file_names:
        
    #    print(this_file_name)
              
        init=this_file_name.strip('.txt').strip('progress').strip('=').split('%')
                
    #    print(init[0],'stress')   
        
        #提取出进展
        progress=float(init[0])
        
    #    print(progress)
        
        map_progress_file_name[progress]=this_file_name
        
    #print(map_progress_file_name)
    
    #对file_names进行排序 
    new_map_progress_file_name=O_D.DictSortByIndex(map_progress_file_name,sorted(list(map_progress_file_name.keys())))
    
    #返回新的文件名
    return list(new_map_progress_file_name.values())

#------------------------------------------------------------------------------
"""
Generate file paths in this case path in the order of progress

Args:
    which_case_path: load path of this case
    
Returns:
    file paths list in this case path in the order of progress
"""
def FilePathsThisCase(which_case_path):
    
    #Generate file names in this case path in the order of progress
    file_names=FileNamesThisCase(which_case_path)
    
    return [which_case_path+'\\'+this_file_name for this_file_name in file_names]

#------------------------------------------------------------------------------
"""
Generate output folder path depending on input mode and output mode

Args:
    which_case_path: load path of all input files
    which_input_mode: 'structural_deformation' 'stress' 'cumulative_strain' 'periodical strain'
    which_output_mode: 'x_normal' 'y_normal' 'shear'...
    
Returns:
    specific output foler path
"""
def OutputFolder(which_case_path,
                 which_input_mode,
                 which_output_mode):
    
    #total data file folder
    total_path=which_case_path.split('\input\\')[0]
    
    #which case
    case_str=which_case_path.split('\input\\')[1]
    
    #case output path
    case_output_path=total_path+'\\output\\'+case_str+'\\'
    
    #considering input mode
    case_output_path_with_IM=case_output_path+which_input_mode.replace('_',' ')+'\\'
    
    #considering output mode
    case_output_path_with_IM_and_OM=case_output_path_with_IM+which_output_mode.replace('_',' ')+'\\'

    return case_output_path_with_IM_and_OM

#------------------------------------------------------------------------------
"""
Calculate the number of files under the folder

Args:
    which_folder: folder to be calculated
    
Returns:
    amount of files under the folder
"""
def FilesAmount(which_folder):
    
    #amount of folders under path
    num_dirs = 0  
    
    #amount of files under path (including folders)
    num_files = 0  
    
    #amount of files under path, including number of files in subfolders, not including empty folders
    num_files_rec = 0  

    #traverse and make statistics
    for root, dirs, files in os.walk(which_folder):
        
        for each in files:
                
            num_files_rec += 1
    
        for name in dirs:
            
            num_dirs += 1
    
            os.path.join(root, name)
    
    for fn in os.listdir(which_folder):
        
        num_files += 1

    return num_dirs,num_files,num_files_rec

#------------------------------------------------------------------------------
"""
Generate file names list of A and B in case path

Args:
    case_path: case path to be operated
    
Returns:
    file names list of A and B in case path
"""
def FileNamesAB(case_path):
    
    #file names of A and B progress respectively
    file_names_A=[this_file_name for this_file_name in os.listdir(case_path) if 'A' in this_file_name]
    file_names_B=[this_file_name for this_file_name in os.listdir(case_path) if 'B' in this_file_name]
    
    #A and B progress respectively
    progress_A=[float(this_file_name.strip('.txt').strip('A_progress').strip('=').split('%')) for this_file_name in file_names_A]
    progress_B=[float(this_file_name.strip('.txt').strip('B_progress').strip('=').split('%')) for this_file_name in file_names_B]
    
    #sort in order
    progress_A.sort()
    progress_B.sort()
    
    #file names after sorting
    file_names_A_in_order=[file_names_A[progress_A.index(this_progress)] for this_progress in progress_A]
    file_names_B_in_order=[file_names_B[progress_B.index(this_progress)] for this_progress in progress_B]
    
    return file_names_A_in_order,file_names_B_in_order
    
#------------------------------------------------------------------------------
"""
Generate file paths list of A and B in case path

Args:
    case_path: case path to be operated
    
Returns:
    file names list of A and B in case path
"""
def FilePathsAB(case_path):
    
    file_names_A_in_order,file_names_B_in_order=FileNamesAB(case_path)
    
    #join case and file names to generate path
    file_paths_A_in_order=[case_path+'\\'+this_file_name for this_file_name in file_names_A_in_order]
    file_paths_B_in_order=[case_path+'\\'+this_file_name for this_file_name in file_names_B_in_order]
    
    return file_paths_A_in_order,file_paths_B_in_order

#------------------------------------------------------------------------------
"""
Translate file name post fix to title string

Args:
    which_post_fix: post fix of file name 

Returns:
    None
"""
def PostFix2Title(which_post_fix):
    
    temp_str=which_post_fix.split('\\')
    
    #S+C to C+S
    temp_str.reverse()

    #output str
    title_str=''
    
    #strain mode
    if 'strain' in temp_str[-1]:
        
        title_str_list=[temp_str[-1].split(' ')[0],
                        temp_str[0],
                        temp_str[-1].split(' ')[1]]
        
    #stress and deformation    
    else:
        
        title_str_list=temp_str[0].split(' ')+[temp_str[-1]]

    for this_str in title_str_list:
        
        title_str+=' '+this_str[0].upper()+this_str[1:]
       
    return title_str

#------------------------------------------------------------------------------
"""
Calculate progress percentage from file path

Args:
    file_path: load path of research case
    
Returns:
    percentage of progress
"""
def ProgressPercentageFromTXT(file_path):
    
    #where is the %
    percentage_index=file_path.index('%')
    
    #start char
    start_char=file_path[percentage_index-5]
    
    if start_char=='\\':
        
        return file_path[percentage_index-4:percentage_index+1]
    
    else:
        
        return file_path[percentage_index-5:percentage_index+1]