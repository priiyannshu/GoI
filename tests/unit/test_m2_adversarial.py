#!/usr/bin/env python3
"""
tests/unit/test_m2_adversarial.py
=================================
Adversarial Empirical Challenge Harness for Milestone 2 (M2_SYLLABUS_TAXONOMY).

Empirically challenges and stress-tests:
1. SQLite Foreign Key enforcement on `exam_syllabus_map` (invalid topic_id, invalid exam_id).
2. SQLite CHECK constraints on depth levels ('Mastery', 'Expert', 'Novice', empty).
3. SQLite CHECK constraints on weightage ranges (<0.0% or >100.0%).
4. Domain CHECK constraints on `syllabus_taxonomy`.
5. Jaccard similarity symmetry J(A, B) == J(B, A) and self-similarity J(A, A) == 1.0 across all 36x36 pairs.
6. Szymkiewicz-Simpson overlap coefficient symmetry.
7. Preparation Carry-Over (PCO) asymmetry: PCO(UPSC CSE -> CSAT) vs PCO(CSAT -> UPSC CSE), and cross-exam PCO.
8. UpSet disjointness: partition completeness, mutual disjointness, and exact 1:1 topic-combination mapping.
9. Negative corruption probes against ingestion engine and database validator.
"""

import copy
import json
import os
import re
import sqlite3
import tempfile
import unittest
from typing import Any, Dict, List, Set

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DB_PATH = os.path.join(BASE_DIR, "data", "grade_a_exams.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "data", "schema.sql")
TAXONOMY_JSON_PATH = os.path.join(BASE_DIR, "data", "syllabus_taxonomy.json")
MATRIX_JSON_PATH = os.path.join(BASE_DIR, "data", "exam_syllabus_matrix.json")

from scripts.populate_syllabus_taxonomy import SyllabusIngestionEngine
from scripts.verify_database import SyllabusTaxonomyAndMatrixValidator

DEPTH_RANK = {
    "Foundation": 1,
    "Intermediate": 2,
    "Advanced": 3,
    "Analytical": 4
}


class TestM2AdversarialDatabaseConstraints(unittest.TestCase):
    """Adversarially tests schema constraints, foreign keys, and CHECK rules on SQLite."""

    def setUp(self):
        # We test both on a freshly initialized in-memory database and using the master DB
        self.mem_conn = sqlite3.connect(":memory:")
        self.mem_conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            self.mem_conn.executescript(f.read())

        # Seed valid master exam and topic for negative testing
        self.mem_conn.execute("""
            INSERT INTO exams (
                exam_id, title, short_code, category, administering_body, frequency,
                official_website, latest_official_notification_url, tentative_timeline_2027
            ) VALUES (
                'TEST_EXAM_01', 'Test Examination', 'TEST', 'Central-Civil', 'UPSC', 'Annual',
                'https://example.gov.in', 'https://example.gov.in/notif.pdf', '{"notification_month": "February"}'
            );
        """)
        self.mem_conn.execute("""
            INSERT INTO syllabus_taxonomy (
                topic_id, domain, sub_domain, topic_title, description
            ) VALUES (
                'general_studies.ancient_history.indus_valley_civilization',
                'General Studies', 'Ancient History', 'Indus Valley Civilization', 'Harappan culture'
            );
        """)
        self.mem_conn.commit()

        # Master DB read-write connection with explicit rollback protection
        self.db_conn = sqlite3.connect(DB_PATH)
        self.db_conn.execute("PRAGMA foreign_keys = ON;")

    def tearDown(self):
        self.mem_conn.close()
        self.db_conn.rollback()
        self.db_conn.close()

    def test_probe_fk_rejection_on_invalid_topic_id(self):
        """Probe: Inserting an exam stage mapping with a non-existent topic_id must fail."""
        with self.assertRaises(sqlite3.IntegrityError, msg="Expected FK failure on invalid topic_id"):
            self.mem_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'TEST_EXAM_01', 'Stage 1', 'non_existent.topic.id_9999', 'Foundation', 0, 10.0, 'Clause 1'
                );
            """)

        # Also probe on real database
        with self.assertRaises(sqlite3.IntegrityError, msg="Expected FK failure on master DB"):
            self.db_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'UPSC_CSE', 'Prelims Paper 1', 'invalid.phantom.topic_slug', 'Foundation', 0, 5.0, 'Clause X'
                );
            """)

    def test_probe_fk_rejection_on_invalid_exam_id(self):
        """Probe: Inserting an exam stage mapping with a non-existent exam_id must fail."""
        with self.assertRaises(sqlite3.IntegrityError, msg="Expected FK failure on invalid exam_id"):
            self.mem_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'PHANTOM_EXAM_GHOST', 'Stage 1', 'general_studies.ancient_history.indus_valley_civilization',
                    'Foundation', 0, 10.0, 'Clause 1'
                );
            """)

    def test_probe_depth_level_check_constraint_invalid_enums(self):
        """Probe: Inserting invalid depth level enums ('Mastery', 'Expert', 'Novice', 'Beginner', '') must fail."""
        invalid_depths = ["Mastery", "Expert", "Novice", "Beginner", "High", "Low", ""]
        for bad_depth in invalid_depths:
            with self.subTest(bad_depth=bad_depth):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"CHECK failed to reject depth '{bad_depth}'"):
                    self.mem_conn.execute("""
                        INSERT INTO exam_syllabus_map (
                            exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                        ) VALUES (
                            'TEST_EXAM_01', 'Stage 1', 'general_studies.ancient_history.indus_valley_civilization',
                            ?, 0, 10.0, 'Clause 1'
                        );
                    """, (bad_depth,))

    def test_probe_depth_level_valid_enums(self):
        """Probe: All four canonical depth levels must be accepted by CHECK constraint."""
        valid_depths = ["Foundation", "Intermediate", "Advanced", "Analytical"]
        for idx, good_depth in enumerate(valid_depths):
            stage = f"Stage_{idx}"
            self.mem_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'TEST_EXAM_01', ?, 'general_studies.ancient_history.indus_valley_civilization',
                    ?, 0, 10.0, 'Clause 1'
                );
            """, (stage, good_depth))
        # Verify all 4 rows inserted
        count = self.mem_conn.execute("SELECT COUNT(*) FROM exam_syllabus_map;").fetchone()[0]
        self.assertEqual(count, 4)

    def test_probe_weightage_negative_ranges(self):
        """Probe: Inserting negative weightage (-0.01%, -5.0%, -100.0%) must fail."""
        negative_weights = [-0.01, -1.0, -5.0, -100.0]
        for bad_w in negative_weights:
            with self.subTest(bad_w=bad_w):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"CHECK failed to reject weightage {bad_w}"):
                    self.mem_conn.execute("""
                        INSERT INTO exam_syllabus_map (
                            exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                        ) VALUES (
                            'TEST_EXAM_01', 'Stage Neg', 'general_studies.ancient_history.indus_valley_civilization',
                            'Foundation', 0, ?, 'Clause 1'
                        );
                    """, (bad_w,))

    def test_probe_weightage_excessive_ranges(self):
        """Probe: Inserting weightage > 100.0% (100.01%, 105.0%, 250.0%) must fail."""
        excessive_weights = [100.01, 105.0, 150.0, 500.0]
        for bad_w in excessive_weights:
            with self.subTest(bad_w=bad_w):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"CHECK failed to reject weightage {bad_w}"):
                    self.mem_conn.execute("""
                        INSERT INTO exam_syllabus_map (
                            exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                        ) VALUES (
                            'TEST_EXAM_01', 'Stage Exc', 'general_studies.ancient_history.indus_valley_civilization',
                            'Foundation', 0, ?, 'Clause 1'
                        );
                    """, (bad_w,))

    def test_probe_weightage_valid_boundary_values(self):
        """Probe: Boundary weightages 0.0, 100.0, fractional 12.34, and NULL must succeed."""
        test_cases = [
            ("Stage_Zero", 0.0),
            ("Stage_Hundred", 100.0),
            ("Stage_Fractional", 12.34),
            ("Stage_Null", None)
        ]
        for stage, w in test_cases:
            self.mem_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'TEST_EXAM_01', ?, 'general_studies.ancient_history.indus_valley_civilization',
                    'Foundation', 0, ?, 'Clause 1'
                );
            """, (stage, w))
        count = self.mem_conn.execute("SELECT COUNT(*) FROM exam_syllabus_map;").fetchone()[0]
        self.assertEqual(count, 4)

    def test_probe_domain_enum_check_constraint(self):
        """Probe: syllabus_taxonomy must reject non-canonical domains."""
        invalid_domains = ["Astrobiology", "Computer Science", "Law", "Art", ""]
        for bad_domain in invalid_domains:
            with self.subTest(bad_domain=bad_domain):
                with self.assertRaises(sqlite3.IntegrityError, msg=f"Domain CHECK failed on '{bad_domain}'"):
                    self.mem_conn.execute("""
                        INSERT INTO syllabus_taxonomy (
                            topic_id, domain, sub_domain, topic_title, description
                        ) VALUES (
                            'tech.cs.dummy_topic', ?, 'Sub', 'Title', 'Desc'
                        );
                    """, (bad_domain,))

    def test_probe_composite_primary_key_uniqueness(self):
        """Probe: Primary key (exam_id, stage_name, topic_id) must prevent duplicate mappings."""
        self.mem_conn.execute("""
            INSERT INTO exam_syllabus_map (
                exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
            ) VALUES (
                'TEST_EXAM_01', 'Stage 1', 'general_studies.ancient_history.indus_valley_civilization',
                'Foundation', 0, 10.0, 'Clause 1'
            );
        """)
        with self.assertRaises(sqlite3.IntegrityError, msg="Expected UNIQUE/PK failure on duplicate mapping"):
            self.mem_conn.execute("""
                INSERT INTO exam_syllabus_map (
                    exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
                ) VALUES (
                    'TEST_EXAM_01', 'Stage 1', 'general_studies.ancient_history.indus_valley_civilization',
                    'Advanced', 1, 20.0, 'Clause 2'
                );
            """)

    def test_probe_cascading_delete(self):
        """Probe: Deleting a topic from syllabus_taxonomy must cascade-delete all its stage mappings."""
        self.mem_conn.execute("""
            INSERT INTO exam_syllabus_map (
                exam_id, stage_name, topic_id, depth_level, is_optional, weightage_pct_estimate, source_clause_ref
            ) VALUES (
                'TEST_EXAM_01', 'Stage 1', 'general_studies.ancient_history.indus_valley_civilization',
                'Foundation', 0, 10.0, 'Clause 1'
            );
        """)
        self.assertEqual(self.mem_conn.execute("SELECT COUNT(*) FROM exam_syllabus_map;").fetchone()[0], 1)
        self.mem_conn.execute("DELETE FROM syllabus_taxonomy WHERE topic_id = 'general_studies.ancient_history.indus_valley_civilization';")
        self.assertEqual(self.mem_conn.execute("SELECT COUNT(*) FROM exam_syllabus_map;").fetchone()[0], 0)


class TestM2AdversarialMathematicalMetrics(unittest.TestCase):
    """Adversarially tests mathematical set analysis metrics in exam_syllabus_matrix.json."""

    @classmethod
    def setUpClass(cls):
        with open(MATRIX_JSON_PATH, "r", encoding="utf-8") as f:
            cls.matrix_data = json.load(f)
        cls.pairwise = cls.matrix_data["pairwise_metrics"]
        cls.exam_ids = sorted(list(cls.pairwise.keys()))
        cls.exam_summaries = cls.matrix_data["exam_summaries"]

    def test_pairwise_matrix_completeness_36x36(self):
        """Ensure pairwise metrics contain exactly 36 source exams and 36 target exams each (1,296 pairs)."""
        self.assertEqual(len(self.exam_ids), 36)
        for eid in self.exam_ids:
            targets = list(self.pairwise[eid].keys())
            self.assertEqual(len(targets), 36, f"Exam {eid} does not have 36 targets")

    def test_jaccard_symmetry_all_pairs(self):
        """Verify Jaccard symmetry: J(A, B) == J(B, A) for all 1,296 pairs."""
        for a in self.exam_ids:
            for b in self.exam_ids:
                j_ab = self.pairwise[a][b]["jaccard_similarity"]
                j_ba = self.pairwise[b][a]["jaccard_similarity"]
                self.assertEqual(
                    j_ab, j_ba,
                    f"Jaccard asymmetry detected between {a} and {b}: J({a}, {b})={j_ab} != J({b}, {a})={j_ba}"
                )

    def test_jaccard_self_similarity_all_exams(self):
        """Verify self-similarity: J(A, A) == 1.0 for all 36 examinations."""
        for a in self.exam_ids:
            j_aa = self.pairwise[a][a]["jaccard_similarity"]
            self.assertEqual(j_aa, 1.0, f"Self-similarity failure for {a}: J({a}, {a})={j_aa}")

    def test_jaccard_bounds(self):
        """Verify Jaccard similarity is strictly bounded in [0.0, 1.0]."""
        for a in self.exam_ids:
            for b in self.exam_ids:
                j = self.pairwise[a][b]["jaccard_similarity"]
                self.assertTrue(0.0 <= j <= 1.0, f"Jaccard out of bounds for ({a}, {b}): {j}")

    def test_simpson_overlap_symmetry(self):
        """Verify Szymkiewicz-Simpson Overlap coefficient symmetry: Overlap(A, B) == Overlap(B, A)."""
        for a in self.exam_ids:
            for b in self.exam_ids:
                o_ab = self.pairwise[a][b]["overlap_coefficient"]
                o_ba = self.pairwise[b][a]["overlap_coefficient"]
                self.assertEqual(
                    o_ab, o_ba,
                    f"Simpson overlap asymmetry between {a} and {b}: {o_ab} != {o_ba}"
                )

    def test_simpson_overlap_self_similarity(self):
        """Verify Szymkiewicz-Simpson self-overlap: Overlap(A, A) == 1.0."""
        for a in self.exam_ids:
            o_aa = self.pairwise[a][a]["overlap_coefficient"]
            self.assertEqual(o_aa, 1.0, f"Simpson self-overlap failure for {a}: {o_aa}")

    def test_intersection_and_union_mathematical_invariants(self):
        """Verify set theory invariants: |A ∪ B| == |A| + |B| - |A ∩ B| and |A ∩ B| <= min(|A|, |B|)."""
        for a in self.exam_ids:
            len_a = self.exam_summaries[a]["total_topics"]
            for b in self.exam_ids:
                len_b = self.exam_summaries[b]["total_topics"]
                entry = self.pairwise[a][b]
                inter = entry["intersection_count"]
                union = entry["union_count"]

                self.assertEqual(
                    union, len_a + len_b - inter,
                    f"Inclusion-exclusion principle violated for ({a}, {b}): {union} != {len_a} + {len_b} - {inter}"
                )
                self.assertTrue(
                    inter <= min(len_a, len_b),
                    f"Intersection larger than minimum set size for ({a}, {b}): {inter} > min({len_a}, {len_b})"
                )

    def test_pco_asymmetry_upsc_cse_vs_csat(self):
        """Verify empirical PCO asymmetry between full UPSC CSE and CSAT stage:
        Preparing for full UPSC CSE covers 100% of CSAT stage topics,
        whereas CSAT covers only 43.04% of UPSC CSE total syllabus.
        """
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT stage_name, topic_id, depth_level FROM exam_syllabus_map WHERE exam_id = 'UPSC_CSE';")
        rows = c.fetchall()
        conn.close()

        cse_topics = {}
        csat_topics = {}
        for stage, tid, depth in rows:
            rank = DEPTH_RANK[depth]
            cse_topics[tid] = max(cse_topics.get(tid, 0), rank)
            if "CSAT" in stage:
                csat_topics[tid] = max(csat_topics.get(tid, 0), rank)

        # Total counts
        self.assertEqual(len(cse_topics), 79, "UPSC CSE expected to have 79 total distinct topics")
        self.assertEqual(len(csat_topics), 34, "CSAT stage expected to have 34 distinct topics")

        # PCO(UPSC CSE -> CSAT)
        inter = set(cse_topics.keys()) & set(csat_topics.keys())
        self.assertEqual(inter, set(csat_topics.keys()), "All CSAT topics must be in UPSC CSE")
        suff_cse_to_csat = [t for t in inter if cse_topics[t] >= csat_topics[t]]
        pco_cse_to_csat = len(suff_cse_to_csat) / len(csat_topics) * 100.0

        # PCO(CSAT -> UPSC CSE)
        suff_csat_to_cse = [t for t in inter if csat_topics[t] >= cse_topics[t]]
        pco_csat_to_cse = len(suff_csat_to_cse) / len(cse_topics) * 100.0

        self.assertEqual(pco_cse_to_csat, 100.0, "PCO(UPSC CSE -> CSAT) must be 100.0%")
        self.assertAlmostEqual(pco_csat_to_cse, 43.04, places=2, msg="PCO(CSAT -> UPSC CSE) must be 43.04%")
        self.assertGreater(pco_cse_to_csat, pco_csat_to_cse, "PCO must be strictly asymmetric")

    def test_pco_cross_exam_asymmetry_prevalence(self):
        """Verify that PCO is fundamentally an asymmetric metric across exam pairs."""
        asymmetric_pairs = 0
        total_non_disjoint = 0

        for i, a in enumerate(self.exam_ids):
            for j, b in enumerate(self.exam_ids):
                if i >= j:
                    continue
                pco_ab = self.pairwise[a][b]["pco_efficiency_pct"]
                pco_ba = self.pairwise[b][a]["pco_efficiency_pct"]
                if pco_ab > 0.0 or pco_ba > 0.0:
                    total_non_disjoint += 1
                    if pco_ab != pco_ba:
                        asymmetric_pairs += 1

        asym_ratio = asymmetric_pairs / total_non_disjoint if total_non_disjoint > 0 else 0
        # Over 95% of non-disjoint exam pairs have asymmetric PCO efficiency
        self.assertGreaterEqual(
            asym_ratio, 0.75,
            f"Expected at least 75% asymmetric PCO pairs, got {asym_ratio * 100:.1f}% ({asymmetric_pairs}/{total_non_disjoint})"
        )

    def test_pco_self_efficiency(self):
        """Verify self-PCO: PCO(A -> A) == 100.0% for all 36 examinations."""
        for a in self.exam_ids:
            pco_aa = self.pairwise[a][a]["pco_efficiency_pct"]
            self.assertEqual(pco_aa, 100.0, f"Self-PCO failure for {a}: PCO({a} -> {a})={pco_aa}%")


class TestM2AdversarialUpSetDisjointness(unittest.TestCase):
    """Adversarially tests UpSet disjoint intersection properties."""

    @classmethod
    def setUpClass(cls):
        with open(MATRIX_JSON_PATH, "r", encoding="utf-8") as f:
            cls.matrix_data = json.load(f)
        cls.upset = cls.matrix_data["disjoint_upset_combinations"]

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT topic_id FROM syllabus_taxonomy;")
        cls.all_topics = {r[0] for r in c.fetchall()}

        # Build ground truth topic -> exam_ids map from SQLite
        c.execute("SELECT DISTINCT exam_id, topic_id FROM exam_syllabus_map;")
        cls.ground_truth_map: Dict[str, Set[str]] = {}
        for eid, tid in c.fetchall():
            cls.ground_truth_map.setdefault(tid, set()).add(eid)
        conn.close()

    def test_upset_disjointness_every_topic_in_exactly_one_combination(self):
        """Verify UpSet disjointness: every topic belongs to exactly ONE combination."""
        topic_combination_map: Dict[str, str] = {}
        duplicates = []

        for comb in self.upset:
            cid = comb["combination_id"]
            for tid in comb["topic_ids"]:
                if tid in topic_combination_map:
                    duplicates.append((tid, topic_combination_map[tid], cid))
                topic_combination_map[tid] = cid

        self.assertEqual(len(duplicates), 0, f"Found topics belonging to multiple UpSet combinations: {duplicates}")
        self.assertEqual(
            len(topic_combination_map), len(self.all_topics),
            f"Expected all {len(self.all_topics)} topics to be mapped, found {len(topic_combination_map)}"
        )

    def test_upset_mutual_disjointness_between_all_combination_pairs(self):
        """Verify pairwise disjointness: intersection of topic sets between any two combinations is empty."""
        for i, comb_i in enumerate(self.upset):
            set_i = set(comb_i["topic_ids"])
            for j, comb_j in enumerate(self.upset):
                if i >= j:
                    continue
                set_j = set(comb_j["topic_ids"])
                overlap = set_i & set_j
                self.assertEqual(
                    len(overlap), 0,
                    f"Combinations {comb_i['combination_id']} and {comb_j['combination_id']} share topics: {overlap}"
                )

    def test_upset_sum_of_topic_counts_equals_total_topics(self):
        """Verify the sum of topic counts across all combinations equals 192."""
        total_count = sum(c["topic_count"] for c in self.upset)
        self.assertEqual(total_count, 192, f"Total UpSet topic count {total_count} != 192")

    def test_upset_degree_and_count_internal_consistency(self):
        """Verify degree == len(exam_ids) and topic_count == len(topic_ids) for every combination."""
        for comb in self.upset:
            cid = comb["combination_id"]
            self.assertEqual(
                comb["degree"], len(comb["exam_ids"]),
                f"Degree mismatch in {cid}: {comb['degree']} != {len(comb['exam_ids'])}"
            )
            self.assertEqual(
                comb["topic_count"], len(comb["topic_ids"]),
                f"Topic count mismatch in {cid}: {comb['topic_count']} != {len(comb['topic_ids'])}"
            )
            self.assertGreater(comb["degree"], 0, f"Empty exam_ids in {cid}")
            self.assertGreater(comb["topic_count"], 0, f"Empty topic_ids in {cid}")

    def test_upset_ground_truth_database_membership_accuracy(self):
        """Verify that every combination's exam_ids match the actual database membership exactly."""
        for comb in self.upset:
            expected_exams = set(comb["exam_ids"])
            for tid in comb["topic_ids"]:
                actual_exams = self.ground_truth_map.get(tid, set())
                self.assertEqual(
                    actual_exams, expected_exams,
                    f"Topic {tid} actual exams {actual_exams} != UpSet combination exams {expected_exams}"
                )


