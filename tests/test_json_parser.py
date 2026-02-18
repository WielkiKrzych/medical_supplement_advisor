"""Tests for JSONParser module."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.json_parser import JSONParser


@pytest.fixture
def parser():
    return JSONParser()


@pytest.fixture
def valid_json_file(tmp_path):
    data = {
        "patient": {
            "name": "Jan",
            "surname": "Nowak",
            "age": 42,
            "conditions": [],
        },
        "blood_tests": [
            {"name": "Witamina D3", "value": 25.0, "unit": "ng/mL"},
        ],
    }
    filepath = tmp_path / "valid.json"
    filepath.write_text(json.dumps(data), encoding="utf-8")
    return filepath


class TestParseDocument:
    def test_valid_file(self, parser, valid_json_file):
        result = parser.parse_document(valid_json_file)

        assert "patient" in result
        assert "blood_tests" in result
        assert result["patient"]["name"] == "Jan"
        assert len(result["blood_tests"]) == 1

    def test_file_not_found(self, parser, tmp_path):
        with pytest.raises(FileNotFoundError):
            parser.parse_document(tmp_path / "nonexistent.json")

    def test_missing_patient_key(self, parser, tmp_path):
        filepath = tmp_path / "no_patient.json"
        filepath.write_text(json.dumps({"blood_tests": []}), encoding="utf-8")

        with pytest.raises(ValueError, match="patient"):
            parser.parse_document(filepath)

    def test_missing_blood_tests_key(self, parser, tmp_path):
        filepath = tmp_path / "no_tests.json"
        filepath.write_text(
            json.dumps({"patient": {"name": "Jan"}}), encoding="utf-8"
        )

        with pytest.raises(ValueError, match="blood_tests"):
            parser.parse_document(filepath)

    def test_blood_tests_not_list(self, parser, tmp_path):
        filepath = tmp_path / "bad_tests.json"
        filepath.write_text(
            json.dumps({"patient": {}, "blood_tests": "not_a_list"}),
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="list"):
            parser.parse_document(filepath)

    def test_invalid_json(self, parser, tmp_path):
        filepath = tmp_path / "bad.json"
        filepath.write_text("{invalid json}", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            parser.parse_document(filepath)


class TestLoadPatientOnly:
    def test_valid_patient_file(self, parser, tmp_path):
        data = {"name": "Jan", "surname": "Nowak", "age": 42, "conditions": []}
        filepath = tmp_path / "patient.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        result = parser.load_patient_only(filepath)

        assert "patient" in result
        assert result["patient"]["name"] == "Jan"

    def test_file_not_found(self, parser, tmp_path):
        with pytest.raises(FileNotFoundError):
            parser.load_patient_only(tmp_path / "missing.json")


class TestLoadBloodTestsOnly:
    def test_valid_tests_file(self, parser, tmp_path):
        data = [{"name": "Witamina D3", "value": 25.0, "unit": "ng/mL"}]
        filepath = tmp_path / "tests.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        result = parser.load_blood_tests_only(filepath)

        assert "blood_tests" in result
        assert len(result["blood_tests"]) == 1

    def test_not_a_list_raises_error(self, parser, tmp_path):
        filepath = tmp_path / "not_list.json"
        filepath.write_text(json.dumps({"key": "value"}), encoding="utf-8")

        with pytest.raises(ValueError, match="list"):
            parser.load_blood_tests_only(filepath)

    def test_file_not_found(self, parser, tmp_path):
        with pytest.raises(FileNotFoundError):
            parser.load_blood_tests_only(tmp_path / "missing.json")
