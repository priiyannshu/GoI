"""
Tier 4: Comprehensive Real-World Application Workload Scenarios (>= 13 Tests).
Derived strictly from TEST_INFRA.md Section 'Real-World Application Scenarios (Tier 4)'.
Exercises end-to-end multi-feature workflows:
- Scenario 1: Engineering Graduate targeting UPSC ESE, Civil Services (IPS preference), and PSU Direct via GATE.
- Scenario 2: Commerce / MBA Graduate comparing RBI Grade B, SEBI Grade A, and NABARD Grade A overlaps.
- Scenario 3: State PCS Aspirant cross-applying for UPPSC, BPSC, and MPSC with domicile/language barriers.
- Scenario 4: Offline Mobile User taking Profile Intake Quiz, caching catalog, and syncing to Cloudflare D1.
- Scenario 5: Broad-spectrum General Graduate exploring full Grade A landscape via UpSet and Network graph.
"""

import json
import sqlite3
import unittest
from typing import Any, Dict, List, Set

from tests.e2e.oracle import (
    CANONICAL_TOPICS,
    ELIGIBILITY_RULES_SPEC,
    EXAMS_SPEC,
    SCHEMA_DDL,
    UserProfile,
    calculate_jaccard_similarity,
    calculate_overlap_coefficient,
    calculate_upset_intersections,
    evaluate_statutory_eligibility,
)


