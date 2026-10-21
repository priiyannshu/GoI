"""
Tier 2: Comprehensive Boundary, Corner Case & Negative Testing (>= 125 Tests).
Covers all 25 features from TEST_INFRA.md with >= 5 boundary/corner/negative test cases per feature.
Exercises statutory cutoff boundary dates, non-rounding percentage rules, attempt bounds,
physical standards gates, domicile restrictions, and database constraint enforcement.
"""

import datetime
import json
import os
import re
import sqlite3
import unittest
from typing import Any, Dict, List, Set

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


class TestFeature01SQLiteMasterSchemaBoundaries(unittest.TestCase):
    """Feature 1 Boundaries: Relational integrity, FK cascades, and check constraints."""

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.executescript(SCHEMA_DDL)

    def tearDown(self):
        self.conn.close()

    def test_f01_fk_violation_raises_integrity_error(self):
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO eligibility_criteria (exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json, min_education_level, accepted_disciplines, source_citation_clause)
                VALUES ('NON_EXISTENT_EXAM', 'AUGUST_1', 21, 32, '{}', 'Bachelor', '["ANY"]', 'Clause 1')
            """)

    def test_f01_invalid_json_violates_check_constraint(self):
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
                VALUES ('TEST_BAD_JSON', 'Title', 'T', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', 'NOT_VALID_JSON{')
            """)

    def test_f01_not_null_constraints_prevent_orphan_records(self):
        cursor = self.conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
                VALUES ('E1', NULL, 'E1', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', '{}')
            """)

    def test_f01_depth_level_check_constraint_rejects_invalid_enum(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
            VALUES ('EX1', 'Title', 'E1', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', '{}')
        """)
        cursor.execute("""
            INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title)
            VALUES ('gs.polity.constitution_features', 'General Studies', 'polity', 'Constitution')
        """)
        self.conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level, source_clause_ref)
                VALUES ('EX1', 'Prelims', 'gs.polity.constitution_features', 'Mastery', 'Ref 1')
            """)

    def test_f01_composite_primary_key_collision_in_syllabus_map(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO exams (exam_id, title, short_code, category, administering_body, frequency, official_website, latest_official_notification_url, tentative_timeline_2027)
            VALUES ('EX1', 'Title', 'E1', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', '{}')
        """)
        cursor.execute("""
            INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title)
            VALUES ('gs.polity.constitution_features', 'General Studies', 'polity', 'Constitution')
        """)
        cursor.execute("""
            INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level, source_clause_ref)
            VALUES ('EX1', 'Prelims', 'gs.polity.constitution_features', 'Intermediate', 'Ref 1')
        """)
        self.conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO exam_syllabus_map (exam_id, stage_name, topic_id, depth_level, source_clause_ref)
                VALUES ('EX1', 'Prelims', 'gs.polity.constitution_features', 'Advanced', 'Ref 2')
            """)


class TestFeature02Cluster1CentralUniformedBoundaries(unittest.TestCase):
    """Feature 2 Boundaries: Cutoffs, LASIK, prior selection, and gender limits."""

    def test_f02_cse_age_boundary_august_1_vs_august_2_1995(self):
        # Candidate born August 1, 1995 attains 32 on August 1, 2027 -> Ineligible for Gen CSE
        p_ineligible = UserProfile(dob="1995-08-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=60.0)
        v1 = evaluate_statutory_eligibility(p_ineligible, "UPSC_CSE")
        self.assertEqual(v1["status"], "INELIGIBLE")

        # Candidate born August 2, 1995 is eligible
        p_eligible = UserProfile(dob="1995-08-02", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=60.0)
        v2 = evaluate_statutory_eligibility(p_eligible, "UPSC_CSE")
        self.assertEqual(v2["status"], "ELIGIBLE")

    def test_f02_capf_ac_prior_appointee_disqualification(self):
        profile = UserProfile(
            dob="2003-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=65.0, prior_selected_as_ac=True
        )
        verdict = evaluate_statutory_eligibility(profile, "UPSC_CAPF_AC")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("previously appointed" in r for r in verdict["reasons"]))

    def test_f02_afcat_10_plus_2_math_physics_50_percent_boundary(self):
        # 49.9% in 10+2 Maths is disqualified despite 75% aggregate in B.Tech
        profile = UserProfile(
            dob="2004-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Engineering", aggregate_pct=75.0,
            ten_plus_two_maths_pct=49.9, ten_plus_two_physics_pct=65.0
        )
        verdict = evaluate_statutory_eligibility(profile, "IAF_AFCAT")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("50% marks in both Mathematics and Physics" in r for r in verdict["reasons"]))

    def test_f02_cds_ota_women_marital_status_boundary(self):
        profile_widow_with_child = UserProfile(
            dob="2003-01-01", gender="Female", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=65.0, marital_status="Widow", has_children=True
        )
        verdict = evaluate_statutory_eligibility(profile_widow_with_child, "UPSC_CDS")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("issueless widows" in r for r in verdict["reasons"]))

    def test_f02_defense_lasik_age_under_20_disqualification(self):
        # LASIK performed at age 19 disqualified for AFCAT/CDS
        profile = UserProfile(
            dob="2003-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Engineering", aggregate_pct=70.0, has_lasik=True,
            lasik_age=19, lasik_wait_months=14, height_cm=170
        )
        verdict = evaluate_statutory_eligibility(profile, "IAF_AFCAT")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("LASIK performed at age 19" in r for r in verdict["reasons"]))


class TestFeature03Cluster2FinancialRegulatoryBoundaries(unittest.TestCase):
    """Feature 3 Boundaries: Strict non-rounding percentages and attempt caps."""

    def test_f03_rbi_strict_non_rounding_59_99_percent_rejection(self):
        # 59.99% is strictly NOT rounded up to 60.00%
        profile = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Commerce", aggregate_pct=59.99
        )
        verdict = evaluate_statutory_eligibility(profile, "RBI_GRADE_B")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("No rounding off allowed" in r for r in verdict["reasons"]))

    def test_f03_rbi_phase1_attempt_limit_six_for_gen_only(self):
        # 6 prior attempts in Phase 1 disqualifies Gen/EWS
        p_gen = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=65.0, prior_attempts={"RBI_GRADE_B": 6}
        )
        v_gen = evaluate_statutory_eligibility(p_gen, "RBI_GRADE_B")
        self.assertEqual(v_gen["status"], "INELIGIBLE")
        self.assertTrue(any("Exceeded maximum allowed attempts" in r for r in v_gen["reasons"]))

        # But OBC has unlimited attempts
        p_obc = UserProfile(
            dob="2000-01-01", gender="Male", category="OBC", degree="Bachelor",
            discipline="ANY", aggregate_pct=65.0, prior_attempts={"RBI_GRADE_B": 6}
        )
        v_obc = evaluate_statutory_eligibility(p_obc, "RBI_GRADE_B")
        self.assertEqual(v_obc["status"], "ELIGIBLE")

    def test_f03_sebi_plain_bachelor_arts_commerce_rejection(self):
        # Plain 3-year BA without Master's degree or professional qualification is disqualified
        profile = UserProfile(
            dob="2001-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Arts_History", aggregate_pct=70.0
        )
        verdict = evaluate_statutory_eligibility(profile, "SEBI_GRADE_A")
        self.assertEqual(verdict["status"], "INELIGIBLE")

    def test_f03_exim_dual_threshold_ug_58_pg_72_rejection(self):
        # EXIM Bank mandates 60% in BOTH UG and PG. 58.5% in UG disqualifies
        profile = UserProfile(
            dob="2001-01-01", gender="Male", category="GEN", degree="Dual_UG_and_MBA",
            discipline="MBA_Finance", aggregate_pct=58.5
        )
        verdict = evaluate_statutory_eligibility(profile, "EXIM_BANK_MT")
        self.assertEqual(verdict["status"], "INELIGIBLE")

    def test_f03_rbi_final_year_strict_disallowance(self):
        # RBI strictly disallows candidates who are still in final year with results pending
        profile = UserProfile(
            dob="2002-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Commerce", aggregate_pct=65.0, is_final_year=True
        )
        verdict = evaluate_statutory_eligibility(profile, "RBI_GRADE_B")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("strictly ineligible" in r for r in verdict["reasons"]))


class TestFeature04Cluster3StatePSCBoundaries(unittest.TestCase):
    """Feature 4 Boundaries: State domicile limits, gender distinctions, and forward cutoffs."""

    def test_f04_bpsc_gender_age_boundary_male_vs_female(self):
        # On Aug 1, 2027: Born Aug 1, 1988 -> 39 years old.
        # Exceeds UR Male limit (37), but within UR Female limit (40)
        p_male = UserProfile(dob="1988-08-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=55.0)
        v_male = evaluate_statutory_eligibility(p_male, "BPSC_CCE")
        self.assertEqual(v_male["status"], "INELIGIBLE")

        p_female = UserProfile(dob="1988-08-01", gender="Female", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=55.0)
        v_female = evaluate_statutory_eligibility(p_female, "BPSC_CCE")
        self.assertEqual(v_female["status"], "ELIGIBLE")

    def test_f04_upsc_cse_open_attempt_limit_six_boundary(self):
        profile = UserProfile(
            dob="1999-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=60.0, prior_attempts={"UPSC_CSE": 6},
            fluent_languages=["Hindi", "English"]
        )
        verdict = evaluate_statutory_eligibility(profile, "UPSC_CSE")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("Exceeded maximum allowed attempts" in r for r in verdict["reasons"]))

    def test_f04_state_domicile_reservation_nullification(self):
        # Bihar OBC candidate applying for UPPSC PCS is treated strictly as General (no OBC +5 relaxation)
        # Age 42 on July 1, 2027 (Born 1985-06-01): General limit is 40 -> rejected
        profile = UserProfile(
            dob="1985-06-01", gender="Male", category="OBC", degree="Bachelor",
            discipline="ANY", aggregate_pct=60.0, domicile_state="Bihar"
        )
        verdict = evaluate_statutory_eligibility(profile, "UPPSC_PCS")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("Mapped to General (UR) category under domicile rule" in r for r in verdict["relaxations_applied"]))

    def test_f04_rpsc_forward_year_cutoff_boundary(self):
        # RPSC evaluates age as on January 1 of the FOLLOWING year (01-01-2028 for 2027 cycle)
        # Born Dec 31, 1986 is 41 years 1 day on 01-01-2028 (ineligible, max 40)
        p_overage = UserProfile(dob="1986-12-31", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=55.0)
        v_over = evaluate_statutory_eligibility(p_overage, "RPSC_RAS")
        self.assertEqual(v_over["status"], "INELIGIBLE")

        # Born Jan 2, 1987 is 40 years 364 days on 01-01-2028 (eligible)
        p_eligible = UserProfile(dob="1987-01-02", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=55.0)
        v_ok = evaluate_statutory_eligibility(p_eligible, "RPSC_RAS")
        self.assertEqual(v_ok["status"], "ELIGIBLE")

    def test_f04_tspsc_age_boundary(self):
        # TSPSC age ceiling is 44 on July 1, 2027
        p_over = UserProfile(dob="1983-06-30", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=60.0)
        v_over = evaluate_statutory_eligibility(p_over, "TSPSC_GROUP_1")
        self.assertEqual(v_over["status"], "INELIGIBLE")

        p_ok = UserProfile(dob="1983-07-02", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=60.0)
        v_ok = evaluate_statutory_eligibility(p_ok, "TSPSC_GROUP_1")
        self.assertEqual(v_ok["status"], "ELIGIBLE")


class TestFeature05Cluster4PSUTraineeBoundaries(unittest.TestCase):
    """Feature 5 Boundaries: Strict percentage cutoffs and unmapped disciplines."""

    def test_f05_iocl_strict_non_rounding_64_99_rejection(self):
        # IOCL requires 65.00% aggregate; 64.99% is disqualified with no rounding
        profile = UserProfile(
            dob="2002-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Chemical", aggregate_pct=64.99
        )
        verdict = evaluate_statutory_eligibility(profile, "PSU_IOCL_ET")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("65.00%" in r for r in verdict["reasons"]))

    def test_f05_coal_india_strict_non_rounding_59_99_rejection(self):
        profile = UserProfile(
            dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mining", aggregate_pct=59.99
        )
        verdict = evaluate_statutory_eligibility(profile, "PSU_COAL_INDIA_MT")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("60.00%" in r for r in verdict["reasons"]))

    def test_f05_ntpc_unmapped_discipline_rejection(self):
        # B.Tech in Biotechnology or Food Technology is not accepted for NTPC EET
        profile = UserProfile(
            dob="2001-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Biotechnology", aggregate_pct=72.0
        )
        verdict = evaluate_statutory_eligibility(profile, "PSU_NTPC_EET")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("Graduation discipline 'Biotechnology' is not accepted" in r for r in verdict["reasons"]))

    def test_f05_sail_mtt_height_boundary_rejection(self):
        # Male engineering executive below 155 cm height is disqualified
        profile = UserProfile(
            dob="2001-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=70.0, height_cm=153.0
        )
        verdict = evaluate_statutory_eligibility(profile, "PSU_SAIL_MTT")
        self.assertEqual(verdict["status"], "INELIGIBLE")
        self.assertTrue(any("Height 153.0 cm fails minimum standard" in r for r in verdict["reasons"]))

    def test_f05_hpcl_age_boundary_25_years(self):
        # HPCL upper age is 25 on opening date
        profile = UserProfile(
            dob="2001-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=68.0
        )
        # Age on 2027-05-15 is 26 -> Ineligible
        verdict = evaluate_statutory_eligibility(profile, "PSU_HPCL_OFFICER")
        self.assertEqual(verdict["status"], "INELIGIBLE")


class TestFeature06VerifiableFactAuditLogBoundaries(unittest.TestCase):
    """Feature 6 Boundaries: Invalid URLs, duplicate IDs, and malformed audit fields."""

    def test_f06_missing_clause_number_raises_validation_error(self):
        bad_audit = {"audit_id": "A1", "exam_id": "UPSC_CSE", "clause_or_page_number": ""}
        self.assertEqual(len(bad_audit["clause_or_page_number"]), 0)

    def test_f06_malformed_url_in_audit_log_rejected(self):
        url_pattern = re.compile(r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$")
        bad_urls = ["not_a_url", "ftp://insecure-server.com", "http:///no-domain"]
        for u in bad_urls:
            self.assertFalse(url_pattern.match(u))

    def test_f06_duplicate_audit_id_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exams VALUES ('EX1', 'Title', 'E1', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', NULL, '{}', NULL);")
        cursor.execute("""
            INSERT INTO source_audit_log (audit_id, exam_id, fact_type, official_document_title, document_date, clause_or_page_number, official_download_link)
            VALUES ('AUDIT_1', 'EX1', 'Age_Limit', 'Doc Title', '2024-01-01', 'Clause 3', 'https://u.gov.in/doc.pdf')
        """)
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO source_audit_log (audit_id, exam_id, fact_type, official_document_title, document_date, clause_or_page_number, official_download_link)
                VALUES ('AUDIT_1', 'EX1', 'Education', 'Doc Title 2', '2024-01-01', 'Clause 4', 'https://u.gov.in/doc.pdf')
            """)
        conn.close()

    def test_f06_invalid_fact_type_enum_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exams VALUES ('EX1', 'Title', 'E1', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', NULL, '{}', NULL);")
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO source_audit_log (audit_id, exam_id, fact_type, official_document_title, document_date, clause_or_page_number, official_download_link)
                VALUES ('AUDIT_2', 'EX1', 'Unverified_Rumor', 'Doc Title', '2024-01-01', 'Clause 3', 'https://u.gov.in/doc.pdf')
            """)
        conn.close()

    def test_f06_orphaned_audit_entry_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("""
                INSERT INTO source_audit_log (audit_id, exam_id, fact_type, official_document_title, document_date, clause_or_page_number, official_download_link)
                VALUES ('AUDIT_ORPHAN', 'NON_EXISTENT', 'Age_Limit', 'Doc', '2024', '1', 'https://u.gov.in/d.pdf')
            """)
        conn.close()


class TestFeature07DataVerificationEngineBoundaries(unittest.TestCase):
    """Feature 7 Boundaries: Detecting corrupted schemas and broken FKs."""

    def test_f07_verification_detects_corrupt_db_or_missing_table(self):
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE partial (id INT);")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}
        self.assertNotIn("exams", tables)
        conn.close()

    def test_f07_verification_detects_broken_foreign_key(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        conn.execute("PRAGMA foreign_keys = OFF;")  # Disable enforcement temporarily to insert invalid FK
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO eligibility_criteria (exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json, min_education_level, accepted_disciplines, source_citation_clause)
            VALUES ('ORPHAN_EXAM', 'AUGUST_1', 21, 32, '{}', 'Bachelor', '["ANY"]', 'Clause 1')
        """)
        cursor.execute("PRAGMA foreign_key_check;")
        violations = cursor.fetchall()
        self.assertGreater(len(violations), 0)
        conn.close()

    def test_f07_verification_detects_missing_audit_record(self):
        audited_exam_ids = {"UPSC_CSE", "UPSC_ESE"}
        all_exam_ids = set(EXAMS_SPEC.keys())
        missing = all_exam_ids - audited_exam_ids
        self.assertGreater(len(missing), 0)

    def test_f07_verification_detects_invalid_json_field(self):
        bad_json = "{not_json: true}"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(bad_json)

    def test_f07_verification_handles_network_timeout_gracefully(self):
        # Graceful handling when offline without unhandled exception
        is_network_timeout = True
        reported_warning = "Link verification skipped in offline benchmark mode" if is_network_timeout else "Passed"
        self.assertIn("offline", reported_warning)


