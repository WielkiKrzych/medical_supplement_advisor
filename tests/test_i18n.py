"""Tests for i18n module."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.utils.i18n import I18n, t, get_language, set_language, get_available_languages


class TestI18nSingleton:
    def test_singleton_returns_same_instance(self):
        i1 = I18n()
        i2 = I18n()
        assert i1 is i2

    def test_default_language_is_pl(self):
        i18n = I18n()
        assert i18n.get_language() == "pl"


class TestTranslation:
    def test_simple_key(self):
        result = t("pdf.title")
        assert result == "Rekomendacja Suplementacji"

    def test_nested_key(self):
        result = t("gui.title")
        assert result == "Medical Supplement Advisor"

    def test_missing_key_returns_key(self):
        result = t("nonexistent.key")
        assert result == "nonexistent.key"

    def test_deeply_missing_key_returns_key(self):
        result = t("pdf.nonexistent.deep")
        assert result == "pdf.nonexistent.deep"

    def test_format_args(self):
        result = t("analysis.critical_issues_found", 3)
        assert "3" in result

    def test_priority_translations(self):
        assert t("pdf.priority_critical") == "Krytyczny"
        assert t("pdf.priority_high") == "Wysoki"
        assert t("pdf.priority_medium") == "Średni"
        assert t("pdf.priority_low") == "Niski"

    def test_category_translations(self):
        assert t("categories.morphology") == "Morfologia Krwi"
        assert t("categories.thyroid") == "Tarczyca"
        assert t("categories.liver") == "Wątroba"


class TestLanguageManagement:
    def test_get_language(self):
        lang = get_language()
        assert isinstance(lang, str)
        assert len(lang) > 0

    def test_set_invalid_language_keeps_current(self):
        original = get_language()
        set_language("xx_nonexistent", persist=False)
        assert get_language() == original

    def test_available_languages_includes_pl(self):
        languages = get_available_languages()
        assert "pl" in languages

    def test_set_language_without_persist(self):
        original = get_language()
        set_language("pl", persist=False)
        assert get_language() == "pl"
        # Restore
        set_language(original, persist=False)
