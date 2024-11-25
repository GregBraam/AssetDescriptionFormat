
import tempfile, os, bpy
from . import adf_types

FILE_HEADER_MAGIC = "ADF "
VERSION = 0

def generate_header_bytes(model_count,texture_count,material_count):
    f_bytes = bytearray(FILE_HEADER_MAGIC,"utf-8")
    f_bytes.append(VERSION)

    model_count_bytes = model_count.to_bytes(4,byteorder="little")
    texture_count_bytes = texture_count.to_bytes(4,byteorder="little")
    material_count_bytes = material_count.to_bytes(4,byteorder="little")

    f_bytes += (model_count_bytes + texture_count_bytes + material_count_bytes)

    return f_bytes

def generate_chunk_bytes(data,chunk_id,chunk_type):
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data

    chunk_bytes = bytearray()

    length = len(data)
    
    length_bytes = length.to_bytes(4,byteorder="little")
    chunk_id_bytes = chunk_id.to_bytes(4,byteorder="little")
    chunk_type_bytes = chunk_type.to_bytes(1,byteorder="little")

    chunk_bytes += (length_bytes + chunk_id_bytes + chunk_type_bytes + data)

    return chunk_bytes

def get_obj_file_data(export_selection):
    # Existing mesh exports write straight to a file
    with tempfile.NamedTemporaryFile(suffix=".obj", delete = False) as temp_file:
        temp_file_path = temp_file.name

    bpy.ops.wm.obj_export(
        filepath = temp_file_path,
        export_selected_objects = export_selection,
        export_materials = False,
        export_pbr_extensions = False
        )
    
    with open(temp_file_path, "rb") as f:
        obj_file_data = f.read()

    os.remove(temp_file_path)

    return obj_file_data

def get_number_of_models(objects):
    models = 0

    for obj in objects:
        if obj.type == "MESH":
            models+=1
    return models

def get_number_of_materials(objects):
    unique_materials = set()

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                if slot.material:
                    unique_materials.add(slot.material)

    return len(unique_materials)

def get_number_of_textures(objects):
    unique_textures = set()

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                material = slot.material
                if material.use_nodes:
                    for node in material.node_tree.nodes:
                        if node.bl_idname == "ShaderNodeTexImage":
                            unique_textures.add(node)
    return len(unique_textures)

def get_materials(objects):
    for obj in objects:
        for material_slot in obj.material_slots:
            material = material_slot.material
            #print(material.node_tree.nodes)
    return

def get_textures(objects):
    unique_textures = set()

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                material = slot.material
                if material.use_nodes:
                    for node in material.node_tree.nodes:
                        if node.bl_idname == "ShaderNodeTexImage":
                            unique_textures.add(node)
    return unique_textures

def adf_write(path,export_selection):

    if export_selection:
        objects = bpy.context.selected_objects
    else:
        objects = bpy.context.scene.objects

    textures = get_textures(objects)

    number_of_models = get_number_of_models(objects)
    number_of_textures = len(textures)
    number_of_materials = get_number_of_materials(objects)

    obj_file_data = get_obj_file_data(export_selection)
    model_chunk_bytes = generate_chunk_bytes(obj_file_data,0,adf_types.ChunkType.MODEL_OBJ)

    # For every Material
    # Create file chunk and append to file

    # Factor this out into function
    for texture in textures:
        image = texture.image
        format = image.file_format
        with tempfile.NamedTemporaryFile(suffix=".file", delete = False) as temp_file:
            temp_file_path = temp_file.name
            image.save(temp_file_path)
        with open(temp_file_path, "rb") as f:
            texture_file_data = f.read()
        # Generate chunk from data

        os.remove(temp_file_path)


    with open(path,"wb") as file:
        file.write(generate_header_bytes(number_of_models,number_of_textures,number_of_materials))
        file.write(model_chunk_bytes)
        
def adf_read(path):
    return
 
