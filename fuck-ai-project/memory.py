import os
import json
from datetime import datetime


class MemoryManager:
    """Centralized memory manager for conversation history.

    Stores recent conversation entries in-memory and persists to
    data/memory.json. Provides helpers to add and retrieve recent
    items so other modules don't manage raw lists.
    """

    def __init__(self, data_dir="data", max_items: int = 100):
        self.data_dir = data_dir
        self.memory_file = os.path.join(data_dir, "memory.json")
        self.max_items = max_items
        os.makedirs(self.data_dir, exist_ok=True)

        self._memory = self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save(self):
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self._memory[-self.max_items :], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def add(self, user: str, neuro: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "neuro": neuro,
        }
        self._memory.append(entry)
        # keep only last max_items
        if len(self._memory) > self.max_items:
            self._memory = self._memory[-self.max_items :]
        self._save()

    def get_recent(self, n: int = 10):
        return list(self._memory[-n:])

    def clear(self):
        self._memory = []
        self._save()

    def to_list(self):
        return list(self._memory)
