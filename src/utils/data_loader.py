import json
from pathlib import Path
from typing import Dict, Any

from src.utils.exceptions import DataLoaderError
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataLoader:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self._cache: Dict[str, Any] = {}

    def load_json(self, filename: str) -> Dict[str, Any]:
        candidate = Path(filename)
        if candidate.is_absolute():
            filepath = candidate.resolve()
        else:
            filepath = (self.data_dir / filename).resolve()

        if not filepath.is_relative_to(self.data_dir.resolve()):
            error_msg = f"Path traversal detected: {filename}"
            logger.error(error_msg)
            raise DataLoaderError(error_msg, file_path=filename)

        if not filepath.exists():
            error_msg = f"File not found: {filepath}"
            logger.error(error_msg)
            raise DataLoaderError(
                error_msg, file_path=str(filepath)
            )

        if not filepath.is_file():
            error_msg = f"Path is not a file: {filepath}"
            logger.error(error_msg)
            raise DataLoaderError(
                error_msg, file_path=str(filepath)
            )

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    error_msg = f"File is empty: {filepath}"
                    logger.error(error_msg)
                    raise DataLoaderError(
                        error_msg, file_path=str(filepath)
                    )
                data = json.loads(content)
                logger.debug(f"Successfully loaded {filename} from {filepath}")
                return data
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON in file: {e}"
            logger.error(error_msg)
            raise DataLoaderError(
                error_msg, file_path=str(filepath)
            ) from e
        except UnicodeDecodeError as e:
            error_msg = f"File encoding error: {e}"
            logger.error(error_msg)
            raise DataLoaderError(
                error_msg, file_path=str(filepath)
            ) from e

    def _load_cached(self, filename: str) -> Dict[str, Any]:
        if filename not in self._cache:
            logger.debug(f"Loading {filename} from file")
            self._cache[filename] = self.load_json(filename)
        else:
            logger.debug(f"Loading {filename} from cache")
        return self._cache[filename]

    def load_reference_ranges(self) -> Dict[str, Any]:
        return self._load_cached("reference_ranges.json")

    def load_supplements(self) -> Dict[str, Any]:
        return self._load_cached("supplements.json")

    def load_timing_rules(self) -> Dict[str, Any]:
        return self._load_cached("timing_rules.json")

    def load_dosage_rules(self) -> Dict[str, Any]:
        return self._load_cached("dosage_rules.json")
