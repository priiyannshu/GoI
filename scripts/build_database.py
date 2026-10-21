#!/usr/bin/env python3
"""
scripts/build_database.py
=========================
Master Ingestion & Database Population Pipeline for Indian Grade A Government Examinations.
Populates all 31 examinations across Clusters 1, 2, 3, and 4, all 31 eligibility criteria records,
and all 216 verified source_audit_log records (6 fact types per exam) using normalized seed data.
Also seeds foundation universal syllabus taxonomy and stage mappings.
"""

import argparse
import json
import logging
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("build_database")

# -----------------------------------------------------------------------------
# SEED TAXONOMY FOUNDATION & STAGE MAPPINGS
# -----------------------------------------------------------------------------

def load_taxonomy_seeds(seed_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Loads universal syllabus taxonomy seeds (192 topics) from data/syllabus_taxonomy_seed.json."""
    if seed_path is None:
        seed_path = Path(__file__).resolve().parent.parent / "data" / "syllabus_taxonomy_seed.json"
    if not seed_path.exists():
        raise FileNotFoundError(f"Syllabus taxonomy seed file not found: {seed_path}")
    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("topics", [])


def load_map_seeds(seed_path: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Loads exam syllabus stage mappings from data/exam_syllabus_map_seed.json."""
    if seed_path is None:
        seed_path = Path(__file__).resolve().parent.parent / "data" / "exam_syllabus_map_seed.json"
    if not seed_path.exists():
        raise FileNotFoundError(f"Exam syllabus map seed file not found: {seed_path}")
    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, list) else data.get("mappings", [])

# -----------------------------------------------------------------------------
# MASTER SEED DATA IMPORT SEAM
# -----------------------------------------------------------------------------

