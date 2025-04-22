from enum import Enum
from datetime import datetime

import bpy

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

def ensure_log_storage():
    return bpy.context.scene.pipeline_logs

def log(message, level=LogLevel.INFO):
    logs = ensure_log_storage()
    log = logs.add()
    log.log_index = len(logs)-1
    log.level = level
    log.message = message
    log.timestamp = datetime.now().strftime("%H:%M:%S")

def clear_logs():
    logs = ensure_log_storage()
    logs.clear()
