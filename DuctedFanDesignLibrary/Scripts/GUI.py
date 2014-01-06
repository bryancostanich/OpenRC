
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
import sys
sys.path.append("./") 
sys.path.append("C:\Python33\Lib\site-packages")#We need access to NumPy/SciPy Python
import bpy
import math
import mathutils
import DLUtils
import EDFLibrary
import TurboMachLib


 
class DrawRotor(bpy.types.Operator):
    bl_idname = "draw.rotor"
    bl_label = "Draw rotor"

    def execute(self, context):
        scene = context.scene
        
        stageProps = EDFLibrary.StageCalc(R=scene.reaction,\
            phi=scene.flowCoefficient,\
            psi=scene.stageLoading,\
            rpm=scene.rpm,\
            rootRadius=scene.hubDia/2,\
            tipRadius=scene.rotorDia/2)
        
        #Compute root properties        
        stagePropsRoot = stageProps.rootProps
        avgBetaRoot= (stagePropsRoot.beta2+stagePropsRoot.beta1)/2                  
        deltaBetaRoot = (stagePropsRoot.beta2-stagePropsRoot.beta1)              
        rootCamber = scene.rotorRootChord/2/math.sin(deltaBetaRoot) - scene.rotorRootChord/2/math.tan(deltaBetaRoot)
        rootCamber/=scene.rotorRootChord
        rootCamber*=-100
        
        #Compute tip properties        
        stagePropsTip = stageProps.tipProps
        avgBetaTip= (stagePropsTip.beta2+stagePropsTip.beta1)/2                 
        deltaBetaTip = (stagePropsTip.beta2-stagePropsTip.beta1)   
        tipCamber = scene.rotorTipChord/2/math.sin(deltaBetaTip) - scene.rotorTipChord/2/math.tan(deltaBetaTip)
        tipCamber/=scene.rotorTipChord
        tipCamber*=-100
        
        print("avgBetaRoot: " + str(avgBetaRoot))
        print("avgBetaTip: " + str(avgBetaTip))
        print("rootCamber: " +str(rootCamber))
        print("tipCamber: " + str(tipCamber))
        print("deltaBetaRoot: " +str(deltaBetaRoot))
        print("deltaBetaTip: " +str(deltaBetaTip))
        
        EDFLibrary.Rotor(rotorName=scene.rotorName,\
                    hubDia=scene.hubDia,\
                    hubHeight=scene.hubLength,\
                    hubThickness=scene.hubThickness,\
                    rotorDia=scene.rotorDia,\
                    axleDia=scene.shaftDia,\
                    camber_root = rootCamber,
                    camber_tip = tipCamber,
                    camber_position=40,\
                    thickness=scene.rotBladeThickness,\
                    bladeHeight=scene.rotorDia/1.7-scene.hubDia/2,\
                    twistAngle=-(avgBetaRoot - avgBetaTip)*180/math.pi,\
                    rootChord=scene.rotorRootChord,\
                    tipChord=scene.rotorTipChord,\
                    clearance=0.5,\
                    centerOfTwist=[scene.rotCenterOfTwistX,scene.rotCenterOfTwistY],\
                    nspan=5,\
                    npts=25,\
                    rootAngle=avgBetaRoot*180/math.pi,\
                    nRotorBlades=scene.nRotBlades)    
                    #twistAngle=-(avgBetaRoot - avgBetaTip)*180/math.pi,\
                    #rootAngle=avgBetaRoot*180/math.pi,\   
        return {'FINISHED'}

