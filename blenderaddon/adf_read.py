import bpy # type: ignore[import-untyped]
from . import adf_utils
from .adf_utils import FILE_HEADER_MAGIC
from .header_data import HeaderData
from .generic_chunk_data import GenericChunkData
from .adf_log import log
from .adf_types import ChunkType
import tempfile, os

import string

def adf_read(file_path: str):
    with open(file_path,"rb") as file:
        data = file.read()

    header_data = __get_header_data(data)
    all_chunks = __get_all_data_chunks_from_data(data,header_data)

    model_chunk, texture_chunks, node_chunk, link_chunk, texture_json_chunk = __organize_chunks(all_chunks)

    __instantiate_model_from_chunk(model_chunk)
    __instantiate_images(texture_chunks,texture_json_chunk)

    return

def __get_all_data_chunks_from_data(data: bytes,header: HeaderData) -> list[GenericChunkData]:
    """All chunks except header chunk."""
    chunks_collection: list[GenericChunkData] = []

    # When no textures/materials present, there is only model chunk.
    if (header.textures >= 1) and (header.materials >= 1):
        total_chunks_count = header.textures + 4
    else:
        total_chunks_count = 1

    offset = 17
    for i in range(0,total_chunks_count):
        chunk = __get_chunk_from_data(data,offset)
        chunks_collection.append(chunk)
        offset = offset + len(chunk.chunk_data) + 9

    return chunks_collection

def __get_chunk_from_data(data: bytes, offset: int) -> GenericChunkData:
    c_length = int.from_bytes(data[offset:offset+4],byteorder="little")
    c_id = int.from_bytes(data[offset+4:offset+8],byteorder="little")
    c_type = data[offset+8]
    c_data = data[offset+8:offset+8+c_length]

    chunk = GenericChunkData(c_length,c_id,c_type,c_data)
    return chunk

def __get_header_data(data: bytes) -> HeaderData:
    """Gets the header chunk data from the bytes of an ADF file."""
    magic = data[0:4].decode("utf-8")
    version = data[4]
    models = int.from_bytes(data[5:9],byteorder="little")
    textures = int.from_bytes(data[9:13],byteorder="little")
    materials = int.from_bytes(data[13:17],byteorder="little")

    return HeaderData(magic,version,models,textures,materials)

def __organize_chunks(chunks: list[GenericChunkData]):
    """From all chunks (except header), organize into model, texture, node, etc."""
    model_chunk = None
    texture_chunks: list[GenericChunkData] = []
    node_chunk = None
    link_chunk = None
    texture_json_chunk = None

    for c in chunks:
        c_type = c.chunk_type
        if (c_type >= ChunkType.MODEL_OBJ) and (c_type <= ChunkType.MODEL_FBX):
            model_chunk = c
        elif (c_type >= ChunkType.TEXTURE_PNG) and (c_type <= ChunkType.TEXTURE_IRIS):
            texture_chunks.append(c)
        elif (c_type == ChunkType.MATERIALS_NODES_JSON):
            node_chunk = c
        elif (c_type == ChunkType.MATERIALS_LINKS_JSON):
            link_chunk = c
        elif (c_type == ChunkType.MATERIALS_TEXTURES_JSON):
            texture_json_chunk = c
        else:
            log(f"Organize Chunks: Chunk of type {ChunkType(c_type)} not organized!","ERROR")

    return model_chunk, texture_chunks, node_chunk, link_chunk, texture_json_chunk

def __instantiate_model_from_chunk(model_chunk: GenericChunkData):
    with tempfile.NamedTemporaryFile(suffix=".file", delete=False) as temp_file:
        temp_file_path = temp_file.name

    with open(temp_file_path,"wb") as f:
        f.write(model_chunk.chunk_data)
    
    bpy.ops.wm.obj_import(filepath=temp_file_path)
    return

def __instantiate_images(texture_data_collection: list[GenericChunkData], texture_names: GenericChunkData):

    # Get texture names from json.
    # Set temp file name, name of image in blender is from 

    for i in range(0,len(texture_data_collection)):
        tex_data = texture_data_collection[i]

        __instantiate_image(tex_data.chunk_data)

def __instantiate_image(texture_data: bytes):
    #TODO: change tempfile name to actual name.
    with tempfile.NamedTemporaryFile(suffix=".file", delete=False) as temp_file:
        temp_file_path = temp_file.name

    with open(temp_file_path,"wb") as f:
        f.write(texture_data)

    bpy.ops.image.open(filepath=temp_file_path)

    return
