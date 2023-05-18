import bpy

# TODO: Add support for quad remesh
# TODO: Specify which textures to generate (normal, diffuse, roughness, AO, metalic)

# Files
input_path = 'D:\\Game Development\\Models\\Gray Alien\\Gray_final_animations_Baked.fbx'
output_path = 'C:\\Users\\Kylec\\Downloads\\alien\\alien.glb'
output_image_dir = 'C:\\Users\\Kylec\\Downloads\\alien'

# Remeshing
remesh_type = 'decimate' # decimate or voxel
voxel_size = 0.05
decimation_ratio = 0.8

# UVs
uv_angle_limit = 66
uv_island_margin = 0.03

# Shade smooth
use_smooth_shade = True
shade_smooth_angle = 60

# Baking
extrusion = 0.2
margin = 32
texture_size = 2048

#### DO NOT MODIFY BELOW


# Helper functions
def set_mode(mode):
    bpy.ops.object.mode_set(mode=mode)

def select(obj):
    obj.select_set(True)

def deselect(obj):
    obj.select_set(False)

def set_active(obj):
    bpy.context.view_layer.objects.active = obj

def select_all():
    bpy.ops.object.select_all(action='SELECT')

def deselect_all():
    bpy.ops.object.select_all(action='DESELECT')

def select_all_mesh():
    bpy.ops.mesh.select_all(action="SELECT")

def delete_selected():
    bpy.ops.object.delete(use_global=False)
    
def import_model(path):
    if path.lower().endswith('fbx'):
        bpy.ops.import_scene.fbx(filepath=path)
    elif path.lower().endswith('gltf'):
        bpy.ops.import_scene.gltf(filepath=path)
    elif path.lower().endswith('obj'):
        bpy.ops.import_scene.obj(filepath=path)
    elif path.lower().endswith('glb'):
        bpy.ops.import_scene.gltf(filepath=path)

def export_model(path):
    if path.lower().endswith('fbx'):
        bpy.ops.export_scene.fbx(filepath=path)
    elif path.lower().endswith('gltf'):
        bpy.ops.export_scene.gltf(filepath=path)
    elif path.lower().endswith('obj'):
        bpy.ops.export_scene.obj(filepath=path)
    elif path.lower().endswith('glb'):
        bpy.ops.export_scene.gltf(filepath=path)

def copy_object(obj):
    model = obj.copy()
    model.data = obj.data.copy()
    return model

def link(obj):
    bpy.context.scene.collection.objects.link(obj)

def unlink(obj):
    bpy.context.scene.collection.objects.unlink(obj)

def shade_smooth(obj):
    obj.data.use_auto_smooth = True
    obj.data.auto_smooth_angle = shade_smooth_angle

def decimate(obj, ratio):
    set_active(obj)
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = ratio
    bpy.ops.object.modifier_apply(modifier="Decimate")

def voxel_remesh(obj, voxel_size, smooth_shade):
    set_active(obj)
    bpy.ops.object.modifier_add(type="REMESH")
    bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
    bpy.context.object.modifiers["Remesh"].voxel_size = voxel_size
    bpy.context.object.modifiers["Remesh"].use_smooth_shade = smooth_shade
    bpy.ops.object.modifier_apply(modifier="Remesh")

def smart_uv(obj, angle_limit, island_margin):
    deselect_all()
    select(obj)
    set_active(obj)
    set_mode('EDIT')
    select_all_mesh()
    bpy.ops.uv.smart_project(angle_limit=angle_limit, island_margin=island_margin)
    set_mode('OBJECT')

def delete(objects, should_unlink=False):
    deselect_all()
    if type(objects) is not list:
        objects = [objects]
    for obj in objects:
        select(obj)
        if should_unlink:
            unlink(obj)
    delete_selected()