class DrawStator(bpy.types.Operator):
    bl_idname = "draw.stator"
    bl_label = "Draw stator"

    def execute(self, context):
        scene = context.scene
        stageProps = EDFLibrary.StageCalc(R=scene.reaction,\
            phi=scene.flowCoefficient,\
            psi=scene.stageLoading,\
            rpm=scene.rpm,\
            rootRadius=scene.hubDia/2,\
            tipRadius=scene.rotorDia/2)
        
        #Compute root properties
        stagePropsRoot = stageProps.rootProps
        avgAlphaRoot= (stagePropsRoot.alpha2+stagePropsRoot.alpha1)/2                  
        deltaAlphaRoot = (stagePropsRoot.alpha2-stagePropsRoot.alpha1)              
        rootCamber = scene.statorRootChord/2/math.sin(deltaAlphaRoot) - scene.statorRootChord/2/math.tan(deltaAlphaRoot)
        rootCamber/=scene.statorRootChord
        rootCamber*=-100
        
        #Commpute tip properties        
        stagePropsTip = stageProps.tipProps
        avgAlphaTip= (stagePropsTip.alpha2+stagePropsTip.alpha1)/2                 
        deltaAlphaTip = (stagePropsTip.alpha2-stagePropsTip.alpha1)   
        tipCamber = scene.statorTipChord/2/math.sin(deltaAlphaTip) - scene.statorTipChord/2/math.tan(deltaAlphaTip)
        tipCamber/=scene.statorTipChord
        tipCamber*=-100
        
        
        
        print("avgAlphaRoot: " + str(avgAlphaRoot))
        print("avgAlphaTip: " + str(avgAlphaTip))
        print("rootCamber: " +str(rootCamber))
        print("tipCamber: " + str(tipCamber))
        print("deltaAlphaRoot: " +str(deltaAlphaRoot))
        print("deltaAlphaTip: " +str(deltaAlphaTip))
        
        EDFLibrary.Stator(ductID=scene.ductID,\
                    ductThickness=scene.ductThickness,\
                    ductLength=scene.ductLength,\
                    res=64,\
                    mountFaceXLoc=scene.mountFaceXLoc,\
                    mountCanID=scene.mountCanID,\
                    mountCanLength=scene.mountCanLength,\
                    nBlades=scene.nStaBlades,\
                    rootAngle=-avgAlphaRoot*180/math.pi,\
                    camberRoot=rootCamber,\
                    camberTip = tipCamber,\
                    camber_position=50,\
                    bladeThickness=scene.staBladeThickness,\
                    bladeHeight=20,\
                    twistAngle=-(avgAlphaTip-avgAlphaRoot)*180/math.pi,\
                    rootChord=scene.statorRootChord,\
                    tipChord=scene.statorTipChord,\
                    centerOfTwist=[scene.staCenterOfTwistX,scene.staCenterOfTwistY],\
                    nspan=5,\
                    npts=25)
             
        return {'FINISHED'}


class DrawStage2D(bpy.types.Operator):
    bl_idname = "draw.stage"
    bl_label = "Draw Stage in 2D"

    def execute(self, context):
        scene = context.scene
        
        stageProps=EDFLibrary.CalcStageBladeAngles(R=scene.reaction,\
                        phi=scene.flowCoefficient,\
                        psi=scene.stageLoading,\
                        radius=scene.meanLineRadius,
                        rpm = scene.rpm)
        print("")
        print("")
        print("Drawing 2D Rotor/Stator blades")  
        print("")
        print("")
                   
        chord=1         
        deltaBeta = (stageProps.beta2-stageProps.beta1)               
        camber = chord/2/math.sin(deltaBeta) - chord/2/math.tan(deltaBeta)
        print("beta " +str((stageProps.beta1+stageProps.beta2)/2*180/math.pi))                     
        print("rotorcamber " + str(camber*100))
        print("deltaBeta "+ str(deltaBeta*180/math.pi))   
        TurboMachLib.NACA4(name='rotor2D',\
                        camber_root=camber*100,\
                        camber_tip=camber*100,\
                        camber_position=35,\
                        thickness=6,\
                        bladeHeight=1,\
                        twistAngle=0,\
                        rootChord=1,\
                        tipChord=1,\
                        centerOfTwist=[0,0],\
                        nspan=1,\
                        npts=24)
                        
                               
        DLUtils.RotateObject('rotor2D',mathutils.Euler([0,0,-(stageProps.beta2+stageProps.beta1)/2]))                
        deltaAlpha = (stageProps.alpha2-stageProps.alpha1)               
        camber = chord/2/math.sin(deltaAlpha) - chord/2/math.tan(deltaAlpha)
        print("alpha " +str((stageProps.alpha1+stageProps.alpha2)/2*180/math.pi))                     
        print("statorcamber " + str(camber*100))
        print("deltaAlpha "+ str(deltaAlpha*180/math.pi))   
        TurboMachLib.NACA4(name='stator2D',\
                        camber_root=camber*100,\
                        camber_tip=camber*100,\
                        camber_position=35,\
                        thickness=6,\
                        bladeHeight=1,\
                        twistAngle=0,\
                        rootChord=1,\
                        tipChord=1,\
                        centerOfTwist=[0,0],\
                        nspan=1,\
                        npts=15)
                       
        DLUtils.MoveObject('stator2D',mathutils.Vector([1,0,0]))
        DLUtils.RotateObject('stator2D',mathutils.Euler([0,0,(stageProps.alpha2+stageProps.alpha1)/2]))                
             
        #stageProps.GenerateReport("test.txt")

        return {'FINISHED'}


