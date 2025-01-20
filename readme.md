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
| Material | 32 | Material nodes JSON chunk |
|  | 33 | Material links JSON chunk |
|  | 34-47 | Unused |
| Objects | 48 | Object JSON representation chunk type |
|  | 49-255 | Unused |

## Material JSON

There are 2 parts to the representation of a material. The nodes that make up the material, and the links between the nodes of a material. The nodes and the links are stored in seperate chunks.

### Example of material nodes JSON
```json
[
    {
        "SimpleTex": [
            {
                "name": "Material Output",
                "type": "OUTPUT_MATERIAL"
            },
            {
                "name": "Principled BSDF",
                "type": "BSDF_PRINCIPLED"
            },
            {
                "name": "Image Texture",
                "type": "TEX_IMAGE"
            }
        ]
    },
    {
        "SimpleMat": [
            {
                "name": "Principled BSDF",
                "type": "BSDF_PRINCIPLED"
            },
            {
                "name": "Material Output",
                "type": "OUTPUT_MATERIAL"
            }
        ]
    }
]
```

### Example of material links JSON
```json
[
    {
        "SimpleTex": [
            {
                "from_node": "Principled BSDF",
                "from_socket": "BSDF",
                "to_node": "Material Output",
                "to_socket": "Surface"
            },
            {
                "from_node": "Image Texture",
                "from_socket": "Color",
                "to_node": "Principled BSDF",
                "to_socket": "Base Color"
            }
        ]
    },
    {
        "SimpleMat": [
            {
                "from_node": "Principled BSDF",
                "from_socket": "BSDF",
                "to_node": "Material Output",
                "to_socket": "Surface"
            }
        ]
    }
]
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