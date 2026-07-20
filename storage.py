import json
import os
import shutil
from datetime import datetime
from dataclasses import asdict
from models import Task

def load_data():
    if not os.path.exists("tasks.json"):
        return 1, []

    if os.path.getsize("tasks.json") == 0:
        return 1, []

    try:
        with open("tasks.json", "r") as f:
            data = json.load(f)
            return data.get("next_id", 1), [Task(**t) for t in data.get("tasks", [])]
        
    except (json.JSONDecodeError, TypeError):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"tasks.json.corrupted.{timestamp}"
        shutil.copy("tasks.json", backup_name)
        print(f"Warning: tasks.json was unreadable. Backed up to {backup_name}. Starting with an empty list.")
        return 1, []
    
def save_data(next_id, tasks):
    with open("tasks.json", "w") as f:
        json.dump({
            "next_id": next_id,
            "tasks": [asdict(t) for t in tasks]
        }, f, indent=2)
        