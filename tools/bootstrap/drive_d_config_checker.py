import os

from pydantic import BaseModel, ConfigDict

"""Drive D: Environment Variable & Path Inspector for EAOS."""


class DriveDEnvCheckDTO(BaseModel):
    """Value object representing drive D: environment variable status."""

    model_config = ConfigDict(frozen=True)

    var_name: str
    current_value: str
    is_on_drive_d: bool


class DriveDEnvironmentInspector:
    """Inspector checking that model and cache paths point to D: drive."""

    TARGET_VARS: tuple[str, ...] = (
        "OLLAMA_MODELS",
        "UV_CACHE_DIR",
        "PIP_CACHE_DIR",
        "HF_HOME",
    )

    def inspect_drive_d_settings(self) -> list[DriveDEnvCheckDTO]:
        """Audits active system environment variables for drive D:."""
        results: list[DriveDEnvCheckDTO] = []
        for var in self.TARGET_VARS:
            val = os.getenv(var, "NOT_SET")
            is_d = val.upper().startswith("D:")
            results.append(
                DriveDEnvCheckDTO(
                    var_name=var,
                    current_value=val,
                    is_on_drive_d=is_d,
                )
            )
        return results


if __name__ == "__main__":
    inspector = DriveDEnvironmentInspector()
    checks = inspector.inspect_drive_d_settings()
    print("====================================================")
    print(" EAOS DRIVE D: ENVIRONMENT VARIABLE AUDIT           ")
    print("====================================================")
    for c in checks:
        icon = "✔" if c.is_on_drive_d else "✖"
        print(f"{icon} {c.var_name:<15} : {c.current_value}")
    print("====================================================")
