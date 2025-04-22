import bpy

from pipeline_bridge.utils.logging_utils import log

class PIPELINE_OT_ImportMixamo(bpy.types.Operator):
    bl_idname = "pipeline.import_mixamo"
    bl_label = "Import Mixamo FBX"
    bl_description = "Import and prepare a Mixamo asset"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH") # type: ignore

    def execute(self, context):
        # Save current selection
        before = set(bpy.data.objects)

        # Import FBX
        bpy.ops.import_scene.fbx(filepath=self.filepath)

        # Detect new objects
        after = set(bpy.data.objects)
        new_objects = after - before

        # Select new objects
        for obj in new_objects:
            obj.select_set(True)
            obj["pipeline_tag"] = "mixamo_import"  # Add a custom tag

        level='INFO'
        message=f"Imported {len(new_objects)} object(s) from Mixamo."
        log(message, level)
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

registered_classes = [PIPELINE_OT_ImportMixamo]

def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls)
