from typing import NamedTuple

class GenericChunkData(NamedTuple):
    chunk_length: int
    chunk_identifier: int
    chunk_type: int
    chunk_data: bytes
    