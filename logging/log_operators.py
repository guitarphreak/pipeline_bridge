from datetime import datetime

import bpy

class PIPELINE_OT_AddTestLog(bpy.types.Operator):
    bl_idname = "pipeline.add_test_log"
    bl_label = "Add Test Log"

    def execute(self, context):
        log = context.scene.pipeline_logs.add()
        log.level = 'INFO'
        log.message = "This is a test log message."
        log.timestamp = datetime.now().strftime("%H:%M:%S")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(PIPELINE_OT_AddTestLog)

def unregister():
    bpy.utils.unregister_class(PIPELINE_OT_AddTestLog)