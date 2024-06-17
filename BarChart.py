import bpy
import math
import csv

context = bpy.context
scene = context.scene

csv_file_path = r"C:\Blender\top15CountriesPowerGeneration.csv"
data_column = 6
country_column = 1
currency_symbol = "TWh"

anim_start_frame = 10
anim_length_bar = 15
anim_length_text = 8
bar_start_position = 0
distance_bet_bars  = 6
data_list = []
country_list = []

# Save the current location of the 3D cursor
saved_cursor_loc = scene.cursor.location.xyz

# Initialize the variables.
bar_counter = 0
anim_curr_frame = anim_start_frame

# Read the CSV file and store the data in an array
with open(csv_file_path, 'r') as file:
    csvreader = csv.DictReader(file)
    for row in csvreader:
        key = str(list(row)[data_column-1])
        data_list.append(float(row[key]))
        key = str(list(row)[country_column-1])
        country_list.append(str(row[key]))

number_of_bars = len(country_list)
bar_height_mean = sum(data_list) / len(data_list)

# Create a new material for the bars
material_1 = bpy.data.materials.new(name="anim_material_1")
material_1.use_nodes = True
if material_1.node_tree:
    material_1.node_tree.links.clear()
    material_1.node_tree.nodes.clear()
nodes = material_1.node_tree.nodes
links = material_1.node_tree.links
output = nodes.new(type='ShaderNodeOutputMaterial')
shader = nodes.new(type='ShaderNodeBsdfPrincipled')
nodes["Principled BSDF"].inputs[0].default_value = (0, 0.7, 1, 1)
links.new(shader.outputs[0], output.inputs[0])

# Create a new material for the text
material_2 = bpy.data.materials.new(name="anim_material_2")
material_2.use_nodes = True
if material_2.node_tree:
    material_2.node_tree.links.clear()
    material_2.node_tree.nodes.clear()
nodes = material_2.node_tree.nodes
links = material_2.node_tree.links
output = nodes.new(type='ShaderNodeOutputMaterial')
shader = nodes.new(type='ShaderNodeEmission')
nodes["Emission"].inputs['Strength'].default_value = 4.0
links.new(shader.outputs[0], output.inputs[0])

# Create a new material for the floor
material_3 = bpy.data.materials.new(name="anim_material_3")
material_3.use_nodes = True
if material_3.node_tree:
    material_3.node_tree.links.clear()
    material_3.node_tree.nodes.clear()
nodes = material_3.node_tree.nodes
links = material_3.node_tree.links
output = nodes.new(type='ShaderNodeOutputMaterial')
shader = nodes.new(type='ShaderNodeBsdfPrincipled')
nodes["Principled BSDF"].inputs[0].default_value = (0.05, 0.05, 0.05, 1)
links.new(shader.outputs[0], output.inputs[0])

# Create the bars in a loop

while (bar_counter < number_of_bars):
    
    bar_height = data_list[bar_counter] * 5/bar_height_mean
    bar_country = country_list[bar_counter]
    bar_data = str(data_list[bar_counter]) +  currency_symbol

    # Add a cube and set its dimensions
    bpy.ops.mesh.primitive_cube_add()
    ob = bpy.context.active_object
    ob.dimensions = [1,1,bar_height]
    ob.location = [bar_start_position,0,bar_height/2]
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)

    # Set origin to the bottom of the cube
    scene.cursor.location = (bar_start_position,0,0)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    # Animate the height of the cube
    ob.dimensions = [1,1,0]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    anim_curr_frame += anim_length_bar
    ob.dimensions = [1,1,bar_height*1.15]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    anim_curr_frame += 10
    ob.dimensions = [1,1,bar_height]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    
    # Assign the material created above
    ob.data.materials.append(material_1)
    
    # Add the 1st caption
    bpy.ops.object.text_add()
    ob = bpy.context.object
    ob.data.body = bar_country
    ob.data.align_x = "CENTER"
    ob.data.align_y = "CENTER"
    ob.data.extrude = 0.01

    ob.location = [bar_start_position,0,bar_height+2]
    ob.rotation_euler = [math.radians(90),0,0]
    
    anim_curr_frame -= 5
    
    # Animate the caption horizontally
    ob.scale = [0,0,0]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame-1)
    ob.scale = [0,1,1]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    anim_curr_frame += anim_length_text
    ob.scale = [1,1,1]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    
    # Assign the blue material created above
    ob.data.materials.append(material_2)
    
    anim_curr_frame -= anim_length_text

    # Add the 1st caption
    bpy.ops.object.text_add()
    ob = bpy.context.object
    ob.data.body = bar_data
    ob.data.align_x = "CENTER"
    ob.data.align_y = "CENTER"
    ob.data.extrude = 0.01

    ob.location = [bar_start_position,0,bar_height+1]
    ob.rotation_euler = [math.radians(90),0,0]

    # Animate the caption horizontally
    ob.scale = [0,0,0]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame-1)
    ob.scale = [0,1,1]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    anim_curr_frame += anim_length_text
    ob.scale = [1,1,1]
    ob.keyframe_insert(data_path="scale", frame = anim_curr_frame)
    
    # Assign the white material created above
    ob.data.materials.append(material_2)
    
    #increase the loop counters
    bar_counter += 1
    bar_start_position += distance_bet_bars

# Add a plane (floor) and set its dimensions
bpy.ops.mesh.primitive_plane_add()
ob = bpy.context.active_object
floor_length = distance_bet_bars * (number_of_bars - 1) + 2
ob.dimensions = [floor_length,2,1]
ob.location = [floor_length/2-1,0,-0.01]
bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)

# Assign the black material created above
ob.data.materials.append(material_3)

# Clean-up work
# Reset 3D cursor location back to the original
scene.cursor.location.xyz = saved_cursor_loc
context.active_object.select_set(False)

# Set the current frame to frame# 1
scene.frame_set(1)

# Set the scene length
scene.frame_start = 1
scene.frame_end = anim_curr_frame + 50

# Turn on bloom effect
scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.use_bloom = True
