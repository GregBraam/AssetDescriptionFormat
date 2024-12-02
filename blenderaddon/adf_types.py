from enum import IntEnum

class ChunkType(IntEnum):
    MODEL_OBJ = 0
    MODEL_FBX = 1
    TEXTURE_PNG = 16
    TEXTURE_JPEG = 17
    TEXTURE_JPEG2000 = 18
    TEXTURE_TARGA = 19
    TEXTURE_TARGA_RAW = 20
    TEXTURE_BMP = 21
    TEXTURE_IRIS = 22
    MATERIALS_JSON = 32
    OBJECTS_JSON = 48

class ImageFormat(IntEnum):
    PNG = 16
    JPEG = 17
    JPEG2000 = 18
    TARGA = 19
    TARGA_RAW = 20
    BMP = 21
    IRIS = 22