class CustomPanel(bpy.types.Panel):
    """A Custom Panel"""
    bl_label = "Ducted Fan Design Library"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    def DrawRotor(self,context):
        print("")
    
    def draw(self,context):
        layout = self.layout
        ###################################################
        row = layout.row()
        row.label(text="Stage Design")    
        ###
        split = layout.split(align=True)
        
        #Right Column
        col = split.column(align=True)

        col.prop(context.scene, "reaction")        
        col.prop(context.scene, "flowCoefficient")
        col.prop(context.scene, "stageLoading")
        col.operator("draw.stage")
        
        row = layout.row()
        row.label(text="Overall fan Details")  
       
        #Left Column
        split = layout.split(align=True)
        col = split.column(align=True)
        #col.prop(context.scene, "nStages")
        col.prop(context.scene, "rotorDia")
        col.prop(context.scene, "ductLength")
        col.prop(context.scene, "meanLineRadius")
        col.prop(context.scene, "rpm")
        
        
        #### ROTOR ###
        row = layout.row()
        row.label(text="Rotor Geometry")    
        ###
        
        row = layout.row()
        row.prop(context.scene,"rotorName")
        
        split = layout.split()
        
        #Left Column
        col = split.column(align=True)
        col.prop(context.scene, "nRotBlades")
        col.prop(context.scene,"shaftDia")
        col.prop(context.scene,"rotorRootChord")
        col.prop(context.scene,"rotorTipChord")
        col.prop(context.scene,"rotBladeThickness")
        
        #Right Column
        col = split.column(align=True)
        col.prop(context.scene, "hubDia")
        col.prop(context.scene, "hubLength")        
        col.prop(context.scene, "hubThickness")
        col.prop(context.scene, "clearance")
        
        row=layout.row(align=True)
        
        row.prop(context.scene,"rotCenterOfTwistX")
        row.prop(context.scene,"rotCenterOfTwistY")
        
        
        row=layout.row()
        row.operator("draw.rotor")
       
        ### STATOR ###
        
        row = layout.row()
        row.label(text="Stator Geometry")    
        ###        
        
        row = layout.row()
        row.prop(context.scene,"statorName")
        
        split = layout.split()
                
        col = split.column(align=True)
        col.prop(context.scene, "nStaBlades")
        col.prop(context.scene, "staBladeThickness")
        
        col = split.column(align=True)
        col.prop(context.scene, "mountCanLength")
        col.prop(context.scene, "mountCanID")
        col.prop(context.scene, "mountFaceXLoc")


        split = layout.split()
        col = split.column(align=True)
        
        col.prop(context.scene, "ductThickness")
        col.prop(context.scene, "ductID")
        col.prop(context.scene, "statorRootChord")
        col.prop(context.scene, "statorTipChord")
        
        col = split.column(align=True)
        col.prop(context.scene, "staMotorScrewHoleDia")
        col.prop(context.scene, "staMotorScrewSpreadDia")
        col.prop(context.scene, "staMotorShaftHoleDia")
               
        row=layout.row()
        row.prop(context.scene,"staCenterOfTwistX")
        row.prop(context.scene,"staCenterOfTwistY")
        
        row=layout.row()
        row.operator("draw.stator")
        
 

