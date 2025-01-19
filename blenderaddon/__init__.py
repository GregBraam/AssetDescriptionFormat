
import bpy # type: ignore[import-untyped]
from .adf_export import ExportADFOperator
from .adf_import import ImportADFOperator
from .experiment_operators import SerializeMaterialOperator
from .adf_log import ADFLogOperator

def add_import_menu(self,context):
    self.layout.operator(ImportADFOperator.bl_idname, text = "ADF (.adf)")

def add_export_menu(self,context):
    self.layout.operator(ExportADFOperator.bl_idname, text = "ADF (.adf)")

classes = (
    ExportADFOperator,
    ImportADFOperator,
    SerializeMaterialOperator,
    ADFLogOperator
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(add_import_menu)
    bpy.types.TOPBAR_MT_file_export.append(add_export_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_file_import.remove(add_import_menu)
    bpy.types.TOPBAR_MT_file_export.remove(add_export_menu)
