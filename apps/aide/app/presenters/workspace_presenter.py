"""Presentation model for the AIDE engineering surface."""

from typing import Final

AIDE_DOMAINS: Final[list[dict[str, str]]] = [
    {"id": "01", "name": "Workspace / IDE", "mode": "AIDE-owned UI"},
    {"id": "02", "name": "AI / Copilot", "mode": "Gateway consumer"},
    {"id": "03", "name": "Agent Engineering", "mode": "Gateway consumer"},
    {"id": "04", "name": "Source Control", "mode": "AIDE UI surface"},
    {"id": "05", "name": "Code Hosting", "mode": "Integration surface"},
    {"id": "06", "name": "Software Delivery", "mode": "Gateway consumer"},
    {"id": "07", "name": "Runtime / Operations", "mode": "Platform consumer"},
    {"id": "08", "name": "Governance / Control", "mode": "Gateway consumer"},
    {"id": "09", "name": "Evidence / Assurance", "mode": "Gateway consumer"},
    {"id": "10", "name": "Knowledge / Memory", "mode": "Platform consumer"},
    {"id": "11", "name": "Observability", "mode": "Gateway consumer"},
    {"id": "12", "name": "Ecosystem / Platform", "mode": "External links"},
    {"id": "13", "name": "Architecture", "mode": "Knowledge consumer"},
    {"id": "14", "name": "Security", "mode": "Governed surface"},
    {"id": "15", "name": "Evolution / Change", "mode": "Gateway consumer"},
    {"id": "16", "name": "Enterprise Context", "mode": "Context surface"},
]


def build_domain_surface() -> list[dict[str, str]]:
    """Return the enterprise engineering domains shown by AIDE."""

    return AIDE_DOMAINS
