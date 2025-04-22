import bpy

registered_classes = []

def register_class(cls):
    registered_classes.append(cls)
    return cls

def safe_register(cls):
    if hasattr(cls, "bl_rna"):
        bpy.utils.register_class(cls)

def safe_unregister(cls):
    if hasattr(cls, "bl_rna"):
        bpy.utils.unregister_class(cls)
        registered_classes.pop(cls)
