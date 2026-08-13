from opentelemetry.sdk.resources import Resource

"""OpenTelemetry resource attributes factory for EAOS."""


def create_eaos_resource(
    service_name: str = "eaos-core",
    environment: str = "production",
) -> Resource:
    """Creates an OpenTelemetry Resource with EAOS Enterprise metadata."""
    return Resource.create(
        {
            "service.name": service_name,
            "deployment.environment": environment,
            "enterprise.system": "EAOS",
            "enterprise.version": "3.0.0",
        }
    )
