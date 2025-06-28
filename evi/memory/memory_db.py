import json
import os
from typing import List, Dict

MEMORY_FILE = "history.json"

class MemoryDB:
    """Simple JSON based memory storage."""
    def __init__(self, path: str = MEMORY_FILE):
        self.path = path
        self.data: List[Dict] = []
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = []

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_message(self, sender: str, text: str, hormones: Dict[str, int]) -> None:
        entry = {
            "sender": sender,
            "text": text,
            "hormones": hormones.copy(),
        }
        self.data.append(entry)
        self.save()
