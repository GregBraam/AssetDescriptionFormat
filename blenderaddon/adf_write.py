import bpy # type: ignore[import-untyped]
import tempfile, os
from .adf_types import ChunkType,ImageFormat
from .id_counter import IDCounter
from .adf_utils import FILE_HEADER_MAGIC, VERSION
from .serialize_utils import serialize_all_material_links,serialize_all_material_nodes
from .adf_errors import MissingImageData

import string
import json

def adf_write(path: str,export_selection: bool,texture_quality: int,texture_format):
    counter = IDCounter(1)

    objects = __get_objects_selection(export_selection)
    header_bytes = __create_header_bytes(objects)
    model_chunk_bytes = __create_model_chunk_bytes(export_selection, counter)

    textures = __get_textures(objects)
    try:
        texture_chunks_bytes = __generate_all_texture_bytes(textures, texture_quality, texture_format, counter)
    except MissingImageData as error:
        raise error
    
    if (__get_number_of_textures(objects) >= 1) and (__get_number_of_materials(objects) >= 1):
        materials = __get_materials(objects)
        mat_nodes = bytearray(serialize_all_material_nodes(materials),"utf-8")
        mat_links = bytearray(serialize_all_material_links(materials),"utf-8")
        nodes_chunk_bytes = __generate_chunk_bytes(mat_nodes,counter.next_id(),ChunkType.MATERIALS_NODES_JSON)
        links_chunk_bytes = __generate_chunk_bytes(mat_links,counter.next_id(),ChunkType.MATERIALS_LINKS_JSON)

        texture_names_bytes = bytearray(__get_texture_names(textures),"utf-8")
        texture_names_chunk_bytes = __generate_chunk_bytes(texture_names_bytes,counter.next_id(),ChunkType.MATERIALS_TEXTURES_JSON)

    with open(path,"wb") as file:
        file.write(header_bytes)
        file.write(model_chunk_bytes)
        if (__get_number_of_textures(objects) >= 1) and (__get_number_of_materials(objects) >= 1):
            file.write(texture_chunks_bytes)

            file.write(nodes_chunk_bytes)
            file.write(links_chunk_bytes)
            file.write(texture_names_chunk_bytes)

def __create_header_bytes(objects: list[bpy.types.Object]) -> bytes:
    number_of_models = __get_number_of_models(objects)
    number_of_textures = __get_number_of_textures(objects)
    number_of_materials = __get_number_of_materials(objects)
    header_bytes = __generate_header_bytes(number_of_models,number_of_textures,number_of_materials)
    return header_bytes

def __create_model_chunk_bytes(export_selection: bool, counter: IDCounter) -> bytes:
    obj_file_data = __get_obj_file_data(export_selection)
    model_chunk_bytes = __generate_chunk_bytes(obj_file_data,counter.next_id(),ChunkType.MODEL_OBJ)
    return model_chunk_bytes

def __get_objects_selection(export_selection: bool) -> list[bpy.types.Object]:
    if export_selection:
        return bpy.context.selected_objects
    else:
        return bpy.context.scene.objects    

#region header data collection

def __get_number_of_models(objects: list[bpy.types.Object]) -> int:
    """Number of objects selected."""
    models = 0

    for obj in objects:
        if obj.type == "MESH":
            models+=1
    return models

def __get_textures(objects: list[bpy.types.Object]) -> list[bpy.types.Node]:
    """Returns collection of unique texture nodes in materials of objects."""
    unique_textures: list[bpy.types.Node] = []

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                material = slot.material
                if material.use_nodes:
                    for node in material.node_tree.nodes:
                        if node.bl_idname == "ShaderNodeTexImage":
                            unique_textures.append(node)
    return unique_textures

def __get_number_of_textures(objects: list[bpy.types.Object]) -> int:
    """Returns total number of unique texture nodes in materials of objects."""
    unique_textures = __get_textures(objects)
    return len(unique_textures)

def __get_materials(objects: list[bpy.types.Object]) -> list[bpy.types.Material]:
    """Returns collection of unique materials of objects."""
    unique_materials: bpy.types.Material = []

    for obj in objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                if slot.material:
                    unique_materials.append(slot.material)

    return unique_materials

def __get_number_of_materials(objects: list[bpy.types.Object]) -> int:
    """Returns total number of unique materials of objects."""
    unique_materials = __get_materials(objects)
    return len(unique_materials)

#endregion

#region collecting data

def __get_obj_file_data(export_selection: bool) -> bytes:
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

def __get_texture_data(texture: bpy.types.Texture,quality: int,export_format) -> tuple[bytes,int]:
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

def __get_texture_names(textures: list[bpy.types.Texture]) -> str:
    """Returns the bytes of the json representation of every textures name."""
    # for every texture
    # add to a list
    # then json dump

    texture_names: list[str] = []

    for tex in textures:
        texture_names.append(tex.image.name)
        #print(tex.image.file_format)
        #TODO: add file extension to texture name.

    json_string: str = json.dumps(texture_names,indent=4)
    return json_string

#endregion 

#region creating chunks

def __generate_chunk_bytes(data: bytes,chunk_id: int,chunk_type: int) -> bytes:
    """Create bytes of generic chunk."""
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data
    chunk_bytes = bytearray()

    length = len(data)
    
    length_bytes = length.to_bytes(4,byteorder="little")
    chunk_id_bytes = chunk_id.to_bytes(4,byteorder="little")
    chunk_type_bytes = chunk_type.to_bytes(1,byteorder="little")

    chunk_bytes += (length_bytes + chunk_id_bytes + chunk_type_bytes + data)

    return bytes(chunk_bytes)

def __generate_header_bytes(model_count: int,texture_count: int,material_count: int) -> bytes:
    """Create bytes of the header chunk."""
    f_bytes = bytearray(FILE_HEADER_MAGIC,"utf-8")
    f_bytes.append(VERSION)

    model_count_bytes = model_count.to_bytes(4,byteorder="little")
    texture_count_bytes = texture_count.to_bytes(4,byteorder="little")
    material_count_bytes = material_count.to_bytes(4,byteorder="little")

    f_bytes += (model_count_bytes + texture_count_bytes + material_count_bytes)

    return bytes(f_bytes)

def __generate_all_texture_bytes(textures: list[bpy.types.Image], texture_quality: int, texture_format: str, counter: IDCounter) -> bytes:
    """Generates a list of texture chunks, for every texture"""
    texture_chunks_bytes = bytearray()
    for texture in textures:
        try:
            texture_data, chunk_type = __get_texture_data(texture,texture_quality,texture_format)
        except MissingImageData as error:
            raise error

        texture_chunks_bytes += __generate_chunk_bytes(texture_data,counter.next_id(),chunk_type)

    return bytes(texture_chunks_bytes)

def __get_image_chunk_type(image: bpy.types.Image) -> int:
    """Convert from blenders image format string, to an ImageFormat enum"""
    # TODO: Error when image.format is not set
    chunk_type = ImageFormat[image.file_format]
    return chunk_type

#endregion

def change_image_file_format(image: bpy.types.Image,export_format: str) -> str:
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
