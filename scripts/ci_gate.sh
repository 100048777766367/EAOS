#!/bin/sh
set -e
echo "===================================================="
echo " EAOS Continuous Integration Quality Gate Runner"
echo "===================================================="
uv run task lint
uv run task test
uv run task validate
echo "✔ All CI quality gates passed 100%!"