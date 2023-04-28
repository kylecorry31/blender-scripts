import bpy

# USER ENTRY
input_path = 'D:\\Game Development\\Models\\Gray Alien\\Gray_final_animations_Baked.fbx'
output_path = 'C:\\Users\\Kylec\\Downloads\\test.obj'
decimation_ratio = 0.1
clear_materials = False

# Set up scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Import
if input_path.lower().endswith('fbx'):
    bpy.ops.import_scene.fbx(filepath=input_path)
elif input_path.lower().endswith('gltf'):
    bpy.ops.import_scene.gltf(filepath=input_path)
elif input_path.lower().endswith('obj'):
    bpy.ops.import_scene.obj(filepath=input_path)
elif input_path.lower().endswith('glb'):
    bpy.ops.import_scene.gltf(filepath=input_path)

# Clear materials
if clear_materials:
    # Remove all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

    # Remove all vertex colors
    for mesh in bpy.data.meshes:
        for vcol_layer in mesh.vertex_colors:
            mesh.vertex_colors.remove(vcol_layer)


# Apply modifiers and simplify geometry
# Set the first mesh object as active if there are any mesh objects in the scene
mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
if mesh_objects:
    bpy.context.view_layer.objects.active = mesh_objects[0]
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.context.view_layer.objects.active = obj
        for mod in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.object.shade_smooth()
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = decimation_ratio
        bpy.ops.object.modifier_apply(modifier="Decimate")
        bpy.ops.object.convert(target='MESH')

# Export
if output_path.lower().endswith('fbx'):
    bpy.ops.export_scene.fbx(filepath=output_path)
elif output_path.lower().endswith('gltf'):
    bpy.ops.export_scene.gltf(filepath=output_path)
elif output_path.lower().endswith('obj'):
    bpy.ops.export_scene.obj(filepath=output_path)
elif output_path.lower().endswith('glb'):
    bpy.ops.export_scene.gltf(filepath=output_path)