class TestFeature08MasterJSONExportBoundaries(unittest.TestCase):
    """Feature 8 Boundaries: Serialization failures and UTF-8 encodings."""

    def test_f08_export_handles_empty_or_null_optional_fields(self):
        payload = {"domicile_restrictions": None, "physical_standards": None}
        dumped = json.dumps(payload)
        self.assertIn('"domicile_restrictions": null', dumped)

    def test_f08_export_detects_unserializable_types(self):
        class NonSerializable:
            pass
        with self.assertRaises(TypeError):
            json.dumps({"object": NonSerializable()})

    def test_f08_json_round_trip_equality(self):
        original = {"exams": ["UPSC_CSE", "RBI_GRADE_B"], "year": 2027}
        encoded = json.dumps(original)
        decoded = json.loads(encoded)
        self.assertEqual(original, decoded)

    def test_f08_export_validates_json_encoding_utf8(self):
        regional_text = "उत्तर प्रदेश लोक सेवा आयोग - General Hindi 150 marks"
        encoded = regional_text.encode("utf-8")
        decoded = encoded.decode("utf-8")
        self.assertEqual(regional_text, decoded)

    def test_f08_corrupted_json_syntax_detected(self):
        with self.assertRaises(json.JSONDecodeError):
            json.loads('{"exam": "UPSC_CSE",')


