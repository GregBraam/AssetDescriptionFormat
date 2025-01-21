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
    
    #Collect all chunks
    all_chunks = __get_all_data_chunks_from_data(data,header_data)
    
    #Organize chunks, then instantaite them.
    return

def __get_all_data_chunks_from_data(data: bytes,header: HeaderData) -> list[GenericChunkData]:
    chunks_collection: list[GenericChunkData] = []

    # number of chunks is models (always 1) + textures (variable) + mat links(1) + mat nodes(1) + tex names (1)
    total_chunks_count = header.textures + 4

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
    model_chunk = None
    texture_chunks: list[GenericChunkData] = []
    for c in chunks:
        if (c.chunk_type >= ChunkType.MODEL_OBJ) and (c.chunk_type <= ChunkType.MODEL_FBX):
            model_chunk = c
        elif (c.chunk_type >= ChunkType.TEXTURE_PNG) and (c.chunk_type <= ChunkType.TEXTURE_IRIS):
            texture_chunks.append(c)
        #repeat for nodes, links, tex names

def __instantiate_images(texture_data_collection: list[bytes]):
    for tex in texture_data_collection:
        print(tex)

def __instantiate_image(texture_data: bytes):
    with tempfile.NamedTemporaryFile(suffix=".file", delete=False) as temp_file:
        temp_file_path = temp_file.name

    with open(temp_file_path,"wb") as f:
        f.write(texture_data)

    bpy.ops.image.open(filepath=temp_file_path)

    return
