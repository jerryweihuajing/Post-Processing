# -*- coding: utf-8 -*-
"""
Created on Fri May 29 21:35:07 2020

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：script for essay-histogram
"""

from script_thesis import *

folder_path=os.getcwd()+'\\smoothing\\'
O_P.GenerateFolder(folder_path)

plt.figure(figsize=(3,3))
plt.bar(['black','gray'],[4,5])

#change ticks
ax=plt.gca()
    
plt.tick_params(labelsize=10)
[label.set_fontname('Times New Roman') for label in ax.get_xticklabels() + ax.get_yticklabels()]

plt.savefig(folder_path+'window histogram.png',dpi=300,bbox_inches='tight')  
plt.close()