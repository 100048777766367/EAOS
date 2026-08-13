"""Digital Twin What-If Simulation Engine."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from digitaltwin.models.twin_models import EnterpriseTwinStateDTO

_SCENARIO_CONFIG: dict[str, dict[str, object]] = {
    "DEPLOY_PATCH": {
        "risk_level": "LOW",
        "health_delta": 0.0,
        "policy_compliant": True,
        "recommendation": "Patch deployment is safe. Blast radius LOCAL.",
    },
    "REFACTOR_DOMAIN": {
        "risk_level": "MEDIUM",
        "health_delta": -5.0,
        "policy_compliant": True,
        "recommendation": "Proceed with integration test gate before merge.",
    },
    "MASS_REPAIR": {
        "risk_level": "HIGH",
        "health_delta": -15.0,
        "policy_compliant": False,
        "recommendation": "Requires L5_RECOVER authority. Run architecture tests first.",
    },
    "ARCHITECTURE_REWRITE": {
        "risk_level": "CRITICAL",
        "health_delta": -30.0,
        "policy_compliant": False,
        "recommendation": "Requires human sign-off. Do not proceed autonomously.",
    },
}


class TwinSimulationResultDTO(BaseModel):
    """Result of a what-if simulation scenario on Digital Twin."""

    model_config = ConfigDict(frozen=True)

    scenario_name: str
    predicted_health_score: float
    risk_level: str = Field(default="LOW")
    policy_compliant: bool = Field(default=True)
    recommendation: str = Field(default="Safe to proceed with deployment.")


class EnterpriseTwinSimulationEngine:
    """Engine simulating architectural changes on Digital Twin."""

    def run_what_if_simulation(self, state: EnterpriseTwinStateDTO, scenario_name: str) -> TwinSimulationResultDTO:
        """Run simulation on current twin state against named scenario."""
        config = _SCENARIO_CONFIG.get(scenario_name.upper())

        if state.overall_health_score < 80.0:
            return TwinSimulationResultDTO(
                scenario_name=scenario_name,
                predicted_health_score=state.overall_health_score - 10.0,
                risk_level="HIGH",
                policy_compliant=False,
                recommendation="Abort deployment: Twin health already degraded.",
            )

        if config is None:
            return TwinSimulationResultDTO(
                scenario_name=scenario_name,
                predicted_health_score=state.overall_health_score,
                risk_level="LOW",
                policy_compliant=True,
                recommendation=f"Unknown scenario '{scenario_name}'. Simulated with default safe assumption.",
            )

        delta = float(config["health_delta"])  # type: ignore[arg-type]
        return TwinSimulationResultDTO(
            scenario_name=scenario_name,
            predicted_health_score=max(0.0, state.overall_health_score + delta),
            risk_level=str(config["risk_level"]),
            policy_compliant=bool(config["policy_compliant"]),
            recommendation=str(config["recommendation"]),
        )
