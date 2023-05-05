import bpy

input_path = 'D:\\Game Development\\Models\\Gray Alien\\Gray_final_animations_Baked.fbx'
output_path = 'C:\\Users\\Kylec\\Downloads\\test.obj'
decimation_ratio = 0.05
voxel_size = 0.1
uv_angle_limit = 66
uv_island_margin = 0.03
use_smooth_shade = True

# Set up scene
bpy.ops.object.mode_set(mode='OBJECT')
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

# Get the high res models
all_high_res = [obj for obj in bpy.context.scene.objects]
high_res_models = []

# Create copies of the model and remove the original one with linked stuff
for obj in all_high_res:
    if obj.type == "MESH":
        model = obj.copy()
        model.data = obj.data.copy()
        high_res_models.append(model)
        bpy.context.scene.collection.objects.link(model)
        
bpy.ops.object.select_all(action="DESELECT")
for high_res_model in all_high_res:
    high_res_model.select_set(True)
    
bpy.ops.object.delete(use_global=False)

# Create copies of the high res models to use as low res
low_res_models = []
for high_res_model in high_res_models:
    low_res_model = high_res_model.copy()
    low_res_model.data = high_res_model.data.copy()
    low_res_models.append(low_res_model)
    bpy.context.scene.collection.objects.link(low_res_model)

# Use the voxel retopology to reduce the polycount of the low res models
for low_res_model in low_res_models:
    bpy.context.view_layer.objects.active = low_res_model
    bpy.ops.object.modifier_add(type="REMESH")
    bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
    bpy.context.object.modifiers["Remesh"].voxel_size = voxel_size
    bpy.context.object.modifiers["Remesh"].use_smooth_shade = use_smooth_shade
    bpy.ops.object.modifier_apply(modifier="Remesh")

# Create smart UV projections for each low res model
for low_res_model in low_res_models:
    bpy.ops.object.select_all(action="DESELECT")
    low_res_model.select_set(True)
    bpy.context.view_layer.objects.active = low_res_model
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=uv_angle_limit, island_margin=uv_island_margin)
    bpy.ops.object.mode_set(mode='OBJECT')


# Bake the texture
for i in range(len(low_res_models)):
    high = high_res_models[i]
    low = low_res_models[i]
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 128
    bpy.ops.object.select_all(action='DESELECT')
    high.select_set(True)
    bpy.context.view_layer.objects.active = low
    bpy.ops.object.bake(type='DIFFUSE', use_selected_to_active=True, cage_extrusion=0.1, pass_filter={'COLOR'}, margin=0)
#    bpy.ops.object.bake(type='NORMAL', use_selected_to_active=True, cage_extrusion=0.2)
    bpy.context.scene.render.engine = original_render_engine
#    bpy.data.images[low.name].save()


bpy.ops.object.select_all(action="DESELECT")

# Remove the high res models
for high_res_model in high_res_models:
    high_res_model.select_set(True)
    bpy.context.scene.collection.objects.unlink(high_res_model)
    
bpy.ops.object.delete(use_global=False)

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
