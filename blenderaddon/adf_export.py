

import bpy
from bpy_extras.io_utils import ExportHelper
from . import adf_utils


class ExportADFOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export_mesh.adf"
    bl_label = "Export ADF"

    # default extension
    filename_ext = ".adf"

    filter_glob: bpy.props.StringProperty(
        default="*.adf",
        options={"HIDDEN"},
        maxlen=255
    ) # type: ignore

    export_materials: bpy.props.BoolProperty(
        name = "Export Materials",
        description = "Include materials and textures in export",
        default=True
    ) # type: ignore

    export_selection: bpy.props.BoolProperty(
        name = "Export Selection",
        description = "Export only selected objects",
        default=True
    ) # type: ignore

    def execute(self, context):

        # implemented by ExportHelper
        path = self.filepath
        # Need to add export options

        adf_utils.adf_write(path)
        return {"FINISHED"}

