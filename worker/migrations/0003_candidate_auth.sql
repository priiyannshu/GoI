-- ============================================================================
-- Candidate Authentication & Unique Identity Mapping Table
-- Target Engine: Cloudflare D1 Serverless SQLite
-- File: worker/migrations/0003_candidate_auth.sql
-- ============================================================================

CREATE TABLE IF NOT EXISTS candidate_accounts (
    account_id TEXT PRIMARY KEY,
    candidate_name TEXT NOT NULL,
    pin_hash TEXT NOT NULL,
    unique_candidate_id TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_cand_name ON candidate_accounts(candidate_name);
CREATE INDEX IF NOT EXISTS idx_cand_name_pin ON candidate_accounts(candidate_name, pin_hash);
CREATE INDEX IF NOT EXISTS idx_cand_unique_id ON candidate_accounts(unique_candidate_id);
