import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, Any

from src.utils.exceptions import DataLoaderError


class DataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def load_json(self, filename: str) -> Dict[str, Any]:
        filepath = self.data_dir / filename

        if not filepath.exists():
            raise DataLoaderError(
                f"File not found: {filepath}", file_path=str(filepath)
            )

        if not filepath.is_file():
            raise DataLoaderError(
                f"Path is not a file: {filepath}", file_path=str(filepath)
            )

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    raise DataLoaderError(
                        f"File is empty: {filepath}", file_path=str(filepath)
                    )
                return json.loads(content)
        except json.JSONDecodeError as e:
            raise DataLoaderError(
                f"Invalid JSON in file: {e}", file_path=str(filepath)
            ) from e
        except UnicodeDecodeError as e:
            raise DataLoaderError(
                f"File encoding error: {e}", file_path=str(filepath)
            ) from e

    @lru_cache(maxsize=10)
    def load_reference_ranges(self) -> Dict[str, Any]:
        return self.load_json("reference_ranges.json")

    @lru_cache(maxsize=10)
    def load_supplements(self) -> Dict[str, Any]:
        return self.load_json("supplements.json")

    @lru_cache(maxsize=10)
    def load_timing_rules(self) -> Dict[str, Any]:
        return self.load_json("timing_rules.json")

    @lru_cache(maxsize=10)
    def load_dosage_rules(self) -> Dict[str, Any]:
        return self.load_json("dosage_rules.json")
