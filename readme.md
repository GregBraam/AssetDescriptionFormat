# Asset Description Format

## File Header

- **Magic Number** (4 Bytes)
- **Version** (1 Byte)
- **Number of Models** (4 Bytes)
- **Number of Textures** (4 Bytes)
- **Number of Materials** (4 Bytes)

## File chunks

- **Chunk Length** (4 Bytes)
- **Chunk Identifier** (4 Bytes)
- **Chunk Type** (1 Bytes) Model, Texture, Materials reprentation JSON and Objects JSON
- **Chunk Data** 

| Main type| Chunk type ID | Description |
| - | - | - |
| Model | 0 | OBJ models |
|  | 1 | FBX models |
|  | 2-15 | Reserved for model chunk types |
| Texture | 16 | PNG textures |
|  | 17 | JPG textures |
|  | 18-31 | Reserved for texture chunk types |
| Material | 32 | Material JSON representation chunk type |
|  | 33-47| Unused |
| Objects | 48 | Object JSON representation chunk type |
|  | 49-255 | Unused |

## Material JSON

JSON representation of all materials
```json
{
    "materials": [
        {
            "material_name": "material_1",
            "material_id": "0",
            "properties": {
                "base_color": {
                    "value": [1,1,1,0]
                },
                "metallic": {
                    "value": 0.8
                },
                "roughness": {
                    "value": 0.4
                },
                "normal": {
                    "texture": "material_1_normal.png",
                    "chunk_id": 2
                },
                "ambient_occlusion":{
                },
                "specular":{
                },
                "displacement":{
                },
                "emissive":{
                },
                "uv_scale":{
                }
            }
        }
    ]

}
```

## Objects JSON

Used to know what materials to assign to which model/object

```json
{
    "objects": [
        {
            "name": "Model1",
            "material_name": "material_1",
            "material_id": 0
        }
    ]
}
```