
import tempfile
import os
import bpy

FILE_HEADER = "ADF "
VERSION = 0

def header_bytes(model_count=0,texture_count=0,material_count=0):
    f_bytes = bytearray(FILE_HEADER,"utf-8")
    f_bytes.append(VERSION)

    model_count_bytes = model_count.to_bytes(4,byteorder="little")
    texture_count_bytes = texture_count.to_bytes(4,byteorder="little")
    material_count_bytes = material_count.to_bytes(4,byteorder="little")

    f_bytes += (model_count_bytes + texture_count_bytes + material_count_bytes)

    return f_bytes

def chunk_bytes(data,chunk_id,chunk_type):
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data

    chunk_bytes = bytearray()

    length = len(data)
    
    length_bytes = length.to_bytes(4,byteorder="little")
    chunk_id_bytes = chunk_id.to_bytes(4,byteorder="little")
    chunk_type_bytes = chunk_type.to_bytes(1,byteorder="little")

    chunk_bytes += (length_bytes + chunk_id_bytes + chunk_type_bytes + data)

    return chunk_bytes

def adf_write(path,models=0,textures=0,materials=0,data=None):

    # For models
    # Create file chunk and append to file
    obj = get_meshes()
    model_chunk_bytes = chunk_bytes(obj,0,0)
    # For every Texture
    # Create file chunk and append to file

    # For every Material
    # Create file chunk and append to file
    
    with open(path,"wb") as file:
        file.write(header_bytes(models,textures,materials))
        file.write(model_chunk_bytes)
        

def get_meshes():
    # Existing mesh exports write straight to a file
    with tempfile.NamedTemporaryFile(suffix=".obj", delete = False) as temp_file:
        temp_file_path = temp_file.name

    bpy.ops.wm.obj_export(
        filepath = temp_file_path,
        export_selected_objects = True,
        export_materials = False,
        export_pbr_extensions = False
        )
    
    with open(temp_file_path, "rb") as f:
        obj_data = f.read()

    os.remove(temp_file_path)

    return obj_data