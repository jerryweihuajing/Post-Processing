#2017/08/06 LI Changsheng @nNanJing University
#change to real 2D 
#1.fix x and fix spin in y z
#2014-2015 Cai ShengYang @NanJing University
from yade import qt, pack, ymport
import math

#setting frict materials -----
fyoung = 8e9
fpoisson = 0.25
frictAng = math.atan(0.6)
fden = 2500

#setting rock materials -----
ryoung = 2e7
rpoisson = 0.25
rfrictAng = math.atan(0.6)
rreps = 0.06
rden = 2500

#setting detachment materials ----- 
dyoung = 2e7
dpoisson = 0
dfrictAng = math.atan(0)
dreps = 0.001
dden = 2100

frict = O.materials.append(FrictMat(young = fyoung,
                                poisson = fpoisson,
                                frictionAngle = frictAng,
                                density = fden))
                                                                       
rock = O.materials.append(CpmMat(young = ryoung,
                          poisson = rpoisson,
                          frictionAngle = rfrictAng,
                          epsCrackOnset = rreps,
                          density = rden,
                          relDuctility = 0))

detachment = O.materials.append(CpmMat(young = dyoung,
                          poisson = dpoisson,
                          frictionAngle = dfrictAng,
                          epsCrackOnset = dreps,
                          density = dden,
                          relDuctility = 0))

#building boxes -----
box_length = 2000.0
box_height = 100.0
box_depth  = 5.0

#wallMask
#determines which walls will be created, in the order -x
#(1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the
#default 63 means to create all walls
#parameter1:center
#parameter2:size
box = geom.facetBox(( box_length/2, box_height/2,0),
                    ( box_length/2, box_height/2,box_depth/2),
                    wallMask = 5,
                    material = frict)

#base detachment 
base_detachment=False

if base_detachment:

    for this_wall in box:
	    
	if this_wall.state.pos[1]==0:
	   
	    this_wall.material=O.materials[detachment]

#push plane
wall = utils.wall(box_length, axis = 0, material = frict)

#adding deposit -----

sample = ymport.text('./sample.txt')
s = O.bodies.append(sample)

count=0

#2017-08-05 lichangsheng 
#change to a real 2D simulation
# fix spin in y z 
# fix x-postion  
#for i in s:
#a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
    #O.bodies[i].state.blockedDOFs='XYz'

global v

v=-1

#defining engines -----
savePeriod = int(5000/abs(v)) # save files for every iterPeriod steps
checkPeriod = int(savePeriod/5) #for print
pre_thres = checkPeriod #for deposition which is not already done

n_stage=100 #save n times
final_thres=savePeriod*n_stage

O.engines = [	
ForceResetter(),
InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor = 1, label = 'ctr1'), Bo1_Facet_Aabb(), Bo1_Wall_Aabb()], verletDist = 0.1),
InteractionLoop(
    [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor = 1, label = 'ctr2'), Ig2_Facet_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
    [Ip2_CpmMat_CpmMat_CpmPhys(cohesiveThresholdIter = pre_thres), Ip2_FrictMat_CpmMat_FrictPhys(), Ip2_FrictMat_FrictMat_FrictPhys()],
    [Law2_ScGeom_FrictPhys_CundallStrack(), Law2_ScGeom_CpmPhys_Cpm()],
    ),

NewtonIntegrator(damping = 0.4, gravity = (0,-9.81,0)),
PyRunner(command = 'startPushing()', iterPeriod = checkPeriod, label = 'controller'),
]

#snapshot = qt.SnapshotEngine(fileBase='-',iterPeriod=savePeriod)

vtkRecorder = VTKRecorder(fileName='0.00%-',recorders=['all'],iterPeriod=savePeriod)

O.dt =1* utils.PWaveTimeStep()

TW1 = TesselationWrapper() #TW1 records cumulative strain data
TW1.setState(0)

#TW1.setState(1)
#TW1.defToVtk("start.vtk")

TW2 = TesselationWrapper() #TW2 records periodical strain data
TW2.setState(0)

import sys
sys.path.append(r'/home/weihuajing/Desktop/2D/Simple')

import get_color_map as Color
yade_rgb_list=Color.get_color_map('ColorRicebal.txt')[0]

maxh = max([O.bodies[i].state.pos[1] for i in s])

n_layer=8

#coloring the sample -----
height_step=maxh/n_layer

case=0

