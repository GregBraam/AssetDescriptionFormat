import tempfile, os, bpy
from .adf_types import ChunkType,ImageFormat
from .id_counter import IDCounter
from .adf_utils import FILE_HEADER_MAGIC, VERSION
from .serialize_utils import serialize_all_material_links,serialize_all_material_nodes
from .adf_errors import MissingImageData

def adf_write(path,export_selection,texture_quality,texture_format):
    counter = IDCounter(1)

    if export_selection:
        objects = bpy.context.selected_objects
    else:
        objects = bpy.context.scene.objects

    number_of_models = __get_number_of_models(objects)
    number_of_textures = __get_number_of_textures(objects)
    number_of_materials = __get_number_of_materials(objects)
    header_bytes = __generate_header_bytes(number_of_models,number_of_textures,number_of_materials)

    obj_file_data = __get_obj_file_data(export_selection)
    model_chunk_bytes = __generate_chunk_bytes(obj_file_data,counter.next_id(),ChunkType.MODEL_OBJ)

    textures = __get_textures(objects)
    try:
        texture_chunks_bytes = __generate_all_texture_bytes(textures, texture_quality, texture_format, counter)
    except MissingImageData as error:
        raise error

    materials = __get_materials(objects)
    mat_nodes = bytearray(serialize_all_material_nodes(materials),"utf-8")
    mat_links = bytearray(serialize_all_material_links(materials),"utf-8")
    nodes_chunk_bytes = __generate_chunk_bytes(mat_nodes,counter.next_id(),ChunkType.MATERIALS_NODES_JSON)
    links_chunk_bytes = __generate_chunk_bytes(mat_links,counter.next_id(),ChunkType.MATERIALS_LINKS_JSON)

    with open(path,"wb") as file:
        file.write(header_bytes)
        file.write(model_chunk_bytes)
        for tex_bytes in texture_chunks_bytes:
            file.write(tex_bytes)

        file.write(nodes_chunk_bytes)
        file.write(links_chunk_bytes)

#region header data collection

def __get_number_of_models(objects):
    """Number of objects selected."""
    models = 0

    for obj in objects:
        if obj.type == "MESH":
            models+=1
    return models

def __get_textures(objects):
    """Returns collection of unique texture nodes in materials of objects."""
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

def __get_number_of_textures(objects):
    """Returns total number of unique texture nodes in materials of objects."""
    unique_textures = __get_textures(objects)
    return len(unique_textures)

def __get_materials(objects):
    """Returns collection of unique materials of objects."""
    unique_materials = set()

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                if slot.material:
                    unique_materials.add(slot.material)

    return unique_materials

def __get_number_of_materials(objects):
    """Returns total number of unique materials of objects."""
    unique_materials = __get_materials(objects)
    return len(unique_materials)

#endregion

#region collecting data

def __get_obj_file_data(export_selection):
    """Returns the bytes of an obj file export without saving the obj seperately."""
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

def __get_texture_data(texture,quality,export_format):
    """Returns bytes of image save without saving as external file, and returns chunk type."""
    image = texture.image
    if not image.has_data:
        raise MissingImageData(image.name)
    
    image = change_image_file_format(image,export_format)
    chunk_type = __get_image_chunk_type(image)
    
    with tempfile.NamedTemporaryFile(suffix=".file", delete = False) as temp_file:
        temp_file_path = temp_file.name
        image.save(filepath=temp_file_path,quality=quality)
    with open(temp_file_path, "rb") as f:
        texture_file_data = f.read()

    os.remove(temp_file_path)

    return texture_file_data, chunk_type

#endregion 

#region creating chunks

def __generate_chunk_bytes(data,chunk_id,chunk_type):
    """Create bytes of generic chunk."""
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data
    chunk_bytes = bytearray()

    length = len(data)
    
    length_bytes = length.to_bytes(4,byteorder="little")
    chunk_id_bytes = chunk_id.to_bytes(4,byteorder="little")
    chunk_type_bytes = chunk_type.to_bytes(1,byteorder="little")

    chunk_bytes += (length_bytes + chunk_id_bytes + chunk_type_bytes + data)

    return chunk_bytes

def __generate_header_bytes(model_count,texture_count,material_count):
    """Create bytes of the header chunk."""
    f_bytes = bytearray(FILE_HEADER_MAGIC,"utf-8")
    f_bytes.append(VERSION)

    model_count_bytes = model_count.to_bytes(4,byteorder="little")
    texture_count_bytes = texture_count.to_bytes(4,byteorder="little")
    material_count_bytes = material_count.to_bytes(4,byteorder="little")

    f_bytes += (model_count_bytes + texture_count_bytes + material_count_bytes)

    return f_bytes

def __generate_all_texture_bytes(textures, texture_quality, texture_format, counter):
    """Generates a list of texture chunks, for every texture"""
    texture_chunks_bytes = []
    for texture in textures:
        try:
            texture_data, chunk_type = __get_texture_data(texture,texture_quality,texture_format)
        except MissingImageData as error:
            raise error

        texture_chunks_bytes.append(__generate_chunk_bytes(texture_data,counter.next_id(),chunk_type))

    return texture_chunks_bytes

def __get_image_chunk_type(image):
    """Convert from blenders image format string, to an ImageFormat enum"""
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
