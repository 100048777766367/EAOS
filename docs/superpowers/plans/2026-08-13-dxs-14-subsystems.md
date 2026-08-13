# DXS 14 Subsystems Implementation Plan

**Goal:** Establish all 14 DXS boundaries, shared contracts, a working Doctor vertical slice, and safe scaffolding.

**Architecture:** RTK remains governance/rule authority. DXS executes developer workflows through contracts. Initial flow: CLI → Doctor → Repository Context → Diagnostics → Evidence.

**Verification:** `ruff format dxs tests/dxs`, `ruff check dxs tests/dxs`, `mypy dxs`, `pytest tests/dxs -q`.

**Non-destructive rule:** Existing EAOS files must not be overwritten when integrating this package.
