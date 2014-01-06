
#///////////////////////////////////////////////
# 	
#    Turbomachinery Design Library (Python/Blender)
#    Copyright (C) 2013  DesignLibre
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    To contribute to the DesignLibre distribution, contact contrib@designlibre.com 
#
#//////////////////////////////////////////////
# 	
#   
#
#	
#
#///////////////////////////////////////////////
import bpy
import os
import math
import mathutils
import DLUtils
import TurboMachLib



        
def Rotor(rotorName,hubDia,rotorDia,hubHeight,hubThickness,axleDia,\
        camber_root,camber_tip,camber_position,thickness,\
        bladeHeight,twistAngle,rootChord,\
        tipChord,clearance,centerOfTwist,nspan,\
        npts,rootAngle,nRotorBlades):

    res = 64
    
    #Delete any existing hubs
    # remove mesh Hub
    DLUtils.DeleteMesh(rotorName)
        
    #Generate Hub    
    bpy.ops.mesh.primitive_cylinder_add(vertices=res,radius=hubDia/2,depth=hubHeight,location=(0,0,0)) 
    cyl = bpy.data.objects["Cylinder"]
    cyl.name = rotorName
    cyl.data.name = rotorName
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
     
    
    #Generate all Blades
    for i in range(0,nRotorBlades):
        
        
        #Generate blade
        TurboMachLib.NACA4("RotorBlade"+str(i),camber_root,camber_tip,camber_position,thickness,	bladeHeight, twistAngle,rootChord,tipChord,	centerOfTwist, nspan,npts)
        
        #Grab the mesh
        me = bpy.data.meshes["RotorBlade"+str(i)]
        
        #We want to rotate the blades (twist angle of the root), so generate the rotation matrix
        R = mathutils.Matrix.Rotation(math.radians(rootAngle),3,(0,0,1))    
        
        #Shift and rotate the verts
        for v in me.vertices:
            v.co += mathutils.Vector((0,0,hubDia/2.5))
            v.co = R*v.co
        
        #Deselect all    
        bpy.ops.object.select_all(action='DESELECT')
        
        #Grab the blade object
        ob = bpy.data.objects["RotorBlade"+str(i)]
        ob.delta_location = [hubThickness/2,0,0]
       
        DLUtils.SelectOnly("RotorBlade"+str(i))
        
        #Remove doubles
        print("RemoveDoubles: RotorBlade"+str(i))  
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.editmode_toggle()    
        
        #Rotate the blade to it's proper position    
        bpy.ops.transform.rotate(value=i*math.pi*2/nRotorBlades,axis=(1.0,0.0,0.0))
    
        #Boolean union the blades to the hub
        print("Boolean: RotorBlade"+str(i)) 
        DLUtils.BooleanMesh(rotorName,"RotorBlade"+str(i),"UNION",False)    

   
    #clean up!
    for n in range(0,nRotorBlades):
        DLUtils.DeleteMesh("RotorBlade"+str(n))    
     
     
    axelName = "AxleHole"
    DLUtils.DeleteMesh(axelName)

    rimThickness = 1.25
    rimDepth = 2

    #Hollow out hub 
    DLUtils.DrawCylinder("cutout",hubDia-hubThickness*2,0,hubHeight,res)
    bpy.data.objects["cutout"].delta_rotation_euler = [0,math.pi/2,0]
    bpy.data.objects["cutout"].delta_location = [hubThickness+(rimDepth+hubThickness),0,0]
    DLUtils.BooleanMesh(rotorName,"cutout","DIFFERENCE",True)

    DLUtils.DrawCylinder("cutout",hubDia-hubThickness*4,0,hubHeight,res)
    bpy.data.objects["cutout"].delta_rotation_euler = [0,math.pi/2,0]
    bpy.data.objects["cutout"].delta_location = [hubThickness,0,0]
    DLUtils.BooleanMesh(rotorName,"cutout","DIFFERENCE",True)


    #Generate axle hole extrusion
    DLUtils.DrawCylinder(axelName,axleDia+hubThickness*2,0,hubHeight-hubThickness*2,res)
    bpy.data.objects[axelName].delta_location = [-hubThickness*0.9,0,0]
    bpy.data.objects[axelName].delta_rotation_euler = [0,math.pi/2,0]
    DLUtils.BooleanMesh(rotorName,axelName,"UNION",True)   
    
    #Generate hole for axle
    DLUtils.DrawCylinder(axelName,axleDia,0,hubHeight*2,res)
    bpy.data.objects[axelName].delta_rotation_euler = [0,math.pi/2,0]
    DLUtils.BooleanMesh(rotorName,axelName,"DIFFERENCE",True)   
    
    #Trim Blades
    DLUtils.DrawCylinder("cutBlades",rotorDia-clearance*2,0,hubHeight*2,res)
    bpy.data.objects["cutBlades"].delta_rotation_euler = [0,math.pi/2,0]
    DLUtils.BooleanMesh(rotorName,"cutBlades","INTERSECT",True)   
    
    #Draw inside spokes
    ri= (axleDia+hubThickness*2)/2
    ro= hubDia/2
    nSpokes=7
    for i in range(0,nSpokes):
        DLUtils.DrawBox("spoke"+str(i),hubHeight-hubThickness*2.5,hubThickness,ro-ri)
        DLUtils.ShiftVerts("spoke"+str(i),mathutils.Vector((-hubThickness*0.9,0,(ri+(ro-ri)/2)*0.9)))
        
        #Rotate the spoke to it's proper position    
        bpy.ops.transform.rotate(value=i*math.pi*2/nSpokes,axis=(1.0,0.0,0.0))
        DLUtils.BooleanMesh(rotorName,"spoke"+str(i),"UNION",True)
        
    #Ream out the rim for the hub cone
    
    DLUtils.DrawCylinder("rimCut",hubDia+1,hubDia-2*rimThickness,rimDepth+1,res)
    bpy.data.objects["rimCut"].delta_rotation_euler = [0,math.pi/2,0]
    DLUtils.MoveObject("rimCut",mathutils.Vector([-(hubHeight/2-rimDepth/2),0,0]))
    
    #remove doubles to prevent errors
    DLUtils.SelectOnly("rimCut")
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()    
    DLUtils.SelectOnly(rotorName)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    #ream it     
    DLUtils.BooleanMesh(rotorName,"rimCut","DIFFERENCE",True)      
        
        
