import os

import bpy

class PIPELINE_OT_ExportUE(bpy.types.Operator):
    bl_idname = "pipeline.export_ue"
    bl_label = "Export Mixamo Asset"
    bl_description = "Export a Mixamo FBX and prepare it for Unreal"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty( # type: ignore
        name="Export Filepath",
        description="Filepath to export the FBX",
        subtype='FILE_PATH',
    )

    def execute(self, context):
        selected = [obj for obj in context.selected_objects if obj.type in {'ARMATURE', 'MESH'}]

        if not selected:
            self.report({'WARNING'}, "No valid objects (Armature or Mesh) selected.")
            return {'CANCELLED'}

        # Ensure the path ends in .fbx
        export_path = self.filepath
        if not export_path.lower().endswith(".fbx"):
            export_path += ".fbx"

        bpy.ops.export_scene.fbx(
            filepath=export_path,
            use_selection=True,
            object_types={'ARMATURE', 'MESH'},
            apply_unit_scale=True,
            global_scale=1.0,
            apply_scale_options='FBX_SCALE_UNITS',
            use_mesh_modifiers=True,
            use_mesh_modifiers_render=True,
            mesh_smooth_type='OFF',
            use_armature_deform_only=True,
            add_leaf_bones=False,
            primary_bone_axis='Y',
            secondary_bone_axis='X',
            bake_anim=True,
            bake_anim_use_all_bones=True,
            bake_anim_use_nla_strips=True,
            bake_anim_use_all_actions=False,
            bake_anim_force_startend_keying=True,
            bake_anim_step=1.0,
            bake_anim_simplify_factor=0.0,
            axis_forward='-Y',
            axis_up='Z',
            armature_nodetype='NULL',
        )

        self.report({'INFO'}, f"Exported to {export_path}")
        return {'FINISHED'}

    def invoke(self, context, event):
        # Default file path suggestion (e.g., from blend file)
        blend_dir = os.path.dirname(bpy.data.filepath)
        self.filepath = os.path.join(blend_dir, "mixamo_export.fbx")
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

registered_classes = [PIPELINE_OT_ExportUE]

def register():
    for cls in registered_classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(registered_classes):
        bpy.utils.unregister_class(cls)
