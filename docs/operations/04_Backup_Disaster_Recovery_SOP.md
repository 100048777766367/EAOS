# 04. EAOS Backup & Disaster Recovery SOP

## 1. PostgreSQL Database Backup & Restore

* **Backup Command:**
  `docker exec eaos-postgres-prod pg_dump -U eaos -d eaos > runtime/backups/postgres_backup.sql`
* **Restore Command:**
  `cat runtime/backups/postgres_backup.sql | docker exec -i eaos-postgres-prod psql -U eaos -d eaos`

---

## 2. Neo4j Graph Database Backup

* **Backup Command:**
  `docker exec eaos-neo4j-prod neo4j-admin database dump neo4j --to-path=/data/backups/`

---

## 3. Disaster Recovery RPO / RTO Targets

* **RPO (Recovery Point Objective):** < **1 hour** (Data loss window).
* **RTO (Recovery Time Objective):** < **15 minutes** (Downtime window).
