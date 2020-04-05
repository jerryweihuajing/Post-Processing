# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:27:48 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-variable of circumstance
"""

'''
circumstance: tectonic circumstance ['extension','compression']
title_position: sub title is inside the axis or not ['exterior','interior'] (default: 'interior')
colorbar_orientation: orientation of colorbar in axes ['horizontal','vertical'] (default: 'horizontal')
'''

circumstance='extension'

if circumstance=='compression':
    
    title_position='interior'
    colorbar_orientation='horizontal'
    
if circumstance=='extension':
    
    title_position='exterior'
    colorbar_orientation='vertical'