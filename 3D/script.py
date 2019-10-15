# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 14:27:36 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

import os
import ImportSpheres as IS

#Import a case
case_path=os.getcwd()+'\\Data\\salt detachment\\fric=0.3 v=0.2\\input\\salt=0.00'


#map between index and spheres
map_all_phase_spheres=IS.GenerateSpheresMapWithSample(case_path)


for this_dict in list(map_all_phase_spheres.values()):
    
    print(len(this_dict))