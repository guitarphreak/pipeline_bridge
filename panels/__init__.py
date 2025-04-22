from pipeline_bridge.panels import ui_log_console, ui_panel

def register():
    ui_panel.register()
    ui_log_console.register()

def unregister():
    ui_log_console.unregister()
    ui_panel.unregister()