def bake(obj, source, material_node, bake_type, margin, extrusion, pass_filter=None):
    deselect_all()
    select(source)
    mat = obj.active_material
    set_active(obj)
    
    mat.node_tree.nodes.active = mat.node_tree.nodes.get(material_node)
    mat.node_tree.nodes.get(material_node).select = True
    bpy.ops.object.bake(type=bake_type, use_selected_to_active=True, cage_extrusion=extrusion, margin=margin, pass_filter=pass_filter)
    mat.node_tree.nodes.get(material_node).select = False

def export_image(image, path):
    bpy.data.images[image].save_render(path)

def hide_render(obj):
    obj.hide_render = True

def show_render(obj):
    obj.hide_render = False

def reset_material(obj, material_name):
    obj.data.materials.clear()
    mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)
    mat.use_nodes = True
    return mat

def add_image_node(obj, node_type, node_name, image_size, image_name):
    mat = obj.active_material
    nodes = mat.node_tree.nodes
    node = nodes.new(type=node_type)
    node.image = bpy.data.images.new(image_name, width=image_size, height=image_size)
    node.name = node_name
    return node


# Set up scene
set_mode('OBJECT')
select_all()
delete_selected()


original_render_engine = bpy.context.scene.render.engine

# Import
import_model(input_path)

# Get the high res models
all_high_res = [obj for obj in bpy.context.scene.objects]
high_res_models = []

# Create copies of the model and remove the original one with linked stuff
for obj in all_high_res:
    if obj.type == "MESH":
        model = copy_object(obj)
        high_res_models.append(model)
        link(model)


delete(all_high_res)

# Create copies of the high res models to use as low res
low_res_models = []
for high_res_model in high_res_models:
    low_res_model = copy_object(high_res_model)
    low_res_models.append(low_res_model)
    link(low_res_model)

# Use the voxel retopology to reduce the polycount of the low res models
for low_res_model in low_res_models:
    if remesh_type == 'voxel':
        voxel_remesh(low_res_model, voxel_size, use_smooth_shade)
    else:
        decimate(low_res_model, decimation_ratio)
        
    # Shade smooth
    if use_smooth_shade:
        shade_smooth(low_res_model)

# Create smart UV projections for each low res model
for low_res_model in low_res_models:
    smart_uv(low_res_model, uv_angle_limit, uv_island_margin)

# Remove the original texture from the low res model
for i in range(len(low_res_models)):
    low = low_res_models[i]
    mat = reset_material(low, "NewMaterial_" + low.name)    
    
    diffuse_node = add_image_node(low, 'ShaderNodeTexImage', 'diffuse', texture_size, 'diffuse_' + low.name + '.png')
    normal_node = add_image_node(low, 'ShaderNodeTexImage', 'normal', texture_size, 'normal_' + low.name + '.png')
    
    normal_map_node = mat.node_tree.nodes.new(type='ShaderNodeNormalMap')
    normal_map_node.uv_map = 'UVMap'
    
    links = mat.node_tree.links
    links.new(normal_node.outputs['Color'], normal_map_node.inputs['Color'])
    links.new(diffuse_node.outputs['Color'], mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'])
    links.new(normal_map_node.outputs['Normal'], mat.node_tree.nodes['Principled BSDF'].inputs['Normal'])


# Bake the texture
for i in range(len(low_res_models)):
    # Hide everything not being rendered
    for j in range(len(low_res_models)):
        if j == i:
            show_render(low_res_models[j])
            show_render(high_res_models[j])
        else:
            hide_render(low_res_models[j])
            hide_render(high_res_models[j])
    
    high = high_res_models[i]
    low = low_res_models[i]
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 5

    bake(low, high, 'diffuse', 'DIFFUSE', margin, extrusion, {'COLOR'})
    bake(low, high, 'normal', 'NORMAL', margin, extrusion)
    
    bpy.context.scene.render.engine = original_render_engine
    
    # Save textures
    export_image("diffuse_" + low.name + ".png", output_image_dir + "/diffuse_" + low.name + ".png")
    export_image("normal_" + low.name + ".png", output_image_dir + "/normal_" + low.name + ".png")


# Remove the high res models
delete(high_res_models, True)

# Export
export_model(output_path)

# Switch back to original render engine
bpy.context.scene.render.engine = original_render_engine
