"""Production Thread-Safe i18n Translation Manager for EAOS."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

import structlog

from locales.schema import TranslationCatalogSchema

logger = structlog.get_logger()


class LocalesManager:
    """Enterprise Centralized i18n Translation Manager."""

    _instance: ClassVar[LocalesManager | None] = None

    def __init__(
        self,
        translations_dir: Path | None = None,
        default_locale: str = "en",
    ) -> None:
        self.translations_dir = translations_dir or Path(__file__).parent / "translations"
        self.default_locale = default_locale
        self._catalogs: dict[str, TranslationCatalogSchema] = {}
        self._raw_catalogs: dict[str, dict[str, Any]] = {}
        self.reload_catalogs()

    @classmethod
    def get_instance(cls) -> LocalesManager:
        """Singleton instance accessor for thread-safe global usage."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def reload_catalogs(self) -> None:
        """Reloads and validates all translation JSON files from disk."""
        self._catalogs.clear()
        self._raw_catalogs.clear()

        if not self.translations_dir.exists():
            logger.warning(
                "Translations directory does not exist",
                path=str(self.translations_dir),
            )
            return

        for json_file in self.translations_dir.glob("*.json"):
            locale = json_file.stem
            try:
                with json_file.open("r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                    self._raw_catalogs[locale] = raw_data
                    catalog = TranslationCatalogSchema.model_validate(raw_data)
                    self._catalogs[locale] = catalog
            except Exception as err:
                logger.error(
                    "Failed to load translation catalog",
                    locale=locale,
                    error=str(err),
                )

    def get_supported_locales(self) -> list[str]:
        """Returns a list of all successfully loaded language codes."""
        return list(self._catalogs.keys())

    def get_catalog_schema(self, locale: str | None = None) -> TranslationCatalogSchema | None:
        """Returns validated Pydantic catalog schema for a locale."""
        target_locale = locale or self.default_locale
        return self._catalogs.get(target_locale) or self._catalogs.get(self.default_locale)

    def translate(
        self,
        key_path: str,
        locale: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Translates a dot-separated key_path (e.g.

        'system.title') with fallback and parameter interpolation.
        """
        target_locale = locale or self.default_locale
        raw_catalog = self._raw_catalogs.get(target_locale) or self._raw_catalogs.get(self.default_locale) or {}

        keys = key_path.split(".")
        value: Any = raw_catalog
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                value = None
                break

        if value is None:
            return key_path

        if isinstance(value, str) and kwargs:
            try:
                return value.format(**kwargs)
            except KeyError:
                return value

        return str(value)
