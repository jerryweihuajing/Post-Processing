# -*- coding: utf-8 -*-
"""
Created on Tue May  7 15:44:28 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：应力空间内计算主应力和主方向
"""

'''
INPUT:应力张量σ_ij
OUTPUT:应力主值σ_1,σ_2,σ_3,应力偏量σ_m,剪应力主值τ_1,τ_2,τ_3

应力张量:
     |σ_x  τ_xy τ_xz|
σ_ij=|τ_xy σ_y  τ_yz|
     |τ_xz τ_yz σ_z |

平均应力:
σ_m=(σ_x+σ_y+σ_z)/3

应力偏张量:
     |s_x  s_xy s_xz| |σ_x-σ_m τ_xy    τ_xz    |
s_ij=|s_xy s_y  s_yz|=|τ_xy    σ_y-σ_m τ_yz    |
     |s_xz s_yz s_z | |τ_xz    τ_yz    σ_z-σ_m |
'''

import copy as cp
import numpy as np

#应力张量
σ_ij=np.array([-10,9,5,9,0,0,5,0,8])
#σ_ij=np.array([1,0,0,0,1,0,0,0,1])

#如果是列表改变尺寸
if isinstance(σ_ij,list):
    
    σ_ij=σ_ij.reshape((int(np.sqrt(len(σ_ij))),int(np.sqrt(len(σ_ij)))))

#print(σ_ij)

#主应力
σ_x=σ_ij[0,0]
σ_y=σ_ij[1,1]
σ_z=σ_ij[2,2]

#print(σ_x,σ_y,σ_z)

#平均应力
σ_m=(σ_x+σ_y+σ_z)/3

#print(σ_m)

#剪应力
τ_xy=(σ_ij[0,1]+σ_ij[1,0])/2
τ_xz=(σ_ij[0,2]+σ_ij[2,0])/2
τ_yz=(σ_ij[1,2]+σ_ij[2,1])/2

#print(τ_xy,τ_xz,τ_yz)
method=1

#系数
I_1=σ_x+σ_y+σ_z
#I_1=0
I_2=τ_xy*τ_xz+τ_xy*τ_yz+τ_xz*τ_yz-(σ_x*σ_x+σ_y*σ_y+σ_z*σ_z)
#I_2=-I_2
I_3=np.linalg.det(σ_ij)

#print(I_3)

#I_3=σ_x*σ_y*σ_z+2*τ_xy*τ_xz*τ_yz-(σ_x*τ_yz**2+σ_y*τ_xz**2+σ_z*τ_xy**2)
#print(I_3)
    
'''方法1'''
if method==1:
            
    #计算系数
    p=(3*I_2-I_1**2)/3
    q=(9*I_1*I_2-2*I_1**3-27*I_3)/27
    
    #实根判断
    R=(p**3)/27+(q**2)/4
    
    if R<0:
        
        print('ERROR:No Real Roots')
    
    #存在相同的根
    if R==0:
        
        #σ_1=σ_2=σ_3
        if q==0:
            
            σ_1=I_1/3
            σ_2=I_1/3
            σ_3=I_1/3
         
        #σ_1≠σ_2=σ_3
        if q<0:
            
            σ_1=I_1/3-2*(q/2)**(1/3)
            σ_2=I_1/3+2*(q/2)**(1/3)
            σ_3=I_1/3+2*(q/2)**(1/3)
    
        #σ_1=σ_2≠σ_3
        if q>0:
            
            σ_1=I_1/3+2*(q/2)**(1/3)
            σ_2=I_1/3+2*(q/2)**(1/3)
            σ_3=I_1/3-2*(q/2)**(1/3)
    
    #不存在相同的根        
    if R>0:
        
        print(-(q/2)*(-(p**3)/27)**(-0.5))
        
        θ=np.arccos(-(q/2)*(-(p**3)/27)**(-0.5))
        
        σ_1=I_1/3+np.sqrt(-p/3)*(2*np.cos(θ/3))
        σ_2=I_1/3-np.sqrt(-p/3)*(np.cos(θ/3)-np.sqrt(3)*np.sin(θ/3))
        σ_3=I_1/3-np.sqrt(-p/3)*(np.cos(θ/3)+np.sqrt(3)*np.sin(θ/3))
        
    print(σ_1,σ_2,σ_3)
    
'''文献2'''
if method==2:
    
    #应力偏张量
    s_ij=cp.deepcopy(σ_ij)

    s_ij[0,0]=σ_ij[0,0]-σ_m
    s_ij[1,1]=σ_ij[1,1]-σ_m
    s_ij[2,2]=σ_ij[2,2]-σ_m
    
    J_1=0
    J_2=-I_2
    J_3=np.linalg.det(s_ij)
    
#    print(J_3)

    w=np.arccos(-(3*np.sqrt(3)/2)*(J_3*(J_2**(-1.5))))
    
    print(w)