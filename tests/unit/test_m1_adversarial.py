#!/usr/bin/env python3
"""
tests/unit/test_m1_adversarial.py
=================================
Adversarial Empirical Challenge Harness for Milestone 1 (M1_DATA_ENGINE).

Executes exhaustive empirical tests:
1. Active Foreign Key and CHECK constraint enforcement on temporary SQLite databases.
2. Negative corruption probes against `scripts/verify_database.py`.
3. Extreme boundary inputs on statutory eligibility logic (leap days, exact cutoff seconds,
   59.9999% vs 60.0%, max attempts + 1).
4. Structural integrity and round-trip fidelity of `data/grade_a_exams.json`.
"""

import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
from datetime import date
from typing import Any, Dict, List

from scripts.verify_database import DatabaseIntegrityVerifier, EligibilityEdgeCaseHarness

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DB_PATH = os.path.join(BASE_DIR, "data", "grade_a_exams.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema.sql")
JSON_PATH = os.path.join(BASE_DIR, "data", "grade_a_exams.json")
VERIFY_SCRIPT_PATH = os.path.join(BASE_DIR, "scripts", "verify_database.py")


class TestM1AdversarialSchemaConstraints(unittest.TestCase):
    """Adversarial stress-testing of relational schema constraints and CHECK rules."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def tearDown(self):
        self.conn.close()

    def test_fk_rejection_in_eligibility_criteria(self):
        """Ensure inserting into eligibility_criteria with an invalid exam_id is rejected."""
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO eligibility_criteria (
                    exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen,
                    relaxations_json, min_education_level, accepted_disciplines,
                    source_citation_clause
                ) VALUES (
                    'NON_EXISTENT_EXAM', 'August 1', 21, 32, '{}', 'Bachelor', '[]', 'Clause 1'
                );
            """)

    def test_fk_rejection_in_source_audit_log(self):
        """Ensure inserting into source_audit_log with an invalid exam_id is rejected."""
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO source_audit_log (
                    audit_id, exam_id, fact_type, official_document_title,
                    document_date, clause_or_page_number, official_download_link
                ) VALUES (
                    'AUD_TEST_01', 'NON_EXISTENT_EXAM', 'Age_Limit', 'Doc Title',
                    '2026-01-01', 'Clause 1', 'https://example.com/doc.pdf'
                );
            """)

    def test_fk_rejection_in_exam_syllabus_map(self):
        """Ensure inserting into exam_syllabus_map with an invalid exam_id or topic_id is rejected."""
        # Insert a valid exam and topic first
        self.conn.execute("""
            INSERT INTO exams (
                exam_id, title, short_code, category, administering_body, frequency,
                official_website, latest_official_notification_url, tentative_timeline_2027
            ) VALUES (
                'TEST_EXAM', 'Test Title', 'TEST', 'Central-Civil', 'UPSC', 'Annual',
                'https://example.com', 'https://example.com/notif', '{}'
            );
        """)
        self.conn.execute("""
            INSERT INTO syllabus_taxonomy (
                topic_id, domain, sub_domain, topic_title
            ) VALUES (
                'test.topic', 'General Studies', 'Polity', 'Test Topic'
            );
        """)

        # Bad exam_id
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level)
                VALUES ('BAD_EXAM', 'Stage 1', 'test.topic', 'Foundation');
            """)

        # Bad topic_id
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level)
                VALUES ('TEST_EXAM', 'Stage 1', 'bad.topic', 'Foundation');
            """)

    def test_cascade_deletion(self):
        """Ensure deleting an exam deletes related rows in child tables."""
        self.conn.execute("""
            INSERT INTO exams (
                exam_id, title, short_code, category, administering_body, frequency,
                official_website, latest_official_notification_url, tentative_timeline_2027
            ) VALUES (
                'CASCADE_EXAM', 'Cascade Title', 'CASC', 'Central-Civil', 'UPSC', 'Annual',
                'https://example.com', 'https://example.com/notif', '{}'
            );
        """)
        self.conn.execute("""
            INSERT INTO eligibility_criteria (
                exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen,
                relaxations_json, min_education_level, accepted_disciplines, source_citation_clause
            ) VALUES (
                'CASCADE_EXAM', 'August 1', 21, 32, '{}', 'Bachelor', '[]', 'Clause 1'
            );
        """)
        self.conn.execute("""
            INSERT INTO source_audit_log (
                audit_id, exam_id, fact_type, official_document_title,
                document_date, clause_or_page_number, official_download_link
            ) VALUES (
                'AUD_CASCADE_01', 'CASCADE_EXAM', 'Age_Limit', 'Doc Title',
                '2026-01-01', 'Clause 1', 'https://example.com/doc.pdf'
            );
        """)

        # Delete exam
        self.conn.execute("DELETE FROM exams WHERE exam_id = 'CASCADE_EXAM';")
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM eligibility_criteria WHERE exam_id = 'CASCADE_EXAM';")
        self.assertEqual(cursor.fetchone()[0], 0)
        cursor.execute("SELECT COUNT(*) FROM source_audit_log WHERE exam_id = 'CASCADE_EXAM';")
        self.assertEqual(cursor.fetchone()[0], 0)

    def test_malformed_json_check_constraints(self):
        """Ensure SQLite CHECK (json_valid(...)) actively rejects malformed JSON."""
        # 1. exams.tentative_timeline_2027
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exams (
                    exam_id, title, short_code, category, administering_body, frequency,
                    official_website, latest_official_notification_url, tentative_timeline_2027
                ) VALUES (
                    'JSON_BAD', 'Bad JSON', 'JB1', 'Central-Civil', 'UPSC', 'Annual',
                    'https://example.com', 'https://example.com/notif', '{broken_json'
                );
            """)

        # Insert valid exam for subsequent tests
        self.conn.execute("""
            INSERT INTO exams (
                exam_id, title, short_code, category, administering_body, frequency,
                official_website, latest_official_notification_url, tentative_timeline_2027
            ) VALUES (
                'JSON_EXAM', 'Good Exam', 'JG1', 'Central-Civil', 'UPSC', 'Annual',
                'https://example.com', 'https://example.com/notif', '{}'
            );
        """)

        # 2. eligibility_criteria.relaxations_json
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO eligibility_criteria (
                    exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen,
                    relaxations_json, min_education_level, accepted_disciplines, source_citation_clause
                ) VALUES (
                    'JSON_EXAM', 'August 1', 21, 32, '{bad_relax', 'Bachelor', '[]', 'Clause'
                );
            """)

        # 3. eligibility_criteria.accepted_disciplines
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO eligibility_criteria (
                    exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen,
                    relaxations_json, min_education_level, accepted_disciplines, source_citation_clause
                ) VALUES (
                    'JSON_EXAM', 'August 1', 21, 32, '{}', 'Bachelor', '[bad_disciplines', 'Clause'
                );
            """)

        # 4. user_profiles.prior_attempts_json
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO user_profiles (
                    user_id, dob, gender, category, graduation_degree,
                    graduation_discipline, graduation_aggregate_pct, state_domicile, prior_attempts_json
                ) VALUES (
                    'U001', '2000-01-01', 'MALE', 'GEN', 'B.Tech', 'CSE', 75.0, 'Delhi', '{bad_json'
                );
            """)

    def test_enum_check_constraints(self):
        """Ensure invalid enum values fail SQLite CHECK constraints."""
        # Invalid Category in exams
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exams (
                    exam_id, title, short_code, category, administering_body, frequency,
                    official_website, latest_official_notification_url, tentative_timeline_2027
                ) VALUES (
                    'ENUM_BAD', 'Bad Enum', 'EB1', 'Invalid-Category', 'UPSC', 'Annual',
                    'https://example.com', 'https://example.com/notif', '{}'
                );
            """)

        # Invalid Frequency in exams
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exams (
                    exam_id, title, short_code, category, administering_body, frequency,
                    official_website, latest_official_notification_url, tentative_timeline_2027
                ) VALUES (
                    'ENUM_BAD2', 'Bad Enum', 'EB2', 'Central-Civil', 'UPSC', 'Quarterly',
                    'https://example.com', 'https://example.com/notif', '{}'
                );
            """)

        # Invalid Domain in syllabus_taxonomy
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title)
                VALUES ('bad.domain', 'Astrology', 'Predictions', 'Horoscope');
            """)

        # Invalid Depth Level in exam_syllabus_map
        self.conn.execute("""
            INSERT INTO exams (
                exam_id, title, short_code, category, administering_body, frequency,
                official_website, latest_official_notification_url, tentative_timeline_2027
            ) VALUES (
                'DEPTH_EXAM', 'Depth Exam', 'DX1', 'Central-Civil', 'UPSC', 'Annual',
                'https://example.com', 'https://example.com/notif', '{}'
            );
        """)
        self.conn.execute("""
            INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title)
            VALUES ('valid.topic', 'General Studies', 'Polity', 'Constitution');
        """)
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level)
                VALUES ('DEPTH_EXAM', 'Prelims', 'valid.topic', 'Grandmaster');
            """)


class TestM1AdversarialVerifierEngine(unittest.TestCase):
    """Stress-tests the verification script against injected database corruptions."""

    def run_verifier_on_temp_db(self, mutate_fn) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            shutil.copyfile(DB_PATH, tmp_path)
            conn = sqlite3.connect(tmp_path)
            mutate_fn(conn)
            conn.commit()
            conn.close()

            res = subprocess.run(
                ["python3", VERIFY_SCRIPT_PATH, "--db", tmp_path],
                capture_output=True,
                text=True
            )
            return res
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_verifier_catches_fk_violation_in_audit_log(self):
        """Verifier must catch foreign key violation in source_audit_log."""
        def mutate(conn):
            conn.execute("PRAGMA foreign_keys = OFF;")
            conn.execute("""
                INSERT INTO source_audit_log (
                    audit_id, exam_id, fact_type, official_document_title,
                    document_date, clause_or_page_number, official_download_link
                ) VALUES (
                    'AUD_CORRUPT', 'GHOST_EXAM', 'Age_Limit', 'Ghost Doc',
                    '2026-01-01', 'Clause 1', 'https://example.com'
                );
            """)

        res = self.run_verifier_on_temp_db(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Foreign key violation", res.stdout)

    def test_verifier_catches_missing_exam(self):
        """Verifier must catch database with fewer than 25 exams."""
        def mutate(conn):
            conn.execute("DELETE FROM exams WHERE exam_id = 'UPSC_CSE';")

        res = self.run_verifier_on_temp_db(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Expected 25 exams", res.stdout)

    def test_verifier_catches_malformed_url(self):
        """Verifier must catch malformed URLs in exam records."""
        def mutate(conn):
            conn.execute("UPDATE exams SET official_website = 'not-a-valid-url' WHERE exam_id = 'UPSC_CSE';")

        res = self.run_verifier_on_temp_db(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("invalid official_website", res.stdout)

    def test_verifier_catches_missing_index(self):
        """Verifier must catch dropped performance indexes."""
        def mutate(conn):
            conn.execute("DROP INDEX idx_exams_category;")

        res = self.run_verifier_on_temp_db(mutate)
        self.assertEqual(res.returncode, 1)
        self.assertIn("Missing required indexes", res.stdout)


class TestM1AdversarialEligibilityBoundaries(unittest.TestCase):
    """Stress-tests the algorithmic eligibility edge-case logic with extreme inputs."""

    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(DB_PATH)
        cls.harness = EligibilityEdgeCaseHarness(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_candidates_born_on_leap_day(self):
        """Verify candidates born on February 29 (leap days) evaluate accurately across cutoff dates."""
        # 1. Born 2000-02-29 applying for UPSC CSE (Aug 1, 2027 -> Age 27 -> Eligible)
        prof_2000 = {"dob": "2000-02-29", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0}
        el, _ = self.harness.evaluate("UPSC_CSE", prof_2000)
        self.assertTrue(el)

        # 2. Born 1996-02-29 applying for UPSC CSE (Aug 1, 2027 -> Age 31 -> Eligible)
        prof_1996 = {"dob": "1996-02-29", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0}
        el, _ = self.harness.evaluate("UPSC_CSE", prof_1996)
        self.assertTrue(el)

        # 3. Born 1992-02-29 applying for UPSC CSE (Aug 1, 2027 -> Age 35 -> Ineligible: overage)
        prof_1992 = {"dob": "1992-02-29", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0}
        el, _ = self.harness.evaluate("UPSC_CSE", prof_1992)
        self.assertFalse(el)

        # 4. Born 2004-02-29 applying for UPPSC (Jul 1, 2027 -> Age 23 -> Eligible)
        prof_2004 = {"dob": "2004-02-29", "category": "GEN", "graduation_aggregate_pct": 55.0}
        el, _ = self.harness.evaluate("UPPSC_PCS", prof_2004)
        self.assertTrue(el)

    def test_lower_age_boundary_exact_days(self):
        """Verify minimum age boundary on exact day and exact day + 1."""
        # UPSC ESE (Cutoff: January 1, 2027, Min Age: 21)
        # Born 2006-01-01 turns 21 on January 1, 2027 -> Eligible
        el_exact, _ = self.harness.evaluate("UPSC_ESE", {"dob": "2006-01-01", "category": "GEN", "graduation_aggregate_pct": 55.0})
        self.assertTrue(el_exact)

        # Born 2006-01-02 is 20 years 364 days on January 1, 2027 -> Ineligible
        el_under, _ = self.harness.evaluate("UPSC_ESE", {"dob": "2006-01-02", "category": "GEN", "graduation_aggregate_pct": 55.0})
        self.assertFalse(el_under)

        # UPPSC PCS (Cutoff: July 1, 2027, Min Age: 21)
        # Born 2006-07-01 turns 21 on July 1 -> Eligible
        el_uppsc_exact, _ = self.harness.evaluate("UPPSC_PCS", {"dob": "2006-07-01", "category": "GEN", "graduation_aggregate_pct": 55.0})
        self.assertTrue(el_uppsc_exact)

        # Born 2006-07-02 is underage on July 1 -> Ineligible
        el_uppsc_under, _ = self.harness.evaluate("UPPSC_PCS", {"dob": "2006-07-02", "category": "GEN", "graduation_aggregate_pct": 55.0})
        self.assertFalse(el_uppsc_under)

    def test_strict_percentage_thresholds(self):
        """Verify strict non-rounding: 59.99% and 59.9999% fail 60.0% threshold."""
        # RBI Grade B requires 60.0%
        prof_5999 = {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 59.99, "prior_phase1_attempts": 0}
        el, _ = self.harness.evaluate("RBI_GRADE_B", prof_5999)
        self.assertFalse(el)

        prof_599999 = {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 59.9999, "prior_phase1_attempts": 0}
        el, _ = self.harness.evaluate("RBI_GRADE_B", prof_599999)
        self.assertFalse(el)

        prof_6000 = {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 60.00, "prior_phase1_attempts": 0}
        el, _ = self.harness.evaluate("RBI_GRADE_B", prof_6000)
        self.assertTrue(el)

        # PSU IOCL requires 65.0%
        prof_6499 = {"dob": "2002-01-01", "category": "GEN", "graduation_aggregate_pct": 64.99}
        el, _ = self.harness.evaluate("PSU_IOCL_ET", prof_6499)
        self.assertFalse(el)

        prof_649999 = {"dob": "2002-01-01", "category": "GEN", "graduation_aggregate_pct": 64.9999}
        el, _ = self.harness.evaluate("PSU_IOCL_ET", prof_649999)
        self.assertFalse(el)

        prof_6500 = {"dob": "2002-01-01", "category": "GEN", "graduation_aggregate_pct": 65.00}
        el, _ = self.harness.evaluate("PSU_IOCL_ET", prof_6500)
        self.assertTrue(el)

    def test_attempt_limits_boundary_and_plus_one(self):
        """Verify attempt limits at limit - 1 (eligible), limit (ineligible), and limit + 1 (ineligible)."""
        # UPSC CSE General (Limit 6)
        p5 = {"dob": "2000-01-01", "category": "GEN", "prior_attempts": 5}
        self.assertTrue(self.harness.evaluate("UPSC_CSE", p5)[0])

        p6 = {"dob": "2000-01-01", "category": "GEN", "prior_attempts": 6}
        self.assertFalse(self.harness.evaluate("UPSC_CSE", p6)[0])

        p7 = {"dob": "2000-01-01", "category": "GEN", "prior_attempts": 7}
        self.assertFalse(self.harness.evaluate("UPSC_CSE", p7)[0])

        # UPSC CSE OBC (Limit 9)
        p8_obc = {"dob": "1997-01-01", "category": "OBC", "prior_attempts": 8}
        self.assertTrue(self.harness.evaluate("UPSC_CSE", p8_obc)[0])

        p9_obc = {"dob": "1997-01-01", "category": "OBC", "prior_attempts": 9}
        self.assertFalse(self.harness.evaluate("UPSC_CSE", p9_obc)[0])

        p10_obc = {"dob": "1997-01-01", "category": "OBC", "prior_attempts": 10}
        self.assertFalse(self.harness.evaluate("UPSC_CSE", p10_obc)[0])

        # UPSC CSE SC (Unlimited)
        p50_sc = {"dob": "1995-01-01", "category": "SC", "prior_attempts": 50}
        self.assertTrue(self.harness.evaluate("UPSC_CSE", p50_sc)[0])

        # RBI Grade B General Phase-1 (Limit 6)
        rbi_p5 = {"dob": "2000-01-01", "category": "GEN", "prior_phase1_attempts": 5, "graduation_aggregate_pct": 60.0}
        self.assertTrue(self.harness.evaluate("RBI_GRADE_B", rbi_p5)[0])

        rbi_p6 = {"dob": "2000-01-01", "category": "GEN", "prior_phase1_attempts": 6, "graduation_aggregate_pct": 60.0}
        self.assertFalse(self.harness.evaluate("RBI_GRADE_B", rbi_p6)[0])

        rbi_p7 = {"dob": "2000-01-01", "category": "GEN", "prior_phase1_attempts": 7, "graduation_aggregate_pct": 60.0}
        self.assertFalse(self.harness.evaluate("RBI_GRADE_B", rbi_p7)[0])


class TestM1AdversarialJSONExportIntegrity(unittest.TestCase):
    """Stress-tests the master JSON export for truncation, structural defects, and round-trip parity."""

    @classmethod
    def setUpClass(cls):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            cls.data = json.load(f)
        cls.conn = sqlite3.connect(DB_PATH)
        cls.conn.row_factory = sqlite3.Row

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_json_root_structure(self):
        """Ensure JSON contains all required top-level keys and correct metadata counts."""
        self.assertIn("$schema", self.data)
        self.assertIn("metadata", self.data)
        self.assertIn("exams", self.data)
        self.assertIn("d3_visualization_index", self.data)

        meta = self.data["metadata"]
        self.assertEqual(meta["total_exams"], 25)
        self.assertEqual(len(self.data["exams"]), 25)

        clusters = meta["cluster_distribution"]
        self.assertEqual(clusters["Cluster 1: Central All-India & Uniformed"], 6)
        self.assertEqual(clusters["Cluster 2: Premier Financial & Regulatory"], 3)
        self.assertEqual(clusters["Cluster 3: State Public Service Commissions"], 5)
        self.assertEqual(clusters["Cluster 4: Maharatna & Navratna PSUs"], 11)

    def test_json_no_double_encoding(self):
        """Ensure no JSON columns in SQLite were exported as double-encoded JSON strings."""
        for exam in self.data["exams"]:
            eid = exam["exam_id"]
            self.assertIsInstance(exam["tentative_timeline_2027"], dict, f"{eid} timeline is not dict")

            elig = exam.get("eligibility")
            self.assertIsNotNone(elig, f"{eid} has null eligibility")
            self.assertIsInstance(elig["relaxations"], dict, f"{eid} relaxations is not dict")
            self.assertIsInstance(elig["accepted_disciplines"], list, f"{eid} accepted_disciplines is not list")

            if elig["domicile_restrictions"] is not None:
                self.assertIsInstance(elig["domicile_restrictions"], dict, f"{eid} domicile is not dict")
            if elig["language_requirements"] is not None:
                self.assertIsInstance(elig["language_requirements"], dict, f"{eid} language is not dict")
            if elig["physical_standards"] is not None:
                self.assertIsInstance(elig["physical_standards"], dict, f"{eid} physical is not dict")

    def test_json_audit_logs_coverage(self):
        """Ensure all 150 audit logs exist in JSON and match expected schema."""
        total_audits = 0
        for exam in self.data["exams"]:
            eid = exam["exam_id"]
            audits = exam.get("audit_trail", [])
            self.assertGreaterEqual(len(audits), 6, f"{eid} has fewer than 6 audit logs")
            total_audits += len(audits)
            for a in audits:
                self.assertIn("audit_id", a)
                self.assertIn("fact_type", a)
                self.assertIn("official_document_title", a)
                self.assertIn("clause_or_page_number", a)
                self.assertIn("official_download_link", a)
                self.assertTrue(a["official_download_link"].startswith("http"))
        self.assertEqual(total_audits, 150)

    def test_json_db_parity_zero_truncation(self):
        """Verify zero text truncation or value discrepancies between DB and JSON."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM exams;")
        db_exams = {row["exam_id"]: dict(row) for row in cursor.fetchall()}

        json_exams = {e["exam_id"]: e for e in self.data["exams"]}
        self.assertEqual(set(db_exams.keys()), set(json_exams.keys()))

        for eid, db_row in db_exams.items():
            j_row = json_exams[eid]
            self.assertEqual(j_row["title"], db_row["title"])
            self.assertEqual(j_row["short_code"], db_row["short_code"])
            self.assertEqual(j_row["category"], db_row["category"])
            self.assertEqual(j_row["administering_body"], db_row["administering_body"])
            self.assertEqual(j_row["frequency"], db_row["frequency"])
            self.assertEqual(j_row["official_website"], db_row["official_website"])
            self.assertEqual(j_row["latest_official_notification_url"], db_row["latest_official_notification_url"])


if __name__ == "__main__":
    unittest.main()
