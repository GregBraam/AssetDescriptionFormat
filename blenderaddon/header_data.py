from typing import NamedTuple

class HeaderData(NamedTuple):
    magic: str
    version: int
    models: int
    textures: int
    materials: int