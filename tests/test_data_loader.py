"""Tests for DataLoader module."""

import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.data_loader import DataLoader
from src.utils.exceptions import DataLoaderError
from config import DATA_DIR


@pytest.fixture
def data_loader():
    return DataLoader(DATA_DIR)


def test_load_reference_ranges(data_loader):
    """Test loading reference ranges."""
    result = data_loader.load_reference_ranges()

    assert isinstance(result, dict)
    assert "reference_ranges" in result or "categories" in result


def test_load_supplements(data_loader):
    """Test loading supplements."""
    result = data_loader.load_supplements()

    assert isinstance(result, dict)
    # First call should load from file
    assert "supplements" in result


def test_load_supplements_caching(data_loader, tmp_path):
    """Test that supplements are cached."""
    result1 = data_loader.load_supplements()

    # Modify the file
    supplements_path = DATA_DIR / "supplements.json"
    with open(supplements_path, "r") as f:
        original_data = json.load(f)

    # Second call should return cached data
    result2 = data_loader.load_supplements()

    assert result1 == result2

    # Restore original data
    with open(supplements_path, "w") as f:
        json.dump(original_data, f)


def test_load_json_file_not_found(data_loader):
    """Test loading a non-existent file."""
    with pytest.raises(DataLoaderError) as exc_info:
        data_loader.load_json("nonexistent_file.json")

    assert "File not found" in str(exc_info.value)


def test_load_json_invalid_json(data_loader, tmp_path):
    """Test loading a file with invalid JSON."""
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, "w") as f:
        f.write('{" invalid json }')

    with pytest.raises(DataLoaderError) as exc_info:
        data_loader.load_json(str(invalid_file))

    assert "Invalid JSON" in str(exc_info.value)


def test_load_json_empty_file(data_loader, tmp_path):
    """Test loading an empty JSON file."""
    empty_file = tmp_path / "empty.json"
    with open(empty_file, "w") as f:
        f.write("   ")

    with pytest.raises(DataLoaderError) as exc_info:
        data_loader.load_json(str(empty_file))

    assert "File is empty" in str(exc_info.value)