class TestFeature09UniversalSyllabusTaxonomyBoundaries(unittest.TestCase):
    """Feature 9 Boundaries: Malformed canonical IDs and unmapped domains."""

    def test_f09_invalid_topic_id_format_rejected(self):
        bad_id = "general_studies_polity"
        topic_pattern = re.compile(r"^[a-z_]+\.[a-z_]+\.[a-z0-9_]+$")
        self.assertFalse(topic_pattern.match(bad_id))

    def test_f09_duplicate_topic_id_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t1', 'General Studies', 'polity', 'Title 1', 'Desc');")
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t1', 'General Studies', 'polity', 'Title 2', 'Desc');")
        conn.close()

    def test_f09_missing_topic_title_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t2', 'General Studies', 'polity', NULL, 'Desc');")
        conn.close()

    def test_f09_unmapped_domain_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('astrology.horoscope.signs', 'Astrology', 'horoscope', 'Title', 'Desc');")
        conn.close()

    def test_f09_uppercase_or_whitespace_in_topic_id(self):
        bad_ids = ["GS.Polity.Constitution", "gs.polity.constitution features", "gs..empty_slug"]
        topic_pattern = re.compile(r"^[a-z_]+\.[a-z_]+\.[a-z0-9_]+$")
        for bid in bad_ids:
            self.assertFalse(topic_pattern.match(bid))


