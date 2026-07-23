"""Security router handling Kyber768 encryption, WAF, ZKP, and SIEM."""

from typing import Annotated, Any

from fastapi import APIRouter, Body
from platform_services.security.cloudflare_waf_driver import (
    CloudflareWAFDriver,
)
from platform_services.security.post_quantum_signer import (
    PostQuantumSignerEngine,
    ZKAttestationProof,
)
from platform_services.security.quantum_envelope import (
    EncryptedEnvelopeDTO,
    QuantumEnvelopeEncryptionEngine,
)
from platform_services.security.wazuh_mtls_adapter import (
    WazuhMTLSSyslogAdapter,
)

router = APIRouter(prefix="", tags=["Security"])
quantum_engine = QuantumEnvelopeEncryptionEngine()
waf_driver = CloudflareWAFDriver()
syslog_adapter = WazuhMTLSSyslogAdapter()
signer_engine = PostQuantumSignerEngine()


@router.post(
    "/security/quantum/encrypt-envelope",
    response_model=EncryptedEnvelopeDTO,
    status_code=201,
)
async def encrypt_quantum_envelope(
    request: dict[str, Any] | None = None,
    secret_data: Annotated[str | None, Body(embed=True)] = None,
    public_key_fingerprint: Annotated[str | None, Body(embed=True)] = None,
) -> EncryptedEnvelopeDTO:
    secret = secret_data
    fingerprint = public_key_fingerprint
    if isinstance(request, dict):
        if not secret:
            secret = str(request.get("secret_data", ""))
        if not fingerprint:
            fingerprint = str(request.get("public_key_fingerprint", ""))
    return quantum_engine.encrypt_secret_payload(
        secret_data=secret or "",
        public_key_fingerprint=fingerprint or "",
    )


@router.post("/security/wazuh/syslog-hmac")
async def sign_wazuh_syslog_payload(
    request: dict[str, Any] | None = None,
    log_data: Annotated[dict[str, Any] | None, Body(embed=True)] = None,
    secret_key: Annotated[str | None, Body(embed=True)] = None,
) -> Any:
    data = log_data
    key = secret_key
    if isinstance(request, dict):
        if not data:
            data = request.get("log_data", {})
        if not key:
            key = str(request.get("secret_key", "default_secret"))

    return syslog_adapter.format_signed_syslog(
        log_data=data or {},
        secret_key=key or "default_secret",
    )


@router.post("/security/cloudflare/block-cooldown")
async def block_cloudflare_ip_cooldown(
    request: dict[str, Any] | None = None,
    ip: Annotated[str | None, Body(embed=True)] = None,
    ttl_seconds: Annotated[int | None, Body(embed=True)] = 3600,
) -> Any:
    ip_addr = ip
    ttl = ttl_seconds
    if isinstance(request, dict):
        if not ip_addr:
            ip_addr = str(request.get("ip", "192.168.1.1"))
        if ttl is None:
            ttl = int(request.get("ttl_seconds", 3600))

    return waf_driver.block_ip_with_cooldown(
        ip=ip_addr or "192.168.1.1",
        ttl_seconds=ttl if ttl is not None else 3600,
    )


@router.post("/security/wazuh/stream-event")
async def stream_wazuh_siem_event(
    event_payload: dict[str, Any],
) -> dict[str, Any]:
    alert = syslog_adapter.stream_audit_event(event_payload)
    return {"status": "STREAMED", "alert": alert.model_dump()}


@router.post("/security/cloudflare/block-ip")
async def block_cloudflare_ip(
    ip_address: Annotated[str, Body(embed=True)],
) -> dict[str, Any]:
    rule = waf_driver.block_malicious_ip(ip_address)
    return {"status": "BLOCKED", "rule": rule.model_dump()}


@router.post("/security/zkp/attest-proof")
async def generate_zkp_attest_proof(
    request: dict[str, Any] | None = None,
    artifact_id: Annotated[str | None, Body(embed=True)] = None,
    payload: Annotated[str | None, Body(embed=True)] = None,
) -> ZKAttestationProof:
    a_id = artifact_id
    p_load = payload
    if isinstance(request, dict):
        if not a_id:
            a_id = str(request.get("artifact_id", "artifact_1"))
        if not p_load:
            p_load = str(request.get("payload", "dummy_payload"))

    return signer_engine.generate_compliance_proof(
        artifact_id=a_id or "artifact_1",
        payload_data=p_load or "dummy_payload",
    )


@router.post("/security/vault/rotate-secret")
async def rotate_vault_ephemeral_secret(
    request: dict[str, Any] | None = None,
    secret_path: Annotated[str | None, Body(embed=True)] = None,
    ttl_sec: Annotated[int | None, Body(embed=True)] = 3600,
) -> dict[str, Any]:
    s_path = secret_path
    ttl = ttl_sec
    if isinstance(request, dict):
        if not s_path:
            s_path = str(request.get("secret_path", "secret/data/db"))
        if ttl is None:
            ttl = int(request.get("ttl_sec", 3600))

    from platform_services.security.vault_ephemeral import (
        VaultEphemeralSigner,
    )

    signer = VaultEphemeralSigner()
    token = signer.generate_ephemeral_token(
        secret_path=s_path or "secret/data/db",
        ttl_sec=ttl if ttl is not None else 3600,
    )
    return token.model_dump()
