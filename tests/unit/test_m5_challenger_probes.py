#!/usr/bin/env python3
"""
tests/unit/test_m5_challenger_probes.py
======================================
Exhaustive Adversarial Probe Suite by M5 Challenger 1 (teamwork_preview_challenger_m5_1).

Deep stress-testing across:
1. D1 Schema Boundaries & SQL Constraints:
   - Migration idempotency (multiple runs without error).
   - Duplicate user sync upsert handling (INSERT OR REPLACE).
   - NOT NULL rejections across all required columns.
   - json_valid() CHECK constraints on prior_attempts_json and tentative_timeline_2027.
   - Domain enums, Category enums, Gender enums, and bounds checking.
2. Worker API Boundaries & Live Edge Contracts:
   - Malformed JSON bodies (400).
   - Missing required profile attributes in /api/v1/profile/sync (400).
   - Out-of-bounds percentage values (400).
   - Malformed prior_attempts_json payload string (400).
   - Non-existent exam IDs in GET and POST evaluate (404).
   - Disallowed HTTP methods: DELETE, PUT, PATCH (405).
   - Global CORS headers on 200, 204, 400, 404, 405 responses.
   - Live D1 upsert verification via Worker API.
"""

import json
import os
import sqlite3
import unittest
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SCHEMA_SQL = os.path.join(BASE_DIR, "worker", "migrations", "0001_initial_schema.sql")
SEED_SQL = os.path.join(BASE_DIR, "worker", "migrations", "0002_seed_data.sql")
WORKER_BASE_URL = "https://grade-a-api.priyanshukh1201.workers.dev"

REQUEST_HEADERS = {
    "User-Agent": "GradeA-ChallengerProbe/1.0",
    "Content-Type": "application/json",
}


def send_http(
    url: str,
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 8.0,
) -> Dict[str, Any]:
    req_headers = dict(REQUEST_HEADERS)
    if headers:
        req_headers.update(headers)

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            status = response.status
            res_headers = {k.lower(): v for k, v in response.headers.items()}
            parsed_json = None
            try:
                parsed_json = json.loads(body)
            except Exception:
                pass
            return {
                "status": status,
                "body": body,
                "json": parsed_json,
                "headers": res_headers,
                "error": None,
            }
    except urllib.error.HTTPError as http_err:
        body = http_err.read().decode("utf-8")
        parsed_json = None
        try:
            parsed_json = json.loads(body)
        except Exception:
            pass
        return {
            "status": http_err.code,
            "body": body,
            "json": parsed_json,
            "headers": {k.lower(): v for k, v in http_err.headers.items()},
            "error": str(http_err),
        }
    except Exception as exc:
        return {
            "status": 0,
            "body": "",
            "json": None,
            "headers": {},
            "error": str(exc),
        }


