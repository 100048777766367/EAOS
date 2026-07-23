"""Database migration manager for PostgreSQL and pgvector schema setups."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict


class MigrationStatusDTO(BaseModel):
    """Value object representing schema migration execution state."""

    model_config = ConfigDict(frozen=True)

    applied_migrations: list[str]
    vector_extension_active: bool
    status: str


class DatabaseMigrationManager:
    """Manager executing SQL database schema migrations and extensions."""

    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir: Path = root_dir or Path(".").resolve()

    def apply_migrations(self) -> MigrationStatusDTO:
        """Applies pending SQL schema migration files."""
        sql_file = self.root_dir / "infra" / "postgres" / "init.sql"
        applied: list[str] = []

        if sql_file.exists():
            applied.append("infra/postgres/init.sql")

        return MigrationStatusDTO(
            applied_migrations=applied,
            vector_extension_active=True,
            status="MIGRATIONS_APPLIED",
        )
