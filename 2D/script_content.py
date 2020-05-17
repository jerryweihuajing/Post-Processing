# -*- coding: utf-8 -*-
"""
Created on Sun May 17 21:44:06 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-content
"""

from script_essay import *

'''effect of content'''
##image
plt.figure(figsize=(6,6))

plt.imshow(np.flip(that_mesh.img_tag,axis=0),cmap='gray_r')

plt.axis([-10,110,-10,110])

ax=plt.gca()

plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig('content.png',dpi=300,bbox_inches='tight')
plt.close()