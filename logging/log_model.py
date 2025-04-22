import bpy

class PipelineLogEntry(bpy.types.PropertyGroup):
    level: bpy.props.EnumProperty( # type: ignore
        name="Level",
        items=[
            ('INFO', "Info", ""),
            ('WARNING', "Warning", ""),
            ('ERROR', "Error", "")
        ],
        default='INFO'
    )
    message: bpy.props.StringProperty(name="Message") # type: ignore
    timestamp: bpy.props.StringProperty(name="Timestamp") # type: ignore

def register():
    bpy.utils.register_class(PipelineLogEntry)
    bpy.types.Scene.pipeline_logs = bpy.props.CollectionProperty(type=PipelineLogEntry)
    bpy.types.Scene.pipeline_logs_index = bpy.props.IntProperty()

def unregister():
    del bpy.types.Scene.pipeline_logs
    bpy.utils.unregister_class(PipelineLogEntry)