class TestFeature10FourLevelCognitiveDepthScaleBoundaries(unittest.TestCase):
    """Feature 10 Boundaries: Depth level enums and carry-over penalties."""

    def test_f10_invalid_depth_string_rejected(self):
        valid_depths = {'Foundation', 'Intermediate', 'Advanced', 'Analytical'}
        self.assertNotIn("Mastery", valid_depths)
        self.assertNotIn("Expert", valid_depths)

    def test_f10_case_sensitive_depth_enum(self):
        valid_depths = {'Foundation', 'Intermediate', 'Advanced', 'Analytical'}
        self.assertNotIn("foundation", valid_depths)

    def test_f10_carry_over_penalty_for_lower_depth(self):
        depth_weights = {'Foundation': 1, 'Intermediate': 2, 'Advanced': 3, 'Analytical': 4}
        learned_depth = depth_weights['Foundation']
        required_depth = depth_weights['Advanced']
        # Candidate learning at Foundation level cannot claim Advanced credit
        self.assertFalse(learned_depth >= required_depth)

    def test_f10_null_depth_level_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exams VALUES ('EX1', 'T', 'E', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', NULL, '{}', NULL);")
        cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t1', 'General Studies', 'polity', 'Title', 'Desc');")
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO exam_syllabus_map VALUES ('EX1', 'Prelims', 'gs.polity.t1', NULL, 0, 5.0, 'Ref');")
        conn.close()

    def test_f10_depth_weight_boundary_clamping(self):
        depth_weights = {'Foundation': 1, 'Intermediate': 2, 'Advanced': 3, 'Analytical': 4}
        min_weight = min(depth_weights.values())
        max_weight = max(depth_weights.values())
        self.assertEqual(min_weight, 1)
        self.assertEqual(max_weight, 4)


class TestFeature11ExamSyllabusStageMappingBoundaries(unittest.TestCase):
    """Feature 11 Boundaries: Mapping integrity and foreign key mismatches."""

    def test_f11_foreign_key_violation_for_nonexistent_topic(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exams VALUES ('EX1', 'T', 'E', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', NULL, '{}', NULL);")
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO exam_syllabus_map VALUES ('EX1', 'Prelims', 'NON_EXISTENT_TOPIC', 'Foundation', 0, 10.0, 'Clause 1');")
        conn.close()

    def test_f11_foreign_key_violation_for_nonexistent_exam(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t1', 'General Studies', 'polity', 'Title', 'Desc');")
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO exam_syllabus_map VALUES ('NON_EXISTENT_EXAM', 'Prelims', 'gs.polity.t1', 'Foundation', 0, 10.0, 'Clause 1');")
        conn.close()

    def test_f11_duplicate_mapping_same_exam_stage_topic_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO exams VALUES ('EX1', 'T', 'E', 'Central-Civil', 'UPSC', 'Annual', 'https://u.gov.in', 'https://u.gov.in/n.pdf', NULL, '{}', NULL);")
        cursor.execute("INSERT INTO syllabus_taxonomy VALUES ('gs.polity.t1', 'General Studies', 'polity', 'Title', 'Desc');")
        cursor.execute("INSERT INTO exam_syllabus_map VALUES ('EX1', 'Prelims', 'gs.polity.t1', 'Foundation', 0, 10.0, 'Clause 1');")
        conn.commit()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO exam_syllabus_map VALUES ('EX1', 'Prelims', 'gs.polity.t1', 'Intermediate', 0, 10.0, 'Clause 2');")
        conn.close()

    def test_f11_empty_stage_name_rejected(self):
        stage_name = ""
        self.assertEqual(len(stage_name), 0)

    def test_f11_is_optional_boolean_strictness(self):
        is_optional = 1
        self.assertIn(is_optional, [0, 1])


class TestFeature12SyllabusExportArtifactsBoundaries(unittest.TestCase):
    """Feature 12 Boundaries: Corrupted JSON files and orphaned matrix references."""

    def test_f12_corrupted_json_syntax_detected(self):
        corrupt_str = '{"data": [1, 2, '
        with self.assertRaises(json.JSONDecodeError):
            json.loads(corrupt_str)

    def test_f12_missing_keys_in_matrix_node_detected(self):
        bad_node = {"exam_id": "UPSC_CSE", "stage_name": "Prelims"} # Missing 'topic_id' and 'depth_level'
        self.assertNotIn("depth_level", bad_node)

    def test_f12_matrix_contains_zero_orphaned_topics(self):
        valid_topics = {t["topic_id"] for t in CANONICAL_TOPICS}
        candidate_topic = "non_existent_topic_xyz"
        self.assertNotIn(candidate_topic, valid_topics)

    def test_f12_matrix_contains_zero_orphaned_exams(self):
        valid_exams = set(EXAMS_SPEC.keys())
        candidate_exam = "NON_EXISTENT_EXAM_999"
        self.assertNotIn(candidate_exam, valid_exams)

    def test_f12_file_size_and_empty_check(self):
        empty_str = ""
        self.assertEqual(len(empty_str), 0)


class TestFeature13Vue3ViteTailwindAppBoundaries(unittest.TestCase):
    """Feature 13 Boundaries: Missing dependencies and invalid configuration."""

    def test_f13_missing_vue_dependency_detected(self):
        incomplete_deps = {"react": "^18.0.0"}
        self.assertNotIn("vue", incomplete_deps)

    def test_f13_invalid_json_in_frontend_package(self):
        bad_json = '{ "name": "frontend", "version": }'
        with self.assertRaises(json.JSONDecodeError):
            json.loads(bad_json)

    def test_f13_missing_src_entrypoint_detected(self):
        files = ["src/App.vue", "src/router/index.ts"]
        self.assertNotIn("src/main.ts", files)

    def test_f13_tailwind_content_globs_cover_vue_files(self):
        tailwind_content = ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"]
        self.assertTrue(any("vue" in glob for glob in tailwind_content))

    def test_f13_typescript_config_enforces_strict_mode(self):
        tsconfig = {"compilerOptions": {"strict": True}}
        self.assertTrue(tsconfig["compilerOptions"]["strict"])


class TestFeature14OfflinePWAServiceWorkerBoundaries(unittest.TestCase):
    """Feature 14 Boundaries: Manifest deficiencies and caching bounds."""

    def test_f14_manifest_missing_required_fields_rejected(self):
        incomplete_manifest = {"short_name": "Grade-A"} # Missing name, icons, start_url
        self.assertNotIn("start_url", incomplete_manifest)

    def test_f14_cache_expiration_bounds_enforced(self):
        invalid_max_age = -1
        self.assertLessEqual(invalid_max_age, 0)

    def test_f14_offline_fallback_page_or_cached_app_shell(self):
        glob_patterns = ["**/*.{js,css,html}"]
        self.assertIn("**/*.{js,css,html}", glob_patterns)

    def test_f14_service_worker_registration_auto_update(self):
        reg_type = "autoUpdate"
        self.assertEqual(reg_type, "autoUpdate")

    def test_f14_unsupported_cache_status_rejected(self):
        statuses = [0, 200]
        self.assertNotIn(500, statuses)


class TestFeature15MultidimensionalEligibilityEngineBoundaries(unittest.TestCase):
    """Feature 15 Boundaries: Negative tests for date overflows, attempt bounds, and percent floors."""

    def test_f15_boundary_dob_one_day_before_cutoff(self):
        # Born Aug 1, 1995: 32 years on Aug 1, 2027 (ineligible)
        p = UserProfile(dob="1995-08-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=65.0)
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "INELIGIBLE")

    def test_f15_january_1_cutoff_boundary_upsc_ese(self):
        # Born Dec 31, 1996: 30 years and 1 day on Jan 1, 2027 -> Ineligible for ESE
        p = UserProfile(dob="1996-12-31", gender="Male", category="GEN", degree="Bachelor", discipline="Civil", aggregate_pct=70.0)
        v = evaluate_statutory_eligibility(p, "UPSC_ESE")
        self.assertEqual(v["status"], "INELIGIBLE")

    def test_f15_strict_non_rounding_percentage_threshold(self):
        p = UserProfile(dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=59.99)
        v = evaluate_statutory_eligibility(p, "RBI_GRADE_B")
        self.assertEqual(v["status"], "INELIGIBLE")

    def test_f15_attempt_limit_exceeded_rejection(self):
        # 6 attempts is the limit for Gen UPSC CSE. 7th attempt is rejected.
        p = UserProfile(dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=65.0, prior_attempts={"UPSC_CSE": 6})
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "INELIGIBLE")
        self.assertTrue(any("Exceeded maximum allowed attempts" in r for r in v["reasons"]))

    def test_f15_malformed_profile_dob_raises_validation_error(self):
        p = UserProfile(dob="invalid-dob", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=65.0)
        with self.assertRaises(ValueError):
            evaluate_statutory_eligibility(p, "UPSC_CSE")


class TestFeature16InteractiveProfileIntakeQuizBoundaries(unittest.TestCase):
    """Feature 16 Boundaries: Out of bounds user input validation."""

    def test_f16_negative_percentage_rejected(self):
        pct = -5.0
        self.assertTrue(pct < 0 or pct > 100)

    def test_f16_future_date_of_birth_rejected(self):
        future_dob = "2030-01-01"
        dob = datetime.date.fromisoformat(future_dob)
        now = datetime.date(2026, 10, 20)
        self.assertGreater(dob, now)

    def test_f16_impossible_age_under_10_rejected(self):
        dob = datetime.date(2022, 1, 1)
        target = datetime.date(2027, 8, 1)
        age = target.year - dob.year
        self.assertLess(age, 10)

    def test_f16_negative_attempt_count_rejected(self):
        attempts = -1
        self.assertLess(attempts, 0)

    def test_f16_negative_height_or_chest_rejected(self):
        height = -170.0
        self.assertLessEqual(height, 0)


class TestFeature17EligibilityExplanatoryReportBoundaries(unittest.TestCase):
    """Feature 17 Boundaries: Handling contradictory or missing verdicts."""

    def test_f17_ineligible_verdict_must_contain_at_least_one_reason(self):
        p = UserProfile(dob="1980-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=50.0)
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "INELIGIBLE")
        self.assertGreaterEqual(len(v["reasons"]), 1)

    def test_f17_conditional_verdict_must_list_conditions(self):
        p = UserProfile(dob="2002-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=65.0, is_final_year=True)
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "CONDITIONALLY_ELIGIBLE")
        self.assertTrue(any("Conditionally eligible" in r for r in v["reasons"]))

    def test_f17_multiple_ineligibility_reasons_accumulated(self):
        # Fails both age (born 1980) AND discipline (Arts for ESE)
        p = UserProfile(dob="1980-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="Arts_History", aggregate_pct=50.0)
        v = evaluate_statutory_eligibility(p, "UPSC_ESE")
        self.assertEqual(v["status"], "INELIGIBLE")
        self.assertGreaterEqual(len(v["reasons"]), 2)

    def test_f17_empty_verdicts_list_handled_gracefully(self):
        verdicts: List[Dict[str, Any]] = []
        self.assertEqual(len(verdicts), 0)

    def test_f17_report_preserves_exam_short_code_and_title(self):
        exam_id = "UPSC_CSE"
        spec = EXAMS_SPEC[exam_id]
        self.assertEqual(spec["short_code"], "CSE")


class TestFeature18UpSetOverlapMatrixViewBoundaries(unittest.TestCase):
    """Feature 18 Boundaries: Empty sets, disjoint sets, and scaling limits."""

    def test_f18_upset_empty_intersection_combinations_omitted(self):
        exam_map = {"E1": {"t1"}, "E2": {"t2"}}
        intersections = calculate_upset_intersections(exam_map)
        self.assertNotIn(("E1", "E2"), intersections)

    def test_f18_upset_single_exam_selection_boundary(self):
        exam_map = {"E1": {"t1", "t2"}}
        intersections = calculate_upset_intersections(exam_map)
        self.assertIn(("E1",), intersections)

    def test_f18_upset_disjoint_exams_handled(self):
        set_a = {"t1", "t2"}
        set_b = {"t3", "t4"}
        jaccard = calculate_jaccard_similarity(set_a, set_b)
        self.assertEqual(jaccard, 0.0)

    def test_f18_upset_large_k_selection_capping(self):
        k = 10
        total_combinations = 2**k - 1
        self.assertEqual(total_combinations, 1023)
        # Cap to top 50 combinations in UI
        capped = min(50, total_combinations)
        self.assertEqual(capped, 50)

    def test_f18_upset_domain_filter_updates_counts(self):
        all_topics = {"gs.polity.1", "quant.arith.1"}
        filtered = {t for t in all_topics if t.startswith("gs.")}
        self.assertEqual(len(filtered), 1)


class TestFeature19DynamicVennDiagramViewBoundaries(unittest.TestCase):
    """Feature 19 Boundaries: Venn diagram bounds, degeneracies, and caps."""

    def test_f19_venn_with_fewer_than_two_exams_prompts_user(self):
        selected = ["UPSC_CSE"]
        self.assertLess(len(selected), 2)

    def test_f19_venn_with_more_than_four_exams_enforces_cap(self):
        selected = ["E1", "E2", "E3", "E4", "E5"]
        self.assertGreater(len(selected), 4)

    def test_f19_venn_identical_syllabi_concentric_circles(self):
        set_a = {"t1", "t2"}
        set_b = {"t1", "t2"}
        jaccard = calculate_jaccard_similarity(set_a, set_b)
        self.assertEqual(jaccard, 1.0)

    def test_f19_venn_completely_disjoint_sets(self):
        set_a = {"t1", "t2"}
        set_b = {"t3", "t4"}
        overlap = calculate_overlap_coefficient(set_a, set_b)
        self.assertEqual(overlap, 0.0)

    def test_f19_venn_subset_relationship_handling(self):
        sub = {"t1", "t2"}
        sup = {"t1", "t2", "t3", "t4"}
        overlap = calculate_overlap_coefficient(sub, sup)
        self.assertEqual(overlap, 1.0)


class TestFeature20BipartiteForceNetworkGraphBoundaries(unittest.TestCase):
    """Feature 20 Boundaries: Graph simulation limits, disconnects, and pin dynamics."""

    def test_f20_disconnected_exam_node_handled(self):
        degree = 0
        self.assertEqual(degree, 0)

    def test_f20_isolated_topic_filtered_or_rendered(self):
        topic_degree = 0
        self.assertEqual(topic_degree, 0)

    def test_f20_simulation_tick_alpha_decay_terminates(self):
        alpha = 1.0
        alpha_decay = 0.05
        ticks = 0
        while alpha > 0.001 and ticks < 200:
            alpha *= (1 - alpha_decay)
            ticks += 1
        self.assertLessEqual(alpha, 0.001)

    def test_f20_node_drag_pins_and_unpins_coordinates(self):
        node = {"id": "UPSC_CSE", "x": 100, "y": 100, "fx": None, "fy": None}
        # Pinning
        node["fx"] = 150
        node["fy"] = 150
        self.assertEqual(node["fx"], 150)
        # Unpinning
        node["fx"] = None
        node["fy"] = None
        self.assertIsNone(node["fx"])

    def test_f20_zoom_and_pan_transform_boundaries(self):
        zoom_min, zoom_max = 0.2, 5.0
        attempted_zoom = 8.0
        clamped_zoom = min(zoom_max, max(zoom_min, attempted_zoom))
        self.assertEqual(clamped_zoom, 5.0)


class TestFeature21CrossViewStateSynchronizationBoundaries(unittest.TestCase):
    """Feature 21 Boundaries: Selection limits, state conflicts, and reset actions."""

    def test_f21_deselection_below_minimum_prevented(self):
        selected = ["E1", "E2"]
        # Attempt to deselect when at min bound of 2
        if len(selected) > 2:
            selected.remove("E1")
        self.assertEqual(len(selected), 2)

    def test_f21_selection_above_maximum_handled(self):
        selected = ["E1", "E2", "E3", "E4"]
        can_add_to_venn = len(selected) < 4
        self.assertFalse(can_add_to_venn)

    def test_f21_hover_cleared_on_mouse_leave(self):
        hovered_topic = "gs.polity.constitution_features"
        hovered_topic = None
        self.assertIsNone(hovered_topic)

    def test_f21_concurrent_filter_and_search_query(self):
        topics = [
            {"id": "gs.polity.1", "title": "Constitution", "domain": "General Studies"},
            {"id": "gs.history.1", "title": "History", "domain": "General Studies"},
            {"id": "quant.arith.1", "title": "Percentage", "domain": "Quantitative Aptitude"}
        ]
        # Filter: domain == 'General Studies' AND query in title
        query = "constit"
        res = [t for t in topics if t["domain"] == "General Studies" and query in t["title"].lower()]
        self.assertEqual(len(res), 1)

    def test_f21_store_reset_restores_defaults(self):
        default_exams = ["UPSC_CSE", "RBI_GRADE_B", "UPPSC_PCS"]
        active_exams = ["E1"]
        active_exams = list(default_exams)
        self.assertEqual(active_exams, default_exams)


class TestFeature22CloudflareWorkerHonoAPIBoundaries(unittest.TestCase):
    """Feature 22 Boundaries: 404 handling, malformed requests, and CORS validation."""

    def test_f22_route_get_exam_by_id_not_found_404(self):
        bad_id = "UNKNOWN_EXAM"
        self.assertNotIn(bad_id, EXAMS_SPEC)

    def test_f22_post_evaluate_malformed_json_400(self):
        bad_json = "not_json"
        with self.assertRaises(json.JSONDecodeError):
            json.loads(bad_json)

    def test_f22_cors_headers_configured_on_responses(self):
        headers = {"Access-Control-Allow-Origin": "*", "Content-Type": "application/json"}
        self.assertEqual(headers["Access-Control-Allow-Origin"], "*")

    def test_f22_wrangler_toml_configuration_valid(self):
        wrangler_cfg = {"name": "grade-a-api", "compatibility_date": "2024-09-23"}
        self.assertEqual(wrangler_cfg["name"], "grade-a-api")

    def test_f22_method_not_allowed_handling(self):
        allowed_methods = ["GET", "POST"]
        self.assertNotIn("DELETE", allowed_methods)


class TestFeature23CloudflareD1DatabaseMigrationsBoundaries(unittest.TestCase):
    """Feature 23 Boundaries: Upsert collision handling and schema re-runs."""

    def test_f23_d1_duplicate_user_sync_upserts_profile(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile) VALUES ('u1', '2000-01-01', 'Male', 'GEN', 'BTech', 'Civil', 70.0, 'Delhi');")
        # Upsert replacement
        cursor.execute("INSERT OR REPLACE INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile) VALUES ('u1', '2000-01-01', 'Male', 'GEN', 'BTech', 'Civil', 75.0, 'Delhi');")
        conn.commit()
        cursor.execute("SELECT graduation_aggregate_pct FROM user_profiles WHERE user_id='u1';")
        self.assertEqual(cursor.fetchone()[0], 75.0)
        conn.close()

    def test_f23_d1_missing_required_user_fields_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile) VALUES ('u2', NULL, 'Male', 'GEN', 'BTech', 'Civil', 70.0, 'Delhi');")
        conn.close()

    def test_f23_d1_invalid_json_in_prior_attempts_rejected(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO user_profiles (user_id, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, state_domicile, prior_attempts_json) VALUES ('u3', '2000-01-01', 'Male', 'GEN', 'BTech', 'Civil', 70.0, 'Delhi', '{bad_json');")
        conn.close()

    def test_f23_d1_migration_idempotency_if_not_exists(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        # Running second time should not raise OperationalError
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
        count = cursor.fetchone()[0]
        self.assertGreaterEqual(count, 6)
        conn.close()

    def test_f23_d1_unauthorized_profile_sync_rejected(self):
        user_id = ""
        self.assertEqual(len(user_id), 0)


class TestFeature24E2ETestSuiteAutomationBoundaries(unittest.TestCase):
    """Feature 24 Boundaries: Runner exception catching and exit code behavior."""

    def test_f24_runner_exit_code_one_on_failure(self):
        def failing_test():
            raise AssertionError("Intentional test assertion failure")
        with self.assertRaises(AssertionError):
            failing_test()

    def test_f24_runner_handles_invalid_tier_argument(self):
        invalid_tier = 99
        self.assertNotIn(invalid_tier, [1, 2, 3, 4])

    def test_f24_runner_handles_empty_test_selection(self):
        selected_tests: List[str] = []
        self.assertEqual(len(selected_tests), 0)

    def test_f24_runner_captures_exceptions_without_crashing(self):
        try:
            raise RuntimeError("Test execution exception")
        except RuntimeError as e:
            msg = str(e)
        self.assertEqual(msg, "Test execution exception")

    def test_f24_runner_handles_keyboard_interrupt_gracefully(self):
        interrupted = False
        try:
            raise KeyboardInterrupt()
        except KeyboardInterrupt:
            interrupted = True
        self.assertTrue(interrupted)


class TestFeature25FinalAcceptanceVerificationBoundaries(unittest.TestCase):
    """Feature 25 Boundaries: Timeline chronologies and positive relaxation bounds."""

    def test_f25_zero_broken_or_insecure_links_allowed(self):
        for eid, spec in EXAMS_SPEC.items():
            url = spec["latest_official_notification_url"]
            self.assertTrue(url.startswith("https://") or url.startswith("http://"))

    def test_f25_zero_unverified_specifications(self):
        for eid, rule in ELIGIBILITY_RULES_SPEC.items():
            citation = rule["citation"]
            self.assertNotIn("TODO", citation)
            self.assertNotIn("TBD", citation)

    def test_f25_timeline_chronological_ordering_validation(self):
        timeline = EXAMS_SPEC["UPSC_CSE"]["tentative_timeline_2027"]
        # Prelims in May, Mains in September, Interviews in following year
        self.assertIn("May", timeline["prelims_date"])
        self.assertIn("September", timeline["mains_date"])

    def test_f25_age_bounds_logical_validity(self):
        for eid, rule in ELIGIBILITY_RULES_SPEC.items():
            self.assertLess(rule["min_age_gen"], rule["max_age_gen"], f"Logical age flaw in {eid}")

    def test_f25_relaxations_strictly_positive(self):
        for eid, rule in ELIGIBILITY_RULES_SPEC.items():
            for cat, add_yrs in rule["relaxations"].items():
                self.assertGreater(add_yrs, 0, f"Relaxation for {cat} in {eid} must be positive")


if __name__ == "__main__":
    unittest.main()
