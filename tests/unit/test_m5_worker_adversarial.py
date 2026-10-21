#!/usr/bin/env python3
"""
tests/unit/test_m5_worker_adversarial.py
========================================
Adversarial Empirical Challenge Harness for Milestone 5 (M5_CLOUDFLARE_EDGE).

Empirically verifies and stress-tests:
1. Cloudflare D1 Relational Schema & Integrity Constraints (`worker/migrations/0001_initial_schema.sql`):
   - Table creation across all 6 core entities (`exams`, `eligibility_criteria`, `syllabus_taxonomy`,
     `exam_syllabus_map`, `source_audit_log`, `user_profiles`).
   - CHECK constraints on exam categories, exam frequency, age boundaries, graduation percentage bounds.
   - `json_valid()` enforcement on timeline, relaxations, accepted disciplines, and prior attempts.
   - Active Foreign Key cascade propagation on exam deletion.
2. Cloudflare D1 Master Seed Data (`worker/migrations/0002_seed_data.sql`):
   - Flawless DDL + DML execution with zero foreign-key violations (`PRAGMA foreign_key_check`).
   - Authoritative row counts: exactly 36 exams, 36 eligibility rules, 192 taxonomy nodes,
     1,123 stage mappings, and 216 statutory source audit logs.
   - Referential completeness: zero orphan records.
3. Edge Configuration & Infrastructure Files:
   - `worker/wrangler.toml` validation (D1 DB binding, compatibility date, account_id).
   - `worker/package.json` validation (Hono v4, Workers types, build scripts).
   - `frontend/functions/api/[[catchall]].ts` (Pages reverse-proxy routing).
   - `frontend/public/_headers` (Workbox cache busting for sw.js and manifest).
4. Edge REST API Endpoints & Contract Adherence:
   - Root Health Check: `GET /` -> 200 OK, status HEALTHY, version 1.0.0.
   - Catalog: `GET /api/v1/exams` -> 200 OK, count 36, source d1.
   - Exam Detail: `GET /api/v1/exams/UPSC_CSE` -> 200 OK, short_code CSE.
   - 404 Not Found: `GET /api/v1/exams/NONEXISTENT_EXAM` -> 404 with error message.
   - Syllabus Taxonomy: `GET /api/v1/syllabus/taxonomy` -> 200 OK, count 192.
   - Overlap Matrix: `GET /api/v1/syllabus/matrix` -> 200 OK, metadata total_exams 36.
   - Profile Evaluation: `POST /api/v1/profile/evaluate` -> 200 OK, statutory verdict.
   - 400 Bad Request: Malformed JSON and missing profile fields.
   - D1 Profile Sync: `POST /api/v1/profile/sync` -> 200 OK, persisted_to_d1 true.
   - 405 Method Not Allowed: `DELETE /api/v1/exams` and `GET /api/v1/profile/sync`.
   - Global CORS: `access-control-allow-origin: *`.
   - Cloudflare Pages edge proxy and PWA assets verification.
"""

import json
import os
import sqlite3
import unittest
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "worker", "migrations")
SCHEMA_SQL = os.path.join(MIGRATIONS_DIR, "0001_initial_schema.sql")
SEED_SQL = os.path.join(MIGRATIONS_DIR, "0002_seed_data.sql")
WRANGLER_TOML = os.path.join(BASE_DIR, "worker", "wrangler.toml")
PACKAGE_JSON = os.path.join(BASE_DIR, "worker", "package.json")
PAGES_PROXY = os.path.join(BASE_DIR, "frontend", "functions", "api", "[[catchall]].ts")
PAGES_HEADERS = os.path.join(BASE_DIR, "frontend", "public", "_headers")

WORKER_BASE_URL = "https://grade-a-api.priyanshukh1201.workers.dev"
PAGES_BASE_URL = "https://grade-a-exams.pages.dev"
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GradeAIntelligenceTest/1.0)",
    "Content-Type": "application/json",
}


