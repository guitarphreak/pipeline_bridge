import subprocess
import os
import time
import argparse
import sys

# Absolute path to Blender executable
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.4\blender.exe"

# Convert to absolute path of the watcher script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WATCHER_SCRIPT = os.path.abspath(os.path.join(CURRENT_DIR, ".", "dev_watch.py"))

parser = argparse.ArgumentParser()
parser.add_argument("--blend", type=str, help="Optional .blend file to load")
args = parser.parse_args()

# Build the Blender launch command
blender_cmd = [BLENDER_PATH]
if args.blend:
    blender_cmd.append(args.blend)

# Launch Blender
print("Launching Blender...")
blender_proc = subprocess.Popen(blender_cmd)

# Optional: Give Blender some time to initialize
time.sleep(5)

# Launch the watcher
print("Starting reload watcher...")
watcher_proc = subprocess.Popen([sys.executable, WATCHER_SCRIPT], cwd=CURRENT_DIR)

blender_proc.wait()

print ("Blender closed. Terminating watcher...")
watcher_proc.terminate()