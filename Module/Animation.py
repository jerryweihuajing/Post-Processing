# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:50:41 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-GIF animation
"""

'''
demand:
input: a batch of images 
output: a gif whose frequency could be control be developer
'''

import imageio,sys,os

if os.getcwd() not in sys.path:
    
    sys.path.append(os.getcwd())
    
import Path as Pa
import Dictionary as Dict

#==============================================================================
#generate a gif from all images in the folder path
def GenerateGIF(which_folder_path,save_path=None,period=0.5):
  
    #names if all files form the load path
    file_names=Pa.FileNames(which_folder_path)
    
    #map between progress and file name
    map_progress_file_name={}
        
    for this_file_name in file_names:
        
        if this_file_name.endswith('.png'):
                
            #progress to float
            this_progress=float(this_file_name.strip('%.png'))
            
    #        print(this_progress)
            
            #collect
            map_progress_file_name[this_progress]=this_file_name
        
    #对file_names进行排序 
    new_map_progress_file_name=Dict.DictSortByIndex(map_progress_file_name,sorted(list(map_progress_file_name.keys())))
    
    #file names in order
    image_names=list(new_map_progress_file_name.values())
        
    #images to create a gif
    images = []
    
    for this_image_name in image_names:
    
        images.append(imageio.imread(which_folder_path+'\\'+this_image_name))
     
        print(this_image_name)
    
    #default path
    if save_path==None:
            
        #name of GIF
        gif_name='gif.gif'
        
        #save this GIF
        imageio.mimsave(which_folder_path+'\\'+gif_name,images,duration=period)
        
    else:
        
        return