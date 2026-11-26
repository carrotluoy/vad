import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import hashlib
import json
from fastapi import FastAPI

from checkout_app import TASK as CHECKOUT_TASK
from drive_app import TASK as DRIVE_TASK
from file_app import TASK as FILE_TASK
from location_app import TASK as LOCATION_TASK
from mail_app import TASK as MAIL_TASK
from editor_app import TASK as EDITOR_TASK
from photo_app import TASK as PHOTO_TASK
from vad_core import create_vad_app


TASKS = {
    "photo": PHOTO_TASK,
    "file": FILE_TASK,
    "location": LOCATION_TASK,
    "drive": DRIVE_TASK,
    "checkout": CHECKOUT_TASK,
    "mail": MAIL_TASK,
    "editor": EDITOR_TASK,
}

app = FastAPI(title="VAD Seven-Scenario Suite")


@app.get("/api/info")
def info():
    return {
        "mode": "suite",
        "protocol": "vad-paper-v3-20261123",
        "backend_hash": hashlib.sha256(Path(__file__).with_name("vad_core.py").read_bytes()).hexdigest(),
        "task_hash": hashlib.sha256(json.dumps(TASKS, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest(),
        "scenarios": {
            name: {
                "task_id": task["task_id"],
                "mount": f"/{name}",
                "path": task["path"],
                "layouts": list(range(11, 21)),
            }
            for name, task in TASKS.items()
        },
    }


for scenario, task in TASKS.items():
    app.mount(f"/{scenario}", create_vad_app(task), name=scenario)
