
import bpy
from bpy_extras.io_utils import ImportHelper
from . import adf_utils

class ImportADFOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "import_mesh.adf"
    bl_label = "Import ADF"

    filename_ext = ".adf"
    filter_glob: bpy.props.StringProperty(
        default="*.adf",
        options={"HIDDEN"},
        maxlen=255
    ) # type: ignore

    def execute(self,context):
        # Import options

        # ADF utils read
        
        return {"FINISHED"}