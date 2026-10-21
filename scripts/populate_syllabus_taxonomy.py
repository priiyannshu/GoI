#!/usr/bin/env python3
"""
scripts/populate_syllabus_taxonomy.py
======================================
Atomic Ingestion Engine for Milestone 2:
Populates Universal Syllabus Taxonomy (>=120 topics across 6 domains)
and comprehensive Cross-Exam Stage Mappings for all 31 Grade A examinations.
Enforces foreign key integrity, check constraints, and transactional safety.
"""

import argparse
import json
import logging
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("populate_syllabus")

# Validation Constants
CANONICAL_DOMAINS = {
    "General Studies",
    "Quantitative Aptitude",
    "Reasoning",
    "English",
    "Economics & Finance",
    "Technical"
}

VALID_DEPTH_LEVELS = {"Foundation", "Intermediate", "Advanced", "Analytical"}
TOPIC_ID_REGEX = re.compile(r"^[a-z_]+\.[a-z_]+\.[a-z0-9_]+$")


class SyllabusIngestionEngine:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)

    def _get_connection(self) -> sqlite3.Connection:
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}. Run build_database.py first.")
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def validate_topic_record(self, topic: Dict[str, Any], index: int) -> Tuple[str, str, str, str, Optional[str]]:
        tid = topic.get("topic_id", "").strip()
        domain = topic.get("domain", "").strip()
        sub_domain = topic.get("sub_domain", "").strip()
        title = topic.get("topic_title", "").strip()
        desc = topic.get("description", "")

        if not tid or not TOPIC_ID_REGEX.match(tid):
            raise ValueError(f"Topic #{index} invalid topic_id format: '{tid}'. Expected [domain].[sub_domain].[slug]")
        if domain not in CANONICAL_DOMAINS:
            raise ValueError(f"Topic '{tid}' invalid domain '{domain}'. Must be one of {sorted(CANONICAL_DOMAINS)}")
        if not sub_domain:
            raise ValueError(f"Topic '{tid}' missing sub_domain")
        if not title:
            raise ValueError(f"Topic '{tid}' missing topic_title")

        return (tid, domain, sub_domain, title, desc if desc else None)

    def validate_map_record(self, mapping: Dict[str, Any], index: int, valid_exams: set, valid_topics: set) -> Tuple:
        eid = mapping.get("exam_id", "").strip()
        stage = mapping.get("stage_name", "").strip()
        tid = mapping.get("topic_id", "").strip()
        depth = mapping.get("depth_level", "").strip()
        is_opt = 1 if mapping.get("is_optional", False) in (1, True, "1", "true") else 0
        weightage = mapping.get("weightage_pct_estimate")
        clause = mapping.get("source_clause_ref", "").strip()

        if eid not in valid_exams:
            raise ValueError(f"Mapping #{index} unknown exam_id '{eid}' (not in master exams table)")
        if not stage:
            raise ValueError(f"Mapping #{index} for exam '{eid}' missing stage_name")
        if tid not in valid_topics:
            raise ValueError(f"Mapping #{index} references non-existent topic_id '{tid}'")
        if depth not in VALID_DEPTH_LEVELS:
            raise ValueError(f"Mapping #{index} invalid depth_level '{depth}'. Must be one of {sorted(VALID_DEPTH_LEVELS)}")
        if weightage is not None:
            try:
                weightage = float(weightage)
                if not (0.0 <= weightage <= 100.0):
                    raise ValueError(f"Mapping #{index} weightage {weightage} out of range [0, 100]")
            except ValueError:
                raise ValueError(f"Mapping #{index} non-numeric weightage '{weightage}'")
        if not clause:
            raise ValueError(f"Mapping #{index} ({eid} - {stage} - {tid}) missing source_clause_ref")

        return (eid, stage, tid, depth, is_opt, weightage, clause)

    def populate(
        self,
        taxonomy_records: List[Dict[str, Any]],
        mapping_records: List[Dict[str, Any]],
        clear_existing: bool = True
    ) -> Dict[str, int]:
        """Atomically ingests taxonomy and mappings within a single database transaction."""
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # 1. Verify master exams table
            cursor.execute("SELECT exam_id FROM exams;")
            existing_exam_ids = {row[0] for row in cursor.fetchall()}
            if len(existing_exam_ids) != 31:
                raise ValueError(f"Expected exactly 31 exams in master table, found {len(existing_exam_ids)}")

            logger.info("Validating taxonomy and stage mapping records...")
            validated_topics = []
            topic_id_set = set()
            for idx, t in enumerate(taxonomy_records):
                row = self.validate_topic_record(t, idx)
                validated_topics.append(row)
                topic_id_set.add(row[0])

            validated_mappings = []
            for idx, m in enumerate(mapping_records):
                row = self.validate_map_record(m, idx, existing_exam_ids, topic_id_set)
                validated_mappings.append(row)

            # 2. Begin atomic transaction
            conn.execute("BEGIN IMMEDIATE;")
            logger.info("Database transaction started.")

            if clear_existing:
                cursor.execute("DELETE FROM exam_syllabus_map;")
                cursor.execute("DELETE FROM syllabus_taxonomy;")
                logger.info("Cleared existing taxonomy and stage mapping records.")

            # 3. Insert syllabus taxonomy nodes
            cursor.executemany("""
                INSERT OR REPLACE INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title, description)
                VALUES (?, ?, ?, ?, ?)
            """, validated_topics)
            logger.info(f"Inserted {len(validated_topics)} taxonomy topics.")

            # 4. Insert exam stage mappings
            cursor.executemany("""
                INSERT OR REPLACE INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, validated_mappings)
            logger.info(f"Inserted {len(validated_mappings)} stage-topic mappings.")

            # 5. Check foreign keys
            fk_violations = cursor.execute("PRAGMA foreign_key_check;").fetchall()
            if fk_violations:
                raise ValueError(f"Foreign key violations detected during ingestion: {fk_violations}")

            # 6. Verify distinct mapped exams
            cursor.execute("SELECT COUNT(DISTINCT exam_id) FROM exam_syllabus_map;")
            mapped_exams_count = cursor.fetchone()[0]
            if mapped_exams_count != 31:
                raise ValueError(f"Not all 31 exams were mapped! Only {mapped_exams_count}/31 mapped.")

            # 7. Check orphan topics
            cursor.execute("""
                SELECT COUNT(*) FROM syllabus_taxonomy 
                WHERE topic_id NOT IN (SELECT DISTINCT topic_id FROM exam_syllabus_map);
            """)
            orphan_count = cursor.fetchone()[0]
            if orphan_count > 0:
                logger.warning(f"Found {orphan_count} orphan topics not mapped to any exam.")

            # Commit transaction
            conn.commit()
            logger.info("Database transaction committed successfully.")

            # 8. Re-index and optimize
            cursor.execute("REINDEX idx_syllabus_domain;")
            cursor.execute("REINDEX idx_map_exam;")
            cursor.execute("REINDEX idx_map_topic;")
            cursor.execute("PRAGMA optimize;")

            return {
                "topics_count": len(validated_topics),
                "mappings_count": len(validated_mappings),
                "mapped_exams_count": mapped_exams_count,
                "orphan_topics_count": orphan_count
            }

        except Exception as e:
            conn.rollback()
            logger.error(f"Ingestion failed! Transaction rolled back: {e}")
            raise
        finally:
            conn.close()


def load_seed_json(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        raise FileNotFoundError(f"Seed file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        if "topics" in data:
            return data["topics"]
        if "mappings" in data:
            return data["mappings"]
        if "syllabus_taxonomy" in data:
            return data["syllabus_taxonomy"]
        if "exam_syllabus_map" in data:
            return data["exam_syllabus_map"]
    if isinstance(data, list):
        return data
    raise ValueError(f"Invalid JSON format in {file_path}")


def populate_syllabus(db_path: Path, tax_seed_path: Path, map_seed_path: Path) -> Dict[str, int]:
    tax_records = load_seed_json(tax_seed_path)
    map_records = load_seed_json(map_seed_path)
    engine = SyllabusIngestionEngine(db_path)
    return engine.populate(tax_records, map_records)


def main():
    parser = argparse.ArgumentParser(description="Populate Syllabus Taxonomy and Exam Mappings into SQLite.")
    parser.add_argument("--db", default="data/grade_a_exams.db", help="Path to SQLite DB")
    parser.add_argument("--taxonomy-seed", default="data/syllabus_taxonomy_seed.json", help="Path to taxonomy seed JSON")
    parser.add_argument("--map-seed", default="data/exam_syllabus_map_seed.json", help="Path to mappings seed JSON")
    parser.add_argument("--export", action="store_true", help="Trigger export pipelines after population")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / args.db if not os.path.isabs(args.db) else Path(args.db)
    tax_seed_path = project_root / args.taxonomy_seed if not os.path.isabs(args.taxonomy_seed) else Path(args.taxonomy_seed)
    map_seed_path = project_root / args.map_seed if not os.path.isabs(args.map_seed) else Path(args.map_seed)

    summary = populate_syllabus(db_path, tax_seed_path, map_seed_path)

    logger.info("=== INGESTION SUMMARY ===")
    for k, v in summary.items():
        logger.info(f"  {k}: {v}")

    if args.export:
        logger.info("Executing export pipelines...")
        subprocess.run([sys.executable, str(project_root / "scripts" / "export_syllabus_matrix.py")], check=True)
        subprocess.run([sys.executable, str(project_root / "scripts" / "export_json.py")], check=True)


if __name__ == "__main__":
    main()
