import bpy

class PIPELINE_PT_MainPanel(bpy.types.Panel):
    bl_label = "Pipeline Bridge"
    bl_idname = "PIPELINE_PT_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pipeline Bridge'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Import Tools")
        layout.operator("pipeline.import_mixamo", icon='IMPORT')
        
        layout.label(text="Validation")
        layout.operator("pipeline.validate_asset", icon='CHECKMARK')
        
        layout.label(text="Export Tools")
        layout.operator("pipeline.export_ue", icon='EXPORT')

registered_classes = [PIPELINE_PT_MainPanel]

def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls)
