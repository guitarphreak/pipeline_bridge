import bpy

from pipeline_bridge.utils.logging_utils import log, clear_logs

class PIPELINE_PT_LogConsole(bpy.types.Panel):
    bl_label = "Pipeline Log Console"
    bl_idname = "PIPELINE_PT_LogConsole"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pipeline Bridge'

    def draw(self, context):
        layout = self.layout
        logs = context.scene.pipeline_logs

        row = layout.row()
        row.operator("pipeline.add_test_log", icon='ADD')
        row.operator("pipeline.clear_logs", icon='TRASH')

        row = layout.row()
        for entry in reversed(logs[-20:]):  # Show last 20 logs max
            layout.template_list("PIPELINE_UL_Log", "", context.scene, "pipeline_logs", context.scene, "pipeline_logs_index")

class PIPELINE_OT_ClearLogs(bpy.types.Operator):
    bl_idname = "pipeline.clear_logs"
    bl_label = "Clear Logs"

    def execute(self, context):
        clear_logs()
        self.report({'INFO'}, "Logs cleared")
        return {'FINISHED'}

class PIPELINE_UL_Log(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_property):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            icon_name = 'INFO' if item.level == 'INFO' else 'ERROR' 
            row.label(text=f"[{item.timestamp}] {item.message}", icon=icon_name)
        
        elif self.layout_type == 'GRID':
            pass

    def draw_filter(self, context, layout):
        return super().draw_filter(context, layout)

registered_classes = [PIPELINE_PT_LogConsole, PIPELINE_OT_ClearLogs, PIPELINE_UL_Log]

def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls)
