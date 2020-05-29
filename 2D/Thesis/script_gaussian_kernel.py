# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:46:37 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-histogram
"""

from script_thesis import *

'''gaussian kernel'''
kernel_length=3
kernel=C_I_S.GaussianKernel(0,1,kernel_length)

plt.figure(figsize=(3,3))

plt.imshow(kernel,cmap='terrain')
PlotMesh(0,0,kernel_length)

plt.savefig('gaussian kernel.png',dpi=300,bbox_inches='tight') 
plt.close()
