import json
from pathlib import Path
from typing import List
from uuid import UUID

from todo_app.models import Task


class UUIDEncoder(json.JSONEncoder):
    """Custom encoder for UUID objects to be JSON serializable."""
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def load_tasks(file_path: Path) -> List[Task]:
    """Loads tasks from a JSON file."""
    if not file_path.exists():
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)
        return [Task(**data) for data in tasks_data]
    except json.JSONDecodeError:
        return []


def save_tasks(file_path: Path, tasks: List[Task]):
    """Saves tasks to a JSON file."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([task.model_dump() for task in tasks], f, indent=4, cls=UUIDEncoder)
