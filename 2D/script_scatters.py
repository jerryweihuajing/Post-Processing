# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:45:35 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-scatter
"""

from script_essay import *

'''effect graphics'''
plt.figure(figsize=(6,6))

BETA_C_S_M.SpheresPlot(spheres,4.7)

plt.axis([x_min-cell_padding_boundary,
          x_max+cell_padding_boundary,
          y_min-cell_padding_boundary,
          y_max+cell_padding_boundary])

'''could not get ticklabel'''
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

plt.savefig('scatters.png',dpi=300,bbox_inches='tight')

x_spheres=[this_sphere.position[0] for this_sphere in spheres]
y_spheres=[this_sphere.position[1] for this_sphere in spheres]

#minimum and maximum of coordinates
spheres_x_min,spheres_x_max=np.min(x_spheres),np.max(x_spheres)
spheres_y_min,spheres_y_max=np.min(y_spheres),np.max(y_spheres)

#plot boundary box
PlotRectangle(spheres_x_min-1,
              spheres_y_min-1,
              spheres_x_max-spheres_x_min+2,
              spheres_y_max-spheres_y_min+2,
              '--',
              'k')

plt.savefig('scatters with boundary box.png',dpi=300,bbox_inches='tight')
plt.close()