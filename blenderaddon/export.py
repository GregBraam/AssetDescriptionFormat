
import bpy
from . import adf_utils

class ExportADFOperator(bpy.types.Operator):
    bl_idname = "export_mesh.adf"
    bl_label = "Export ADF"
    def execute(self, context):
        # get meshes, materials, textures
        # use fbx export to get models
        # export ADF file

        adf_utils.adf_write("file.adf")
        return {"FINISHED"}

