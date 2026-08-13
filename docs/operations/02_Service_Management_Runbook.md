# 02. EAOS 24/7 Container Stack Service Management Runbook

## Daily Operational Routine

1. **Morning Check (08:00 AM):**
   - Execute Doctor CLI: `uv run python -m tools.cli.main doctor`
   - Verify all 10 services report `PASS` or `WARN` status.
2. **Mid-day Monitoring:**
   - Access Grafana Dashboard (`http://localhost:3000`).
   - Monitor CPU, Memory, and RAG Vector Retrieval Latency.
3. **Evening Maintenance (05:00 PM):**
   - Check backup log artifacts in `runtime/backups/`.

---

## Service Restart Command Reference

| Service | Port | Restart Command | Health Probe Command |
| :--- | :--- | :--- | :--- |
| **PostgreSQL 16** | 5433 | `docker restart eaos-postgres-prod` | `docker exec eaos-postgres-prod pg_isready -U eaos` |
| **Redis 7** | 6380 | `docker restart eaos-redis-prod` | `docker exec eaos-redis-prod redis-cli ping` |
| **Neo4j Graph** | 7474 | `docker restart eaos-neo4j-prod` | `curl -f http://localhost:7474` |
| **MinIO S3** | 9001 | `docker restart eaos-minio-prod` | `curl -f http://localhost:9000/minio/health/live` |
| **Qdrant Vector** | 6333 | `docker restart eaos-qdrant-prod` | `curl -f http://localhost:6333/healthz` |
| **Ollama AI** | 11434 | `docker restart eaos-ollama-prod` | `curl -f http://localhost:11434/api/tags` |
