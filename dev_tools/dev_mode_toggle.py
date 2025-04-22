import bpy

from pipeline_bridge.dev_tools.socket_server import DevReloadServer
from pipeline_bridge.dev_tools.dev_config import RELOAD_PORT


def update_reload_server(self, context):
    server = DevReloadServer(port=RELOAD_PORT)
    if self.enable_reload_server:
        server.start()
    else:
        server.stop()


class PipelineBridgePreferences(bpy.types.AddonPreferences):
    bl_idname = "pipeline_bridge"

    developer_mode: bpy.props.BoolProperty(  # type: ignore
        name="Enable Developer Mode",
        default=False
    )

    enable_reload_server: bpy.props.BoolProperty(  # type: ignore
        name="Enable Reload Server",
        default=False,
        update=update_reload_server  # Link the toggle behavior
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "developer_mode")
        if self.developer_mode:
            layout.prop(self, "enable_reload_server")
