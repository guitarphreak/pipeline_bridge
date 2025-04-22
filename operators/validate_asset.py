import bpy

class PIPELINE_OT_ValidateAsset(bpy.types.Operator):
    bl_idname = "pipeline.validate_asset"
    bl_label = "Validate Mixamo Asset"
    bl_description = "Validate a Mixamo FBX and prepare it for Unreal"

    def execute(self, context):
        self.report({'INFO'}, "Validate Mixamo placeholder")
        return {'FINISHED'}

registered_classes = [PIPELINE_OT_ValidateAsset]

def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls)