for i in s:

    for k in range(n_layer):

	#case0
        if k*height_step<=O.bodies[i].state.pos[1]<=(k+1)*height_step:

            O.bodies[i].shape.color = yade_rgb_list[k]
            O.bodies[i].material = O.materials[rock]

	    #case1
	    if case==1:
    	        if k==4:
	
	            O.bodies[i].shape.color = yade_rgb_list[4]
	            O.bodies[i].material = O.materials[detachment]
	
	    #case2
	    if case==2:
    	        if k==4 or k==3:
	
                    O.bodies[i].shape.color = yade_rgb_list[4]
                    O.bodies[i].material = O.materials[detachment]
	
	    #case3
	    if case==3:
		if k==4 or k==3 or k==5:
	
		    O.bodies[i].shape.color = yade_rgb_list[4]
		    O.bodies[i].material = O.materials[detachment]

	    #case4
	    if case==4:
        	if k==4 or k==3 or k==5 or k==2:
	
           	 O.bodies[i].shape.color = yade_rgb_list[4]
           	 O.bodies[i].material = O.materials[detachment]
	
print "The max length is %.3f" % maxh

#TW records stress data
TW=TesselationWrapper()
TW.computeVolumes()
stress=bodyStressTensors()

offset=box_length-wall.state.pos[0] #wall ypos
progress=(offset/box_length)*100

out_file=open('stress/stress'+'%.2f%%' %progress+".txt",'w')

for b in sample:

    this_stress=stress[b.id]*4.*pi/3.*b.shape.radius**3/TW.volume(b.id)

    #print(this_stress)
    
    #id
    out_file.write(str(b.id))  
    out_file.write(',')

    #radius
    out_file.write(str(b.shape.radius))

    #color
    for this_color in b.shape.color:

        out_file.write(',')

        out_file.write(str(this_color))
    
    #position
    for this_pos in b.state.pos:

        out_file.write(',')

        out_file.write(str(this_pos))

    for this_line in this_stress:

	for this_str in this_line:

    	     out_file.write(',')
   	     out_file.write(str(this_str))

    out_file.write('\n')

O.bodies.append(box)
O.bodies.append(wall)

#init
TW1.setState(1)
TW1.defToVtk("./cumulative strain/progress="+'%.2f%%' %progress+".vtk")

TW2.setState(1)
TW2.defToVtk("./periodical strain/progress="+'%.2f%%' %progress+".vtk")

TW2.setState(0)

#pushing stage -----
def startPushing():
    
    if O.iter < pre_thres:
        return

    wall.state.vel = Vector3( v, 0,0)
    controller.command = 'stopSimulation()'

    O.engines = O.engines

    #[snap] [VTK][vtkRecorder]
    

#flag = 1 #judging whether to save data. 1 is yes, 0 is no
#count = 0 #for indicating the progress of simulation
def stopSimulation():
    #global flag
    #global count
    
    print 'iter',O.iter
    
    offset=box_length-wall.state.pos[0] #wall ypos

    #show where the wall is
    print 'the offset is %.2f' %offset 

    progress=(offset/box_length)*100

    #show the progress
    print 'the progress is %.2f%%' %progress
    
    print '\n'
    #save the state every 10% of the progress

    if O.iter%savePeriod==0:

	TW1.setState(1)
	TW1.defToVtk("./cumulative strain/progress="+'%.2f%%' %progress+".vtk")

	TW2.setState(1)
	TW2.defToVtk("./periodical strain/progress="+'%.2f%%' %progress+".vtk")

	TW2.setState(0)

	TW=TesselationWrapper()
	TW.computeVolumes()
	s=bodyStressTensors()

	out_file=open('stress/stress'+'%.2f%%' %progress+".txt",'w')

	for b in sample:

	    this_stress=s[b.id]*4.*pi/3.*b.shape.radius**3/TW.volume(b.id)

	    #print(this_stress)
	    
	    #id
	    out_file.write(str(b.id))
	    out_file.write(',')

	    #radius
	    out_file.write(str(b.shape.radius))

	    #color
	    for this_color in b.shape.color:

	        out_file.write(',')

	        out_file.write(str(this_color))
	    
	    #position
	    for this_pos in b.state.pos:

	        out_file.write(',')

	        out_file.write(str(this_pos))

	    for this_line in this_stress:

		for this_str in this_line:

	    	     out_file.write(',')
	   	     out_file.write(str(this_str))

	    out_file.write('\n')

    if progress/100 > 0.5:

	O.pause()    
 

