from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    name: str
    description: str
    deadline: str
    status: str = "pending"
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def display_status(self):
        if self.status == "done":
            return "done"
        try:
            if datetime.fromisoformat(self.deadline) < datetime.now():
                return "expired"
        except ValueError:
            return "invalid deadline"
        return "pending"