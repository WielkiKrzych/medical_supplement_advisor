from src.models.patient import Patient
from src.models.blood_test import BloodTest
from src.utils.exceptions import ValidationError, AnalysisError
from typing import List


class Validator:
    @staticmethod
    def validate_patient(data: dict) -> Patient:
        return Patient(**data)

    @staticmethod
    def validate_blood_tests(data: List[dict]) -> List[BloodTest]:
        return [BloodTest(**test) for test in data]

    @staticmethod
    def validate_reference_ranges(data: dict) -> None:
        """Validate reference ranges data structure.

        Raises:
            ValidationError: If reference_ranges key is missing or structure is invalid.
        """
        if "reference_ranges" not in data:
            raise ValidationError(
                "Missing 'reference_ranges' key in data", field="reference_ranges"
            )

        for idx, ref_range in enumerate(data["reference_ranges"]):
            if not all(key in ref_range for key in ["name", "min", "max", "unit"]):
                raise ValidationError(
                    f"Reference range at index {idx} missing required fields (name, min, max, unit)",
                    field="reference_ranges",
                )

    @staticmethod
    def validate_supplements(data: dict) -> None:
        """Validate supplements data structure.

        Raises:
            ValidationError: If supplements key is missing or structure is invalid.
        """
        if "supplements" not in data:
            raise ValidationError(
                "Missing 'supplements' key in data", field="supplements"
            )

        for idx, supplement in enumerate(data["supplements"]):
            if not all(key in supplement for key in ["id", "name", "condition"]):
                raise ValidationError(
                    f"Supplement at index {idx} missing required fields (id, name, condition)",
                    field="supplements",
                )

    @staticmethod
    def validate_dosage_rules(data: dict) -> None:
        """Validate dosage rules data structure.

        Raises:
            ValidationError: If dosage_rules key is missing or structure is invalid.
        """
        if "dosage_rules" not in data:
            raise ValidationError(
                "Missing 'dosage_rules' key in data", field="dosage_rules"
            )

        for idx, rule in enumerate(data["dosage_rules"]):
            if "condition_type" not in rule or "supplements" not in rule:
                raise ValidationError(
                    f"Rule at index {idx} missing required fields (condition_type, supplements)",
                    field="dosage_rules",
                )
