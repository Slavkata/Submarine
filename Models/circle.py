import bpy
import bmesh
import math
import mathutils
import csv

# Make a new BMesh
csv_file = open('path-to-file', newline='')
submarine_data = csv.reader(csv_file, delimiter=',')

for row in submarine_data:
    bm = bmesh.new()
    bmesh.ops.create_circle(
        bm,
        cap_ends=False,
        radius=float(row[1]),
        segments=30)
            
    bmesh.ops.translate(
        bm,
        verts=bm.verts,
        vec=(0.0, 0.0, float(row[0])))

    me = bpy.data.meshes.new("Mesh")
    bm.to_mesh(me)
    bm.free()


    # Add the mesh to the scene
    obj = bpy.data.objects.new("Circle", me)
    bpy.context.collection.objects.link(obj)

MSH_OBJS = [m for m in bpy.context.scene.objects if m.type == 'MESH']
for OBJS in MSH_OBJS:
    #Select all mesh objects
    OBJS.select_set(state=True)

    #Makes one active
    bpy.context.view_layer.objects.active = OBJS
    
bpy.ops.object.join()

bpy.ops.object.mode_set(mode='EDIT')

ob = bpy.context.edit_object
me = ob.data
bm = bmesh.from_edit_mesh(me)

verts = bm.verts

verts = sorted(verts, key= lambda vert: vert.co[2])

for i in range(int(len(verts)-31)):
    selected = [verts[i], verts[i+1], verts[i+30], verts[i+1+30]]
    bmesh.ops.contextual_create(bm, geom=selected)
    

bmesh.update_edit_mesh(me)
