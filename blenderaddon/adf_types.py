from enum import IntEnum

class ChunkType(IntEnum):
    MODEL_OBJ = 0
    MODEL_FBX = 1
    TEXTURE_PNG = 16
    TEXTURE_JPG = 17
    MATERIALS_JSON = 32
    OBJECTS_JSON = 48