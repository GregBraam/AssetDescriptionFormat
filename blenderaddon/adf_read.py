from . import adf_utils
from .adf_utils import FILE_HEADER_MAGIC

def adf_read(file_path):
    with open(file_path,"rb") as file:
        data = file.read()


    __get_header_data(data)
    return

def __get_header_data(data):
    magic = data[0:4].decode("utf-8")
    version = int.from_bytesdata[4]
    return 
