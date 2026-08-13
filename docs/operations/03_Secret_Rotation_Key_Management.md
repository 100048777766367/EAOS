# 03. EAOS Secret Rotation & Key Management SOP

## 1. Secret Rotation Schedule

* **JWT & API Secrets:** Rotated every **30 days**.
* **Database Credentials:** Rotated every **90 days**.
* **Post-Quantum Kyber768 Key Pairs:** Rotated every **180 days**.

---

## 2. Step-by-Step Database Password Rotation

1. Generate new strong password in PowerShell:
   `$newPass = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 24 | % {[char]$_})`
2. Update `.env` file with `DB_PASSWORD=$newPass`.
3. Update Postgres user password in container:
   `docker exec -it eaos-postgres-prod psql -U eaos -c "ALTER USER eaos WITH PASSWORD '$newPass';"`
4. Restart API Gateway service:
   `uv run python -m tools.cli.main runtime`
