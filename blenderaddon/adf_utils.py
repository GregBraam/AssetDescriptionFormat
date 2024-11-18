
import tempfile
import os
import bpy

file_header = "ADF "
version = 0

def header_bytes(models=0,textures=0,materials=0):
    f_bytes = bytearray(file_header,"utf-8")
    f_bytes.append(version)

    models_4_bytes = models.to_bytes(4,byteorder="little")
    textures_4_bytes = textures.to_bytes(4,byteorder="little")
    materials_4_bytes = materials.to_bytes(4,byteorder="little")

    f_bytes += (models_4_bytes + textures_4_bytes + materials_4_bytes)

    return f_bytes

def chunk_bytes(chunk_id,type,data=None):
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data
    return

def adf_write(path,models=0,textures=0,materials=0,data=None):

    # For models
    # Create file chunk and append to file
    obj = get_meshes()
    # For every Texture
    # Create file chunk and append to file

    # For every Material
    # Create file chunk and append to file
    
    with open(path,"wb") as file:
        file.write(header_bytes(models,textures,materials))
        file.write(obj)
        

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