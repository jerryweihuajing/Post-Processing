# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:15:13 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Data-YADE rgb list
"""

'''
1: red-detachment
2: green-deposit
3: yellow
4: rock-light gray
8: rock-dark gray
9: blue-uplift
-1: white-blank
'''
yade_rgb_list=[[0.50,0.50,0.50],
               [1.00,0.00,0.00],
               [0.00,1.00,0.00],
               [1.00,1.00,0.00],
               [0.85,0.85,0.85],
               [0.00,1.00,1.00],
               [1.00,0.00,1.00],
               [0.90,0.90,0.90],
               [0.15,0.15,0.15],
               [0.00,0.00,1.00]]

yade_rgb_map=dict(zip(range(len(yade_rgb_list)),yade_rgb_list))

#add blank
yade_rgb_map[-1]=[1.0,1.0,1.0]