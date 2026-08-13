from typing import ClassVar

from pydantic import BaseModel, ConfigDict

"""Framework View Translator rendering EAOS into TOGAF/ArchiMate/Zachman."""


class FrameworkViewProjectionDTO(BaseModel):
    """Value object representing a framework-specific view projection."""

    model_config = ConfigDict(frozen=True)

    framework_name: str
    viewpoint: str
    projected_artifacts: list[str]


class FrameworkViewTranslator:
    """Translator mapping EAOS Unified Meta-Model into standard views."""

    SUPPORTED_FRAMEWORKS: ClassVar[tuple[str, ...]] = (
        "TOGAF",
        "ZACHMAN",
        "ARCHIMATE",
        "SABSA",
        "RM-ODP",
    )

    def project_view(self, framework_name: str, viewpoint: str) -> FrameworkViewProjectionDTO:
        """Projects EAOS architecture into target framework perspective."""
        name_upper = framework_name.upper()

        if name_upper == "TOGAF":
            artifacts = [
                "Business Architecture (capabilities/)",
                "Information Architecture (data/)",
                "Application Architecture (apps/ & packages/)",
                "Technology Architecture (infra/ & platform/)",
            ]
        elif name_upper == "ZACHMAN":
            artifacts = [
                "What: Data Models (packages/*/domain)",
                "How: Workflows & Use Cases (packages/*/application)",
                "Where: Network & Infra (infra/)",
                "Who: Identity & IAM (packages/identity)",
                "When: Schedulers & SRE (operations/)",
                "Why: Architecture Constitution (ARCHITECTURE_CONSTITUTION.md)",
            ]
        elif name_upper == "ARCHIMATE":
            artifacts = [
                "Business Layer: Business Capabilities & Services",
                "Application Layer: Application Components & Interfaces",
                "Technology Layer: Infrastructure Nodes & Devices",
            ]
        else:
            artifacts = [f"Generic Projection for {framework_name}"]

        return FrameworkViewProjectionDTO(
            framework_name=framework_name,
            viewpoint=viewpoint,
            projected_artifacts=artifacts,
        )


if __name__ == "__main__":
    translator = FrameworkViewTranslator()
    proj = translator.project_view("TOGAF", "ADM Architecture Development")
    print(f"✔ Projected Framework View: {proj.framework_name}")
