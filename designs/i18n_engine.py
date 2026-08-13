from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

"""I18n Catalog Engine Implementation."""


__all__ = ["I18nCatalogEngine"]


@dataclass
class I18nCatalogEngine:
    locales_dir: Path | str | None = None
    _catalogs: dict[str, dict[str, str]] = field(
        default_factory=lambda: {
            "vi": {
                "title": "Hệ điều hành EAOS",
                "app.title": "Hệ điều hành EAOS",
            },
            "en": {
                "title": "EAOS Operating System",
                "app.title": "EAOS Operating System",
            },
        }
    )

    def load_language(self, lang: str) -> None:
        """Load catalog for the specified language."""
        if self.locales_dir:
            path = Path(self.locales_dir) / f"{lang}.json"
            if path.exists():
                pass

    def translate(self, lang: str, key: str, **kwargs: str) -> str:
        """Translate key for given language: translate(lang, key)."""
        catalog: Final[dict[str, str]] = self._catalogs.get(lang, self._catalogs.get("vi", {}))
        val = catalog.get(key, key)
        if kwargs and isinstance(val, str):
            for k, v in kwargs.items():
                val = val.replace(f"{{{k}}}", str(v))
        return val

    def get_text(self, key: str, locale: str = "vi") -> str:
        return self.translate(locale, key)

    def get(self, key: str, locale: str = "vi") -> str:
        return self.translate(locale, key)
