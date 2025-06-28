import json
import os
from typing import Any, Dict

SETTINGS_FILE = "settings.json"

class SettingsDB:
    """Simple JSON settings storage."""
    def __init__(self, path: str = SETTINGS_FILE):
        self.path = path
        self.data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def save(self) -> None:
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)
