import importlib
import os
import socket
import sys
import threading

import bpy

ADDON_NAME = "pipeline_bridge"

class DevReloadServer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DevReloadServer, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, host="localhost", port=9999):
        if not hasattr(self, "initialized"):
            self.host = host
            self.port = port
            self._socket = None
            self._thread = None
            self._stop_event = threading.Event()
            self._is_running = False

    def reload_addon(self):
        print(f"[{ADDON_NAME}] Reloading from socket...")
        modules_to_reload = [name for name in sys.modules if name.startswith(ADDON_NAME)]
        for mod in modules_to_reload:
            del sys.modules[mod]

        if ADDON_NAME in bpy.context.preferences.addons:
            bpy.ops.preferences.addon_disable(module=ADDON_NAME)

        addon_path = os.path.join(bpy.utils.user_resource('SCRIPTS', path="addons"), ADDON_NAME)
        spec = importlib.util.spec_from_file_location(ADDON_NAME, os.path.join(addon_path, "__init__.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "register"):
            module.register()

        print(f"[{ADDON_NAME}] Reload complete.")

    def _run_server(self):
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind((self.host, self.port))
            self._socket.listen(1)
            self._socket.settimeout(1.0)  # So we can check the stop flag regularly

            print(f"[{ADDON_NAME}] Socket listening on {self.host}:{self.port}...")

            while not self._stop_event.is_set():
                try:
                    conn, addr = self._socket.accept()
                    with conn:
                        print(f"[Server] Connected by {addr}")
                        msg = conn.recv(1024).decode()
                        print(f"[Server] Received: {msg}")
                        if msg == "reload":
                            self.reload_addon()
                            conn.sendall(b"OK")
                except socket.timeout:
                    continue
                except OSError:
                    break

        finally:
            if self._socket:
                self._socket.close()
                self._socket = None
                print(f"[{ADDON_NAME}] Socket closed.")

    def start(self):
        if self._is_running:
            print(f"[{ADDON_NAME}] Server already running.")
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_server, daemon=True)
        self._thread.start()
        self._is_running = True

    def stop(self):
        if not self._is_running:
            return
        print(f"[{ADDON_NAME}] Stopping server...")
        self._stop_event.set()
        # Ping the socket to unblock `accept()` if it's waiting
        try:
            with socket.create_connection((self.host, self.port), timeout=1):
                pass
        except Exception:
            pass
        self._thread.join()
        self._is_running = False
        print(f"[{ADDON_NAME}] Server stopped.")

    def restart(self):
        self.stop()
        self.start()
