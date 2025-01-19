import bpy # type: ignore[import-untyped]
import os

class ADFLogOperator(bpy.types.Operator):
    bl_idname = "adf.log"
    bl_label = "Log"
    bl_options = {"INTERNAL"}

    should_log = False

    message: bpy.props.StringProperty(name="Message",default="") # type: ignore[valid-type]
    message_type: bpy.props.StringProperty(name="Message Type",default="INFO") # type: ignore[valid-type]
    
    def __init__(self):
        self.get_config()

    def execute(self,context):
        if self.should_log:
            self.report({self.message_type},self.message)
        
        return {"FINISHED"}

    def get_config(self):
        config_path = os.path.join(os.path.dirname(__file__), "config")
        if os.path.exists(config_path):
            self.should_log = True
        return






