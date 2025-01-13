from . import adf_utils
from .adf_utils import FILE_HEADER_MAGIC
from .header_data import HeaderData
from .model_data import ModelData

import string

def adf_read(file_path: str):
    with open(file_path,"rb") as file:
        data = file.read()

    header_data = __get_header_data(data)
    model_data = __get_model_data(data)

    # get textures and instantiate images in blender
    # get materials data\
    # instantiate material, instantiate nodes and then connect them with links

    return

def __get_header_data(data: bytes) -> HeaderData:
    """Gets the header chunk data from the bytes of an ADF file."""
    magic = data[0:4].decode("utf-8")
    version = data[4]
    models = int.from_bytes(data[5:9],byteorder="little")
    textures = int.from_bytes(data[9:13],byteorder="little")
    materials = int.from_bytes(data[13:17],byteorder="little")

    return HeaderData(magic,version,models,textures,materials)

def __get_model_data(data: bytes) -> ModelData:
    """Get all model data from the bytes of an ADF file."""
    chunk_length = int.from_bytes(data[17:21],byteorder="little")
    chunk_identifier = int.from_bytes(data[21:25],byteorder="little")
    chunk_type = data[25]
    chunk_data = data[25:25+chunk_length]

    return ModelData(chunk_length,chunk_identifier,chunk_type,chunk_data)

def __get_all_texture_data(data: bytes,header_data: HeaderData):
    """Get all textures from an adf file"""
    
    for i in range(0,header_data.textures):
        return
    # Will need an offset for this
    # For number of textures peform get_texture_data
    return

def __get_texture_data():
    """Get a single texture from adf file"""
    # Will need an offset for this
    return 

def __get_all_material_data():
    """Get all materials"""
    # Will need an offset for this
    return

def __get_material_data():
    """Get a single material"""
    return

def __get_nodes_data():
    """Get the node chunk data."""
    return

def __get_links_data():
    """Get the links chunk data."""
    return