def register():        


########
## Fan Properties
#####

    bpy.types.Scene.nStages = bpy.props.IntProperty(
            name="nStages", 
            description="Number of compressor stages", 
            default=1, 
            min=1, 
            max=20)
    bpy.types.Scene.meanLineRadius = bpy.props.FloatProperty(
            name="meanLineRadius", 
            description="Mean blade radius location for mean line analysis.", 
            default=64/2+28.8/2, 
            min=1e-6, 
            max=1000)
    bpy.types.Scene.rpm = bpy.props.FloatProperty(
            name="rpm", 
            description="rpm.", 
            default=30000 ,
            min=1e-6, 
            max=9e8)
    bpy.types.Scene.reaction = bpy.props.FloatProperty(
            name="Reaction", 
            description="Reaction", 
            default=0.9, 
            min=1e-6, 
            max=1)
    bpy.types.Scene.flowCoefficient = bpy.props.FloatProperty(
            name="Flow Coefficient", 
            description="Flow Coefficient", 
            default=0.6, 
            min=0, 
            max=10)
    bpy.types.Scene.stageLoading = bpy.props.FloatProperty(
            name="Stage Loading", 
            description="Stage Loading", 
            default=0.3, 
            min=1e-6, 
            max=1)
    
    bpy.types.Scene.rotorDia = bpy.props.FloatProperty(
            name="Rotor Diameter",
            description="Rotor Diameter",
            default=64,
            min = 1e-6,
            max=1e6)
            
########
## Rotor Properties
#####    
    
    bpy.types.Scene.rotorName = bpy.props.StringProperty(
            name="Rotor Name",
            description="Name to assign to the Rotor object and mesh",
            default="Rotor")
    
    centerOfTwist=[50,0]
    bpy.types.Scene.rotCenterOfTwistX = bpy.props.IntProperty(
            name="CenterOfTwistX", 
            description="The X coordinate of the location of the blade center of twise from the leading edge of the root.", 
            default=50, 
            min=0, 
            max=100)
    bpy.types.Scene.rotCenterOfTwistY = bpy.props.IntProperty(
            name="CenterOfTwistY", 
            description="The Y coordinate of the location of the blade center of twise from the leading edge of the root.", 
            default=0, 
            min=0, 
            max=100)
    bpy.types.Scene.hubDia = bpy.props.FloatProperty(
            name="hubDia", 
            description="Hub Diameter", 
            default=25, 
            min=1e-6, 
            max=1e6)
    bpy.types.Scene.rotBladeThickness = bpy.props.FloatProperty(
            name="Blade Thickness", 
            description="Blade Thickness", 
            default=6, 
            min=1e-6, 
            max=1e6)
    bpy.types.Scene.hubThickness = bpy.props.FloatProperty(
            name="hubThickness", 
            description="Hub Thickness", 
            default=1, 
            min=1e-6, 
            max=1e6)
    bpy.types.Scene.hubLength = bpy.props.FloatProperty(
        name="hub length", 
        description="Length of the hub", 
        default=20, 
        min=1e-6, 
        max=1000)
    bpy.types.Scene.shaftDia = bpy.props.FloatProperty(
        name="Shaft diameter", 
        description="Diameter of shaft", 
        default=5.5, 
        min=1e-6, 
        max=1000)   
    bpy.types.Scene.nRotBlades = bpy.props.IntProperty(
        name="nRotBlades", 
        description="Number of rotor blades", 
        default=7, 
        min=1, 
        max=30)        
    bpy.types.Scene.rotorRootChord = bpy.props.FloatProperty(
        name="Root chord", 
        description="Blade root chord", 
        default=20, 
        min=1e-6, 
        max=1000)               
    bpy.types.Scene.rotorTipChord = bpy.props.FloatProperty(
        name="Tip chord", 
        description="Blade tip chord", 
        default=15, 
        min=1e-6, 
        max=1000)
    bpy.types.Scene.clearance = bpy.props.FloatProperty(
        name="Blade Clearance", 
        description="Blade clearance with duct.", 
        default=1, 
        min=1e-6, 
        max=100)        
