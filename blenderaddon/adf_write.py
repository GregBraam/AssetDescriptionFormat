import tempfile, os, bpy
from .adf_types import ChunkType,ImageFormat
from .id_counter import IDCounter
from .adf_utils import FILE_HEADER_MAGIC, VERSION

def adf_write(path,export_selection,texture_quality,texture_format):
    counter = IDCounter(1)

    if export_selection:
        objects = bpy.context.selected_objects
    else:
        objects = bpy.context.scene.objects

    number_of_models = get_number_of_models(objects)
    number_of_textures = get_number_of_textures(objects)
    number_of_materials = get_number_of_materials(objects)
    header_bytes = generate_header_bytes(number_of_models,number_of_textures,number_of_materials)

    obj_file_data = get_obj_file_data(export_selection)
    model_chunk_bytes = generate_chunk_bytes(obj_file_data,counter.next_id(),ChunkType.MODEL_OBJ)

    textures = get_textures(objects)
    texture_chunks_bytes = generate_all_texture_bytes(textures, texture_quality, texture_format, counter)

    with open(path,"wb") as file:
        file.write(header_bytes)
        file.write(model_chunk_bytes)
        for tex_bytes in texture_chunks_bytes:
            file.write(tex_bytes)

#region header data collection

def get_number_of_models(objects):
    models = 0

    for obj in objects:
        if obj.type == "MESH":
            models+=1
    return models

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

def get_number_of_textures(objects):
    unique_textures = get_textures(objects)
    return len(unique_textures)

def get_materials(objects):
    unique_materials = set()

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                if slot.material:
                    unique_materials.add(slot.material)

    return unique_materials

def get_number_of_materials(objects):
    unique_materials = get_materials(objects)
    return len(unique_materials)

#endregion

#region collecting data

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

def get_texture_data(texture,quality,export_format):
    image = texture.image
    image = change_image_file_format(image,export_format)
    chunk_type = get_image_chunk_type(image)
    
    with tempfile.NamedTemporaryFile(suffix=".file", delete = False) as temp_file:
        temp_file_path = temp_file.name
        image.save(filepath=temp_file_path,quality=quality)
    with open(temp_file_path, "rb") as f:
        texture_file_data = f.read()

    os.remove(temp_file_path)

    return texture_file_data, chunk_type

#endregion 

#region creating chunks

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

def generate_header_bytes(model_count,texture_count,material_count):
    f_bytes = bytearray(FILE_HEADER_MAGIC,"utf-8")
    f_bytes.append(VERSION)

    model_count_bytes = model_count.to_bytes(4,byteorder="little")
    texture_count_bytes = texture_count.to_bytes(4,byteorder="little")
    material_count_bytes = material_count.to_bytes(4,byteorder="little")

    f_bytes += (model_count_bytes + texture_count_bytes + material_count_bytes)

    return f_bytes

def generate_all_texture_bytes(textures, texture_quality, texture_format, counter):
    texture_chunks_bytes = []
    for texture in textures:
        texture_data, chunk_type = get_texture_data(texture,texture_quality,texture_format)
        texture_chunks_bytes.append(generate_chunk_bytes(texture_data,counter.next_id(),chunk_type))

    return texture_chunks_bytes

def get_image_chunk_type(image):
    # TODO: Error when image.format is not set
    chunk_type = ImageFormat[image.file_format]
    return chunk_type

#endregion

def change_image_file_format(image,export_format):
    if export_format == "KEEP":
        return image
    export_format_type = ImageFormat[export_format]
    match export_format_type:
        case ImageFormat.PNG:
            image.file_format = "PNG"
        case ImageFormat.JPEG:
            image.file_format = "JPEG"
        case ImageFormat.JPEG2000:
            image.file_format = "JPEG2000"
        case ImageFormat.TARGA:
            image.file_format = "TARGA"
        case ImageFormat.TARGA_RAW:
            image.file_format = "TARGA_RAW"
        case ImageFormat.BMP:
            image.file_format = "BMP"
        case ImageFormat.IRIS:
            image.file_format = "IRIS"
        case _:
            image.file_format = "PNG"

    return image
