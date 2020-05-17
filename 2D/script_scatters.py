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

BETA_C_S_M.SpheresPlot(spheres,5)

plt.axis([400-10,500+10,-10,110])

'''could not get ticklabel'''
#change ticks
ax=plt.gca()

x_major_realticks=np.linspace(400,500,6)
x_major_showticks=[str(int(item)) for item in list(np.linspace(0,100,6))]

ax.set_xticks(x_major_realticks)
ax.set_xticklabels(x_major_showticks)

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('scatters.png',dpi=300,bbox_inches='tight')
plt.close()