import json
from pathlib import Path
from typing import Dict, Any, List


class JSONParser:
    """Prosty parser dla plików JSON zawierających dane pacjenta i badania krwi."""

    def __init__(self):
        pass

    def parse_document(self, filepath: Path) -> Dict[str, Any]:
        """
        Parsuje plik JSON i zwraca słownik z danymi pacjenta i badaniami krwi.

        Oczekiwany format JSON:
        {
            "patient": {
                "name": "...",
                "surname": "...",
                "age": 30,
                "conditions": ["..."]
            },
            "blood_tests": [
                {
                    "name": "...",
                    "value": 1.23,
                    "unit": "mg/dL"
                }
            ]
        }
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Walidacja podstawowej struktury
        if "patient" not in data:
            raise ValueError("Brak klucza 'patient' w pliku JSON")

        if "blood_tests" not in data:
            raise ValueError("Brak klucza 'blood_tests' w pliku JSON")

        if not isinstance(data["blood_tests"], list):
            raise ValueError("'blood_tests' musi być listą")

        return {"patient": data["patient"], "blood_tests": data["blood_tests"]}

    def load_patient_only(self, filepath: Path) -> Dict[str, Any]:
        """
        Ładuje tylko dane pacjenta z pliku JSON.

        Oczekiwany format:
        {
            "name": "...",
            "surname": "...",
            "age": 30,
            "conditions": ["..."]
        }
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return {"patient": data}

    def load_blood_tests_only(self, filepath: Path) -> Dict[str, Any]:
        """
        Ładuje tylko dane badań krwi z pliku JSON.

        Oczekiwany format:
        [
            {
                "name": "...",
                "value": 1.23,
                "unit": "mg/dL"
            }
        ]
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Plik nie istnieje: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise ValueError("Badania krwi muszą być listą")

        return {"blood_tests": data}
