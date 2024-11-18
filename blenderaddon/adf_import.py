
import bpy
from . import adf_utils

class ImportADFOperator(bpy.types.Operator):
    bl_idname = "import_mesh.adf"
    bl_label = "Import ADF"

    def execute(self,context):
        # Import options

        # ADF utils read
        
        return {"FINISHED"}