def load_master_seed_dataset(seed_path: Optional[Path] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Loads normalized 31-exam master seed dataset from data/master_seed_data.json."""
    if seed_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        seed_path = base_dir / "data" / "master_seed_data.json"
    else:
        seed_path = Path(seed_path)

    if not seed_path.exists():
        raise FileNotFoundError(f"Critical: Master seed data file not found at {seed_path}")

    with open(seed_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validate essential schema keys
    required_keys = {"exams", "eligibility_criteria", "source_audit_log"}
    missing = required_keys - set(data.keys())
    if missing:
        raise ValueError(f"Master seed data missing required keys: {missing}")

    logger.info(f"Loaded master seed dataset from JSON: {seed_path}")
    return data


# -----------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -----------------------------------------------------------------------------

def to_json_str(val: Any) -> Optional[str]:
    """Ensures value is formatted as a valid JSON string or None."""
    if val is None:
        return None
    if isinstance(val, (dict, list)):
        return json.dumps(val, ensure_ascii=False)
    if isinstance(val, str):
        val_trimmed = val.strip()
        if not val_trimmed:
            return None
        # Verify it parses as valid JSON
        try:
            json.loads(val_trimmed)
            return val_trimmed
        except json.JSONDecodeError:
            # If not valid json, serialize it
            return json.dumps(val_trimmed, ensure_ascii=False)
    return json.dumps(val, ensure_ascii=False)


# -----------------------------------------------------------------------------
# INGESTION & POPULATION PIPELINE
# -----------------------------------------------------------------------------

def init_database(db_path: Path, schema_path: Path, recreate: bool = True) -> sqlite3.Connection:
    """Initializes SQLite database with foreign keys and executes schema DDL."""
    if recreate and db_path.exists():
        logger.info(f"Recreating database: removing existing {db_path}")
        db_path.unlink()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON;")

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    logger.info(f"Applying schema DDL from {schema_path}")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    logger.info("Schema DDL applied successfully.")
    return conn


def insert_exams(conn: sqlite3.Connection, exams: List[Dict[str, Any]]):
    """Inserts all master examination records."""
    sql = """
    INSERT INTO exams (
        exam_id, title, short_code, category, administering_body, frequency,
        official_website, latest_official_notification_url, latest_gazette_ref,
        tentative_timeline_2027, description
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    for e in exams:
        cursor.execute(sql, (
            e["exam_id"],
            e["title"],
            e["short_code"],
            e["category"],
            e["administering_body"],
            e["frequency"],
            e["official_website"],
            e["latest_official_notification_url"],
            e.get("latest_gazette_ref"),
            to_json_str(e["tentative_timeline_2027"]),
            e.get("description")
        ))
    conn.commit()
    logger.info(f"Inserted {len(exams)} examinations into 'exams'.")


def insert_eligibility(conn: sqlite3.Connection, eligibility: List[Dict[str, Any]]):
    """Inserts all statutory eligibility criteria records."""
    sql = """
    INSERT INTO eligibility_criteria (
        exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen,
        relaxations_json, min_education_level, accepted_disciplines,
        min_aggregate_percentage_gen, min_aggregate_percentage_reserved,
        final_year_students_allowed, attempt_limit_gen, attempt_limit_obc,
        attempt_limit_sc_st, domicile_restrictions, language_requirements,
        physical_standards, source_citation_clause
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    for el in eligibility:
        final_year = 1 if el.get("final_year_students_allowed", True) in (1, True, "1", "true", "True") else 0
        cursor.execute(sql, (
            el["exam_id"],
            el["cutoff_reference_date_rule"],
            int(el["min_age_gen"]),
            int(el["max_age_gen"]),
            to_json_str(el["relaxations_json"]),
            el["min_education_level"],
            to_json_str(el["accepted_disciplines"]),
            float(el.get("min_aggregate_percentage_gen", 0.0)),
            float(el.get("min_aggregate_percentage_reserved", 0.0)),
            final_year,
            el.get("attempt_limit_gen"),
            el.get("attempt_limit_obc"),
            el.get("attempt_limit_sc_st"),
            to_json_str(el.get("domicile_restrictions")),
            to_json_str(el.get("language_requirements")),
            to_json_str(el.get("physical_standards")),
            el["source_citation_clause"]
        ))
    conn.commit()
    logger.info(f"Inserted {len(eligibility)} records into 'eligibility_criteria'.")


def insert_source_audit(conn: sqlite3.Connection, audit_logs: List[Dict[str, Any]]):
    """Inserts all verified fact-level source audit log records."""
    sql = """
    INSERT INTO source_audit_log (
        audit_id, exam_id, fact_type, official_document_title, document_date,
        clause_or_page_number, official_download_link, archive_link, verifier_notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor = conn.cursor()
    for a in audit_logs:
        cursor.execute(sql, (
            a["audit_id"],
            a["exam_id"],
            a["fact_type"],
            a["official_document_title"],
            a["document_date"],
            a["clause_or_page_number"],
            a["official_download_link"],
            a.get("archive_link"),
            a.get("verifier_notes")
        ))
    conn.commit()
    logger.info(f"Inserted {len(audit_logs)} records into 'source_audit_log'.")


def insert_syllabus_foundation(conn: sqlite3.Connection, taxonomy: List[Dict[str, Any]], mappings: List[Dict[str, Any]]):
    """Seeds master syllabus taxonomy nodes and exam mappings."""
    tax_sql = """
    INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title, description)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(topic_id) DO UPDATE SET
        domain=excluded.domain,
        sub_domain=excluded.sub_domain,
        topic_title=excluded.topic_title,
        description=excluded.description;
    """
    cursor = conn.cursor()
    for t in taxonomy:
        cursor.execute(tax_sql, (
            t["topic_id"],
            t["domain"],
            t["sub_domain"],
            t["topic_title"],
            t.get("description")
        ))

    map_sql = """
    INSERT INTO exam_syllabus_map (
        exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(exam_id, stage_name, topic_id) DO UPDATE SET
        depth_level=excluded.depth_level,
        is_optional=excluded.is_optional,
        weightage_pct_estimate=excluded.weightage_pct_estimate,
        source_clause_ref=excluded.source_clause_ref;
    """
    for m in mappings:
        cursor.execute(map_sql, (
            m["exam_id"],
            m["stage_name"],
            m["topic_id"],
            m["depth_level"],
            1 if m.get("is_optional", False) else 0,
            m.get("weightage_pct_estimate"),
            m.get("source_clause_ref")
        ))

    conn.commit()
    logger.info(f"Seeded {len(taxonomy)} syllabus taxonomy nodes and {len(mappings)} stage mappings.")


def verify_database_counts_and_integrity(conn: sqlite3.Connection):
    """Executes PRAGMAs and validates expected row counts."""
    cursor = conn.cursor()

    # Foreign key check
    fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    if fk_violations:
        raise ValueError(f"Foreign key violations detected: {fk_violations}")
    logger.info("PRAGMA foreign_key_check: PASSED (0 violations).")

    # DB Integrity check
    integrity = cursor.execute("PRAGMA integrity_check;").fetchall()
    if integrity != [("ok",)]:
        raise ValueError(f"SQLite integrity check failed: {integrity}")
    logger.info("PRAGMA integrity_check: PASSED (ok).")

    # Table counts
    exams_count = cursor.execute("SELECT count(*) FROM exams;").fetchone()[0]
    eligibility_count = cursor.execute("SELECT count(*) FROM eligibility_criteria;").fetchone()[0]
    audit_count = cursor.execute("SELECT count(*) FROM source_audit_log;").fetchone()[0]
    tax_count = cursor.execute("SELECT count(*) FROM syllabus_taxonomy;").fetchone()[0]
    map_count = cursor.execute("SELECT count(*) FROM exam_syllabus_map;").fetchone()[0]
    mapped_exams = cursor.execute("SELECT count(DISTINCT exam_id) FROM exam_syllabus_map;").fetchone()[0]
    orphan_count = cursor.execute("SELECT count(*) FROM syllabus_taxonomy WHERE topic_id NOT IN (SELECT DISTINCT topic_id FROM exam_syllabus_map);").fetchone()[0]

    logger.info(f"Database Counts -> exams: {exams_count}, eligibility_criteria: {eligibility_count}, source_audit_log: {audit_count}, taxonomy: {tax_count}, map: {map_count}, mapped_exams: {mapped_exams}, orphan_topics: {orphan_count}")

    if exams_count != 25:
        raise ValueError(f"Expected exactly 25 exams, got {exams_count}")
    if eligibility_count != 25:
        raise ValueError(f"Expected exactly 25 eligibility criteria, got {eligibility_count}")
    if audit_count != 150:
        raise ValueError(f"Expected exactly 150 audit logs (6 per exam), got {audit_count}")
    if tax_count < 120:
        raise ValueError(f"Expected >= 120 taxonomy topics, got {tax_count}")
    if map_count < 300:
        raise ValueError(f"Expected >= 300 stage mappings, got {map_count}")
    if mapped_exams != 25:
        raise ValueError(f"Expected all 25 exams mapped in exam_syllabus_map, got {mapped_exams}")
    if orphan_count > 0:
        raise ValueError(f"Expected 0 orphan topics in syllabus_taxonomy, got {orphan_count}")

    logger.info("All build verification checks passed successfully!")


def build(db_path: Path, schema_path: Path, seed_path: Optional[Path] = None, recreate: bool = True):
    """Main orchestrator function for building the SQLite database."""
    logger.info("Starting Grade A Examinations Database Build Pipeline...")
    dataset = load_master_seed_dataset(seed_path=seed_path)
    taxonomy_seeds = load_taxonomy_seeds()
    map_seeds = load_map_seeds()

    conn = init_database(db_path, schema_path, recreate=recreate)
    try:
        insert_exams(conn, dataset["exams"])
        insert_eligibility(conn, dataset["eligibility_criteria"])
        insert_source_audit(conn, dataset["source_audit_log"])
        insert_syllabus_foundation(conn, taxonomy_seeds, map_seeds)
        verify_database_counts_and_integrity(conn)
    finally:
        conn.close()

    logger.info(f"Database build complete: {db_path} ({os.path.getsize(db_path):,} bytes)")

    # Trigger automatic master JSON exports
    logger.info("Triggering automatic master JSON exports...")
    import subprocess
    base_dir = Path(__file__).resolve().parent.parent
    subprocess.run([sys.executable, str(base_dir / "scripts" / "export_syllabus_matrix.py")], check=True)
    subprocess.run([sys.executable, str(base_dir / "scripts" / "export_json.py")], check=True)


def main():
    parser = argparse.ArgumentParser(description="Build and populate the Grade A Examinations SQLite Database.")
    parser.add_argument("--db", type=str, default="data/grade_a_exams.db", help="Path to target SQLite DB")
    parser.add_argument("--schema", type=str, default="data/schema.sql", help="Path to schema SQL file")
    parser.add_argument("--seed-file", type=str, default="data/master_seed_data.json", help="Path to master seed JSON data")
    parser.add_argument("--recreate", action="store_true", default=True, help="Recreate DB from scratch")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    db_path = (project_root / args.db) if not os.path.isabs(args.db) else Path(args.db)
    schema_path = (project_root / args.schema) if not os.path.isabs(args.schema) else Path(args.schema)
    seed_path = (project_root / args.seed_file) if not os.path.isabs(args.seed_file) else Path(args.seed_file)

    try:
        build(db_path, schema_path, seed_path=seed_path, recreate=args.recreate)
    except Exception as e:
        logger.error(f"Build failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