def Stator(ductID=64,ductThickness=2,ductLength=60,res=64,\
            mountFaceXLoc=20,mountCanID=28.8,mountCanLength=20,\
            nBlades=1,rootAngle=0,camberRoot=6,camberTip=6,camber_position=50,\
            bladeThickness=6,bladeHeight=50,twistAngle=5,rootChord=10,\
            tipChord=10,centerOfTwist=[50,0],nspan=5,npts=25,screwHoleDia=2.6,screwHoleSpreadDia=16,shaftHoleDia=9):

    #Names we are going to use, we are going to clean up first
    ductName = "duct"
    mountName= "can"
    bladeName= "blade"
    
    DLUtils.DeleteMesh(ductName)
    DLUtils.DeleteMesh(mountName)
    DLUtils.DeleteMesh(mountName+"Inside")    
    for i in range(0,nBlades):
        DLUtils.DeleteMesh(bladeName+str(i))
        

    #Draw duct
    DLUtils.DrawCylinder(ductName,ductID+ductThickness*2,ductID,ductLength,res)
    DLUtils.SelectOnly(ductName)
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
    #Draw duct tabs
    tabLength = 36.8
    tabWidth = 11
    tabHeight = 1.5
    DLUtils.DrawBox("tab1", tabLength,tabWidth,tabHeight)    
    DLUtils.DrawBox("tab2", tabLength,tabWidth,tabHeight)    
    DLUtils.MoveObject("tab1",mathutils.Vector([0,ductID/2+tabWidth/2 + ductThickness/2,0]))
    DLUtils.MoveObject("tab2",mathutils.Vector([0,-(ductID/2+tabWidth/2 + ductThickness/2),0]))
    DLUtils.BooleanMesh(ductName,"tab1","UNION",True)
    DLUtils.BooleanMesh(ductName,"tab2","UNION",True)
    
    #Draw mount can    
    DLUtils.DrawCylinder(mountName,mountCanID+ductThickness*2,0,mountCanLength,res)
    DLUtils.DrawCylinder(mountName+"Inside",mountCanID,0,mountCanLength,res)
    bpy.data.objects[mountName+"Inside"].delta_location = [0,0,ductThickness]
        
    #Cut out the can interior
    DLUtils.BooleanMesh(mountName,mountName+"Inside","DIFFERENCE",True)

    #Cut out mount and shaft holes
    DLUtils.DrawCylinder("shaftHole",shaftHoleDia,0,mountCanLength*2,res)
    bpy.data.objects["shaftHole"].delta_location = [0,0,0]
    DLUtils.BooleanMesh(mountName,"shaftHole","DIFFERENCE",True)
    #ewHoleDia=2.5,screwHoleSpreadDia=16,shaftHoleDia=8):
    for i in range(0,4):
        DLUtils.DrawCylinder("screwHole",screwHoleDia,0,mountCanLength*2,res)
        bpy.data.objects["screwHole"].delta_location = [screwHoleSpreadDia/2*math.cos(i*math.pi*2/4),screwHoleSpreadDia/2*math.sin(i*math.pi*2/4),0]
        DLUtils.BooleanMesh(mountName,"screwHole","DIFFERENCE",True)
    
        
    #Rotate the mount horizontally
    DLUtils.SelectOnly(mountName)
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
    #Add box to cut out wire hole
    DLUtils.DrawBox("wireBox", 15,10,15)
    bpy.data.objects["wireBox"].delta_location = [mountCanLength/2-2,-mountCanID/2,0]
    #DLUtils.MoveObject("wireBox",mathutils.Vector([mountCanLength-7,-mountCanID/2,0]))
    DLUtils.BooleanMesh(mountName,"wireBox","DIFFERENCE",True)
    
         
    for i in range(0,nBlades):
        #Generate blade
        TurboMachLib.NACA4(bladeName+str(i),camberRoot, camberTip,camber_position,bladeThickness,	bladeHeight, twistAngle,rootChord,tipChord,	centerOfTwist, nspan,npts)
        
        #Grab the mesh
        me = bpy.data.meshes[bladeName+str(i)]
        
        #We want to rotate the blades (twist angle of the root), so generate the rotation matrix
        R = mathutils.Matrix.Rotation(math.radians(rootAngle),3,(0,0,1))    
        
        #Shift and rotate the verts
        for v in me.vertices:
            v.co += mathutils.Vector((0,0,mountCanID/2))
            v.co = R*v.co
        
        #Deselect all    
        bpy.ops.object.select_all(action='DESELECT')
        
        #Grab the blade object
        ob = bpy.data.objects[bladeName+str(i)]
        ob.delta_location = [ductThickness/2,0,0]
        #ensure it is selected
        ob.select = True
        
        #Remove doubles
        print("RemoveDoubles: "+bladeName+str(i))  
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.editmode_toggle()    
        
        #Rotate the blade to it's proper position    
        bpy.ops.transform.rotate(value=i*math.pi*2/nBlades,axis=(1.0,0.0,0.0))
    
        #Boolean union the blades to the hub
        print("Boolean: blade"+str(i)) 
        #DLUtils.BooleanMesh(ductName,bladeName+str(i),"UNION",False)        
    
    #Add inside blade cut
    DLUtils.DrawCylinder("bladeCut",mountCanID+ductThickness,0,mountCanLength,res)
    DLUtils.SelectOnly("bladeCut")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
     
    for i in range(0,nBlades):
         DLUtils.BooleanMesh(bladeName+str(i),"bladeCut","DIFFERENCE",False)
         DLUtils.BooleanMesh(mountName,bladeName+str(i),"UNION",True)
       
    #Delete "BladeCut"
    DLUtils.DeleteMesh("bladeCut")
    
    #Add outside blade Cut
    DLUtils.DrawCylinder("bladeCut",ductID+ductThickness,0,ductLength,res)
    DLUtils.SelectOnly("bladeCut")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
    #cut the outside of the blades 
    DLUtils.BooleanMesh(mountName,"bladeCut","INTERSECT",True)
           
    
    #Move the can to the mountFaceXLoc 
    bpy.data.objects[mountName].delta_location = [mountCanLength/2-ductLength/2+mountFaceXLoc,0,0]
      
    #Union the can and the duct  
    DLUtils.BooleanMesh(ductName,mountName,"UNION",True)


    LEDHolder()
    
