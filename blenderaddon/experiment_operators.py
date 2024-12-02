import bpy
from .adf_write import get_materials

class SerializeNodesOperator(bpy.types.Operator):
    bl_idname = "experiment.serialize_nodes"
    bl_label = "Serialize Nodes"
    def execute(self,context):
        print("Serialize Nodes")

        selection = bpy.context.selected_objects
        materials = get_materials(selection)

        return {"FINISHED"}
