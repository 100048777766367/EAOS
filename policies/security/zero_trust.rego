package eaos.security.authz

default allow = false

allow {
    input.role == "admin"
    input.environment == "production"
}

allow {
    input.tenant_id != ""
    input.action == "read"
}