from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

"""Compiler Symbol Table and Type System (Sprint 3.2)."""


class SymbolEntry(BaseModel):
    """Symbol table entry for semantic analysis."""

    model_config = ConfigDict(frozen=True)

    symbol_name: str = Field(..., description="Symbol identifier")
    category: str = Field(..., description="CAPABILITY, ENTITY, POLICY, EVENT")
    type_definition: str = Field(default="Object")


class SymbolTable(BaseModel):
    """Symbol Table aggregate for scope resolution."""

    model_config = ConfigDict(frozen=True)

    symbols: dict[str, SymbolEntry] = Field(default_factory=dict)

    def contains(self, symbol_name: str) -> bool:
        """Check if symbol exists in table."""
        return symbol_name in self.symbols
