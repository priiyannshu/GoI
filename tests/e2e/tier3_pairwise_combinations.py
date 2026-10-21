"""
Tier 3: Pairwise Combinatorial Interaction Testing (>= 25 Tests).
Covers multi-dimensional interactions across social categories, academic disciplines,
service sectors, domicile rules, and physical constraints.
Derived strictly from statutory examination notifications, gazette rules, and PROJECT.md contracts.
"""

import unittest
from typing import Any, Dict, List

from tests.e2e.oracle import UserProfile, evaluate_statutory_eligibility


class TestTier3PairwiseCombinations(unittest.TestCase):
    """Pairwise combinatorial interaction tests across categories, disciplines, and services."""

    def test_t3_01_gen_male_btech_civil_all_clusters(self):
        # Gen Male B.Tech Civil, age 25, 72%: Eligible for CSE, ESE, ONGC GT, IOCL ET, UPPSC PCS
        p = UserProfile(dob="2001-08-15", gender="Male", category="GEN", degree="Bachelor", discipline="Civil", aggregate_pct=72.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_ESE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")

    def test_t3_02_obc_male_btech_mech_psu_vs_ese(self):
        # OBC Male B.Tech Mech, age 31: ESE max 33 for OBC (Eligible), ONGC max 33 (Eligible), IOCL max 29 (Ineligible)
        p = UserProfile(dob="1996-01-15", gender="Male", category="OBC", degree="Bachelor", discipline="Mechanical", aggregate_pct=68.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_ESE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "INELIGIBLE")

    def test_t3_03_sc_female_ba_arts_regulatory_vs_civil(self):
        # SC Female BA History, age 28: Eligible for UPSC CSE, UPPSC PCS, BPSC CCE; Ineligible for ESE (Engineering only)
        p = UserProfile(dob="1999-05-10", gender="Female", category="SC", degree="Bachelor", discipline="Arts_History", aggregate_pct=58.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "BPSC_CCE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_ESE")["status"], "INELIGIBLE")

    def test_t3_04_st_male_bcom_finance_rbi_vs_nabard_vs_sidbi(self):
        # ST Male B.Com, age 27, 56% aggregate:
        # RBI Gr B reserved threshold is 50% -> Eligible
        # NABARD Gr A reserved threshold is 55% -> Eligible
        # SIDBI Gr A requires Law, Engineering, Master_Any, CA/CS/CFA -> Ineligible
        p = UserProfile(dob="2000-03-01", gender="Male", category="ST", degree="Bachelor", discipline="Commerce", aggregate_pct=56.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "NABARD_GRADE_A")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "SIDBI_GRADE_A")["status"], "INELIGIBLE")

    def test_t3_05_ews_male_btech_cs_regulatory_it_vs_gate(self):
        # EWS Male B.Tech CS, age 25, 75%: Eligible for SIDBI Engineering, ONGC CS, IOCL CS
        p = UserProfile(dob="2002-02-10", gender="Male", category="EWS", degree="Bachelor", discipline="Computer_Science", aggregate_pct=75.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "SIDBI_GRADE_A")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "ELIGIBLE")

    def test_t3_06_pwbd_gen_btech_civil_ese_vs_iocl(self):
        # PwBD Gen B.Tech Civil, age 35: ESE max 40 for PwBD (Eligible), IOCL max 36 for PwBD (Eligible)
        p = UserProfile(dob="1992-01-15", gender="Male", category="PWBD_GEN", degree="Bachelor", discipline="Civil", aggregate_pct=66.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_ESE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "ELIGIBLE")

    def test_t3_07_pwbd_sc_ba_upsc_cse_attempt_and_age_relaxations(self):
        # PwBD SC candidate, age 44, 8 prior attempts: UPSC CSE max 47 for PwBD SC with unlimited attempts -> Eligible
        p = UserProfile(dob="1983-05-20", gender="Male", category="PWBD_SC_ST", degree="Bachelor", discipline="ANY", aggregate_pct=55.0, prior_attempts={"UPSC_CSE": 8})
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "ELIGIBLE")

    def test_t3_08_ex_servicemen_bcom_defense_vs_civil(self):
        # Ex-Servicemen aged 33 with 5 years service:
        # UPSC CSE has +5 years ESM relaxation (Eligible, max 37)
        # CDS IMA has strict 19-24 combat commission age without ESM relaxation -> Ineligible
        p = UserProfile(dob="1994-04-10", gender="Male", category="GEN", degree="Bachelor", discipline="Commerce", aggregate_pct=60.0, is_ex_serviceman=True, ex_service_years=5)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CDS")["status"], "INELIGIBLE")

    def test_t3_09_gen_female_bpsc_vs_uppsc_age_divergence(self):
        # General Female aged 38 on Aug 1, 2027:
        # BPSC CCE: UR Female cap is 40 -> Eligible
        # UPPSC PCS: Gen cap is 40 -> Eligible
        # UPSC CSE: Gen cap is 32 -> Ineligible
        p = UserProfile(dob="1989-05-15", gender="Female", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=62.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "BPSC_CCE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "INELIGIBLE")

    def test_t3_10_obc_female_btech_capf_ac_physical_standards(self):
        # OBC Female B.Tech, height 158 cm (CAPF AC female min 157 cm) -> Eligible
        p = UserProfile(dob="2003-05-01", gender="Female", category="OBC", degree="Bachelor", discipline="Civil", aggregate_pct=65.0, height_cm=158.0)
        v = evaluate_statutory_eligibility(p, "UPSC_CAPF_AC")
        self.assertEqual(v["status"], "ELIGIBLE")

    def test_t3_11_gen_llb_law_sidbi_vs_state_psc_sub_registrar(self):
        # General LL.B. Law graduate: Eligible for SIDBI Gr A (Law stream accepts LL.B.) and UPPSC PCS
        p = UserProfile(dob="2000-02-15", gender="Male", category="GEN", degree="Bachelor", discipline="Law", aggregate_pct=64.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "SIDBI_GRADE_A")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")

    def test_t3_12_ews_msc_physics_cse_vs_barc(self):
        # EWS M.Sc. Physics, age 24: Eligible for UPSC CSE and BARC OCES Physics
        p = UserProfile(dob="2003-01-10", gender="Male", category="EWS", degree="Bachelor", discipline="Physics", aggregate_pct=70.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_BARC_OCES")["status"], "ELIGIBLE")

    def test_t3_13_sc_ma_economics_rbi_depr_vs_cse(self):
        # SC Economics graduate, age 33: Eligible for UPSC CSE (cap 37 for SC) and RBI Gr B (cap 35 for SC)
        p = UserProfile(dob="1994-02-20", gender="Male", category="SC", degree="Bachelor", discipline="Economics", aggregate_pct=58.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "ELIGIBLE")

    def test_t3_14_st_msc_statistics_rbi_dsim_vs_cse(self):
        # ST Statistics graduate, age 29: Eligible for UPSC CSE and RBI Gr B
        p = UserProfile(dob="1998-04-12", gender="Male", category="ST", degree="Bachelor", discipline="Statistics", aggregate_pct=55.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "ELIGIBLE")

    def test_t3_15_gen_mba_finance_sidbi_vs_rbi(self):
        # Gen MBA Finance with 65% aggregate: Eligible for SIDBI Grade A and RBI Grade B
        p = UserProfile(dob="2001-08-10", gender="Male", category="GEN", degree="Master", discipline="Master_Any", aggregate_pct=65.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "SIDBI_GRADE_A")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "ELIGIBLE")

    def test_t3_16_obc_btech_electrical_powergrid_vs_ntpc(self):
        # OBC B.Tech Electrical, age 29: PGCIL ET max 31 for OBC (Eligible), NTPC EET max 30 for OBC (Eligible)
        p = UserProfile(dob="1998-02-01", gender="Male", category="OBC", degree="Bachelor", discipline="Electrical", aggregate_pct=66.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_PGCIL_ET")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_NTPC_EET")["status"], "ELIGIBLE")

    def test_t3_17_gen_btech_chemical_iocl_vs_ongc_percentage(self):
        # Gen B.Tech Chemical with 62.0% aggregate:
        # ONGC requires 60.0% -> Eligible
        # IOCL requires 65.0% -> Ineligible
        p = UserProfile(dob="2002-05-15", gender="Male", category="GEN", degree="Bachelor", discipline="Chemical", aggregate_pct=62.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "INELIGIBLE")

    def test_t3_18_sc_btech_mining_cil_vs_ntpc_cutoff(self):
        # SC B.Tech Mining, 52% aggregate:
        # Coal India requires 50% for SC -> Eligible
        # NTPC requires 55% for SC -> Ineligible
        p = UserProfile(dob="2001-07-20", gender="Male", category="SC", degree="Bachelor", discipline="Mining", aggregate_pct=52.0)
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_COAL_INDIA_MT")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_NTPC_EET")["status"], "INELIGIBLE")

    def test_t3_19_gen_final_year_civil_cse_vs_ese_vs_gate(self):
        # Final year B.Tech Civil: Provisionally/conditionally eligible for CSE, ESE, and ONGC GT
        p = UserProfile(dob="2004-03-10", gender="Male", category="GEN", degree="Bachelor", discipline="Civil", aggregate_pct=70.0, is_final_year=True)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "CONDITIONALLY_ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_ESE")["status"], "CONDITIONALLY_ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "CONDITIONALLY_ELIGIBLE")

    def test_t3_20_obc_final_year_bcom_rbi_disallowance_vs_nabard(self):
        # Final year B.Com: Strictly ineligible for RBI Gr B, conditionally eligible for NABARD Gr A
        p = UserProfile(dob="2003-06-15", gender="Male", category="OBC", degree="Bachelor", discipline="Commerce", aggregate_pct=65.0, is_final_year=True)
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "INELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "NABARD_GRADE_A")["status"], "CONDITIONALLY_ELIGIBLE")

    def test_t3_21_gen_outside_domicile_uppsc_vs_upsc_attempts(self):
        # Delhi General applicant: In UPPSC (unlimited attempts) -> Eligible; In UPSC CSE (attempt cap 6) -> Ineligible if attempts=6
        p = UserProfile(
            dob="1999-01-01", gender="Male", category="GEN", degree="Bachelor",
            discipline="ANY", aggregate_pct=60.0, domicile_state="Delhi",
            fluent_languages=["Hindi", "English"], prior_attempts={"UPSC_CSE": 6}
        )
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "INELIGIBLE")

    def test_t3_22_st_outside_domicile_bpsc_cce_relaxation_loss(self):
        # UP ST candidate applying in Bihar (BPSC CCE), age 39:
        # Outside domicile: Mapped to General UR Male (cap 37) -> Ineligible (losing home ST cap 42)
        p = UserProfile(dob="1988-06-01", gender="Male", category="ST", degree="Bachelor", discipline="ANY", aggregate_pct=55.0, domicile_state="Uttar Pradesh")
        v = evaluate_statutory_eligibility(p, "BPSC_CCE")
        self.assertEqual(v["status"], "INELIGIBLE")
        self.assertTrue(any("Mapped to General" in r for r in v["relaxations_applied"]))

    def test_t3_23_pwbd_obc_btech_iocl_percentage_relaxation(self):
        # PwBD OBC with 57.0% in B.Tech Mechanical:
        # IOCL General requires 65.0%, but reserved/PwBD requires 55.0% -> Eligible
        p = UserProfile(dob="2000-01-10", gender="Male", category="PWBD_OBC", degree="Bachelor", discipline="Mechanical", aggregate_pct=57.0)
        v = evaluate_statutory_eligibility(p, "PSU_IOCL_ET")
        self.assertEqual(v["status"], "ELIGIBLE")

    def test_t3_24_gen_59_99_bcom_rbi_ineligible_cse_eligible(self):
        # Gen with 59.99% B.Com:
        # RBI Gr B requires 60.00% without rounding -> Ineligible
        # UPSC CSE requires Graduation with passing marks -> Eligible
        p = UserProfile(dob="2000-01-01", gender="Male", category="GEN", degree="Bachelor", discipline="Commerce", aggregate_pct=59.99)
        self.assertEqual(evaluate_statutory_eligibility(p, "RBI_GRADE_B")["status"], "INELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")

    def test_t3_25_gen_64_99_btech_iocl_ineligible_ongc_eligible(self):
        # Gen B.Tech Civil with 64.99%:
        # IOCL requires 65.00% without rounding -> Ineligible
        # ONGC requires 60.00% -> Eligible
        p = UserProfile(dob="2002-04-01", gender="Male", category="GEN", degree="Bachelor", discipline="Civil", aggregate_pct=64.99)
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_IOCL_ET")["status"], "INELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "PSU_ONGC_GT")["status"], "ELIGIBLE")

    def test_t3_26_ex_servicemen_age_deduction_upsc_vs_state_psc(self):
        # ESM aged 35 with 4 years service: Eligible for UPSC CSE (cap 32 + 5 = 37) and UPPSC PCS (cap 40 + 5 = 45)
        p = UserProfile(dob="1992-06-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=58.0, is_ex_serviceman=True, ex_service_years=4)
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CSE")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPPSC_PCS")["status"], "ELIGIBLE")

    def test_t3_27_female_widow_gen_rpsc_no_age_cap_vs_cds_ota(self):
        # Gen Widow aged 42:
        # RPSC RAS: No upper age limit for widows/divorcees in Rajasthan -> Eligible
        # CDS OTA Women: Maximum age is 25 -> Ineligible
        p = UserProfile(dob="1985-01-01", gender="Female", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=55.0, marital_status="Widow", domicile_state="Rajasthan")
        self.assertEqual(evaluate_statutory_eligibility(p, "RPSC_RAS")["status"], "ELIGIBLE")
        self.assertEqual(evaluate_statutory_eligibility(p, "UPSC_CDS")["status"], "INELIGIBLE")

    def test_t3_28_defense_personnel_disabled_in_ops_cse_relaxation(self):
        # Disabled defense personnel: up to 5 years relaxation for CSE
        p = UserProfile(dob="1992-04-01", gender="Male", category="GEN", degree="Bachelor", discipline="ANY", aggregate_pct=60.0, is_ex_serviceman=True, ex_service_years=3)
        v = evaluate_statutory_eligibility(p, "UPSC_CSE")
        self.assertEqual(v["status"], "ELIGIBLE")


if __name__ == "__main__":
    unittest.main()
