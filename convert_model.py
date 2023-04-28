import bpy

# USER ENTRY
input_path = ''
output_path = ''


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

# Export to another format
if output_path.lower().endswith('fbx'):
    bpy.ops.export_scene.fbx(filepath=output_path)
elif output_path.lower().endswith('gltf'):
    bpy.ops.export_scene.gltf(filepath=output_path)
elif output_path.lower().endswith('obj'):
    bpy.ops.export_scene.obj(filepath=output_path)
elif output_path.lower().endswith('glb'):
    bpy.ops.export_scene.gltf(filepath=output_path)
