"""Simple persistent conversation memory manager.

Provides a tiny API to add/retrieve recent conversation entries
and persist them under `data/memory.json`.
"""

from datetime import datetime
from typing import List, Dict
import json
import os


class MemoryManager:
    """Centralized memory manager for conversation history.

    Minimal, robust, and file-backed. Methods are small and clear:
    - `add(user, neuro)` add one entry
    - `get_recent(n)` return most recent `n` entries
    - `clear()` wipe memory
    - `to_list()` return full list
    """

    def __init__(self, data_dir: str = "data", max_items: int = 100) -> None:
        self.data_dir = data_dir
        self.memory_file = os.path.join(data_dir, "memory.json")
        self.max_items = int(max_items)
        os.makedirs(self.data_dir, exist_ok=True)

        self._memory: List[Dict[str, str]] = self._load()

    def _load(self) -> List[Dict[str, str]]:
        if not os.path.exists(self.memory_file):
            return []
        try:
            with open(self.memory_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return []

    def _save(self) -> None:
        try:
            with open(self.memory_file, "w", encoding="utf-8") as fh:
                json.dump(self._memory[-self.max_items :], fh, ensure_ascii=False, indent=2)
        except Exception:
            # Best-effort persistence; don't raise for UI flows
            pass

    def add(self, user: str, neuro: str) -> None:
        """Append a user/neuro exchange to memory and persist."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user,
            "neuro": neuro,
        }
        self._memory.append(entry)
        # trim
        if len(self._memory) > self.max_items:
            self._memory = self._memory[-self.max_items :]
        self._save()

    def get_recent(self, n: int = 10) -> List[Dict[str, str]]:
        return list(self._memory[-int(n) :])

    def clear(self) -> None:
        self._memory = []
        self._save()

    def to_list(self) -> List[Dict[str, str]]:
        return list(self._memory)
