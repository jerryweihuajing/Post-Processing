#2017/08/06 LI Changsheng @nNanJing University
#change to real 2D 
#1.fix x and fix spin in y z
#weihuajing @NanJing University


from yade import qt, pack, export
import math

#setting frict materials -----
fyoung = 8e9
fpoisson = 0.25
frictAng = 0
fden = 2500

#setting rock materials -----
ryoung = 2e7
rpoisson = 0.25
rfrictAng = math.atan(0.6)
reps = 0.06
rden = 2500
                             
frict = O.materials.append(FrictMat(
    young = fyoung,
    poisson = fpoisson,
    frictionAngle = frictAng,
    density = fden))

temp_con = O.materials.append(CpmMat(
    young = ryoung,
    poisson = rpoisson,
    frictionAngle = rfrictAng,
    epsCrackOnset = 1e-13,	
    density = rden,
    relDuctility = 0))
                                    
#building boxes -----
box_length = 1000.0
box_height = 100.0
box_depth  = 5

#wallMask
#determines which walls will be created, in the order 
#-x(1), +x (2), -y (4), +y (8), -z (16), +z (32). The numbers are ANDed; the
#default 63 means to create all walls
#parameter1:center
#parameter2:size
''''''
box = geom.facetBox(( box_length/2, box_height/2,0),
                    ( box_length/2, box_height/2,box_depth/2),
                    wallMask = 63,
                    material = frict)
                    
#push plane
wall = utils.wall(box_length, axis = 0, material = frict)

O.bodies.append(box)
O.bodies.append(wall)

''''''
#adding deposit -----
sample_height = box_height #not the final thickness 
sample = pack.SpherePack()
sample.makeCloud((0.0, 0.0, 0.0), ( box_length, sample_height,0), rMean = 1, rRelFuzz = 0.2)
s = sample.toSimulation(material = temp_con)

#2019-01-19 weihuajing
#change to a real 2D simulation
# fix spin in y x 
# fix z-postion  
for i in s:

    #a sphere can be made to move only in the yz plane  and fix spin in Y Z by saying:
    O.bodies[i].state.blockedDOFs='XYz'
	

#defining engines -----
thres = 2000	
O.engines = [
    ForceResetter(),
    InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor = 1), Bo1_Facet_Aabb(), Bo1_Wall_Aabb()], verletDist = 0.1),
    InteractionLoop(
        [Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor = 1), Ig2_Facet_Sphere_ScGeom(), Ig2_Wall_Sphere_ScGeom()],
        [Ip2_CpmMat_CpmMat_CpmPhys(cohesiveThresholdIter = thres), Ip2_FrictMat_CpmMat_FrictPhys(), Ip2_FrictMat_FrictMat_FrictPhys()],
        [Law2_ScGeom_FrictPhys_CundallStrack(), Law2_ScGeom_CpmPhys_Cpm()],
        ),
    
    NewtonIntegrator(damping = 0.4, gravity = (0, -9.81,0)),
    PyRunner(command = 'modifyLayer()', iterPeriod = 1000, label = 'controller'),
    ]
    
O.dt = utils.PWaveTimeStep()

ratio=12
    
threshold_height=box_length/ratio

def modifyLayer():
    if O.iter < thres:
        return

    if O.iter > thres:
        O.pause()

    for i in s:
        if O.bodies[i].state.pos[1] > box_height or O.bodies[i].state.pos[0]>box_length:

	    #delete spheres that are above the target height
            O.bodies.erase(i) 

	    #also,delete the corresponding ids in the id list
            s.remove(i) 	    
            
    export.text('sample.txt')   
        

