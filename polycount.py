import bpy

for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        print("Poly count of", obj.name + ":", len(obj.data.polygons))