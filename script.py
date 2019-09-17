# -*- coding: utf-8 -*-
"""
Created on Sun May 26 15:11:51 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：execution script
"""

''' 
demand 3:
    improve morphorlogy of outline
     
demand 10:
    smooth stress and strain
    
demand 11:
    gaussian convolution by matrix 
'''

from __init__ import *

#A experiment
#experiment_path=os.getcwd()+'\\Data\\100-1000\\base detachment\\fric=0.0 v=1.0'

#CP.ExperimentPlot(experiment_path,'XoY',1,'standard')

#EP.ExperimentPlotAll(experiment_path)

#path_A=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=2.72\structural deformation\images\19.68%.png'
#path_B=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\salt detachment\fric=0.0 v=0.2\output\salt=2.72\periodical strain\distortional\images\19.68%.png'
#
##Input 2 PNG images
#image_A=plt.imread(path_A)
#image_B=plt.imread(path_B)

#IS.OpacitySuperposeImages(image_A,image_B)

'''for testing'''
#case_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45'
#
#PP.ProgressStructuralDeformation(case_path,with_fracture=True)
#
#file_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.3 v=1.0\output\base=5.45\structural deformation\values\27.87%.txt'
#
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='standard',with_fracture=True)
#IAP.SingleIntegralAnalysisInProgress(file_path,mode='all',with_fracture=True)


#------------------------------------------------------------------------------
"""
Gaussian convolution kernel

Args:
    miu: mathematical expectation of gaussian distribution
    sigma: standard deviation of the gaussian distribution
    kernel_size: size of kernel (n*n)
        
Returns:
    gaussian convolution kernel matrix
"""
def GaussianKernel(miu,sigma,kernel_size):
      
    #kernel_size must be odd
    if kernel_size%2!=1:
        
        print('--ERROR: please redefine the window_size')
        
        return

    #define void kernel
    kernel=np.zeros((kernel_size,kernel_size))
    
    #wingspan
    wingspan=kernel_size//2
    
    #relative_coordinate of guassian kernel
    relative_coordinates=list(np.linspace(-wingspan,wingspan,kernel_size))

    for x in relative_coordinates:
        
        j=int(x+wingspan)
        
        for y in relative_coordinates:

            i=int(y+wingspan)
            
            #value assignment
            kernel[i,j]=np.exp(-(x**2+y**2)/2*sigma**2)/(2*np.pi*sigma**2)
            
    return kernel
        
#------------------------------------------------------------------------------
"""
window matrix

Args:
    which_image: image matrix to be smoothed
    i,j: index if image
    window_size: size of window (n*n)
        
Returns:
    window matrix
"""    
def Window(which_image,i,j,window_size):
    
    #wingspan
    wingspan=window_size//2
    
    #relative_coordinate of window
    relative_coordinates=list(np.linspace(-wingspan,wingspan,window_size))

    #define void window
    window=np.zeros((window_size,window_size))
    
    try:
 
        for x in relative_coordinates:
            
            j=int(x+wingspan)
            
            for y in relative_coordinates:
    
                i=int(y+wingspan)

                #value assignment
                window[i,j]=which_image[i+int(x),j+int(y)]
                
    except IndexError:

        print('->IndexError: index out of bound')
        
        window[:,:]=1
        
    return window

#------------------------------------------------------------------------------
"""
Smooth image

Args:
    which_image: image matrix to be smoothed
    smooth_operator: operator which performs (default: Gaussian)
        
Returns:
    image matrix which has been smoothed
"""
def ImageSmooth(which_image,smooth_operator='Gaussian'):
    
    #result image
    smooth_image=cp.deepcopy(which_image)
    
    if smooth_operator=='Gaussian':
        
        #image boundary length
        wingspan=2
        window_size=2*wingspan+1
        
        #kernel default to be (0,1)
        kernel=GaussianKernel(0,1,window_size)
        
        for i in range(wingspan,np.shape(which_image)[0]-wingspan):
            
            for j in range(wingspan,np.shape(which_image)[1]-wingspan):
                
                smooth_image[i,j]=np.sum(Window(which_image,i,j,window_size)*GaussianKernel(0,1,window_size))
                      
    return smooth_image
       

txt_path=r'C:\魏华敬\GitHub\YADE\PostProcessing\Data\100-1000\base detachment\fric=0.0 v=0.2\output\base=10.89\periodical strain\distortional\values\27.87%.txt'
mat=Mat.ImportMatrixFromTXT(txt_path)

'''consider and expire nan'''
s=ImageSmooth(mat)

#%%
plt.figure()
plt.imshow(mat,cmap='seismic',norm=colors.Normalize(vmin=-1,vmax=1))

plt.figure()
plt.imshow(s,cmap='seismic')