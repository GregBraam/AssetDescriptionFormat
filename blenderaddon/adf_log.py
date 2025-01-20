import bpy # type: ignore[import-untyped]
import os

def log(message,message_type="INFO"):
    bpy.context.window_manager.popup_menu(
        lambda self, context: self.layout.label(text=message),
        title="Message",
        icon='INFO'
    )
    print(f"{message_type}: {message}")
