"""Internationalization (i18n) utility module."""

import json
from pathlib import Path
from typing import Dict
from config import BASE_DIR


class I18n:
    """Internationalization utility for managing translations."""

    _instance = None
    _current_language = "pl"
    _translations: Dict[str, Dict] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18n, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._load_translations()

    def _load_translations(self):
        """Load all available translations."""
        i18n_dir = BASE_DIR / "i18n"
        if not i18n_dir.exists():
            return

        for json_file in i18n_dir.glob("*.json"):
            language_code = json_file.stem
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    self._translations[language_code] = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Failed to load translation file {json_file}: {e}")

    def set_language(self, language: str):
        """Set the current language."""
        if language in self._translations:
            self._current_language = language
        else:
            print(f"Warning: Language '{language}' not available, using '{self._current_language}'")

    def get_language(self) -> str:
        """Get the current language."""
        return self._current_language

    def t(self, key: str, *args, **kwargs) -> str:
        """Translate a key using current language.

        Args:
            key: Translation key in dot notation (e.g., 'pdf.title')
            *args: Arguments for string formatting
            **kwargs: Named arguments for string formatting

        Returns:
            Translated string, or key if not found
        """
        parts = key.split(".")
        translations = self._translations.get(self._current_language, {})

        for part in parts:
            if isinstance(translations, dict):
                translations = translations.get(part)
            else:
                return key

        if translations is None or not isinstance(translations, str):
            return key

        if args or kwargs:
            return translations.format(*args, **kwargs)
        return translations


# Singleton instance
_i18n = I18n()


def set_language(language: str):
    """Set the application language."""
    _i18n.set_language(language)


def get_language() -> str:
    """Get the current application language."""
    return _i18n.get_language()


def t(key: str, *args, **kwargs) -> str:
    """Translate a key using current language.

    Usage:
        t('pdf.title')
        t('pdf.supplements_count', 5)

    Args:
        key: Translation key in dot notation (e.g., 'pdf.title')
        *args: Arguments for string formatting
        **kwargs: Named arguments for string formatting

    Returns:
        Translated string
    """
    return _i18n.t(key, *args, **kwargs)


def get_available_languages() -> list[str]:
    """Get list of available languages."""
    return list(_i18n._translations.keys())
