from pipeline_bridge.logging import log_model, log_operators

def register():
    log_model.register()
    log_operators.register()

def unregister():
    log_operators.unregister()
    log_model.unregister()
