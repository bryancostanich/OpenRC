
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
import math
import mathutils
import scipy.spatial
import numpy

def DeleteMesh(name):
    
    if name in bpy.data.objects:        
        ob = bpy.data.objects[name]
        bpy.context.scene.objects.unlink(ob)
        bpy.data.objects.remove(ob)
    if name in bpy.data.meshes:
        mesh = bpy.data.meshes[name]
        bpy.data.meshes.remove(mesh)
 
def createMesh(name, origin, verts, edges, faces):
    
    # remove mesh Cube
    DeleteMesh(name)
    
    # Create mesh and object
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True
    # Link object to scene
    bpy.context.scene.objects.link(ob)
    bpy.context.scene.objects.active=ob
 
    # Create mesh from given verts, edges, faces. Either edges or
    # faces should be [], or you ask for problems
    me.from_pydata(verts, edges, faces)
 
    # Update mesh with new data
    me.update(calc_edges=True)
    return ob

def SelectOnly(name):
    #Select and activates only the object with the name name.
    
    #Deselect All
    bpy.ops.object.select_all(action='DESELECT')
        
    #grab object 1 and select it
    obj1 = bpy.data.objects[name]
    bpy.context.scene.objects.active=obj1
    obj1.select=True
def MoveObject(name,deltaLocation):
    #name is a string
    #deltaLocation is a vector

	#bpy.data.objects[name].delta_location += deltaLocation
	bpy.data.objects[name].matrix_world[0][3] += deltaLocation[0]
	bpy.data.objects[name].matrix_world[1][3] += deltaLocation[1]
	bpy.data.objects[name].matrix_world[2][3] += deltaLocation[2]
	bpy.context.scene.update()
	bpy.data.meshes[name].update()
	
      
def RotateObject(name,deltaOrientation):    
    #name is a string
    #deltaLocation is a vector
    bpy.data.objects[name].delta_rotation_euler.x += deltaOrientation.x
    bpy.data.objects[name].delta_rotation_euler.y += deltaOrientation.y
    bpy.data.objects[name].delta_rotation_euler.z += deltaOrientation.z
def BooleanMesh(name1,name2,boolType,boolDel2):
    
    #Deselect All
    bpy.ops.object.select_all(action='DESELECT')
            
    #grab object 1 and select it
    obj1 = bpy.data.objects[name1]
    bpy.context.scene.objects.active=obj1
    
    #Boolean the two  
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[name2]
    bpy.context.object.modifiers["Boolean"].operation = boolType
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    if(boolDel2):
        DeleteMesh(name2)
        
def ConvexHull(listOfMeshes):
	listOfVertices = []
	points = []
	ids=[]
	realIDs=[]
	
	#Cycle through all the objects we want to use to form a convex hull
	for obName in listOfMeshes:
		ob = bpy.data.objects[obName]
		me = bpy.data.meshes[obName]
		mat = ob.matrix_world
		#print(mat)
		#Store all the verts in one contiguous array
		for v in me.vertices:
			points.extend([mat*v.co])
	
	#find the convex hull of the verts
	Hull = scipy.spatial.ConvexHull(points)
	mesh = bpy.data.meshes.new(name='Convex Hull')
	oldFaces = []
	
	#We need to strip the verts of unused ones, so we have to adjust the poly's vert ids accordingly
	#preparing a few data structures to allow that to happen.
	for s in Hull.simplices:
	
		norm = CalcNorm(points[int(s[0])],points[int(s[1])],points[int(s[2])])
		vect = mathutils.Vector(points[int(s[0])])
		if(mathutils.Vector(norm)*vect > 0):
			oldFaces.extend([[int(s[0]),int(s[1]),int(s[2])]])
		else:
			oldFaces.extend([[int(s[2]),int(s[1]),int(s[0])]])
		
		ids.append(int(s[0]))
		ids.append(int(s[1]))
		ids.append(int(s[2]))
	ids.sort()	
	
	
	#Assign only the required the verts to a list
	for id in ids:
		listOfVertices.append(points[id])
		realIDs.append(id)
	
	#newFaces has
	newFaces = []
	for face in oldFaces:
		tmpFace=[]
		for oldID in face:
			for vID in range(0,len(realIDs)):
				if(oldID == realIDs[vID]):
					tmpFace.append(vID)
					break
		newFaces.append([tmpFace[0],tmpFace[1],tmpFace[2]])
	
	#create the geometry and update
	mesh.from_pydata(listOfVertices, [], newFaces)
	ob = bpy.data.objects.new('Convex Hull',mesh)
	scn = bpy.context.scene
	scn.objects.link(ob)
	bpy.context.scene.objects.active=ob
	mesh.update(calc_edges=True)
	
def CalcNorm(vert1,vert2,vert3):

	edge1 = vert2-vert1
	edge2 = vert3-vert1
	
	norm = CrossProd(edge1,edge2)
	return norm

def CrossProd(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c	
def ShiftVerts(name,displacement):
    
    for v in bpy.data.objects[name].data.vertices:
        v.co += displacement               
def ScaleVerts(name,scaleX,scaleY,scaleZ):
        
    sX = mathutils.Matrix.Scale(scaleX,3,(1,0,0))
    sY = mathutils.Matrix.Scale(scaleY,3,(0,1,0))
    sZ = mathutils.Matrix.Scale(scaleZ,3,(0,0,1))
    for v in bpy.data.objects[name].data.vertices:
        v.co = sX*v.co
        v.co = sY*v.co
        v.co = sZ*v.co
def DrawBox(name, length,width,height):
    
    #delete any existing mesh
    DeleteMesh("Cube")
    
    #add cube
    bpy.ops.mesh.primitive_cube_add()        
     
    #Rename Cube 
    cube = bpy.data.objects["Cube"]
    cube.name = name
    cube.data.name = name
    
    #Create a unit cube
    ScaleVerts(name,0.5*length,0.5*width,0.5*height)
def DrawSphere(name,od,res):
    DeleteMesh("Sphere")
    
    bpy.ops.mesh.primitive_uv_sphere_add(segments=res,ring_count=res,size=od/2)
    #Rename Cube 
    sphere = bpy.data.objects["Sphere"]
    sphere.name = name
    sphere.data.name = name    
def DrawCylinder(name,od,id,h,res):
    
    if(od < id):
        print("Error: EDFLibrary.DrawCylinder() - od<id.  OD: "+str(od)+", ID: "+str(id))
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=res,radius=od/2,depth=h,location=(0,0,0)) 
    cyl = bpy.data.objects["Cylinder"]
    cyl.name = name
    cyl.data.name = name
    
    

    if(id != 0):
        bpy.ops.mesh.primitive_cylinder_add(vertices=res,radius=id/2,depth=h+1,location=(0,0,0)) 
        cyl2 = bpy.data.objects["Cylinder"]
        cyl2.name = name+".hole"
        cyl2.data.name = name+".hole"
        
        
       
        
        
        
        #Boolean difference the mesh
        BooleanMesh(name,name+".hole","DIFFERENCE",True)
         