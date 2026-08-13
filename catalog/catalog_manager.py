from __future__ import annotations

from .aggregates.aggregate_catalog import AggregateCatalog
from .automation.dry_run_catalog_simulator import DryRunCatalogSimulator

"""Catalog manager module."""


class CatalogManager:
    """Catalog manager."""

    def __init__(self) -> None:
        self.aggregate_catalog = AggregateCatalog()
        self.simulator = DryRunCatalogSimulator()
