-- EAOS PostgreSQL 16 Initial Infrastructure Bootstrapper
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE SCHEMA IF NOT EXISTS eaos_core;

CREATE TABLE IF NOT EXISTS eaos_core.health_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    system_id VARCHAR(64) NOT NULL,
    health_score INT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);