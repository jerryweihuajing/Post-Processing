# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:00:21 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-interpolation
"""

from script_essay import *

'''effect of interplation'''
#plot scatter points in grid

plt.figure(figsize=(6,6))

#plot gird without value
for this_sphere in spheres:
        
    plt.plot(this_sphere.position[0],
             this_sphere.position[1],
             marker='o',
             markersize=1,
             color='b')  
    
plt.axis([x_min-cell_padding_boundary,
          x_max+cell_padding_boundary,
          y_min-cell_padding_boundary,
          y_max+cell_padding_boundary])   
    
#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(x_min,x_max,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(x_min_relative,x_max_relative,6))]
y_major_realticks=np.linspace(y_min,y_max,6)
y_major_showticks=[str(int(item)) for item in list(np.linspace(y_min_relative,y_max_relative,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)
ax.set_yticks(y_major_realticks)
ax.set_yticklabels(y_major_showticks)

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('interpolation samples.png',dpi=300,bbox_inches='tight')  