def LEDHolder(LEDDia = 5.5,
				thick=1.5,
				tol = 0.5,
				L=15,
				W=20):
    
    
    od = LEDDia+4
    
    DLUtils.DeleteMesh("Sphere1")
    DLUtils.DeleteMesh("Sphere2")
    DLUtils.DeleteMesh("Base")
	
    DLUtils.DrawCylinder("LEDHole",LEDDia,0,10,64)
    DLUtils.MoveObject("LEDHole",mathutils.Vector((0,0,4.5)))
    DLUtils.DrawCylinder("LEDHole2",LEDDia+1,0,6,64)
    DLUtils.MoveObject("LEDHole2",mathutils.Vector((0,0,-3)))
    
    
    DLUtils.DrawBox("Base",L,1,W)
    DLUtils.MoveObject("Base",mathutils.Vector([0,-od/2,0]))
    DLUtils.DrawSphere("Sphere1",od,16)
    DLUtils.MoveObject("Sphere1",mathutils.Vector([0,0,L/4]))
    DLUtils.DrawSphere("Sphere2",od,32)
    DLUtils.MoveObject("Sphere2",mathutils.Vector([0,0,-L/4]))
    
    DLUtils.ConvexHull(["Sphere1","Sphere2","Base"])
    
    DLUtils.BooleanMesh("Convex Hull","LEDHole","DIFFERENCE",True)
    DLUtils.BooleanMesh("Convex Hull","LEDHole2","DIFFERENCE",True)
    DLUtils.DeleteMesh("Sphere1")
    DLUtils.DeleteMesh("Sphere2")
    DLUtils.DeleteMesh("Base")
    
