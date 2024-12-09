import bpy
import json
from .adf_write import get_materials
from . import experiment_utils

class SerializeMaterialOperator(bpy.types.Operator):
    bl_idname = "experiment.serialize_material"
    bl_label = "Serialize Material"
    def execute(self,context):
        selection = bpy.context.selected_objects
        materials = get_materials(selection)

        serialized_nodes = experiment_utils.serialize_all_material_nodes(materials)
        serialized_links = experiment_utils.serialize_all_material_links(materials)

        print(f"\nMaterial links:{serialized_links}")
        print(f"\nMaterial nodes:{serialized_nodes}")

        return {"FINISHED"}
