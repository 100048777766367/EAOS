from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, order=True)
class ContractVersion:
    """Immutable semantic version for a repository contract."""

    major: int
    minor: int = 0
    patch: int = 0

    def __post_init__(self) -> None:
        if self.major < 0:
            raise ValueError("major version cannot be negative")

        if self.minor < 0:
            raise ValueError("minor version cannot be negative")

        if self.patch < 0:
            raise ValueError("patch version cannot be negative")

    @classmethod
    def parse(cls, value: str) -> ContractVersion:
        """Parse a semantic version such as ``1.2.3``."""

        parts = value.strip().split(".")

        if len(parts) != 3:
            raise ValueError(f"Invalid contract version: {value!r}. Expected MAJOR.MINOR.PATCH.")

        try:
            major, minor, patch = (int(part) for part in parts)
        except ValueError as exc:
            raise ValueError(f"Invalid contract version: {value!r}") from exc

        return cls(
            major=major,
            minor=minor,
            patch=patch,
        )

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def major_line(self) -> int:
        return self.major
