"""Tests for PDFFormatter module."""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.formatter import PDFFormatter, register_polish_fonts, sanitize_filename


class TestSanitizeFilename:
    def test_normal_name(self):
        assert sanitize_filename("Jan_Nowak") == "Jan_Nowak"

    def test_removes_invalid_chars(self):
        result = sanitize_filename('file<>:"/\\|?*name')
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result
        assert '"' not in result
        assert "\\" not in result
        assert "|" not in result
        assert "?" not in result
        assert "*" not in result

    def test_truncates_long_names(self):
        long_name = "a" * 200
        result = sanitize_filename(long_name)
        assert len(result) <= 100

    def test_empty_string(self):
        assert sanitize_filename("") == ""

    def test_polish_characters_preserved(self):
        result = sanitize_filename("Źółćęśąż")
        assert result == "Źółćęśąż"


class TestRegisterPolishFonts:
    def test_returns_font_names(self):
        regular, bold = register_polish_fonts()
        assert isinstance(regular, str)
        assert isinstance(bold, str)
        assert len(regular) > 0
        assert len(bold) > 0

    def test_fallback_fonts_are_valid(self):
        regular, bold = register_polish_fonts()
        # Should return either custom or fallback Helvetica
        assert regular in ("CustomFont", "Helvetica")
        assert bold in ("CustomFont-Bold", "Helvetica-Bold")


class TestPDFFormatter:
    @pytest.fixture
    def output_dir(self, tmp_path):
        return tmp_path

    @pytest.fixture
    def formatter(self, output_dir):
        return PDFFormatter(output_dir)

    def test_init_sets_output_dir(self, formatter, output_dir):
        assert formatter.output_dir == output_dir

    def test_init_configures_fonts(self, formatter):
        assert formatter.font_name is not None
        assert formatter.font_name_bold is not None

    def test_get_priority_display_valid(self, formatter):
        result = formatter._get_priority_display("high")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_priority_display_invalid(self, formatter):
        result = formatter._get_priority_display("invalid_priority")
        assert isinstance(result, str)

    def test_generate_pdf_creates_file(self, formatter, output_dir):
        from src.models.recommendation import Recommendation, SupplementRecommendation

        recommendation = Recommendation(
            patient_name="Jan",
            patient_surname="Nowak",
            date=datetime.now(),
            supplements=[
                SupplementRecommendation(
                    name="Witamina D3",
                    dosage="2000 IU",
                    timing="rano",
                    priority="high",
                    reason="Niedobór witaminy D3",
                ),
            ],
        )

        filepath = formatter.generate_pdf(recommendation)

        assert filepath.exists()
        assert filepath.suffix == ".pdf"
        assert filepath.stat().st_size > 0

    def test_generate_pdf_no_supplements(self, formatter, output_dir):
        from src.models.recommendation import Recommendation

        recommendation = Recommendation(
            patient_name="Jan",
            patient_surname="Nowak",
            date=datetime.now(),
            supplements=[],
        )

        filepath = formatter.generate_pdf(recommendation)

        assert filepath.exists()
        assert filepath.suffix == ".pdf"

    def test_generate_pdf_filename_contains_patient_name(self, formatter, output_dir):
        from src.models.recommendation import Recommendation

        recommendation = Recommendation(
            patient_name="Jan",
            patient_surname="Nowak",
            date=datetime.now(),
            supplements=[],
        )

        filepath = formatter.generate_pdf(recommendation)

        assert "Jan" in filepath.name
        assert "Nowak" in filepath.name
