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
    
import Path as Pa
import Dictionary as Dict

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
    return Pa.GenerateFileNames(mode_input_folder_path)

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
    file_names=Pa.FileNames(which_case_path)
    
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
    new_map_progress_file_name=Dict.DictSortByIndex(map_progress_file_name,sorted(list(map_progress_file_name.keys())))
    
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