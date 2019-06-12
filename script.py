# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：执行脚本
"""

import sys

sys.path.append(r'C:\Users\whj\Desktop\Spyder\YADE\Stress Strain')

from Module import IntegralPlot as IP

#organize the raw data
#total path
#对所有路径进行读取与处理
folder_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 4'

print(folder_path)

##folders_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0'

IP.SinglePlot(folder_path,'stress','structural_deformation',1)
IP.SinglePlot(folder_path,'stress','mean_normal_stress',1)
IP.SinglePlot(folder_path,'cumulative_strain','volumetric_strain',1)
IP.SinglePlot(folder_path,'periodical_strain','volumetric_strain',1)

#IP.SinglePlot(folder_path,'periodical_strain','y_normal_strain',10,1)


#for this_folder_name in os.listdir(folders_path):
#
#    folder_path=folders_path+'\\'+this_folder_name
#    
#    #SP.SinglePlot(folder_path,'stress','structural_deformation',20,test=1)
#    SP.SinglePlot(folder_path,'stress','structural_deformation',1)

#输出哪些哥
#output_type=['structural_deformation','mean_normal_stress','maximal_shear_stress']

#for this_type in output_type:   
 
# 
#this_folder_name=os.listdir(folders_path)[4]
#
##当前参数文件夹的路径
#folder_path=folders_path+'\\'+this_folder_name
#
#print('path:'+folder_path)
#
#SP.SinglePlot(folder_path,'structural_deformation',1)
    
#SP.SubPlot(folder_path,output_type,1)
    
'''有问题'''
#folder_path=r'C:\Users\whj\Desktop\L=2000 v=1.0 r=1.0\case 0'

#SinglePlot(folder_path,'series',20,True)

#SinglePlot(folder_path,'structural_deformation',1)
#SinglePlot(folder_path,'mean_normal_stress',1)
#SinglePlot(folder_path,'maximal_shear_stress',1)

#图像的axis要乘上步长
#SubPlot(folder_path,'structural_deformation',20)
#SubPlot(folder_path,'mean_normal_stress',20,)
#SubPlot(folder_path,'maximal_shear_stress',20)


