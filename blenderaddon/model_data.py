from typing import NamedTuple

class ModelData(NamedTuple):
    chunk_length: int
    chunk_identifier: int
    chunk_type: int
    chunk_data: bytes