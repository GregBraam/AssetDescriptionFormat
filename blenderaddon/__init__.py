
import bpy
from . import export

def register():
    bpy.utils.register_class(export.ExportADFOperator)

def unregister():
    bpy.utils.unregister_class(export.ExportADFOperator)
