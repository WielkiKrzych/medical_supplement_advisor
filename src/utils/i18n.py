"""Internationalization (i18n) utility module."""

import json
from pathlib import Path
from typing import Dict, Optional
from config import BASE_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Config file path for language persistence
_CONFIG_FILE = BASE_DIR / "config" / "user_settings.json"


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
        self._load_saved_language()

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
                logger.warning(f"Failed to load translation file {json_file}: {e}")

    def _load_saved_language(self):
        """Load saved language preference from config file."""
        try:
            if _CONFIG_FILE.exists():
                with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    saved_lang = settings.get("language")
                    if saved_lang and saved_lang in self._translations:
                        self._current_language = saved_lang
                        logger.info(f"Loaded saved language preference: {saved_lang}")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load saved language setting: {e}")

    def _save_language(self, language: str):
        """Save language preference to config file."""
        try:
            _CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            settings = {}
            if _CONFIG_FILE.exists():
                with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            settings["language"] = language
            with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2)
            logger.info(f"Saved language preference: {language}")
        except IOError as e:
            logger.warning(f"Failed to save language setting: {e}")

    def set_language(self, language: str, persist: bool = True):
        """Set the current language.
        
        Args:
            language: Language code to set
            persist: If True, save preference to config file
        """
        if language in self._translations:
            self._current_language = language
            if persist:
                self._save_language(language)
        else:
            logger.warning(f"Language '{language}' not available, using '{self._current_language}'")

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


def set_language(language: str, persist: bool = True):
    """Set the application language.
    
    Args:
        language: Language code to set
        persist: If True, save preference to config file
    """
    _i18n.set_language(language, persist=persist)


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
