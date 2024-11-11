

file_header = "ADF "
version = 0

def header_bytes(models=0,textures=0,materials=0):
    f_bytes = bytearray(file_header,"utf-8")
    f_bytes.append(version)

    models_4_bytes = models.to_bytes(4,byteorder="little")
    textures_4_bytes = textures.to_bytes(4,byteorder="little")
    materials_4_bytes = materials.to_bytes(4,byteorder="little")

    f_bytes += (models_4_bytes + textures_4_bytes + materials_4_bytes)

    return f_bytes

def chunk_bytes(chunk_id,type,data=None):
    # Calculate chunk length from data
    # Length(4Bytes), ID(4Bytes), Type (1byte), Data
    return

def adf_write(path,models=0,textures=0,materials=0,data=None):

    with open(path,"wb") as file:
        file.write(header_bytes(models,textures,materials))

    # For every model
    # Create file chunk and append to file

    # For every Texture
    # Create file chunk and append to file

    # For every Material
    # Create file chunk and append to file

adf_write("file.adf")