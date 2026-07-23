"""Specification and rule AST parser engine for EAOS."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ParsedRuleDTO(BaseModel):
    """Value object representing a parsed specification rule."""

    model_config = ConfigDict(frozen=True)

    rule_id: str
    expression: str
    error_message: str


class ParsedSpecDTO(BaseModel):
    """Value object containing full parsed specification AST."""

    model_config = ConfigDict(frozen=True)

    spec_id: str
    spec_name: str
    rules: list[ParsedRuleDTO]


class SpecificationParserEngine:
    """Parser engine parsing raw YAML/JSON specs into structured DTOs."""

    def parse_raw_dict(
        self,
        raw_spec: dict[str, Any],
    ) -> ParsedSpecDTO:
        """Parses dictionary payload into typed specification DTO."""
        raw_rules = raw_spec.get("rules", [])
        parsed_rules = [
            ParsedRuleDTO(
                rule_id=str(r.get("id", f"R_{idx}")),
                expression=str(r.get("expression", "True")),
                error_message=str(r.get("error_message", "Rule failed")),
            )
            for idx, r in enumerate(raw_rules, start=1)
        ]

        return ParsedSpecDTO(
            spec_id=str(raw_spec.get("id", "spec.default")),
            spec_name=str(raw_spec.get("name", "Default Specification")),
            rules=parsed_rules,
        )
