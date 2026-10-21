-- ============================================================================
-- INDIA GRADE A GOVERNMENT EXAMINATIONS RESEARCH DATABASE SCHEMA
-- Target Database: SQLite 3.38+ with Foreign Keys & JSON Validations
-- File: data/schema.sql
-- ============================================================================

PRAGMA foreign_keys = ON;

-- 1. Core Exam Master Table
CREATE TABLE IF NOT EXISTS exams (
    exam_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL CHECK (category IN ('Central-Civil', 'Regulatory', 'Defense', 'State-PSC', 'PSU')),
    administering_body TEXT NOT NULL,
    frequency TEXT NOT NULL CHECK (frequency IN ('Annual', 'Bi-annual', 'Periodic')),
    official_website TEXT NOT NULL,
    latest_official_notification_url TEXT NOT NULL,
    latest_gazette_ref TEXT,
    tentative_timeline_2027 JSON NOT NULL CHECK (json_valid(tentative_timeline_2027)),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_exams_category ON exams(category);
CREATE INDEX IF NOT EXISTS idx_exams_cat ON exams(category);
CREATE INDEX IF NOT EXISTS idx_exams_admin_body ON exams(administering_body);

-- 2. Comprehensive Eligibility Rules Table
CREATE TABLE IF NOT EXISTS eligibility_criteria (
    exam_id TEXT PRIMARY KEY,
    cutoff_reference_date_rule TEXT NOT NULL,
    min_age_gen INTEGER NOT NULL CHECK (min_age_gen >= 16 AND min_age_gen <= 35),
    max_age_gen INTEGER NOT NULL CHECK (max_age_gen >= 20 AND max_age_gen <= 50),
    relaxations_json JSON NOT NULL CHECK (json_valid(relaxations_json)),
    min_education_level TEXT NOT NULL CHECK (min_education_level IN ('Bachelor', 'Bachelor_Tech', 'Master', 'Specific_BTech', 'Specific_Degree')),
    accepted_disciplines JSON NOT NULL CHECK (json_valid(accepted_disciplines)),
    min_aggregate_percentage_gen REAL DEFAULT 0 CHECK (min_aggregate_percentage_gen >= 0 AND min_aggregate_percentage_gen <= 100),
    min_aggregate_percentage_reserved REAL DEFAULT 0 CHECK (min_aggregate_percentage_reserved >= 0 AND min_aggregate_percentage_reserved <= 100),
    final_year_students_allowed BOOLEAN NOT NULL DEFAULT 1 CHECK (final_year_students_allowed IN (0, 1)),
    attempt_limit_gen INTEGER CHECK (attempt_limit_gen IS NULL OR attempt_limit_gen > 0),
    attempt_limit_obc INTEGER CHECK (attempt_limit_obc IS NULL OR attempt_limit_obc > 0),
    attempt_limit_sc_st INTEGER CHECK (attempt_limit_sc_st IS NULL OR attempt_limit_sc_st > 0),
    domicile_restrictions JSON CHECK (domicile_restrictions IS NULL OR json_valid(domicile_restrictions)),
    language_requirements JSON CHECK (language_requirements IS NULL OR json_valid(language_requirements)),
    physical_standards JSON CHECK (physical_standards IS NULL OR json_valid(physical_standards)),
    source_citation_clause TEXT NOT NULL,
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_eligibility_age ON eligibility_criteria(min_age_gen, max_age_gen);

-- 3. Universal Master Syllabus Ontology Table
CREATE TABLE IF NOT EXISTS syllabus_taxonomy (
    topic_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL CHECK (domain IN ('General Studies', 'Quantitative Aptitude', 'Reasoning', 'English', 'Economics & Finance', 'Technical')),
    sub_domain TEXT NOT NULL,
    topic_title TEXT NOT NULL,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_syllabus_domain ON syllabus_taxonomy(domain, sub_domain);

-- 4. Exam to Syllabus Mapping Table
CREATE TABLE IF NOT EXISTS exam_syllabus_map (
    exam_id TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    depth_level TEXT NOT NULL CHECK (depth_level IN ('Foundation', 'Intermediate', 'Advanced', 'Analytical')),
    is_optional BOOLEAN NOT NULL DEFAULT 0 CHECK (is_optional IN (0, 1)),
    weightage_pct_estimate REAL CHECK (weightage_pct_estimate IS NULL OR (weightage_pct_estimate >= 0 AND weightage_pct_estimate <= 100)),
    source_clause_ref TEXT,
    PRIMARY KEY(exam_id, stage_name, topic_id),
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE,
    FOREIGN KEY(topic_id) REFERENCES syllabus_taxonomy(topic_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_map_exam ON exam_syllabus_map(exam_id);
CREATE INDEX IF NOT EXISTS idx_map_topic ON exam_syllabus_map(topic_id);

-- 5. Verifiable Source Audit Log Table
CREATE TABLE IF NOT EXISTS source_audit_log (
    audit_id TEXT PRIMARY KEY,
    exam_id TEXT NOT NULL,
    fact_type TEXT NOT NULL CHECK (fact_type IN ('Age_Limit', 'Education', 'Syllabus', 'Pattern', 'Timeline_2027', 'Physical_Standards', 'Reservation_Rules')),
    official_document_title TEXT NOT NULL,
    document_date TEXT NOT NULL,
    clause_or_page_number TEXT NOT NULL,
    official_download_link TEXT NOT NULL,
    archive_link TEXT,
    verifier_notes TEXT,
    verified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(exam_id) REFERENCES exams(exam_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_audit_exam_fact ON source_audit_log(exam_id, fact_type);
CREATE INDEX IF NOT EXISTS idx_audit_exam ON source_audit_log(exam_id, fact_type);

-- 6. User Profiles (Local & Cloudflare D1 Compatible)
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    dob TEXT NOT NULL, -- YYYY-MM-DD
    gender TEXT NOT NULL CHECK (gender IN ('MALE', 'FEMALE', 'OTHER')),
    category TEXT NOT NULL CHECK (category IN ('GEN', 'OBC_NCL', 'SC', 'ST', 'EWS', 'PwBD')),
    graduation_degree TEXT NOT NULL,
    graduation_discipline TEXT NOT NULL,
    graduation_aggregate_pct REAL NOT NULL CHECK (graduation_aggregate_pct >= 0 AND graduation_aggregate_pct <= 100),
    is_final_year BOOLEAN NOT NULL DEFAULT 0 CHECK (is_final_year IN (0, 1)),
    state_domicile TEXT NOT NULL,
    mother_tongue TEXT,
    height_cm REAL,
    chest_cm REAL,
    vision_specs TEXT,
    prior_attempts_json JSON CHECK (prior_attempts_json IS NULL OR json_valid(prior_attempts_json)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_dob ON user_profiles(dob);
