import json
from pathlib import Path
from typing import Dict, Any


class DataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_json(self, filename: str) -> Dict[str, Any]:
        filepath = self.data_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_reference_ranges(self) -> Dict[str, Any]:
        return self.load_json("reference_ranges.json")

    def load_supplements(self) -> Dict[str, Any]:
        return self.load_json("supplements.json")

    def load_timing_rules(self) -> Dict[str, Any]:
        return self.load_json("timing_rules.json")

    def load_dosage_rules(self) -> Dict[str, Any]:
        return self.load_json("dosage_rules.json")