class StageProps():
    beta1=0
    beta2=0
    alpha1=0
    alpha2=0
    Cx=0
    rpm=0
    radius=0
    camber=0
    R=0
    phi=0
    psi=0
    
    
        
class LinearStageProps():
    rootProps = StageProps()
    meanProps = StageProps()
    tipProps = StageProps()
    rootRadius = 0
    tipRadius = 0
    def GenerateSpecSheet(self,filePath):
        print(os.getcwd())
        os.chdir('Z:\DesignLibre\Mavrix_aircraft\Tools\DuctedFanDesignLibrary' )
        file = open(filePath,'w')
        
        file.write('DesignLibre.com Ducted Fan Design Library\n');
        file.write('Xmm Fan design spec.\n\n\n')
        file.write('Stage design:\n')
        file.write('\tReation = ' + str(meanProps.R) + '\n')
        file.write('\tFlow coefficient = ' + str(meanProps.phi) + '\n')
        file.write('\tStage loading = ' + str(meanProps.psi) +'\n')
        file.write('\n\n')
        
        file.write('Power prediction: ' + '\n')
        
       
        file.close()  
        
def StageCalc(R=0.5,\
            phi=0.4,\
            psi=0.07,\
            rpm=100,\
            rootRadius=28.8/2,\
            tipRadius=64.0/2):
    linearStageProps = LinearStageProps()
    linearStageProps.rootRadius = rootRadius
    linearStageProps.tipRadius = tipRadius
    
    meanLineRadius=(rootRadius+tipRadius)/2
    
    #Get the meanLineProps to grab Cx            
    linearStageProps.meanProps = CalcStageBladeAngles(R=R,phi=phi,psi=psi,rpm = rpm, radius = meanLineRadius)               
    
    linearStageProps.meanProps.R = R
    linearStageProps.meanProps.psi=psi
    linearStageProps.meanProps.phi=phi
    
    #Keep the stage loading coefficient constant  
    linearStageProps.rootProps = CalcStageBladeAngles(R=R,phi=phi,psi=psi,rpm = rpm, radius = rootRadius)               
    
    Lphi = 1e-6
    Hphi = 2-1e-6
    rootPhi = phi
    while(abs(linearStageProps.meanProps.Cx -linearStageProps.rootProps.Cx) > 1e-3):
        if(linearStageProps.rootProps.Cx < linearStageProps.meanProps.Cx):
            Lphi  = rootPhi   
        else:
            Hphi = rootPhi
        rootPhi = (Hphi + Lphi)/2
        linearStageProps.rootProps = CalcStageBladeAngles(R=R,phi=rootPhi,psi=psi,rpm = rpm, radius = rootRadius)           
    
    linearStageProps.meanProps.R = R
    linearStageProps.meanProps.psi=psi
    linearStageProps.meanProps.phi=rootPhi
    
    #Same for tip        
    linearStageProps.tipProps = CalcStageBladeAngles(R=R,phi=phi,psi=psi,rpm = rpm, radius = tipRadius)               
    
    Lphi = 1e-6
    Hphi = 2-1e-6
    tipPhi = phi
    while(abs(linearStageProps.meanProps.Cx -linearStageProps.tipProps.Cx) > 1e-3):
        if(linearStageProps.tipProps.Cx < linearStageProps.meanProps.Cx):
            Lphi  = tipPhi   
        else:
            Hphi = tipPhi
        tipPhi = (Hphi + Lphi)/2
        linearStageProps.tipProps = CalcStageBladeAngles(R=R,phi=tipPhi,psi=psi,rpm = rpm, radius = tipRadius)     
        
    linearStageProps.meanProps.R = R
    linearStageProps.meanProps.psi=psi
    linearStageProps.meanProps.phi=tipPhi
    
    return linearStageProps    
        
