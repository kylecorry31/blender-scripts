import bpy

# USER ENTRY
input_path = 'D:\\Game Development\\Models\\Gray Alien\\Gray_final_animations_Baked.fbx'
output_path = 'C:\\Users\\Kylec\\Downloads\\test.obj'
decimation_ratio = 0.05

# Set up scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

original_render_engine = bpy.context.scene.render.engine


# Import
if input_path.lower().endswith('fbx'):
    bpy.ops.import_scene.fbx(filepath=input_path)
elif input_path.lower().endswith('gltf'):
    bpy.ops.import_scene.gltf(filepath=input_path)
elif input_path.lower().endswith('obj'):
    bpy.ops.import_scene.obj(filepath=input_path)
elif input_path.lower().endswith('glb'):
    bpy.ops.import_scene.gltf(filepath=input_path)
    
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':

        # Make a copy of the object
        copy_obj = obj.copy()
        copy_obj.data = obj.data.copy()
        bpy.context.scene.collection.objects.link(copy_obj)

        # Decimate the object
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].ratio = decimation_ratio
        bpy.ops.object.modifier_apply(modifier="Decimate")

        # TODO: Bake normals (bake from multires)
        
        # TODO: Set max samples to 10

        # Bake the texture
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.ops.object.select_all(action='DESELECT')
        copy_obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.bake(type='COMBINED', use_selected_to_active=True, cage_extrusion=0.2)
        bpy.context.scene.render.engine = original_render_engine

        # Delete the copy of the object
        bpy.data.objects.remove(copy_obj)

# Export
if output_path.lower().endswith('fbx'):
    bpy.ops.export_scene.fbx(filepath=output_path)
elif output_path.lower().endswith('gltf'):
    bpy.ops.export_scene.gltf(filepath=output_path)
elif output_path.lower().endswith('obj'):
    bpy.ops.export_scene.obj(filepath=output_path)
elif output_path.lower().endswith('glb'):
    bpy.ops.export_scene.gltf(filepath=output_path)

# Switch back to original render engine
bpy.context.scene.render.engine = original_render_engine