import bpy
import json
from .adf_write import __get_materials
from . import serialize_utils

class SerializeMaterialOperator(bpy.types.Operator):
    bl_idname = "experiment.serialize_material"
    bl_label = "Serialize Material"
    def execute(self,context):
        selection = bpy.context.selected_objects
        materials = __get_materials(selection)

        serialized_nodes = serialize_utils.serialize_all_material_nodes(materials)
        serialized_links = serialize_utils.serialize_all_material_links(materials)

        print(f"\nMaterial links:{serialized_links}")
        print(f"\nMaterial nodes:{serialized_nodes}")

        return {"FINISHED"}