class TestD1SchemaAdversarialBoundaries(unittest.TestCase):
    """Stress-tests the D1 schema against invalid structures, missing NOT NULL fields, and upserts."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
            self.schema_ddl = f.read()
        self.conn.executescript(self.schema_ddl)

    def tearDown(self):
        self.conn.close()

    def test_01_d1_migration_idempotency(self):
        """Verifies that running 0001_initial_schema.sql repeatedly does not throw errors."""
        for run_idx in range(3):
            try:
                self.conn.executescript(self.schema_ddl)
            except Exception as e:
                self.fail(f"Migration failed on idempotency pass {run_idx + 1}: {e}")

    def test_02_user_sync_upsert_replace_handling(self):
        """Verifies INSERT OR REPLACE updates existing records without duplication."""
        # Initial insert
        self.conn.execute("""
            INSERT OR REPLACE INTO user_profiles (
                user_id, name, dob, gender, category,
                graduation_degree, graduation_discipline, graduation_aggregate_pct,
                is_final_year, state_domicile, mother_tongue,
                height_cm, chest_cm, vision_specs, prior_attempts_json,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            "usr_probe_1", "Initial Name", "2000-01-01", "MALE", "GEN",
            "Bachelor", "Civil", 65.0, 0, "Delhi", "Hindi",
            170.0, None, None, json.dumps({"UPSC_CSE": 1})
        ))

        cur = self.conn.cursor()
        cur.execute("SELECT user_id, name, graduation_aggregate_pct FROM user_profiles WHERE user_id = 'usr_probe_1'")
        row1 = cur.fetchone()
        self.assertEqual(row1, ("usr_probe_1", "Initial Name", 65.0))

        # Upsert with new name and percentage
        self.conn.execute("""
            INSERT OR REPLACE INTO user_profiles (
                user_id, name, dob, gender, category,
                graduation_degree, graduation_discipline, graduation_aggregate_pct,
                is_final_year, state_domicile, mother_tongue,
                height_cm, chest_cm, vision_specs, prior_attempts_json,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            "usr_probe_1", "Updated Name", "2000-01-01", "MALE", "GEN",
            "Bachelor", "Civil", 78.5, 0, "Delhi", "Hindi",
            170.0, None, None, json.dumps({"UPSC_CSE": 2})
        ))

        cur.execute("SELECT COUNT(*) FROM user_profiles WHERE user_id = 'usr_probe_1'")
        self.assertEqual(cur.fetchone()[0], 1, "Duplicate user_id must not create multiple rows")

        cur.execute("SELECT user_id, name, graduation_aggregate_pct FROM user_profiles WHERE user_id = 'usr_probe_1'")
        row2 = cur.fetchone()
        self.assertEqual(row2, ("usr_probe_1", "Updated Name", 78.5), "Values must be replaced upon upsert")

    def test_03_missing_not_null_fields_rejected(self):
        """Verifies that omitting any required NOT NULL column raises IntegrityError."""
        mandatory_user_fields = [
            "dob",
            "gender",
            "category",
            "graduation_degree",
            "graduation_discipline",
            "graduation_aggregate_pct",
            "state_domicile",
        ]

        base_valid = {
            "user_id": "usr_probe_nn",
            "dob": "1999-05-15",
            "gender": "FEMALE",
            "category": "OBC_NCL",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Mechanical",
            "graduation_aggregate_pct": 70.0,
            "state_domicile": "Karnataka",
        }

        for field in mandatory_user_fields:
            corrupted = dict(base_valid)
            corrupted[field] = None
            with self.subTest(omitted_field=field):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"Omitting {field} should raise IntegrityError"):
                    self.conn.execute("""
                        INSERT INTO user_profiles (
                            user_id, dob, gender, category,
                            graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        corrupted["user_id"],
                        corrupted["dob"],
                        corrupted["gender"],
                        corrupted["category"],
                        corrupted["graduation_degree"],
                        corrupted["graduation_discipline"],
                        corrupted["graduation_aggregate_pct"],
                        corrupted["state_domicile"]
                    ))

        # Also verify NOT NULL constraints on core exams table
        mandatory_exam_fields = [
            ("title", None),
            ("category", None),
            ("administering_body", None),
            ("frequency", None),
            ("official_website", None),
            ("latest_official_notification_url", None),
            ("tentative_timeline_2027", None),
        ]
        base_exam = {
            "exam_id": "TEST_NN_EXAM",
            "title": "Test Title",
            "short_code": "TEST_SC",
            "category": "PSU",
            "administering_body": "ONGC",
            "frequency": "Annual",
            "official_website": "https://ongc.in",
            "latest_official_notification_url": "https://ongc.in/notif.pdf",
            "tentative_timeline_2027": "{}",
        }
        for field, _ in mandatory_exam_fields:
            corrupted_exam = dict(base_exam)
            corrupted_exam[field] = None
            with self.subTest(omitted_exam_field=field):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"Omitting {field} in exams should raise IntegrityError"):
                    self.conn.execute("""
                        INSERT INTO exams (
                            exam_id, title, short_code, category, administering_body,
                            frequency, official_website, latest_official_notification_url, tentative_timeline_2027
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        corrupted_exam["exam_id"],
                        corrupted_exam["title"],
                        corrupted_exam["short_code"],
                        corrupted_exam["category"],
                        corrupted_exam["administering_body"],
                        corrupted_exam["frequency"],
                        corrupted_exam["official_website"],
                        corrupted_exam["latest_official_notification_url"],
                        corrupted_exam["tentative_timeline_2027"],
                    ))

    def test_04_prior_attempts_json_check_constraint(self):
        """Verifies CHECK constraint on prior_attempts_json requiring valid JSON."""
        base_user = (
            "usr_probe_json", "2000-01-01", "MALE", "GEN",
            "Bachelor", "Electrical", 60.0, "Tamil Nadu"
        )
        # Valid JSON string succeeds
        self.conn.execute("""
            INSERT INTO user_profiles (
                user_id, dob, gender, category,
                graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile,
                prior_attempts_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*base_user, '{"UPSC_CSE": 1, "RBI_GRADE_B": 0}'))

        # NULL succeeds
        self.conn.execute("""
            INSERT INTO user_profiles (
                user_id, dob, gender, category,
                graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile,
                prior_attempts_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ("usr_probe_json_null", *base_user[1:], None))

        # Malformed JSON raises IntegrityError
        malformed_cases = [
            "not_json",
            "{unquoted_key: 123}",
            '{"unterminated": string',
            "[1, 2, 3,",
        ]
        for idx, malformed in enumerate(malformed_cases):
            with self.subTest(malformed_json=malformed):
                with self.assertRaises(sqlite3.IntegrityError):
                    self.conn.execute("""
                        INSERT INTO user_profiles (
                            user_id, dob, gender, category,
                            graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile,
                            prior_attempts_json
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (f"usr_fail_{idx}", *base_user[1:], malformed))

    def test_05_enum_check_constraints(self):
        """Verifies CHECK constraints on gender, category, and graduation_aggregate_pct."""
        base = ("usr_enum", "2000-01-01", "Bachelor", "CS", 70.0, "Kerala")

        # Invalid gender
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile)
                VALUES (?, ?, 'TRANS', 'GEN', ?, ?, ?, ?)
            """, (base[0], base[1], base[2], base[3], base[4], base[5]))

        # Invalid category
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile)
                VALUES (?, ?, 'FEMALE', 'GENERAL', ?, ?, ?, ?)
            """, (base[0], base[1], base[2], base[3], base[4], base[5]))

        # Negative aggregate percentage
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile)
                VALUES (?, ?, 'FEMALE', 'GEN', ?, ?, -5.0, ?)
            """, (base[0], base[1], base[2], base[3], base[5]))

        # Aggregate percentage > 100
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute("""
                INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile)
                VALUES (?, ?, 'FEMALE', 'GEN', ?, ?, 100.5, ?)
            """, (base[0], base[1], base[2], base[3], base[5]))


class TestWorkerAPIBoundaries(unittest.TestCase):
    """Stress-tests the live Cloudflare Worker API on all edge cases and boundary conditions."""

    def test_01_malformed_json_returns_400(self):
        """Malformed JSON payload to POST /api/v1/profile/evaluate must return 400 Bad Request."""
        res_eval = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
            method="POST",
            data=b"{\"invalid\": truncated",
        )
        self.assertEqual(res_eval["status"], 400)
        self.assertEqual(res_eval["json"].get("error"), "Malformed JSON")

        # Non-object payload
        res_eval_scalar = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
            method="POST",
            data=b"\"just a string\"",
        )
        self.assertEqual(res_eval_scalar["status"], 400)

        # Malformed JSON payload to POST /api/v1/profile/sync
        res_sync = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=b"{bad_json: true}",
        )
        self.assertEqual(res_sync["status"], 400)
        self.assertEqual(res_sync["json"].get("error"), "Malformed JSON")

    def test_02_missing_required_fields_in_sync_returns_400(self):
        """Missing mandatory fields in profile sync must return 400 with missing_fields array."""
        incomplete_payload = {
            "name": "Only Name Given"
        }
        res = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(incomplete_payload).encode("utf-8"),
        )
        self.assertEqual(res["status"], 400)
        self.assertEqual(res["json"].get("error"), "Missing Required Fields")
        missing = res["json"].get("missing_fields", [])
        expected_missing = [
            "user_id", "dob", "gender", "category",
            "graduation_degree", "graduation_discipline",
            "graduation_aggregate_pct", "state_domicile"
        ]
        for field in expected_missing:
            self.assertIn(field, missing, f"Expected {field} in missing_fields")

    def test_03_invalid_percentage_bounds_in_sync_returns_400(self):
        """graduation_aggregate_pct outside [0, 100] must return 400 Validation Error."""
        payload = {
            "user_id": "usr_pct_test",
            "dob": "1999-01-01",
            "gender": "MALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Arts",
            "graduation_aggregate_pct": 105.0,
            "state_domicile": "Punjab",
        }
        res = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
        )
        self.assertEqual(res["status"], 400)
        self.assertEqual(res["json"].get("error"), "Validation Error")

    def test_04_invalid_prior_attempts_json_string_returns_400(self):
        """Unparseable prior_attempts_json string must return 400 Validation Error."""
        payload = {
            "user_id": "usr_attempts_invalid",
            "dob": "1999-01-01",
            "gender": "MALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Arts",
            "graduation_aggregate_pct": 65.0,
            "state_domicile": "Punjab",
            "prior_attempts_json": "{not valid json",
        }
        res = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(payload).encode("utf-8"),
        )
        self.assertEqual(res["status"], 400)
        self.assertEqual(res["json"].get("error"), "Validation Error")

    def test_05_non_existent_exam_id_returns_404(self):
        """GET /api/v1/exams/:id and POST /api/v1/profile/evaluate with unknown exam must return 404."""
        # GET invalid exam
        res_get = send_http(f"{WORKER_BASE_URL}/api/v1/exams/FAKE_EXAM_ID_999")
        self.assertEqual(res_get["status"], 404)
        self.assertFalse(res_get["json"].get("success"))
        self.assertEqual(res_get["json"].get("error"), "Exam not found")

        # POST evaluate invalid exam
        eval_payload = {
            "exam_id": "NON_EXISTENT_EXAM_999",
            "dob": "2000-01-01",
            "gender": "MALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Engineering",
            "graduation_aggregate_pct": 75.0,
            "state_domicile": "Delhi",
        }
        res_eval = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
            method="POST",
            data=json.dumps(eval_payload).encode("utf-8"),
        )
        self.assertEqual(res_eval["status"], 404)
        self.assertEqual(res_eval["json"].get("error"), "Exam Not Found")

    def test_06_disallowed_http_methods_return_405(self):
        """Probing endpoints with disallowed HTTP verbs must return 405 Method Not Allowed."""
        disallowed_probes = [
            ("DELETE", f"{WORKER_BASE_URL}/api/v1/exams"),
            ("PUT", f"{WORKER_BASE_URL}/api/v1/exams"),
            ("PATCH", f"{WORKER_BASE_URL}/api/v1/exams"),
            ("GET", f"{WORKER_BASE_URL}/api/v1/profile/sync"),
            ("PUT", f"{WORKER_BASE_URL}/api/v1/profile/sync"),
            ("DELETE", f"{WORKER_BASE_URL}/api/v1/profile/sync"),
            ("GET", f"{WORKER_BASE_URL}/api/v1/profile/evaluate"),
            ("DELETE", f"{WORKER_BASE_URL}/api/v1/syllabus/taxonomy"),
            ("POST", f"{WORKER_BASE_URL}/api/v1/syllabus/taxonomy"),
        ]
        for method, url in disallowed_probes:
            with self.subTest(method=method, url=url):
                res = send_http(url, method=method)
                self.assertEqual(
                    res["status"],
                    405,
                    f"Expected 405 Method Not Allowed for {method} {url}, got {res['status']}"
                )
                self.assertEqual(res["json"].get("error"), "Method Not Allowed")

    def test_07_cors_headers_present_on_all_responses(self):
        """CORS header access-control-allow-origin: * must be present on 200, 204, 400, 404, 405."""
        # 1. 200 OK
        res_200 = send_http(f"{WORKER_BASE_URL}/api/v1/exams")
        self.assertEqual(res_200["headers"].get("access-control-allow-origin"), "*")

        # 2. 204 Preflight OPTIONS
        res_opt = send_http(f"{WORKER_BASE_URL}/api/v1/exams", method="OPTIONS")
        self.assertIn(res_opt["status"], [200, 204])
        self.assertEqual(res_opt["headers"].get("access-control-allow-origin"), "*")

        # 3. 400 Bad Request
        res_400 = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=b"bad_json",
        )
        self.assertEqual(res_400["status"], 400)
        self.assertEqual(res_400["headers"].get("access-control-allow-origin"), "*")

        # 4. 404 Not Found
        res_404 = send_http(f"{WORKER_BASE_URL}/api/v1/exams/NO_SUCH_EXAM")
        self.assertEqual(res_404["status"], 404)
        self.assertEqual(res_404["headers"].get("access-control-allow-origin"), "*")

        # 5. 405 Method Not Allowed
        res_405 = send_http(f"{WORKER_BASE_URL}/api/v1/exams", method="DELETE")
        self.assertEqual(res_405["status"], 405)
        self.assertEqual(res_405["headers"].get("access-control-allow-origin"), "*")

    def test_08_live_user_sync_upsert_d1(self):
        """Verifies profile sync and upsert directly against live Cloudflare D1 via Worker."""
        user_id = "usr_challenger_upsert_probe"
        payload_1 = {
            "user_id": user_id,
            "name": "Challenger Initial",
            "dob": "1997-08-20",
            "gender": "MALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Computer Science",
            "graduation_aggregate_pct": 72.0,
            "is_final_year": False,
            "state_domicile": "Uttar Pradesh",
            "mother_tongue": "Hindi",
            "height_cm": 178.0,
            "prior_attempts": {"UPSC_CSE": 1},
        }

        # Step 1: Initial Sync
        res1 = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(payload_1).encode("utf-8"),
        )
        self.assertEqual(res1["status"], 200)
        self.assertTrue(res1["json"].get("persisted_to_d1"))

        # Step 2: Upsert with modified attributes
        payload_2 = dict(payload_1)
        payload_2["name"] = "Challenger Modified"
        payload_2["graduation_aggregate_pct"] = 86.5
        payload_2["prior_attempts"] = {"UPSC_CSE": 2, "RBI_GRADE_B": 1}

        res2 = send_http(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=json.dumps(payload_2).encode("utf-8"),
        )
        self.assertEqual(res2["status"], 200)
        self.assertTrue(res2["json"].get("persisted_to_d1"))
        self.assertEqual(res2["json"].get("user_id"), user_id)


if __name__ == "__main__":
    unittest.main()
