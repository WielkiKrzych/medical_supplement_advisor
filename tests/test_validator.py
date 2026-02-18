"""Tests for Validator module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.validator import Validator
from src.utils.exceptions import ValidationError
from src.models.patient import Patient
from src.models.blood_test import BloodTest


@pytest.fixture
def validator():
    return Validator()


class TestValidatePatient:
    def test_valid_patient(self, validator):
        data = {"name": "Jan", "surname": "Nowak", "age": 42, "conditions": ["osteoporoza"]}
        patient = validator.validate_patient(data)

        assert isinstance(patient, Patient)
        assert patient.name == "Jan"
        assert patient.surname == "Nowak"
        assert patient.age == 42
        assert patient.conditions == ["osteoporoza"]

    def test_valid_patient_no_conditions(self, validator):
        data = {"name": "Anna", "surname": "Kowalska", "age": 30}
        patient = validator.validate_patient(data)

        assert patient.conditions == []

    def test_missing_name_raises_validation_error(self, validator):
        data = {"surname": "Nowak", "age": 42}
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_patient(data)
        assert "patient" in str(exc_info.value)

    def test_empty_name_raises_validation_error(self, validator):
        data = {"name": "", "surname": "Nowak", "age": 42}
        with pytest.raises(ValidationError):
            validator.validate_patient(data)

    def test_negative_age_raises_validation_error(self, validator):
        data = {"name": "Jan", "surname": "Nowak", "age": -1}
        with pytest.raises(ValidationError):
            validator.validate_patient(data)

    def test_age_over_150_raises_validation_error(self, validator):
        data = {"name": "Jan", "surname": "Nowak", "age": 200}
        with pytest.raises(ValidationError):
            validator.validate_patient(data)

    def test_extra_fields_ignored(self, validator):
        data = {"name": "Jan", "surname": "Nowak", "age": 42, "extra": "ignored"}
        patient = validator.validate_patient(data)
        assert patient.name == "Jan"


class TestValidateBloodTests:
    def test_valid_blood_tests(self, validator):
        data = [
            {"name": "Witamina D3", "value": 25.0, "unit": "ng/mL"},
            {"name": "Żelazo", "value": 80.0, "unit": "ug/dL"},
        ]
        tests = validator.validate_blood_tests(data)

        assert len(tests) == 2
        assert all(isinstance(t, BloodTest) for t in tests)

    def test_empty_list(self, validator):
        tests = validator.validate_blood_tests([])
        assert tests == []

    def test_missing_value_raises_validation_error(self, validator):
        data = [{"name": "Witamina D3", "unit": "ng/mL"}]
        with pytest.raises(ValidationError):
            validator.validate_blood_tests(data)

    def test_negative_value_raises_validation_error(self, validator):
        data = [{"name": "Witamina D3", "value": -5.0, "unit": "ng/mL"}]
        with pytest.raises(ValidationError):
            validator.validate_blood_tests(data)

    def test_nan_value_raises_validation_error(self, validator):
        data = [{"name": "Witamina D3", "value": float("nan"), "unit": "ng/mL"}]
        with pytest.raises(ValidationError):
            validator.validate_blood_tests(data)

    def test_empty_name_raises_validation_error(self, validator):
        data = [{"name": "", "value": 25.0, "unit": "ng/mL"}]
        with pytest.raises(ValidationError):
            validator.validate_blood_tests(data)


class TestValidateReferenceRanges:
    def test_valid_reference_ranges(self, validator):
        data = {
            "reference_ranges": [
                {"name": "Test", "min": 0.0, "max": 100.0, "unit": "mg/dL"}
            ]
        }
        validator.validate_reference_ranges(data)

    def test_missing_key_raises_error(self, validator):
        with pytest.raises(ValidationError):
            validator.validate_reference_ranges({})

    def test_missing_fields_raises_error(self, validator):
        data = {"reference_ranges": [{"name": "Test"}]}
        with pytest.raises(ValidationError):
            validator.validate_reference_ranges(data)


class TestValidateSupplements:
    def test_valid_supplements(self, validator):
        data = {
            "supplements": [
                {"id": "vit_d3", "name": "Witamina D3", "condition": "deficiency"}
            ]
        }
        validator.validate_supplements(data)

    def test_missing_key_raises_error(self, validator):
        with pytest.raises(ValidationError):
            validator.validate_supplements({})

    def test_missing_fields_raises_error(self, validator):
        data = {"supplements": [{"id": "vit_d3"}]}
        with pytest.raises(ValidationError):
            validator.validate_supplements(data)


class TestValidateDosageRules:
    def test_valid_dosage_rules(self, validator):
        data = {
            "dosage_rules": [
                {"condition_type": "single_test", "supplements": ["vit_d3"]}
            ]
        }
        validator.validate_dosage_rules(data)

    def test_missing_key_raises_error(self, validator):
        with pytest.raises(ValidationError):
            validator.validate_dosage_rules({})

    def test_missing_fields_raises_error(self, validator):
        data = {"dosage_rules": [{"condition_type": "single_test"}]}
        with pytest.raises(ValidationError):
            validator.validate_dosage_rules(data)
