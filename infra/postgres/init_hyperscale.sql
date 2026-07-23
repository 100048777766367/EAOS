-- EAOS Hyperscale PostgreSQL Schema Initialization & RLS Policies
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE TABLE IF NOT EXISTS enterprise_tenants (
    tenant_id VARCHAR(64) PRIMARY KEY,
    tenant_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tenant_documents (
    doc_id VARCHAR(64) PRIMARY KEY,
    tenant_id VARCHAR(64) NOT NULL REFERENCES enterprise_tenants(tenant_id),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE tenant_documents ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON tenant_documents
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant', true));

CREATE INDEX IF NOT EXISTS idx_tenant_docs_hnsw
    ON tenant_documents USING hnsw (embedding vector_cosine_ops);