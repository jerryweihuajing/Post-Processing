# -*- coding: utf-8 -*-
"""
Created on Mon May 27 14:01:01 2019

@author:Wei Huajing
@company:Nanjing University
@e-mail:jerryweihuajing@126.com

@title：Module-Calculation about colorbar
"""



import Path as Pa
import IntegralPlot as IP
import SpheresGeneration as SG

#organize the raw data
#total path
#folder_path=r'C:\Users\whj\Desktop\L=1000 v=1.0 r=1.0\case 0'
#
#pixel_step=10
#
#which_spheres=SP.GenerateSpheres(folder_path,-1)[:100]
#
#this_img=SP.Analysis(which_spheres,'cumulative_strain','distortional_strain',pixel_step)
#import matplotlib.pyplot as plt
#plt.imshow(this_img,cmap='seismic')  
##%%
#this_fig=plt.figure()
#
#this_ax=plt.subplot()
#
##plot the strain
#norm_strain=colors.Normalize(vmin=-200,vmax=-50)
#
#this_im=this_ax.imshow(this_img,norm=norm_strain,cmap='seismic')
#
##this_im=this_ax.imshow(this_img,cmap='seismic')
#
#In.TicksAndSpines(this_ax)


##posible condition of stress
#stress_mode=['x_normal_stress',
#             'y_normal_stress',
#             'shear_stress',
#             'mean_normal_stress',
#             'maximal_shear_stress']
#
##posible condition of stain
#strain_mode=['x_normal_strain',
#             'y_normal_strain',
#             'shear_strain',
#             'volumetric_strain',
#             'distortional_strain']
#    
##the mode which I search for
#mode_list=['mean_normal_stress',
#           'maximal_shear_stress',
#           'volumetric_strain',
#           'shear_strain']
#
#img_fig=plt.figure()
#
##ax of deformation
#ax_deformation=plt.subplot(len(mode_list)+1,1,1)
#
##plot the deformation
#spheres_grids.Plot()
#In.TicksAndSpines(ax_deformation)
#
##id of subplot
#ax_id=1
#
##img矩阵几何
#imgs=[]
#
##imshow对象
#ims=[]
#
##traverse all modes
#for this_mode in mode_list:
#    
#    ax_id+=1
#    
#    #ax of this img
#    this_ax=plt.subplot(len(mode_list)+1,1,ax_id)
#    
#    this_img=Analysis(which_vtk,which_txt,this_mode,surface,pixel_step)  
#     
#    if this_mode in stress_mode:
#        
#        print('stress')
#        
#        #plot the stress
#        this_im=this_ax.imshow(this_img,cmap='gist_rainbow')
#
#    if this_mode in strain_mode:
#        
#        print('strain')
#        
#        #control the tick of colormap
#        norm_strain=colors.Normalize(vmin=-1,vmax=1)
#
#        #plot the strain
#        this_im=this_ax.imshow(this_img,norm=norm_strain,cmap='seismic')
#
#    In.TicksAndSpines(this_ax)
#    
#    imgs.append(this_img)
#    ims.append(this_im)
#
##%%
# 
#img_fig=plt.figure()
#this_ax=plt.subplot(4,1,1)
#spheres_grids.Plot()
#In.TicksAndSpines(this_ax)
#count=1
#
#for this_img in imgs[:-1]:
#    
#    count+=1
#    
#    this_ax=plt.subplot(4,1,count)
#    
#    if count==2 or count==3:
#        
#        plt.imshow(this_img,cmap='gist_rainbow')
#        
#    if count==4:
#
#        norm=colors.Normalize(vmin=-0.5,vmax=0.5)      
#        plt.imshow(this_img,norm=norm,cmap='seismic')
#        
#    In.TicksAndSpines(this_ax)
#    
##%%   
##define the font
#font = {'family' : 'serif',
#        'color'  : 'darkred',
#        'weight' : 'normal',
#        'size'   : 13,}
#
#colorbar_fig=plt.figure()
#   
#ax=plt.subplot()
#
#for k in range(len(ims)-1):
#    
#    #colorbar position of stress
#    this_colorbar_position=colorbar_fig.add_axes([0.1, 0.8-k*0.2, 0.8, 0.05])    
#
#    #plot colorbar
#    this_colorbar=plt.colorbar(ims[k],cax=this_colorbar_position,orientation='horizontal')
#
#    #set the label
#    this_colorbar.set_label(mode_list[k],fontdict=font)
###    
##    '''只适合大的整数'''
##    if mode_list[k] in stress_mode:
##
##        '''5如何来'''
##        start=int(str(int(MatrixMinimum(imgs[k])))[:3])*10**4
##    
##        #why this step?
##        step=30*10**4
##        
##        this_ticks=tuple([start+k*step for k in range(5)][1:])
#        
#        
##        if len(str(MatrixMaximum(imgs[k])-MatrixMinimum(imgs[k])))>3:
##            
##            offset=MatrixMaximum(imgs[k])-MatrixMinimum(imgs[k])
##            
##            exp=len(str(MatrixMaximum(imgs[k])-MatrixMinimum(imgs[k])))-3
##            
##            #shrink factor
##            factor=10**exp
##            
##            #number of step
##            n_step=5
##            
##            #step of linspace
##            step=factor*(offset//factor)/n_step
##            
##            this_ticks=np.linspace(factor*(MatrixMinimum(imgs[k])//factor)+step,
##                                   factor*(MatrixMaximum(imgs[k])//factor)+step,
##                                   n_step)      
###             
##        this_ticks_labels=tuple([str(this_tick) for this_tick in this_ticks])
##  
##        this_colorbar.set_ticks(this_ticks)
##        this_colorbar.set_ticklabels(this_ticks_labels)
#        
#    if mode_list[k] in strain_mode:
#
#        this_colorbar.set_ticks([-1,0,1])
#        this_colorbar.set_ticklabels(('-1','0','1'))
#                     
#In.TicksAndSpines(ax)
#
##save 2 fig
#img_fig.savefig('./image',dpi=300,bbox_inches='tight')
#colorbar_fig.savefig('./colorbar',dpi=300,bbox_inches='tight')
#     
#