########
## Stator + Duct Properties
#####    

    bpy.types.Scene.statorName = bpy.props.StringProperty(
            name="Stator Name",
            description="Name to assign to the Stator object and mesh",
            default="Stator")
    bpy.types.Scene.nStaBlades = bpy.props.IntProperty(
        name="nStaBlades", 
        description="Number of rotor blades", 
        default=0, 
        min=0, 
        max=25)
    
    bpy.types.Scene.ductID = bpy.props.FloatProperty(
        name="Duct ID",
        description="The internal diameter of the duct.", 
        default=64, 
        min=0.0, 
        max=1000.0)
        
    bpy.types.Scene.ductThickness = bpy.props.FloatProperty(
        name="Duct Thickness",
        description="The thickness of the duct.", 
        default=1.5, 
        min=0.0, 
        max=1000.0)

    bpy.types.Scene.mountFaceXLoc = bpy.props.FloatProperty(
        name="canXLoc",
        description="The X location of the mounting can from the front face.", 
        default=25, 
        min=0.0, 
        max=1000.0)
      
    bpy.types.Scene.mountCanID = bpy.props.FloatProperty(
        name="mountCanID",
        description="The ID of the mounting can.", 
        default=28.8, 
        min=0.0, 
        max=1000.0)
         
    bpy.types.Scene.mountCanLength = bpy.props.FloatProperty(
        name="mountCanLength",
        description="The length of the mounting can.", 
        default=30, 
        min=0.0, 
        max=1000.0)

    bpy.types.Scene.nStaBlades = bpy.props.IntProperty(
        name="nStaBlades",
        description="Number of stator blades.", 
        default=7, 
        min=0, 
        max=1000)
        
        
    bpy.types.Scene.staBladeThickness = bpy.props.FloatProperty(
        name="bladeThickness",
        description="Thickness of the stator blades.", 
        default=8, 
        min=0, 
        max=1000)
        
    bpy.types.Scene.ductLength = bpy.props.FloatProperty(
        name="Duct length",
        description="Duct length.", 
        default=55.25, 
        min=0.1, 
        max=1000)
        
    bpy.types.Scene.staCenterOfTwistX = bpy.props.IntProperty(
            name="CenterOfTwistX", 
            description="The X coordinate of the location of the blade center of twise from the leading edge of the root.", 
            default=50, 
            min=0, 
            max=100)
    bpy.types.Scene.staCenterOfTwistY = bpy.props.IntProperty(
            name="CenterOfTwistY", 
            description="The Y coordinate of the location of the blade center of twise from the leading edge of the root.", 
            default=0, 
            min=0, 
            max=100)
    bpy.types.Scene.staMotorScrewSpreadDia = bpy.props.FloatProperty(
        name="screwHoleSpreadDia",
        description="The radius about which 4 mount screw holes will be added to the mount.", 
        default=16, 
        min=0.1, 
        max=1000)
    bpy.types.Scene.staMotorScrewHoleDia = bpy.props.FloatProperty(
        name="screwHoleDia",
        description="The hole diameter for the 4 mount screw holes.", 
        default=2.6, 
        min=0.1, 
        max=1000)
    bpy.types.Scene.staMotorShaftHoleDia = bpy.props.FloatProperty(
        name="shaftHoleDia",
        description="The hole diameter for the motor shaft.", 
        default=9, 
        min=0.1, 
        max=1000)
        
    bpy.types.Scene.statorRootChord = bpy.props.FloatProperty(
        name="Stator root chord", 
        description="Stator blade root chord", 
        default=30, 
        min=1e-6, 
        max=1000)               
    bpy.types.Scene.statorTipChord = bpy.props.FloatProperty(
        name="Stator tip chord", 
        description="Stator blade tip chord", 
        default=25, 
        min=1e-6, 
        max=1000)
    
    bpy.utils.register_class(DrawRotor)
    bpy.utils.register_class(DrawStator)
    bpy.utils.register_class(DrawStage2D)
    bpy.utils.register_class(CustomPanel)

def unregister():
    bpy.utils.unregister_class(CustomPanel)
 
if __name__ == "__main__":
    register()       
