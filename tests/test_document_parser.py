"""Tests for DocumentParser module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.document_parser import DocumentParser, PatientData, BloodTest


@pytest.fixture
def parser():
    return DocumentParser()


class TestPatientData:
    def test_to_dict(self):
        patient = PatientData(name="Jan", surname="Nowak", age=42, conditions=["osteoporoza"])
        result = patient.to_dict()

        assert result == {
            "name": "Jan",
            "surname": "Nowak",
            "age": 42,
            "conditions": ["osteoporoza"],
        }

    def test_to_dict_empty_conditions(self):
        patient = PatientData(name="Anna", surname="Kowalska", age=30, conditions=[])
        result = patient.to_dict()
        assert result["conditions"] == []


class TestBloodTestDataclass:
    def test_to_dict(self):
        test = BloodTest(name="Witamina D3", value=25.0, unit="ng/mL")
        result = test.to_dict()

        assert result == {"name": "Witamina D3", "value": 25.0, "unit": "ng/mL"}


class TestParseNumericValue:
    def test_integer(self, parser):
        assert parser._parse_numeric_value("42") == 42.0

    def test_float_with_dot(self, parser):
        assert parser._parse_numeric_value("3.14") == 3.14

    def test_float_with_comma(self, parser):
        assert parser._parse_numeric_value("3,14") == 3.14

    def test_value_with_extra_chars(self, parser):
        assert parser._parse_numeric_value("< 5.0") == 5.0

    def test_empty_string(self, parser):
        assert parser._parse_numeric_value("") is None

    def test_non_numeric(self, parser):
        assert parser._parse_numeric_value("abc") is None

    def test_multiple_decimal_points_rejected(self, parser):
        assert parser._parse_numeric_value("1.2.3") is None

    def test_multiple_commas_rejected(self, parser):
        assert parser._parse_numeric_value("1,2,3") is None

    def test_negative_value(self, parser):
        assert parser._parse_numeric_value("-5.0") == -5.0

    def test_multiple_minus_rejected(self, parser):
        assert parser._parse_numeric_value("--5") is None

    def test_minus_not_at_start_rejected(self, parser):
        assert parser._parse_numeric_value("5-3") is None


class TestParseBloodTestRow:
    def test_valid_row(self, parser):
        result = parser._parse_blood_test_row(["Witamina D3", "25.0", "ng/mL"])

        assert result is not None
        assert result.name == "Witamina D3"
        assert result.value == 25.0
        assert result.unit == "ng/mL"

    def test_empty_name_returns_none(self, parser):
        assert parser._parse_blood_test_row(["", "25.0", "ng/mL"]) is None

    def test_empty_value_returns_none(self, parser):
        assert parser._parse_blood_test_row(["Witamina D3", "", "ng/mL"]) is None

    def test_non_numeric_value_returns_none(self, parser):
        assert parser._parse_blood_test_row(["Witamina D3", "abc", "ng/mL"]) is None

    def test_missing_unit_defaults_empty(self, parser):
        result = parser._parse_blood_test_row(["Witamina D3", "25.0"])
        assert result is not None
        assert result.unit == ""


class TestIsTextGarbled:
    def test_normal_text_not_garbled(self, parser):
        assert parser._is_text_garbled("Witamina D3 25.0 ng/mL") is False

    def test_empty_text_is_garbled(self, parser):
        assert parser._is_text_garbled("") is True

    def test_cid_encoded_text_is_garbled(self, parser):
        text = "(cid:1) " * 20
        assert parser._is_text_garbled(text) is True

    def test_few_cid_patterns_not_garbled(self, parser):
        text = "Normal text (cid:1) more text"
        assert parser._is_text_garbled(text) is False

    def test_mostly_special_chars_is_garbled(self, parser):
        text = "!@#$%^&*" * 50
        assert parser._is_text_garbled(text) is True


class TestParseTextContent:
    def test_extract_patient_name_format(self, parser):
        text = "Pacjent: Nowak Jan\nWiek: 42\nWitamina D3 25.0 ng/mL"
        patient_data, blood_tests = parser._parse_text_content(text)

        assert patient_data.surname == "Nowak"
        assert patient_data.name == "Jan"

    def test_extract_patient_imie_nazwisko_format(self, parser):
        text = "Imię: Jan\nNazwisko: Nowak\nWiek: 42"
        patient_data, _ = parser._parse_text_content(text)

        assert patient_data.name == "Jan"
        assert patient_data.surname == "Nowak"

    def test_extract_age_from_wiek(self, parser):
        text = "Imię: Jan\nNazwisko: Nowak\nWiek: 42"
        patient_data, _ = parser._parse_text_content(text)
        assert patient_data.age == 42

    def test_extract_age_from_birth_date(self, parser):
        text = "Imię: Jan\nNazwisko: Nowak\nData urodzenia: 1984-06-15"
        patient_data, _ = parser._parse_text_content(text)
        assert patient_data.age > 0

    def test_missing_patient_info_returns_empty(self, parser):
        text = "Some random text without patient info"
        patient_data, _ = parser._parse_text_content(text)
        assert patient_data.name == ""
        assert patient_data.surname == ""

    def test_extract_blood_test_from_text(self, parser):
        text = "Pacjent: Nowak Jan\nWitamina D3: 25.0 ng/mL\nŻelazo: 80.0 ug/dL"
        _, blood_tests = parser._parse_text_content(text)

        # Parser requires keyword match or medical unit — verify at least one test extracted
        assert len(blood_tests) > 0


class TestParseDocument:
    def test_unsupported_format(self, parser, tmp_path):
        filepath = tmp_path / "test.txt"
        filepath.write_text("some text")

        from src.utils.exceptions import DataLoaderError

        with pytest.raises(DataLoaderError, match="Unsupported"):
            parser.parse_document(filepath)

    def test_file_not_found(self, parser):
        from src.utils.exceptions import DataLoaderError

        with pytest.raises(DataLoaderError, match="not found"):
            parser.parse_document(Path("/nonexistent/file.pdf"))

    def test_file_too_large(self, parser, tmp_path):
        filepath = tmp_path / "large.pdf"
        filepath.write_bytes(b"x" * (51 * 1024 * 1024))

        from src.utils.exceptions import DataLoaderError

        with pytest.raises(DataLoaderError, match="too large"):
            parser.parse_document(filepath)
