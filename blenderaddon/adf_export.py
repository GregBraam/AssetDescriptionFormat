

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
        description = "Include materials and textures in export.",
        default=True
    ) # type: ignore

    export_selection: bpy.props.BoolProperty(
        name = "Export Selection",
        description = "Export only selected objects.",
        default=True
    ) # type: ignore

    texture_format: bpy.props.EnumProperty(
        items = [
            ("PNG", "PNG", "Save all textures as PNG."),
            ("JPEG", "JPEG", "Save all textures as JPEG."),
            ("KEEP", "Keep", "Keep texture format for all textures.")],
        name = "Texture Format",
        description = "Format to save all textures as."
    ) # type: ignore

    texture_quality: bpy.props.IntProperty(
        name = "Texture Quality",
        description = "Texture quality for JPEG formats. 100 is highest quality, 0 is lowest quality.",
        subtype = "PERCENTAGE",
        default = 90,
        min = 0,
        max = 100
    ) # type: ignore

    def execute(self, context):
        # implemented by ExportHelper
        path = self.filepath

        quality = self.texture_quality

        adf_utils.adf_write(path,self.export_selection,quality)
        return {"FINISHED"}

