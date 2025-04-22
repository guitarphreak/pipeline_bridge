import os
import socket
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURABLE ---
ADDON_NAME = "pipeline_bridge"
RELOAD_PORT = 9999  # Default, but can be overridden by env or import
WATCH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# --- PATH SETUP ---
current_file = os.path.abspath(__file__)
dev_tools_dir = os.path.dirname(current_file)            # .../pipeline_bridge/dev_tools
addon_root = os.path.abspath(os.path.join(dev_tools_dir, ".."))  # .../pipeline_bridge
project_root = os.path.abspath(os.path.join(addon_root, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from pipeline_bridge.dev_tools.dev_config import RELOAD_PORT as CONFIG_PORT
    RELOAD_PORT = CONFIG_PORT
except Exception as e:
    print(f"[Warning] Couldn't import dev_config: {e}")

def send_reload():
    try:
        with socket.create_connection(("localhost", RELOAD_PORT), timeout=1) as sock:
            sock.sendall(b"reload")
            print(f"[Watcher] Reload signal sent on port {RELOAD_PORT}.")
    except Exception as e:
        print(f"[Watcher] Could not send reload: {e}")

# --- SOCKET HANDLER ---
class ReloadHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory or not event.src_path.endswith(".py"):
            return
        print(f"[Watcher] Detected change in {event.src_path}. Sending reload...")
        send_reload()

# --- MAIN ---
def main():
    print(f"[Watcher] Watching '{WATCH_PATH}' on port {RELOAD_PORT}...")
    observer = Observer()
    observer.schedule(ReloadHandler(), path=WATCH_PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[Watcher] Shutting down.")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