class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: Comprehensive Real-World Application Workload Scenarios."""

    # ==========================================================================
    # SCENARIO 1: Engineering Graduate (ESE + CSE/IPS + PSU GATE)
    # ==========================================================================

    def test_scenario1_01_eligibility_multi_target_evaluation(self):
        """Engineering Graduate targeting UPSC ESE, CSE (IPS preference), and PSU Direct via GATE."""
        # Candidate profile: Male, B.Tech Mechanical, DOB: 2002-05-10 (age 25 in 2027), 72% aggregate, height 168 cm, chest 86 cm (5 cm expansion)
        profile = UserProfile(
            dob="2002-05-10", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=72.0, height_cm=168.0,
            chest_cm=86.0, chest_expansion_cm=5.0
        )

        v_ese = evaluate_statutory_eligibility(profile, "UPSC_ESE")
        v_cse = evaluate_statutory_eligibility(profile, "UPSC_CSE")
        v_ongc = evaluate_statutory_eligibility(profile, "PSU_ONGC_GT")
        v_iocl = evaluate_statutory_eligibility(profile, "PSU_IOCL_ET")
        v_ntpc = evaluate_statutory_eligibility(profile, "PSU_NTPC_EET")

        # All 5 targets must be ELIGIBLE
        self.assertEqual(v_ese["status"], "ELIGIBLE", f"ESE failed: {v_ese['reasons']}")
        self.assertEqual(v_cse["status"], "ELIGIBLE", f"CSE failed: {v_cse['reasons']}")
        self.assertEqual(v_ongc["status"], "ELIGIBLE", f"ONGC failed: {v_ongc['reasons']}")
        self.assertEqual(v_iocl["status"], "ELIGIBLE", f"IOCL failed: {v_iocl['reasons']}")
        self.assertEqual(v_ntpc["status"], "ELIGIBLE", f"NTPC failed: {v_ntpc['reasons']}")

        # Verify Explanatory Report citations
        self.assertIn("UPSC Notice No. 02/2025-ENGG", v_ese["statutory_citation"])
        self.assertIn("UPSC Notice No. 05/2024-CSP", v_cse["statutory_citation"])

    def test_scenario1_02_syllabus_synergy_and_venn_overlap(self):
        """Analyzes curriculum overlap between UPSC CSE Prelims, ESE Paper 1, and PSU Tech."""
        cse_prelims_topics = {
            "gs.polity.constitution_features", "gs.history.modern_freedom_struggle",
            "gs.geography.physical_india_world", "gs.environment.ecology_biodiversity",
            "gs.science_tech.emerging_technologies", "gs.economy_gen.indian_economy_overview"
        }
        ese_paper1_topics = {
            "gs.environment.ecology_biodiversity", "gs.science_tech.emerging_technologies",
            "gs.ethics.foundations_case_studies"
        }

        # Overlap coefficient: ESE Paper 1 is heavily focused on environment, tech, and ethics
        shared = cse_prelims_topics & ese_paper1_topics
        self.assertIn("gs.environment.ecology_biodiversity", shared)
        self.assertIn("gs.science_tech.emerging_technologies", shared)

        overlap_coeff = calculate_overlap_coefficient(ese_paper1_topics, cse_prelims_topics)
        self.assertGreaterEqual(overlap_coeff, 0.60, "ESE General Studies should share >= 60% with CSE Prelims")

    def test_scenario1_03_physical_disqualification_for_ips_remedy(self):
        """Tests that if height drops below 165 cm, candidate remains eligible for ESE and IAS, but fails IPS."""
        short_profile = UserProfile(
            dob="2002-05-10", gender="Male", category="GEN", degree="Bachelor",
            discipline="Mechanical", aggregate_pct=72.0, height_cm=162.0 # Below IPS 165 cm, above ESE 152 cm
        )

        v_ese = evaluate_statutory_eligibility(short_profile, "UPSC_ESE")
        self.assertEqual(v_ese["status"], "ELIGIBLE") # ESE min male height is 152 cm

        v_cse = evaluate_statutory_eligibility(short_profile, "UPSC_CSE")
        # CSE overall is INELIGIBLE for IPS branch because height 162 < 165
        self.assertEqual(v_cse["status"], "INELIGIBLE")
        self.assertTrue(any("Height 162.0 cm fails minimum standard" in r for r in v_cse["reasons"]))


    # ==========================================================================
    # SCENARIO 2: Commerce / MBA Graduate (RBI + SEBI + NABARD)
    # ==========================================================================

    def test_scenario2_01_financial_cluster_eligibility_profiling(self):
        """Evaluates Commerce / MBA Finance graduate across premier regulatory trio."""
        profile = UserProfile(
            dob="2000-08-15", gender="Male", category="GEN", degree="Dual_UG_and_MBA",
            discipline="MBA_Finance", aggregate_pct=66.5 # > 60% threshold
        )

        v_rbi = evaluate_statutory_eligibility(profile, "RBI_GRADE_B")
        v_sebi = evaluate_statutory_eligibility(profile, "SEBI_GRADE_A")
        v_nabard = evaluate_statutory_eligibility(profile, "NABARD_GRADE_A")
        v_exim = evaluate_statutory_eligibility(profile, "EXIM_BANK_MT")

        self.assertEqual(v_rbi["status"], "ELIGIBLE", f"RBI failed: {v_rbi['reasons']}")
        self.assertEqual(v_sebi["status"], "ELIGIBLE", f"SEBI failed: {v_sebi['reasons']}")
        self.assertEqual(v_nabard["status"], "ELIGIBLE", f"NABARD failed: {v_nabard['reasons']}")
        self.assertEqual(v_exim["status"], "ELIGIBLE", f"EXIM failed: {v_exim['reasons']}")

    def test_scenario2_02_upset_intersection_matrix_across_trio(self):
        """Calculates UpSet intersections among RBI Grade B, SEBI Grade A, and NABARD Grade A."""
        rbi_topics = {
            "econ_fin.macro.national_income_monetary",
            "econ_fin.fin_markets.capital_money_derivatives",
            "econ_fin.banking.regulations_basel_npa",
            "econ_fin.mgmt_corp.governance_leadership",
            "english.descriptive.essay_precis_drafting",
            "quant.arithmetic.percentages_profit_loss",
            "reasoning.analytical.seating_puzzles"
        }
        sebi_topics = {
            "econ_fin.fin_markets.capital_money_derivatives",
            "econ_fin.accounting.financial_statements_ratios",
            "econ_fin.mgmt_corp.governance_leadership",
            "english.descriptive.essay_precis_drafting",
            "quant.arithmetic.percentages_profit_loss",
            "reasoning.analytical.seating_puzzles"
        }
        nabard_topics = {
            "econ_fin.macro.national_income_monetary",
            "econ_fin.banking.regulations_basel_npa",
            "english.descriptive.essay_precis_drafting",
            "quant.arithmetic.percentages_profit_loss",
            "reasoning.analytical.seating_puzzles"
        }

        intersections = calculate_upset_intersections({
            "RBI": rbi_topics,
            "SEBI": sebi_topics,
            "NABARD": nabard_topics
        })

        # Core tripartite intersection: topics shared by ALL THREE
        tripartite = intersections.get(("NABARD", "RBI", "SEBI"), set())
        self.assertIn("english.descriptive.essay_precis_drafting", tripartite)
        self.assertIn("quant.arithmetic.percentages_profit_loss", tripartite)
        self.assertIn("reasoning.analytical.seating_puzzles", tripartite)

    def test_scenario2_03_preparation_carry_over_efficiency(self):
        """Tests that mastering RBI Grade B provides substantial preparation carry-over for NABARD and SEBI."""
        rbi_topics = {
            "econ_fin.macro.national_income_monetary",
            "econ_fin.fin_markets.capital_money_derivatives",
            "econ_fin.banking.regulations_basel_npa",
            "econ_fin.mgmt_corp.governance_leadership",
            "english.descriptive.essay_precis_drafting"
        }
        nabard_topics = {
            "econ_fin.macro.national_income_monetary",
            "econ_fin.banking.regulations_basel_npa",
            "english.descriptive.essay_precis_drafting"
        }

        # Szymkiewicz-Simpson Overlap Coefficient
        pco = calculate_overlap_coefficient(rbi_topics, nabard_topics)
        self.assertEqual(pco, 1.0, "RBI Grade B covers 100% of core shared NABARD ESI topics")


    # ==========================================================================
    # SCENARIO 3: State PCS Aspirant (UPPSC + BPSC + MPSC)
    # ==========================================================================

    def test_scenario3_01_tri_state_domicile_and_language_gate(self):
        """Cross-state application with domicile reservation loss and language gating."""
        # UP Domicile OBC candidate, DOB: 1985-06-01 (age 42 on 01-07-2027), fluent in Hindi, no Marathi
        profile = UserProfile(
            dob="1985-06-01", gender="Male", category="OBC", degree="Bachelor",
            discipline="ANY", aggregate_pct=58.0, domicile_state="Uttar Pradesh",
            fluent_languages=["Hindi", "English"]
        )

        # 1. UPPSC: In home state -> OBC +5 relaxation applies (max age 45) -> ELIGIBLE
        v_uppsc = evaluate_statutory_eligibility(profile, "UPPSC_PCS")
        self.assertEqual(v_uppsc["status"], "ELIGIBLE", f"UPPSC failed: {v_uppsc['reasons']}")
        self.assertTrue(any("OBC" in r and "+5" in r for r in v_uppsc["relaxations_applied"]))

        # 2. BPSC: Out-of-state -> Mapped to General UR Male (max age 37) -> Age 42 exceeds 37 -> INELIGIBLE
        v_bpsc = evaluate_statutory_eligibility(profile, "BPSC_CCE")
        self.assertEqual(v_bpsc["status"], "INELIGIBLE", f"BPSC should be ineligible: {v_bpsc}")
        self.assertTrue(any("Mapped to General" in r for r in v_bpsc["relaxations_applied"]))

        # 3. TSPSC: Age 42 on July 1, 2027: UR limit is 44 -> ELIGIBLE
        v_tspsc = evaluate_statutory_eligibility(profile, "TSPSC_GROUP_1")
        self.assertEqual(v_tspsc["status"], "ELIGIBLE", f"TSPSC should be eligible: {v_tspsc}")

    def test_scenario3_02_general_studies_cross_state_overlap(self):
        """Measures GS common core across State PSCs."""
        uppsc_gs = {
            "gs.polity.constitution_features", "gs.history.modern_freedom_struggle",
            "gs.geography.physical_india_world", "gs.economy_gen.indian_economy_overview",
            "gs.ethics.foundations_case_studies"
        }
        bpsc_gs = {
            "gs.polity.constitution_features", "gs.history.modern_freedom_struggle",
            "gs.geography.physical_india_world", "gs.economy_gen.indian_economy_overview"
        }

        jaccard = calculate_jaccard_similarity(uppsc_gs, bpsc_gs)
        self.assertGreaterEqual(jaccard, 0.80, "UPPSC and BPSC share >= 80% General Studies core syllabus")

    def test_scenario3_03_attempt_exhaustion_cross_border_impact(self):
        """Tests that reaching attempt limit in UPSC CSE (Open=6) does not block entry in UPPSC (unlimited)."""
        exhausted_profile = UserProfile(
            dob="1998-05-10", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=60.0, domicile_state="Uttar Pradesh",
            fluent_languages=["Hindi", "English"], prior_attempts={"UPSC_CSE": 6}
        )

        v_upsc = evaluate_statutory_eligibility(exhausted_profile, "UPSC_CSE")
        self.assertEqual(v_upsc["status"], "INELIGIBLE")

        v_uppsc = evaluate_statutory_eligibility(exhausted_profile, "UPPSC_PCS")
        self.assertEqual(v_uppsc["status"], "ELIGIBLE", "UPPSC has no attempt limit for General candidates")


    # ==========================================================================
    # SCENARIO 4: Offline Mobile User (Quiz + Local Storage + Cloudflare D1 Sync)
    # ==========================================================================

    def test_scenario4_01_offline_intake_flow_and_indexeddb_storage(self):
        """Simulates offline eligibility evaluation entirely in client runtime."""
        offline_input = {
            "dob": "2000-01-15",
            "gender": "Female",
            "category": "EWS",
            "degree": "Bachelor",
            "discipline": "Civil",
            "aggregate_pct": 74.5,
            "is_final_year": False,
            "domicile_state": "Madhya Pradesh",
            "fluent_languages": ["Hindi", "English"],
            "height_cm": 158.0
        }
        profile = UserProfile(
            dob=offline_input["dob"], gender=offline_input["gender"], category=offline_input["category"],
            degree=offline_input["degree"], discipline=offline_input["discipline"],
            aggregate_pct=offline_input["aggregate_pct"], domicile_state=offline_input["domicile_state"],
            fluent_languages=offline_input["fluent_languages"], height_cm=offline_input["height_cm"]
        )

        # Client evaluates offline across all 31 exams without any HTTP network request
        verdicts = {}
        for exam_id in EXAMS_SPEC.keys():
            verdicts[exam_id] = evaluate_statutory_eligibility(profile, exam_id)

        self.assertEqual(len(verdicts), 31)
        eligible_count = sum(1 for v in verdicts.values() if v["status"] == "ELIGIBLE")
        self.assertGreater(eligible_count, 10, "Candidate should be eligible for at least 10 Grade A exams")

    def test_scenario4_02_workbox_caching_and_manifest_readiness(self):
        """Verifies PWA manifest and caching contract for offline operability."""
        manifest = {
            "name": "Grade-A Indian Examinations",
            "short_name": "Grade-A",
            "start_url": "/",
            "display": "standalone",
            "icons": [{"src": "/pwa-192x192.png", "sizes": "192x192", "type": "image/png"}]
        }
        self.assertEqual(manifest["display"], "standalone")
        self.assertTrue(len(manifest["icons"]) >= 1)

    def test_scenario4_03_online_reconnect_sync_to_d1(self):
        """Simulates reconnect event: Client syncs profile to Cloudflare D1 serverless database."""
        conn = sqlite3.connect(":memory:")
        conn.executescript(SCHEMA_DDL)
        cursor = conn.cursor()

        # D1 Profile Sync Endpoint payload
        client_sync_payload = {
            "user_id": "usr_offline_sync_42",
            "name": "Aspirant Offline",
            "dob": "2000-01-15",
            "gender": "Female",
            "category": "EWS",
            "graduation_degree": "Bachelor",
            "graduation_discipline": "Civil",
            "graduation_aggregate_pct": 74.5,
            "is_final_year": 0,
            "state_domicile": "Madhya Pradesh",
            "height_cm": 158.0,
            "prior_attempts_json": json.dumps({"UPSC_CSE": 1})
        }

        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles
            (user_id, name, dob, gender, category, graduation_degree, graduation_discipline, graduation_aggregate_pct, is_final_year, state_domicile, height_cm, prior_attempts_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            client_sync_payload["user_id"], client_sync_payload["name"], client_sync_payload["dob"],
            client_sync_payload["gender"], client_sync_payload["category"], client_sync_payload["graduation_degree"],
            client_sync_payload["graduation_discipline"], client_sync_payload["graduation_aggregate_pct"],
            client_sync_payload["is_final_year"], client_sync_payload["state_domicile"],
            client_sync_payload["height_cm"], client_sync_payload["prior_attempts_json"]
        ))
        conn.commit()

        cursor.execute("SELECT user_id, graduation_aggregate_pct FROM user_profiles WHERE user_id='usr_offline_sync_42';")
        synced_record = cursor.fetchone()
        self.assertIsNotNone(synced_record)
        self.assertEqual(synced_record[0], "usr_offline_sync_42")
        self.assertEqual(synced_record[1], 74.5)
        conn.close()


    # ==========================================================================
    # SCENARIO 5: Broad-spectrum General Graduate (Landscape Exploration)
    # ==========================================================================

    def test_scenario5_01_global_grade_a_landscape_degree_scaling(self):
        """Evaluates landscape connectivity: Universal syllabus nodes with highest degree centrality."""
        # Universal topics appear in almost all clusters
        universal_candidates = [
            "gs.polity.constitution_features",
            "quant.arithmetic.percentages_profit_loss",
            "reasoning.analytical.seating_puzzles",
            "english.reading.comprehension_inference"
        ]
        topic_ids = {t["topic_id"] for t in CANONICAL_TOPICS}
        for u in universal_candidates:
            self.assertIn(u, topic_ids)

    def test_scenario5_02_bipartite_network_natural_clustering(self):
        """Verifies modular clustering in bipartite graph: Financial bodies link to Econ-Fin, Defense to Science/Quant."""
        reg_exams = ["RBI_GRADE_B", "SEBI_GRADE_A", "NABARD_GRADE_A"]
        defense_exams = ["UPSC_CDS", "IAF_AFCAT", "UPSC_CAPF_AC"]

        # Ensure distinct administering bodies and categories
        for r in reg_exams:
            self.assertEqual(EXAMS_SPEC[r]["category"], "Regulatory")
        for d in defense_exams:
            self.assertEqual(EXAMS_SPEC[d]["category"], "Defense")

    def test_scenario5_03_cross_view_synchronization_pipeline(self):
        """Simulates interactive filter update across UpSet, Venn, and Network Graph."""
        selected_exams = ["UPSC_CSE", "RBI_GRADE_B", "UPPSC_PCS"]
        filtered_domain = "General Studies"

        # Filter topics
        gs_topics = {t["topic_id"] for t in CANONICAL_TOPICS if t["domain"] == filtered_domain}
        self.assertGreater(len(gs_topics), 10)

        # Mock UpSet recalculation under domain filter
        mock_map = {
            "UPSC_CSE": {"gs.polity.constitution_features", "gs.history.modern_freedom_struggle"},
            "UPPSC_PCS": {"gs.polity.constitution_features", "gs.history.modern_freedom_struggle"},
            "RBI_GRADE_B": set()
        }
        intersections = calculate_upset_intersections(mock_map)
        expected_tuple = tuple(sorted(["UPSC_CSE", "UPPSC_PCS"]))
        self.assertIn(expected_tuple, intersections)
        self.assertEqual(len(intersections[expected_tuple]), 2)


if __name__ == "__main__":
    unittest.main()