def CalcStageBladeAngles(R=0.5,\
                        phi=0.4,\
                        psi=0.07,\
                        rpm = 30000,\
                        radius=64):
                            
    #Inputs:
    #   R is the Reaction
    #   phi is the flow coefficient
    #   psi is the stage loading coefficient
    #   rpm is revolutions per minute
    #   radius is the blade radius location
    
    #Outputs:
    #   beta1
    #   beta2
    #   alpha1
    #   alpha2
    U = rpm/60*2*math.pi*radius/1000
    stageProps = StageProps()
    stageProps.rpm =rpm
    stageProps.radius=radius
    stageProps.beta2=math.atan((R-psi/2)/phi);
    stageProps.beta1=math.atan(psi/phi+(2*R-psi)/(2*phi))
    stageProps.Cx=phi*U
    W1 = stageProps.Cx/math.cos(stageProps.beta1)
    W2 = stageProps.Cx/math.cos(stageProps.beta2)
    CTheta1=U-W1*math.sin(stageProps.beta1)
    CTheta2=U-W2*math.sin(stageProps.beta2)
    stageProps.alpha1=math.atan(CTheta1/stageProps.Cx)
    stageProps.alpha2=math.atan(CTheta2/stageProps.Cx)
   
    if(False):
        print("U" + str(U))
        print("Cx" + str(stageProps.Cx))
        print("beta1" + str(stageProps.beta1))
        print("beta2" + str(stageProps.beta2))
        print("W1" + str(W1))
        print("W2" + str(W2))
        print("CTheta1" + str(CTheta1))
        print("CTheta2" + str(CTheta2))
        print("alpha1" + str(stageProps.alpha1))
        print("alpha2" + str(stageProps.alpha2))    
       
    return stageProps