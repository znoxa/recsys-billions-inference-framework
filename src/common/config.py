from dataclasses import dataclass
from typing import Any, Dict
import yaml, os

@dataclass
class Settings:
    raw: Dict[str, Any]

    @classmethod
    def from_file(cls, path: str) -> "Settings":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(raw=data)

    def get(self, key: str, default=None):
        cur = self.raw
        for part in key.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return default
            cur = cur[part]
        return cur
