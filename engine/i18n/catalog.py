from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final, Protocol, override

"""I18n Catalog Engine Implementation."""


__all__ = ["I18nCatalogEngine", "SupportedLocale", "TranslationCatalogProtocol"]


class SupportedLocale(StrEnum):
    VIETNAMESE = "vi"
    ENGLISH = "en"


class TranslationCatalogProtocol(Protocol):
    def get_text(self, key: str, locale: SupportedLocale | str = SupportedLocale.VIETNAMESE) -> str: ...


@dataclass(frozen=True, slots=True)
class I18nCatalogEngine(TranslationCatalogProtocol):
    """Engine dịch thuật đa ngôn ngữ cấp Domain/Engine."""

    _catalogs: dict[str, dict[str, str]] = field(
        default_factory=lambda: {
            "vi": {
                "app.title": "Hệ điều hành EAOS",
                "dashboard.welcome": "EAOS Cybernetic Control Room",
            },
            "en": {
                "app.title": "EAOS Operating System",
                "dashboard.welcome": "EAOS Cybernetic Control Room",
            },
        }
    )

    @override
    def get_text(self, key: str, locale: SupportedLocale | str = SupportedLocale.VIETNAMESE) -> str:
        loc_str: Final[str] = locale.value if isinstance(locale, SupportedLocale) else str(locale)
        catalog: Final[dict[str, str]] = self._catalogs.get(loc_str, self._catalogs["vi"])
        return catalog.get(key, key)
