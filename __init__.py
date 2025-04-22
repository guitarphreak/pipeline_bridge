bl_info = {
    "name": "Pipeline Bridge",
    "author": "Andres Quiroz",
    "version": (0, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Pipeline Bridge",
    "description": "Import, process, and export Mixamo assets to Unreal",
    "category": "Import-Export"
}

import bpy

def register():
    from pipeline_bridge import logging, operators, panels
    from pipeline_bridge.dev_tools.dev_mode_toggle import PipelineBridgePreferences
    bpy.utils.register_class(PipelineBridgePreferences)
    panels.register()
    operators.register()
    logging.register() 

def unregister():
    from pipeline_bridge import logging, operators, panels
    from pipeline_bridge.dev_tools.dev_mode_toggle import PipelineBridgePreferences
    bpy.utils.unregister_class(PipelineBridgePreferences)
    logging.unregister()
    operators.unregister()
    panels.unregister()

if __name__ == "__main__":
    print ("Starting Addon")
    register()
