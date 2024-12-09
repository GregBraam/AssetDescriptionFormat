import bpy
from bpy_extras.io_utils import ExportHelper
from .adf_write import adf_write
from .adf_errors import MissingImageData


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
            ("JPEG2000", "JPEG2000", "Save all textures as JPEG2000."),
            ("TARGA", "TARGA", "Save all textures as TARGA."),
            ("TARGA_RAW", "TARGA RAW", "Save all textures as TARGA RAW."),
            ("BMP", "BMP", "Save all textures as BMP."),
            ("IRIS", "IRIS", "Save all textures as IRIS"),
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

    mesh_format: bpy.props.EnumProperty(
        items = [
            ("OBJ","OBJ","Save all meshes as OBJ.")],
        name = "Mesh Format",
        description = "Format to save meshes as."
    ) # type: ignore

    def execute(self, context):
        # implemented by ExportHelper
        path = self.filepath

        export_selection = self.export_selection
        quality = self.texture_quality
        texture_format = self.texture_format
        try:
            adf_write(path,export_selection,quality,texture_format)
        except MissingImageData as error:
            self.report({"WARNING"}, f"Image {error.image_name} is missing data.")
        return {"FINISHED"}

