
import bpy
from . import adf_export, adf_import

def add_import_menu(self,context):
    self.layout.operator(adf_import.ImportADFOperator.bl_idname, text = "ADF (.adf)")

def add_export_menu(self,context):
    self.layout.operator(adf_export.ExportADFOperator.bl_idname, text = "ADF (.adf)")

def register():
    bpy.utils.register_class(adf_export.ExportADFOperator)
    bpy.utils.register_class(adf_import.ImportADFOperator)

    bpy.types.TOPBAR_MT_file_import.append(add_import_menu)
    bpy.types.TOPBAR_MT_file_export.append(add_export_menu)

def unregister():
    bpy.utils.unregister_class(adf_export.ExportADFOperator)
    bpy.utils.unregister_class(adf_import.ImportADFOperator)

    bpy.types.TOPBAR_MT_file_import.remove(add_import_menu)
    bpy.types.TOPBAR_MT_file_export.remove(add_export_menu)
