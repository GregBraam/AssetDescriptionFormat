
import bpy
from . import adf_utils

class ExportADFOperator(bpy.types.Operator):
    bl_idname = "export_mesh.adf"
    bl_label = "Export ADF"
    def execute(self, context):

        # Need to add export options

        adf_utils.adf_write("file.adf")
        return {"FINISHED"}

