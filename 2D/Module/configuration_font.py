# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:30:57 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-font
"""

import matplotlib.font_manager as fm

#annotation font
annotation_font=fm.FontProperties(fname="C:\Windows\Fonts\GIL_____.ttf",size=16)
        
#title font
title_font=fm.FontProperties(fname=r"C:\Windows\Fonts\GILI____.ttf",size=13)

#define the font
colorbar_font = {'family' : 'serif',
                 'color'  : 'black',
                 'weight' : 'normal',
                 'size'   : 8,}