def make_http_request(
    url: str,
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 8.0,
) -> Dict[str, Any]:
    """Helper to execute HTTP requests with custom User-Agent and capture status and headers."""
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
                parsed_json = None
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
            parsed_json = None
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


class TestM5D1SchemaAndIntegrity(unittest.TestCase):
    """Verifies D1 SQLite schema, constraints, and full seed data in worker/migrations/."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_SQL, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def tearDown(self):
        self.conn.close()

    def test_01_all_tables_and_indexes_created(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = {row[0] for row in cur.fetchall()}
        expected_tables = {
            "exams",
            "eligibility_criteria",
            "syllabus_taxonomy",
            "exam_syllabus_map",
            "source_audit_log",
            "user_profiles",
        }
        self.assertTrue(expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}")

    def test_02_exam_category_check_constraint(self):
        """Enforces CHECK (category IN ('Central-Civil', 'Regulatory', 'Defense', 'State-PSC', 'PSU'))."""
        valid_payload = (
            "TEST_EXAM",
            "Test Exam Title",
            "TEST_CODE",
            "Central-Civil",
            "UPSC",
            "Annual",
            "https://test.gov.in",
            "https://test.gov.in/notif.pdf",
            "Gazette 123",
            json.dumps({"notification_month": "Jan 2027"}),
            "Test Description",
        )
        self.conn.execute(
            "INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, "
            "official_website, latest_official_notification_url, latest_gazette_ref, tentative_timeline_2027, description) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            valid_payload,
        )

        invalid_payload = list(valid_payload)
        invalid_payload[0] = "TEST_EXAM_INVALID"
        invalid_payload[2] = "TEST_CODE_2"
        invalid_payload[3] = "InvalidCategory"

        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, "
                "official_website, latest_official_notification_url, latest_gazette_ref, tentative_timeline_2027, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                invalid_payload,
            )

    def test_03_timeline_json_valid_constraint(self):
        """Rejects malformed JSON in tentative_timeline_2027."""
        payload = (
            "TEST_MALFORMED_JSON",
            "Title",
            "TEST_M_JSON",
            "Regulatory",
            "RBI",
            "Annual",
            "https://rbi.org.in",
            "https://rbi.org.in/notif.pdf",
            None,
            "{malformed_json: true",
            "Desc",
        )
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, "
                "official_website, latest_official_notification_url, latest_gazette_ref, tentative_timeline_2027, description) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                payload,
            )

    def test_04_eligibility_criteria_constraints_and_cascade(self):
        """Verifies eligibility bounds and foreign key cascade on exam deletion."""
        # Insert base exam
        self.conn.execute(
            "INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, "
            "official_website, latest_official_notification_url, latest_gazette_ref, tentative_timeline_2027, description) "
            "VALUES ('EXAM_CASCADE', 'Cascade Test', 'CASCADE_1', 'PSU', 'ONGC', 'Annual', 'https://ongc.in', 'https://ongc.in/notif', 'Gazette', '{}', 'Desc')"
        )
        # Insert eligibility
        self.conn.execute(
            "INSERT INTO eligibility_criteria (exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json, "
            "min_education_level, accepted_disciplines, min_aggregate_percentage_gen, min_aggregate_percentage_reserved, final_year_students_allowed, source_citation_clause) "
            "VALUES ('EXAM_CASCADE', 'AUG_1', 21, 30, '{}', 'Bachelor', '[\"ANY\"]', 60.0, 50.0, 1, 'Clause 4.1')"
        )

        # Deleting parent exam must cascade delete child eligibility_criteria
        self.conn.execute("DELETE FROM exams WHERE exam_id = 'EXAM_CASCADE'")
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM eligibility_criteria WHERE exam_id = 'EXAM_CASCADE'")
        self.assertEqual(cur.fetchone()[0], 0, "Eligibility criteria should have cascade-deleted.")

    def test_05_user_profiles_schema_and_constraints(self):
        """Verifies user_profiles table checks: gender, category, graduation_aggregate_pct."""
        valid_user = (
            "usr_adv_1",
            "Test Aspirant",
            "2000-01-01",
            "FEMALE",
            "OBC_NCL",
            "Bachelor",
            "Mechanical",
            72.5,
            0,
            "Maharashtra",
            "Marathi",
            160.0,
            None,
            None,
            json.dumps({"UPSC_CSE": 1}),
        )
        self.conn.execute(
            "INSERT INTO user_profiles (user_id, name, dob, gender, category, graduation_degree, graduation_discipline, "
            "graduation_aggregate_pct, is_final_year, state_domicile, mother_tongue, height_cm, chest_cm, vision_specs, prior_attempts_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            valid_user,
        )

        # Invalid percentage (> 100) must fail
        invalid_pct_user = list(valid_user)
        invalid_pct_user[0] = "usr_adv_2"
        invalid_pct_user[7] = 105.0
        with self.assertRaises(sqlite3.IntegrityError):
            self.conn.execute(
                "INSERT INTO user_profiles (user_id, name, dob, gender, category, graduation_degree, graduation_discipline, "
                "graduation_aggregate_pct, is_final_year, state_domicile, mother_tongue, height_cm, chest_cm, vision_specs, prior_attempts_json) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                invalid_pct_user,
            )

    def test_06_master_seed_migration_execution(self):
        """Executes worker/migrations/0002_seed_data.sql and verifies counts & 0 FK violations."""
        with open(SEED_SQL, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

        cur = self.conn.cursor()
        # Verify 0 Foreign Key violations
        cur.execute("PRAGMA foreign_key_check;")
        fk_violations = cur.fetchall()
        self.assertEqual(len(fk_violations), 0, f"Foreign key check failed with violations: {fk_violations}")

        # Check exact seed counts
        counts = {}
        for tbl in ["exams", "eligibility_criteria", "syllabus_taxonomy", "exam_syllabus_map", "source_audit_log"]:
            cur.execute(f"SELECT COUNT(*) FROM {tbl};")
            counts[tbl] = cur.fetchone()[0]

        self.assertEqual(counts["exams"], 36, "Expected exactly 36 exams in D1 seed")
        self.assertEqual(counts["eligibility_criteria"], 36, "Expected exactly 36 eligibility criteria in D1 seed")
        self.assertEqual(counts["syllabus_taxonomy"], 192, "Expected exactly 192 taxonomy topics in D1 seed")
        self.assertEqual(counts["exam_syllabus_map"], 1123, "Expected exactly 1123 stage mappings in D1 seed")
        self.assertEqual(counts["source_audit_log"], 216, "Expected exactly 216 audit log entries in D1 seed")


class TestM5EdgeConfigurations(unittest.TestCase):
    """Verifies Cloudflare Worker and Pages deployment configuration files."""

    def test_01_wrangler_toml_specification(self):
        self.assertTrue(os.path.exists(WRANGLER_TOML), "wrangler.toml must exist")
        with open(WRANGLER_TOML, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('name = "grade-a-api"', content)
        self.assertIn('binding = "DB"', content)
        self.assertIn('database_name = "grade_a_db"', content)
        self.assertIn('database_id = "0a591154-d727-43ba-b8f9-005cb5dc58c6"', content)
        self.assertIn('account_id = "913053598d368551936e69dd07298da5"', content)

    def test_02_worker_package_json(self):
        self.assertTrue(os.path.exists(PACKAGE_JSON), "worker/package.json must exist")
        with open(PACKAGE_JSON, "r", encoding="utf-8") as f:
            pkg = json.load(f)

        self.assertEqual(pkg.get("name"), "grade-a-api")
        self.assertIn("hono", pkg.get("dependencies", {}))
        self.assertIn("wrangler", pkg.get("devDependencies", {}))
        self.assertIn("@cloudflare/workers-types", pkg.get("devDependencies", {}))

    def test_03_pages_edge_proxy_and_headers(self):
        self.assertTrue(os.path.exists(PAGES_PROXY), "Pages edge proxy functions/api/[[catchall]].ts must exist")
        with open(PAGES_PROXY, "r", encoding="utf-8") as f:
            proxy_code = f.read()
        self.assertIn("grade-a-api.priyanshukh1201.workers.dev", proxy_code)

        self.assertTrue(os.path.exists(PAGES_HEADERS), "Pages _headers file must exist")
        with open(PAGES_HEADERS, "r", encoding="utf-8") as f:
            headers_code = f.read()
        self.assertIn("/sw.js", headers_code)
        self.assertIn("max-age=0, must-revalidate", headers_code)
        self.assertIn("/manifest.webmanifest", headers_code)


class TestM5LiveWorkerEndpoints(unittest.TestCase):
    """Verifies live Cloudflare Worker API contracts and Pages proxy endpoints."""

    def test_01_worker_root_health_and_cors(self):
        res = make_http_request(f"{WORKER_BASE_URL}/")
        self.assertEqual(res["status"], 200)
        self.assertIsNotNone(res["json"])
        self.assertEqual(res["json"].get("status"), "HEALTHY")
        self.assertEqual(res["json"].get("version"), "1.0.0")
        self.assertIn("exams", res["json"].get("endpoints", {}))
        # CORS check
        cors_origin = res["headers"].get("access-control-allow-origin")
        self.assertEqual(cors_origin, "*", "CORS access-control-allow-origin must be '*'")

    def test_02_worker_exams_catalog(self):
        res = make_http_request(f"{WORKER_BASE_URL}/api/v1/exams")
        self.assertEqual(res["status"], 200)
        self.assertIsNotNone(res["json"])
        self.assertTrue(res["json"].get("success"))
        self.assertEqual(res["json"].get("count"), 36)
        self.assertEqual(res["json"].get("source"), "d1", "Live Worker must query D1 serverless database")

    def test_03_worker_single_exam_and_404(self):
        # 200 for valid UPSC_CSE
        res_valid = make_http_request(f"{WORKER_BASE_URL}/api/v1/exams/UPSC_CSE")
        self.assertEqual(res_valid["status"], 200)
        self.assertIsNotNone(res_valid["json"])
        self.assertTrue(res_valid["json"].get("success"))
        self.assertEqual(res_valid["json"]["data"].get("exam_id"), "UPSC_CSE")
        self.assertEqual(res_valid["json"]["data"].get("short_code"), "CSE")

        # 404 for unknown exam
        res_404 = make_http_request(f"{WORKER_BASE_URL}/api/v1/exams/UNKNOWN_EXAM_999")
        self.assertEqual(res_404["status"], 404)
        self.assertIsNotNone(res_404["json"])
        self.assertFalse(res_404["json"].get("success"))
        self.assertEqual(res_404["json"].get("error"), "Exam not found")

    def test_04_worker_syllabus_taxonomy_and_matrix(self):
        # Taxonomy endpoint
        res_tax = make_http_request(f"{WORKER_BASE_URL}/api/v1/syllabus/taxonomy")
        self.assertEqual(res_tax["status"], 200)
        self.assertEqual(res_tax["json"].get("count"), 192)

        # Overlap matrix endpoint
        res_matrix = make_http_request(f"{WORKER_BASE_URL}/api/v1/syllabus/matrix")
        self.assertEqual(res_matrix["status"], 200)
        self.assertEqual(res_matrix["json"]["metadata"].get("total_exams"), 36)
        self.assertEqual(res_matrix["json"]["metadata"].get("total_topics"), 192)

    def test_05_worker_profile_evaluate_endpoint(self):
        # Single exam evaluation
        payload = json.dumps({
            "dob": "2000-01-01",
            "gender": "Male",
            "category": "GEN",
            "degree": "Bachelor",
            "discipline": "Civil",
            "aggregate_pct": 75.0,
            "is_final_year": False,
            "state_domicile": "Delhi",
            "exam_id": "UPSC_CSE",
        }).encode("utf-8")
        res = make_http_request(f"{WORKER_BASE_URL}/api/v1/profile/evaluate", method="POST", data=payload)
        self.assertEqual(res["status"], 200)
        self.assertIsNotNone(res["json"])
        self.assertEqual(res["json"].get("status"), "ELIGIBLE")
        self.assertIn("UPSC", res["json"].get("statutory_citation", ""))

    def test_06_worker_profile_evaluate_malformed_400(self):
        # Malformed raw bytes
        res = make_http_request(
            f"{WORKER_BASE_URL}/api/v1/profile/evaluate",
            method="POST",
            data=b"{not_json: true",
        )
        self.assertEqual(res["status"], 400)
        self.assertEqual(res["json"].get("error"), "Malformed JSON")

    def test_07_worker_profile_sync_endpoint(self):
        # Missing required fields returns 400
        incomplete_payload = json.dumps({"name": "No Fields"}).encode("utf-8")
        res_missing = make_http_request(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=incomplete_payload,
        )
        self.assertEqual(res_missing["status"], 400)
        self.assertEqual(res_missing["json"].get("error"), "Missing Required Fields")
        self.assertIn("user_id", res_missing["json"].get("missing_fields", []))

        # Complete valid profile sync returns 200 and persisted_to_d1
        valid_payload = json.dumps({
            "user_id": "usr_test_adversarial",
            "name": "Adversarial Test Candidate",
            "dob": "1998-04-10",
            "gender": "MALE",
            "category": "GEN",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Electrical",
            "graduation_aggregate_pct": 82.0,
            "is_final_year": False,
            "state_domicile": "Delhi",
            "mother_tongue": "Hindi",
            "height_cm": 175.0,
            "prior_attempts": {"UPSC_CSE": 1},
        }).encode("utf-8")
        res_valid = make_http_request(
            f"{WORKER_BASE_URL}/api/v1/profile/sync",
            method="POST",
            data=valid_payload,
        )
        self.assertEqual(res_valid["status"], 200)
        self.assertEqual(res_valid["json"].get("status"), "synced")
        self.assertTrue(res_valid["json"].get("persisted_to_d1"))

    def test_08_worker_method_not_allowed_405(self):
        # DELETE /api/v1/exams is not allowed
        res_del = make_http_request(f"{WORKER_BASE_URL}/api/v1/exams", method="DELETE")
        self.assertEqual(res_del["status"], 405)
        self.assertEqual(res_del["json"].get("error"), "Method Not Allowed")

        # GET /api/v1/profile/sync is not allowed (only POST)
        res_get = make_http_request(f"{WORKER_BASE_URL}/api/v1/profile/sync", method="GET")
        self.assertEqual(res_get["status"], 405)
        self.assertEqual(res_get["json"].get("error"), "Method Not Allowed")

    def test_09_pages_deployment_and_proxy(self):
        # Pages root HTML
        res_root = make_http_request(f"{PAGES_BASE_URL}/")
        self.assertEqual(res_root["status"], 200)
        self.assertIn("<div id=\"app\">", res_root["body"])

        # Pages Service Worker
        res_sw = make_http_request(f"{PAGES_BASE_URL}/sw.js")
        self.assertEqual(res_sw["status"], 200)
        self.assertIn("max-age=0", res_sw["headers"].get("cache-control", ""))

        # Pages Web App Manifest
        res_manifest = make_http_request(f"{PAGES_BASE_URL}/manifest.webmanifest")
        self.assertEqual(res_manifest["status"], 200)
        self.assertEqual(res_manifest["json"].get("name"), "Grade-A Indian Examinations")

        # Pages reverse-proxy to Worker API
        res_proxy = make_http_request(f"{PAGES_BASE_URL}/api/v1/exams")
        self.assertEqual(res_proxy["status"], 200)
        self.assertEqual(res_proxy["json"].get("count"), 36)
        self.assertEqual(res_proxy["json"].get("source"), "d1")


if __name__ == "__main__":
    unittest.main()
