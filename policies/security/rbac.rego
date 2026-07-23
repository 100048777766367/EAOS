package eaos.authz

default allow = false

allow {
    input.role == "admin"
}