class TestM2AdversarialNegativeValidationProbes(unittest.TestCase):
    """Negative corruption probes against IngestionEngine and SyllabusTaxonomyAndMatrixValidator."""

    def test_ingestion_engine_rejection_probes(self):
        """Ensure SyllabusIngestionEngine raises ValueError on corrupted records."""
        with tempfile.NamedTemporaryFile(suffix=".db") as tf:
            db_path = tf.name

        # Create schema
        conn = sqlite3.connect(db_path)
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.close()

        engine = SyllabusIngestionEngine(db_path)
        valid_exams = {"TEST_EXAM"}
        valid_topics = {"general_studies.ancient_history.indus_valley"}

        # 1. Invalid topic_id regex
        bad_topic = {"topic_id": "BadTopicID", "domain": "General Studies", "sub_domain": "Sub", "topic_title": "T"}
        with self.assertRaises(ValueError):
            engine.validate_topic_record(bad_topic, 1)

        # 2. Invalid domain
        bad_domain = {"topic_id": "domain.sub.slug", "domain": "Astronomy", "sub_domain": "Sub", "topic_title": "T"}
        with self.assertRaises(ValueError):
            engine.validate_topic_record(bad_domain, 2)

        # 3. Missing topic_title
        bad_title = {"topic_id": "domain.sub.slug", "domain": "General Studies", "sub_domain": "Sub", "topic_title": ""}
        with self.assertRaises(ValueError):
            engine.validate_topic_record(bad_title, 3)

        # 4. Unknown exam in mapping
        bad_map_exam = {
            "exam_id": "UNKNOWN_EXAM", "stage_name": "Stage 1", "topic_id": "general_studies.ancient_history.indus_valley",
            "depth_level": "Foundation", "source_clause_ref": "Clause 1"
        }
        with self.assertRaises(ValueError):
            engine.validate_map_record(bad_map_exam, 1, valid_exams, valid_topics)

        # 5. Invalid depth in mapping
        bad_map_depth = {
            "exam_id": "TEST_EXAM", "stage_name": "Stage 1", "topic_id": "general_studies.ancient_history.indus_valley",
            "depth_level": "Mastery", "source_clause_ref": "Clause 1"
        }
        with self.assertRaises(ValueError):
            engine.validate_map_record(bad_map_depth, 2, valid_exams, valid_topics)

        # 6. Negative weightage in mapping
        bad_map_weight = {
            "exam_id": "TEST_EXAM", "stage_name": "Stage 1", "topic_id": "general_studies.ancient_history.indus_valley",
            "depth_level": "Foundation", "weightage_pct_estimate": -10.0, "source_clause_ref": "Clause 1"
        }
        with self.assertRaises(ValueError):
            engine.validate_map_record(bad_map_weight, 3, valid_exams, valid_topics)

        # 7. Missing source_clause_ref in mapping
        bad_map_clause = {
            "exam_id": "TEST_EXAM", "stage_name": "Stage 1", "topic_id": "general_studies.ancient_history.indus_valley",
            "depth_level": "Foundation", "source_clause_ref": ""
        }
        with self.assertRaises(ValueError):
            engine.validate_map_record(bad_map_clause, 4, valid_exams, valid_topics)

    def test_validator_catches_orphan_topics(self):
        """Ensure SyllabusTaxonomyAndMatrixValidator catches orphan topics in the database."""
        conn = sqlite3.connect(":memory:")
        conn.execute("PRAGMA foreign_keys = ON;")
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        # Copy real database into memory using SQLite backup API
        src_conn = sqlite3.connect(DB_PATH)
        src_conn.backup(conn)
        src_conn.close()

        # Add an orphan topic
        conn.execute("""
            INSERT INTO syllabus_taxonomy (topic_id, domain, sub_domain, topic_title, description)
            VALUES ('general_studies.history.orphan_topic_test', 'General Studies', 'History', 'Orphan Topic', 'Test');
        """)
        conn.commit()

        validator = SyllabusTaxonomyAndMatrixValidator(conn, BASE_DIR)
        errors = validator.verify()
        self.assertTrue(
            any("orphan topics" in err.lower() for err in errors),
            f"Validator failed to detect orphan topic. Errors returned: {errors}"
        )
        conn.close()


if __name__ == "__main__":
    unittest.main()
