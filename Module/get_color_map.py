# -*- coding: utf-8 -*-
"""
2018/05/28
LI ChangSheng @ nanyang technological university
use：
get the color map of colorfile

input：
[1]ColorFileName
a str

output：
[1]ColorMap
a dict

example：
ColorFileName  = r'./ColorRicebal.txt'

"""

import os
import shutil
import numpy as np

def get_color_map(filename):
    
    xfile = open(filename, "r")#, encoding = 'utf-8')
    
    colorlist = []
    
    for line in xfile:
        
        ltmp = line.split()
              
        for i in range(len(ltmp)):
                
            ltmp[i] = float(ltmp[i])
        
        colorlist.append(ltmp)      

    xfile.close()
	
    colormap={}

    colormap['medium gray'] = (colorlist[0],0)
    colormap['red']         = (colorlist[1],1)
    colormap['green']       = (colorlist[2],2)
    colormap['yellow']      = (colorlist[3],3)
    colormap['light gray']  = (colorlist[4],4)
    colormap['green blue']  = (colorlist[5],5)
    colormap['violet']      = (colorlist[6],6)
    colormap['white']       = (colorlist[7],7)
    colormap['black']       = (colorlist[8],8)
    colormap['blue']        = (colorlist[9],9)
	
    return colorlist,colormap

#DispGrad = np.mat(entries)
#print (DispGrad )
    
#get_color_map('ColorRicebal.txt')
