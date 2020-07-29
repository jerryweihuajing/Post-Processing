# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:51:32 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：Module-Calculation of Histogram
"""

'''
demand:
1 statistical law: spatial distribution of stress and strain
2 statistical law: temporal distribution of stress and strain 
'''

import numpy as np
import matplotlib.pyplot as plt

import StrainPlot as Strain

#==============================================================================    
#which values histogram
def ValueHistogram(which_values,value_step,show=False):
    
    #maximum and minimum
    values_max=np.max(which_values)
    values_min=np.min(which_values)

    #knots
    knots=np.arange(values_min,values_max,value_step)
    
    #amount of knots
    n_knots=len(knots)

    #map between knot and values
    map_knot_values=dict(zip(list(np.arange(n_knots)),[0]*n_knots))
    
    for this_value in which_values:
        
        map_knot_values[int(np.floor((this_value-values_min)/value_step))]+=1

    #coordinate of histogram
    x_histogram=list(values_min+value_step*np.array(list(map_knot_values.keys())))
    y_histogram=list(map_knot_values.values())
    
    if show:
        
        plt.plot(x_histogram,y_histogram,'k')
        
    return dict(zip(x_histogram,y_histogram))

#==============================================================================   
#Histogram of stress or strain 
def SpheresHistogram(which_spheres,input_mode,output_mode,value_step,show=False):
    
    #discrete point objects
    discrete_points=Strain.DiscreteValueStrain(which_spheres,input_mode,output_mode)
    
    #selsect pos_z
    values=[this_discrete_point.pos_z for this_discrete_point in discrete_points]
    
    return ValueHistogram(values,value_step,show)

##test
#folder_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 4'
#
##strain distribution histogram
#spheres=SG.GenerateSpheres(folder_path,-1)
#
##plot the histogram
#SpheresHistogram(spheres,'cumulative_strain','distortional_strain',0.5,1)
