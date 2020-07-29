# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:56:52 2019

@author: Wei Huajing
@company: Nanjing University
@e-mail: jerryweihuajing@126.com

@title：YADE imports the calculation results and draws the geometry
"""

import numpy as np
import matplotlib.pyplot as plt
      
#==============================================================================  
class sphere:
    def __init__(self,
                 Id=None,
                 mass=None,
                 radius=None,
                 color=None,
                 position=None):
    
        self.Id=Id
        self.mass=mass
        self.radius=radius
        self.color=color
        self.position=position
        
#============================================================================== 
#返回color字符
def ColorOfColormap(dictionary,value):
    
    #要查询的值为value
    keys=list(dictionary.keys())
    values=list(dictionary.values())
    
    #可能有俩答案
    for this_value in values:
        
        if value in this_value:
            
            return keys[values.index(this_value)]
        
#==============================================================================  
#返回tag     
def TagOfColormap(dictionary,value):
    
    #可能有俩答案
    for this_value in list(dictionary.values()):
        
        if value in this_value:
            
            return this_value[1]   
'''
b: blue
g: green
r: red
c: cyan
m: magenta
y: yellow
k: black
w: white
'''     
#==============================================================================   
#建立新的颜色映射 
#amount_color表示颜色有多少个
def ColorDict(amount_color):     

    map_color_rgb = {
    'aliceblue':            '#F0F8FF',
    'antiquewhite':         '#FAEBD7',
    'aqua':                 '#00FFFF',
    'aquamarine':           '#7FFFD4',
    'azure':                '#F0FFFF',
    'beige':                '#F5F5DC',
    'bisque':               '#FFE4C4',
    'black':                '#000000',
    'blanchedalmond':       '#FFEBCD',
    'blue':                 '#0000FF',
    'blueviolet':           '#8A2BE2',
    'brown':                '#A52A2A',
    'burlywood':            '#DEB887',
    'cadetblue':            '#5F9EA0',
    'chartreuse':           '#7FFF00',
    'chocolate':            '#D2691E',
    'coral':                '#FF7F50',
    'cornflowerblue':       '#6495ED',
    'cornsilk':             '#FFF8DC',
    'crimson':              '#DC143C',
    'cyan':                 '#00FFFF',
    'darkblue':             '#00008B',
    'darkcyan':             '#008B8B',
    'darkgoldenrod':        '#B8860B',
    'darkgray':             '#A9A9A9',
    'darkgreen':            '#006400',
    'darkkhaki':            '#BDB76B',
    'darkmagenta':          '#8B008B',
    'darkolivegreen':       '#556B2F',
    'darkorange':           '#FF8C00',
    'darkorchid':           '#9932CC',
    'darkred':              '#8B0000',
    'darksalmon':           '#E9967A',
    'darkseagreen':         '#8FBC8F',
    'darkslateblue':        '#483D8B',
    'darkslategray':        '#2F4F4F',
    'darkturquoise':        '#00CED1',
    'darkviolet':           '#9400D3',
    'deeppink':             '#FF1493',
    'deepskyblue':          '#00BFFF',
    'dimgray':              '#696969',
    'dodgerblue':           '#1E90FF',
    'firebrick':            '#B22222',
    'floralwhite':          '#FFFAF0',
    'forestgreen':          '#228B22',
    'fuchsia':              '#FF00FF',
    'gainsboro':            '#DCDCDC',
    'ghostwhite':           '#F8F8FF',
    'gold':                 '#FFD700',
    'goldenrod':            '#DAA520',
    'gray':                 '#808080',
    'green':                '#008000',
    'greenyellow':          '#ADFF2F',
    'honeydew':             '#F0FFF0',
    'hotpink':              '#FF69B4',
    'indianred':            '#CD5C5C',
    'indigo':               '#4B0082',
    'ivory':                '#FFFFF0',
    'khaki':                '#F0E68C',
    'lavender':             '#E6E6FA',
    'lavenderblush':        '#FFF0F5',
    'lawngreen':            '#7CFC00',
    'lemonchiffon':         '#FFFACD',
    'lightblue':            '#ADD8E6',
    'lightcoral':           '#F08080',
    'lightcyan':            '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgreen':           '#90EE90',
    'lightgray':            '#D3D3D3',
    'lightpink':            '#FFB6C1',
    'lightsalmon':          '#FFA07A',
    'lightseagreen':        '#20B2AA',
    'lightskyblue':         '#87CEFA',
    'lightslategray':       '#778899',
    'lightsteelblue':       '#B0C4DE',
    'lightyellow':          '#FFFFE0',
    'lime':                 '#00FF00',
    'limegreen':            '#32CD32',
    'linen':                '#FAF0E6',
    'magenta':              '#FF00FF',
    'maroon':               '#800000',
    'mediumaquamarine':     '#66CDAA',
    'mediumblue':           '#0000CD',
    'mediumorchid':         '#BA55D3',
    'mediumpurple':         '#9370DB',
    'mediumseagreen':       '#3CB371',
    'mediumslateblue':      '#7B68EE',
    'mediumspringgreen':    '#00FA9A',
    'mediumturquoise':      '#48D1CC',
    'mediumvioletred':      '#C71585',
    'midnightblue':         '#191970',
    'mintcream':            '#F5FFFA',
    'mistyrose':            '#FFE4E1',
    'moccasin':             '#FFE4B5',
    'navajowhite':          '#FFDEAD',
    'navy':                 '#000080',
    'oldlace':              '#FDF5E6',
    'olive':                '#808000',
    'olivedrab':            '#6B8E23',
    'orange':               '#FFA500',
    'orangered':            '#FF4500',
    'orchid':               '#DA70D6',
    'palegoldenrod':        '#EEE8AA',
    'palegreen':            '#98FB98',
    'paleturquoise':        '#AFEEEE',
    'palevioletred':        '#DB7093',
    'papayawhip':           '#FFEFD5',
    'peachpuff':            '#FFDAB9',
    'peru':                 '#CD853F',
    'pink':                 '#FFC0CB',
    'plum':                 '#DDA0DD',
    'powderblue':           '#B0E0E6',
    'purple':               '#800080',
    'red':                  '#FF0000',
    'rosybrown':            '#BC8F8F',
    'royalblue':            '#4169E1',
    'saddlebrown':          '#8B4513',
    'salmon':               '#FA8072',
    'sandybrown':           '#FAA460',
    'seagreen':             '#2E8B57',
    'seashell':             '#FFF5EE',
    'sienna':               '#A0522D',
    'silver':               '#C0C0C0',
    'skyblue':              '#87CEEB',
    'slateblue':            '#6A5ACD',
    'slategray':            '#708090',
    'snow':                 '#FFFAFA',
    'springgreen':          '#00FF7F',
    'steelblue':            '#4682B4',
    'tan':                  '#D2B48C',
    'teal':                 '#008080',
    'thistle':              '#D8BFD8',
    'tomato':               '#FF6347',
    'turquoise':            '#40E0D0',
    'violet':               '#EE82EE',
    'wheat':                '#F5DEB3',
    'white':                '#FFFFFF',
    'whitesmoke':           '#F5F5F5',
    'yellow':               '#FFFF00',
    'yellowgreen':          '#9ACD32'}

    #取其索引值列表
    total_color_list=list(map_color_rgb.keys())
    
    #分段取值
    n_step=int(np.floor(len(total_color_list)/amount_color))
    
    #颜色列表
    color_list=[total_color_list[2+k*n_step] for k in range(amount_color)]
    
    return dict(zip([k for k in range(len(color_list))],color_list))

'''用VTU格式的文件导出颗粒的信息'''        
#============================================================================== 
#导入csv数据并生成颗粒对象列表    
def ImportData(particle_data_file,show=False):
        
    import pandas
    
    file=pandas.read_csv(particle_data_file)
    
    file=file.rename(columns=lambda x: x.replace(':',''))
    
    #file.loc[k]可访问很多值
    
    #print(file.columns)
    
    """
    'radii', 'id', 'mask', 'mass', 'clumpId', 'color0', 'color1', 'color2',
    'linVelVec0', 'linVelVec1', 'linVelVec2', 'angVelVec0', 'angVelVec1',
    'angVelVec2', 'linVelLen', 'angVelLen', 'SPH_Rho', 'SPH_Press',
    'SPH_Neigh', 'normalStress0', 'normalStress1', 'normalStress2',
    'shearStress0', 'shearStress1', 'shearStress2', 'normalStressNorm',
    'forceVec0', 'forceVec1', 'forceVec2', 'forceLen', 'torqueVec0',
    'torqueVec1', 'torqueVec2', 'torqueLen', 'materialId', 'Points0',
    'Points1', 'Points2'
    """
    
    #颗粒集合
    spheres=[]
    
    for k in range(len(file)):
        
        #建立一个新的球
        this_sphere=sphere()
        
        #定义它们的变量
        this_sphere.Id=file.loc[k].id
        this_sphere.radius=file.loc[k].radii
        this_sphere.mass=file.loc[k].mass
        this_sphere.color=[file.loc[k].color0,file.loc[k].color1,file.loc[k].color2]
        this_sphere.position=[file.loc[k].Points0,file.loc[k].Points1,file.loc[k].Points2]
        
        #收录至集合中
        spheres.append(this_sphere)
        
    #取片段做个实验
#    spheres_clip=spheres[:10]

    #显示吗
    if show:
    
        SpheresSinglePlot(spheres)

    return spheres
        
#==============================================================================
#显示所有的spheres对象在一张图表中
def SpheresSinglePlot(which_spheres,
                      x_boundary=None,
                      y_boundary=None):
    
    from get_color_map import get_color_map
    
    #导出颜色dict
    colorlist,colormap=get_color_map('ColorRicebal.txt')
    
    #新的颜色映射
    colordict=ColorDict(10)
    
    plt.figure()
    
    #把他们画出来
    for this_sphere in which_spheres:
            
        this_x=this_sphere.position[0]
        this_y=this_sphere.position[1]
        this_radius=this_sphere.radius
        this_color=colordict[TagOfColormap(colormap,this_sphere.color)]
           
        plt.plot(this_x,this_y,'o',markersize=this_radius,color=this_color)
        
    #限制坐标范围
    if x_boundary and y_boundary:
        
        plt.axis('scaled') 
        plt.xlim(x_boundary)
        plt.ylim(y_boundary)
  
    else:
         
        plt.axis('scaled')     
    
#==============================================================================
#显示所有的spheres对象在一张subplot中
def SpheresSubPlot(phases_spheres,
                   x_boundary=None,
                   y_boundary=None,
                   spines=True,
                   ticks=True):
  
    from get_color_map import get_color_map
    
    #导出颜色dict
    colorlist,colormap=get_color_map('ColorRicebal.txt')
    
    #新的颜色映射
    colordict=ColorDict(10)  
    
    #新的图像对象
    plt.figure()
    
    #用subplot展示
    for k in range(len(phases_spheres)):

        #第几个呢
        ax=plt.subplot(len(phases_spheres),1,k+1)

        #把他们画出来
        for this_sphere in phases_spheres[k]:
                
            this_x=this_sphere.position[0]
            this_y=this_sphere.position[1]
            this_radius=this_sphere.radius
            this_color=colordict[TagOfColormap(colormap,this_sphere.color)]
               
            plt.plot(this_x,this_y,'o',markersize=this_radius,color=this_color)
                        
        #限制坐标范围
        if x_boundary and y_boundary:
             
            plt.axis('scaled') 
            plt.xlim(x_boundary)
            plt.ylim(y_boundary)
            
        #去掉上下左右边框   
        if not spines:
            
            ax.spines['top'].set_visible(False) 
            ax.spines['bottom'].set_visible(False) 
            ax.spines['left'].set_visible(False) 
            ax.spines['right'].set_visible(False) 
        
        #去掉坐标刻度
        if not ticks:
            
            ax.set_xticks([])
            ax.set_yticks([])
            
#==============================================================================
#展现各个期次的形态
#导入路径,csv从1开始
def ShowDeformation(file_path):

    #所有期次spheres的集合
    phases_spheres=[]
        
    #所有spheres的集合
    all_spheres=[]
    
    #从文件1开始    
    for number in range(1,7):
        
        file_name=file_path+str(number)+'.csv'
        
    #    print(file_name)
        
        ImportData(file_name)
        
        phases_spheres.append(ImportData(file_name))
        all_spheres+=ImportData(file_name)
        
    #从总的颗粒集合中得到颗粒的边界
    x_all_spheres=[this_sphere.position[0] for this_sphere in all_spheres]
    y_all_spheres=[this_sphere.position[1] for this_sphere in all_spheres]
        
    #长度和宽度
    width=max(x_all_spheres)-min(x_all_spheres)
    height=max(y_all_spheres)-min(y_all_spheres)
    
    #放缩因子
    factor=20
    
    #计算出边界,并增加一定的padding
    x_boundary=[min(x_all_spheres)-width/factor,max(x_all_spheres)+width/factor]
    y_boundary=[min(y_all_spheres)-height/factor,max(y_all_spheres)+height/factor]    
        
#    #分开输出
#    for this_spheres in phases_spheres:
#        
#        SpheresSinglePlot(this_spheres,x_boundary,y_boundary)
      
    #画在一张图上
    SpheresSubPlot(phases_spheres,x_boundary,y_boundary)
    
#执行
ShowDeformation('new/')
