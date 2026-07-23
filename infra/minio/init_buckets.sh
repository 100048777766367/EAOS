#!/bin/sh
# Initialize default EAOS S3 buckets
mc alias set myminio http://localhost:9000 eaos_admin eaos_minio_pass_2026
mc mb myminio/eaos-artifacts --ignore-existing
mc mb myminio/eaos-backups --ignore-existing