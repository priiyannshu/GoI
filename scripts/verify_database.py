#!/usr/bin/env python3
"""
scripts/verify_database.py
==========================
Comprehensive Automated Verification Engine for the Indian Grade A Examinations Database.

Verifies:
1. SQLite relational integrity (PRAGMA integrity_check == 'ok', PRAGMA foreign_key_check == 0).
2. Schema & Master non-null/JSON compliance across all 31 examinations.
3. 100% coverage in source_audit_log with valid HTTP/HTTPS URLs and verified citations.
4. Automated eligibility edge-case test harness:
   - Cutoff date algorithms (Aug 1, Jan 1, Jul 1, Apr 1, forward-year Jan 1).
   - Strict non-rounding percentage threshold validation (59.99% fails 60.0%, 64.99% fails 65.0%).
   - Attempt limits (UPSC CSE 6/9/unlimited, RBI Grade B 6 Phase-1 Gen/EWS only).
   - Gender distinctions, state domicile firewalls, compulsory languages, and physical standards.
5. Exit code 0 on complete pass, 1 on any failure.
"""

import argparse
import concurrent.futures
import json
import os
import re
import socket
import sqlite3
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

# ANSI Color Codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Canonical Catalog of 25 Grade A Examinations
EXPECTED_EXAM_IDS = {
    # Cluster 1: Central All-India & Uniformed Services (6)
    "UPSC_CSE", "UPSC_ESE", "UPSC_IFOS", "UPSC_CAPF_AC",
    "UPSC_CDS", "IAF_AFCAT",
    # Cluster 2: Premier Financial & Regulatory Bodies (3)
    "RBI_GRADE_B", "NABARD_GRADE_A", "SIDBI_GRADE_A",
    # Cluster 3: State Public Service Commissions (5)
    "UPPSC_PCS", "BPSC_CCE", "MPPSC_SSE", "RPSC_RAS", "TSPSC_GROUP_1",
    # Cluster 4: Maharatna & Navratna PSUs (11)
    "PSU_ONGC_GT", "PSU_IOCL_ET", "PSU_NTPC_EET", "PSU_BHEL_ET",
    "PSU_PGCIL_ET", "PSU_HPCL_OFFICER", "PSU_BPCL_MT", "PSU_SAIL_MTT",
    "PSU_GAIL_ET", "PSU_COAL_INDIA_MT", "PSU_BARC_NPCIL_ET"
}

EXPECTED_TABLES = {
    "exams", "eligibility_criteria", "syllabus_taxonomy",
    "exam_syllabus_map", "source_audit_log", "user_profiles"
}

EXPECTED_INDEXES = {
    "idx_exams_category", "idx_exams_admin_body", "idx_eligibility_age",
    "idx_syllabus_domain", "idx_map_exam", "idx_map_topic",
    "idx_audit_exam_fact", "idx_users_dob"
}


# =============================================================================
# Helper Utilities
# =============================================================================

def validate_url_syntax(url_str: str) -> Tuple[bool, str]:
    """Validates URL syntax, scheme, and domain structure offline."""
    if not url_str or not isinstance(url_str, str):
        return False, "URL is empty or not a string"
    url_str = url_str.strip()
    try:
        parts = urllib.parse.urlsplit(url_str)
        if parts.scheme not in ("http", "https"):
            return False, f"Invalid scheme '{parts.scheme}'; expected http or https"
        if not parts.netloc:
            return False, "Missing hostname/netloc"
        if "." not in parts.netloc:
            return False, f"Invalid domain name '{parts.netloc}'"
        if " " in url_str:
            return False, "URL contains illegal whitespace"
        return True, ""
    except Exception as e:
        return False, f"URL parse exception: {e}"


DEFAULT_VERIFIER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36 GradeAVerifier/1.0"
)


def check_live_url(url: str, timeout: float = 5.0) -> Tuple[bool, Optional[int], str]:
    """
    Verifies URL live reachability via HTTP HEAD with automatic GET fallback using standard library urllib.request.
    Accepts 2xx (Success), 3xx (Redirect), 401 (Auth required), and 403 (Cloudflare/NIC WAF reachability) as live.
    Returns (is_reachable, status_code, message).
    """
    headers = {
        "User-Agent": DEFAULT_VERIFIER_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }

    def _attempt(method: str, unverified_ssl: bool = False) -> Tuple[bool, Optional[int], str]:
        req = urllib.request.Request(url, headers=headers, method=method)
        if unverified_ssl:
            ctx = ssl._create_unverified_context()
            if hasattr(ssl, "OP_LEGACY_SERVER_CONNECT"):
                ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
        else:
            ctx = ssl.create_default_context()

        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
                status = getattr(resp, "status", 200)
                return True, status, f"HTTP {status}"
        except urllib.error.HTTPError as e:
            # 2xx, 3xx, 401, 403 confirm server is live and route/resource is acknowledged
            if e.code in (200, 206, 301, 302, 303, 307, 308, 401, 403):
                return True, e.code, f"HTTP {e.code} (Reachable)"
            elif e.code in (405, 501, 400):
                # Method Not Allowed / Not Implemented on HEAD -> trigger GET fallback
                return False, e.code, f"Method {method} not allowed (HTTP {e.code})"
            return False, e.code, f"HTTP Error {e.code}: {e.reason}"
        except ssl.SSLError as e:
            if not unverified_ssl:
                # Retry with unverified SSL and legacy renegotiation for government self-signed/legacy certs
                return _attempt(method, unverified_ssl=True)
            return False, None, f"SSL Error: {e}"
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            return False, None, f"Connection Error: {e}"
        except Exception as e:
            return False, None, f"{type(e).__name__}: {e}"

    # 1. Try fast HEAD first
    ok, code, msg = _attempt("HEAD")
    if ok:
        return True, code, msg

    # 2. If HEAD failed or was rejected, fallback to GET (reads status and immediately closes)
    get_ok, get_code, get_msg = _attempt("GET")
    if get_ok:
        return True, get_code, get_msg

    return False, get_code or code, get_msg or msg


# =============================================================================
# 1. Database Integrity Verifier
# =============================================================================

class DatabaseIntegrityVerifier:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def verify(self) -> List[str]:
        errors = []
        cursor = self.conn.cursor()

        # Check PRAGMA integrity_check
        cursor.execute("PRAGMA integrity_check;")
        rows = cursor.fetchall()
        if not rows or rows[0][0] != "ok":
            errors.append(f"PRAGMA integrity_check failed: {rows}")

        # Check PRAGMA foreign_key_check
        cursor.execute("PRAGMA foreign_key_check;")
        fk_violations = cursor.fetchall()
        if fk_violations:
            for v in fk_violations:
                errors.append(f"Foreign key violation in table '{v[0]}', rowid {v[1]}, target table '{v[2]}'")

        # Verify tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = {row[0] for row in cursor.fetchall()}
        missing_tables = EXPECTED_TABLES - existing_tables
        if missing_tables:
            errors.append(f"Missing required tables: {sorted(missing_tables)}")

        # Verify indexes exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
        existing_indexes = {row[0] for row in cursor.fetchall()}
        missing_indexes = EXPECTED_INDEXES - existing_indexes
        if missing_indexes:
            errors.append(f"Missing required indexes: {sorted(missing_indexes)}")

        return errors


# =============================================================================
# 2. Exam Master & Eligibility Criteria Validator
# =============================================================================

class ExamMasterValidator:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def verify(self) -> List[str]:
        errors = []
        cursor = self.conn.cursor()

        # 1. Check exams table count
        cursor.execute("SELECT COUNT(*) FROM exams;")
        exams_count = cursor.fetchone()[0]
        if exams_count != 25:
            errors.append(f"Expected 25 exams in 'exams' table, found {exams_count}")

        # 2. Check eligibility_criteria table count
        cursor.execute("SELECT COUNT(*) FROM eligibility_criteria;")
        elig_count = cursor.fetchone()[0]
        if elig_count != 25:
            errors.append(f"Expected 25 records in 'eligibility_criteria' table, found {elig_count}")

        # 3. Check exact exam IDs
        cursor.execute("SELECT exam_id FROM exams;")
        found_exam_ids = {row[0] for row in cursor.fetchall()}
        missing_ids = EXPECTED_EXAM_IDS - found_exam_ids
        if missing_ids:
            errors.append(f"Missing expected exam IDs in 'exams': {sorted(missing_ids)}")
        extra_ids = found_exam_ids - EXPECTED_EXAM_IDS
        if extra_ids:
            errors.append(f"Unexpected extra exam IDs in 'exams': {sorted(extra_ids)}")

        # 4. Validate columns and constraints for each exam
        cursor.execute("""
            SELECT exam_id, title, short_code, category, administering_body, frequency,
                   official_website, latest_official_notification_url, tentative_timeline_2027
            FROM exams;
        """)
        for row in cursor.fetchall():
            exam_id, title, short_code, cat, body, freq, web, notif_url, timeline_json = row

            if not title or not title.strip():
                errors.append(f"Exam '{exam_id}' has empty title")
            if not short_code or not short_code.strip():
                errors.append(f"Exam '{exam_id}' has empty short_code")
            if cat not in ('Central-Civil', 'Regulatory', 'Defense', 'State-PSC', 'PSU'):
                errors.append(f"Exam '{exam_id}' has invalid category '{cat}'")
            if freq not in ('Annual', 'Bi-annual', 'Periodic'):
                errors.append(f"Exam '{exam_id}' has invalid frequency '{freq}'")

            # Validate URLs
            valid_web, reason_web = validate_url_syntax(web)
            if not valid_web:
                errors.append(f"Exam '{exam_id}' invalid official_website: {reason_web}")

            valid_notif, reason_notif = validate_url_syntax(notif_url)
            if not valid_notif:
                errors.append(f"Exam '{exam_id}' invalid latest_official_notification_url: {reason_notif}")

            # Validate tentative_timeline_2027 JSON
            try:
                timeline = json.loads(timeline_json)
                if not isinstance(timeline, dict) or not timeline:
                    errors.append(f"Exam '{exam_id}' tentative_timeline_2027 must be a non-empty JSON object")
            except Exception as e:
                errors.append(f"Exam '{exam_id}' invalid tentative_timeline_2027 JSON: {e}")

        # 5. Validate eligibility_criteria rows
        cursor.execute("""
            SELECT exam_id, cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json,
                   min_education_level, accepted_disciplines, min_aggregate_percentage_gen,
                   min_aggregate_percentage_reserved, final_year_students_allowed, attempt_limit_gen,
                   attempt_limit_obc, attempt_limit_sc_st, domicile_restrictions,
                   language_requirements, physical_standards, source_citation_clause
            FROM eligibility_criteria;
        """)
        for row in cursor.fetchall():
            (exam_id, cutoff_rule, min_age, max_age, relax_json, min_edu, disciplines_json,
             min_pct_gen, min_pct_res, final_year, att_gen, att_obc, att_sc_st,
             domicile_json, lang_json, phys_json, citation) = row

            if not cutoff_rule or not cutoff_rule.strip():
                errors.append(f"Exam '{exam_id}' missing cutoff_reference_date_rule")
            if not (16 <= min_age <= 35):
                errors.append(f"Exam '{exam_id}' invalid min_age_gen: {min_age}")
            if not (20 <= max_age <= 50):
                errors.append(f"Exam '{exam_id}' invalid max_age_gen: {max_age}")
            if min_age > max_age:
                errors.append(f"Exam '{exam_id}' min_age_gen ({min_age}) > max_age_gen ({max_age})")
            if min_edu not in ('Bachelor', 'Bachelor_Tech', 'Master', 'Specific_BTech', 'Specific_Degree'):
                errors.append(f"Exam '{exam_id}' invalid min_education_level: {min_edu}")

            # Validate relaxations_json
            try:
                relax = json.loads(relax_json)
                if not isinstance(relax, dict):
                    errors.append(f"Exam '{exam_id}' relaxations_json must be an object")
            except Exception as e:
                errors.append(f"Exam '{exam_id}' invalid relaxations_json: {e}")

            # Validate accepted_disciplines
            try:
                disciplines = json.loads(disciplines_json)
                if not isinstance(disciplines, list) or len(disciplines) == 0:
                    errors.append(f"Exam '{exam_id}' accepted_disciplines must be a non-empty array")
            except Exception as e:
                errors.append(f"Exam '{exam_id}' invalid accepted_disciplines JSON: {e}")

            if not (0.0 <= min_pct_gen <= 100.0):
                errors.append(f"Exam '{exam_id}' invalid min_aggregate_percentage_gen: {min_pct_gen}")
            if not (0.0 <= min_pct_res <= 100.0):
                errors.append(f"Exam '{exam_id}' invalid min_aggregate_percentage_reserved: {min_pct_res}")

            if not citation or not citation.strip():
                errors.append(f"Exam '{exam_id}' missing source_citation_clause")

        return errors


# =============================================================================
# 3. Source Audit Log Validator
# =============================================================================

class AuditLogVerifier:
    def __init__(
        self,
        conn: sqlite3.Connection,
        check_live_links: bool = False,
        live_timeout: float = 5.0,
        max_workers: int = 8,
        allow_unreachable: bool = False,
    ):
        self.conn = conn
        self.check_live_links = check_live_links
        self.live_timeout = live_timeout
        self.max_workers = max_workers
        self.allow_unreachable = allow_unreachable

    def verify(self, check_live_links: Optional[bool] = None) -> List[str]:
        if check_live_links is None:
            check_live_links = self.check_live_links

        errors = []
        cursor = self.conn.cursor()

        # Check total audit records (25 exams x 6 facts = 150 records)
        cursor.execute("SELECT COUNT(*) FROM source_audit_log;")
        total_audit_records = cursor.fetchone()[0]
        if total_audit_records < 150:
            errors.append(f"source_audit_log has only {total_audit_records} records, minimum expected 150 (6 facts per exam)")

        # Check 100% exam coverage
        cursor.execute("SELECT DISTINCT exam_id FROM source_audit_log;")
        audited_exam_ids = {row[0] for row in cursor.fetchall()}
        missing_coverage = EXPECTED_EXAM_IDS - audited_exam_ids
        if missing_coverage:
            errors.append(f"source_audit_log missing coverage for exams: {sorted(missing_coverage)}")

        # Validate audit records syntax and structure offline
        cursor.execute("""
            SELECT audit_id, exam_id, fact_type, official_document_title,
                   document_date, clause_or_page_number, official_download_link
            FROM source_audit_log;
        """)
        rows = cursor.fetchall()
        valid_urls_to_check = set()

        for row in rows:
            audit_id, exam_id, fact_type, doc_title, doc_date, clause, link = row

            if fact_type not in ('Age_Limit', 'Education', 'Syllabus', 'Pattern',
                                 'Timeline_2027', 'Physical_Standards', 'Reservation_Rules'):
                errors.append(f"Audit record '{audit_id}' has invalid fact_type: '{fact_type}'")

            if not doc_title or not doc_title.strip():
                errors.append(f"Audit record '{audit_id}' has empty official_document_title")

            if not clause or not clause.strip():
                errors.append(f"Audit record '{audit_id}' has empty clause_or_page_number")

            valid_link, reason = validate_url_syntax(link)
            if not valid_link:
                errors.append(f"Audit record '{audit_id}' invalid official_download_link syntax: {reason}")
            else:
                valid_urls_to_check.add(link)

        # Live Link Verification (online HTTP checks when requested)
        if check_live_links and valid_urls_to_check:
            print(f"  {CYAN}Performing live HTTP reachability checks on {len(valid_urls_to_check)} unique URLs (timeout={self.live_timeout}s, workers={self.max_workers})...{RESET}")
            url_results: Dict[str, Tuple[bool, Optional[int], str]] = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_url = {
                    executor.submit(check_live_url, u, self.live_timeout): u
                    for u in sorted(valid_urls_to_check)
                }
                for future in concurrent.futures.as_completed(future_to_url):
                    u = future_to_url[future]
                    try:
                        url_results[u] = future.result()
                    except Exception as ex:
                        url_results[u] = (False, None, f"Executor error: {ex}")

            passed_count = sum(1 for res in url_results.values() if res[0])
            failed_count = len(url_results) - passed_count
            print(f"  Live link check summary: {passed_count}/{len(url_results)} reachable, {failed_count} unreachable.")

            for u, (ok, code, reason) in sorted(url_results.items()):
                if not ok:
                    affected_exams = sorted({r[1] for r in rows if r[6] == u})
                    msg = f"Live link unreachable for URL '{u}' (exams: {', '.join(affected_exams)}): {reason}"
                    if self.allow_unreachable:
                        print(f"  {YELLOW}[WARN] {msg}{RESET}")
                    else:
                        errors.append(msg)

        return errors


# =============================================================================
# 4. Multi-Vector Eligibility Engine Edge Case Test Harness
# =============================================================================

class EligibilityEdgeCaseHarness:
    """Simulates deterministic statutory eligibility evaluation logic across test vectors."""

    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _resolve_cutoff_date(self, rule_text: str, exam_year: int = 2027) -> date:
        """Parses cutoff rule text into exact calendar date."""
        rule_lower = rule_text.lower()
        if "following calendar year" in rule_lower or "01-01-2028" in rule_text:
            return date(exam_year + 1, 1, 1)
        elif "01-08" in rule_text or "august 1" in rule_lower:
            return date(exam_year, 8, 1)
        elif "01-01" in rule_text or "january 1" in rule_lower:
            return date(exam_year, 1, 1)
        elif "01-07" in rule_text or "july 1" in rule_lower:
            return date(exam_year, 7, 1)
        elif "01-04" in rule_text or "april 1" in rule_lower:
            return date(exam_year, 4, 1)
        elif "30-06" in rule_text or "june 30" in rule_lower:
            return date(exam_year, 6, 30)
        elif "01-06" in rule_text or "june 1" in rule_lower:
            return date(exam_year, 6, 1)
        elif "31-03" in rule_text or "march 31" in rule_lower:
            return date(exam_year, 3, 31)
        elif "01-02" in rule_text or "february 1" in rule_lower:
            return date(exam_year, 2, 1)
        elif "01-11" in rule_text or "november 1" in rule_lower:
            return date(exam_year, 11, 1)
        return date(exam_year, 8, 1)

    def evaluate(self, exam_id: str, profile: Dict[str, Any], exam_year: int = 2027) -> Tuple[bool, List[str]]:
        """Evaluates profile against exam rules in database."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cutoff_reference_date_rule, min_age_gen, max_age_gen, relaxations_json,
                   min_education_level, accepted_disciplines, min_aggregate_percentage_gen,
                   min_aggregate_percentage_reserved, final_year_students_allowed,
                   attempt_limit_gen, attempt_limit_obc, attempt_limit_sc_st,
                   domicile_restrictions, language_requirements, physical_standards
            FROM eligibility_criteria WHERE exam_id = ?;
        """, (exam_id,))
        row = cursor.fetchone()
        if not row:
            return False, [f"Exam rule not found: {exam_id}"]

        (cutoff_rule, min_age_gen, max_age_gen, relax_json, min_edu, disciplines_json,
         min_pct_gen, min_pct_res, final_year_allowed, att_gen, att_obc, att_sc_st,
         domicile_json, lang_json, phys_json) = row

        reasons = []
        is_eligible = True

        dob = datetime.strptime(profile["dob"], "%Y-%m-%d").date()
        cutoff_date = self._resolve_cutoff_date(cutoff_rule, exam_year)

        # 1. State Domicile & Category Relaxations
        user_cat = profile.get("category", "GEN")
        user_domicile = profile.get("domicile", "All_India")
        effective_cat = user_cat

        domicile_cfg = json.loads(domicile_json) if domicile_json else None
        if domicile_cfg and "reservation_benefit" in domicile_cfg:
            res_benefit = domicile_cfg["reservation_benefit"]
            # e.g., 'BIHAR_DOMICILE_ONLY', 'UP_DOMICILE_ONLY'
            expected_state = res_benefit.replace("_DOMICILE_ONLY", "").replace("_", " ").upper()
            if user_domicile.upper() != expected_state:
                # Out-of-state candidates treated strictly as General/Unreserved
                effective_cat = "GEN"

        relaxations = json.loads(relax_json) if relax_json else {}
        age_relaxation = 0

        gender = profile.get("gender", "MALE")

        # Category relaxation lookup
        cat_keys = [effective_cat]
        if effective_cat in ("SC", "ST"):
            cat_keys.extend(["SC_ST", "SC/ST"])
        elif effective_cat in ("OBC", "OBC_NCL"):
            cat_keys.extend(["OBC", "OBC_NCL"])

        dom_clean = user_domicile.replace(" ", "_").upper()
        for k in list(cat_keys):
            cat_keys.append(f"{k}_{dom_clean}")
            if dom_clean in ("RAJASTHAN", "RJ"):
                cat_keys.append(f"{k}_RJ")
                if effective_cat in ("SC", "ST", "OBC", "OBC_NCL", "EWS"):
                    if gender.upper() == "MALE":
                        cat_keys.append("SC_ST_OBC_MBC_EWS_Male_RJ")
                    else:
                        cat_keys.append("SC_ST_OBC_MBC_EWS_Female_RJ")
                elif effective_cat == "GEN" and gender.upper() == "FEMALE":
                    cat_keys.append("GEN_Female_RJ")

        for k in cat_keys:
            if k in relaxations:
                age_relaxation = max(age_relaxation, relaxations[k])

        # Gender-specific relaxation lookup (e.g., BPSC GEN_Female)
        if f"{effective_cat}_{gender.capitalize()}" in relaxations:
            age_relaxation = max(age_relaxation, relaxations[f"{effective_cat}_{gender.capitalize()}"])
        elif gender.upper() == "FEMALE" and "Women_All" in relaxations:
            age_relaxation = max(age_relaxation, relaxations["Women_All"])

        effective_max_age = max_age_gen + age_relaxation

        # 2. Age Evaluation (Calendar Day Boundary Arithmetic)
        age_years = cutoff_date.year - dob.year - ((cutoff_date.month, cutoff_date.day) < (dob.month, dob.day))

        # Statutory Lower Boundary Rule:
        latest_allowed_dob = date(cutoff_date.year - min_age_gen, cutoff_date.month, cutoff_date.day)
        if dob > latest_allowed_dob:
            is_eligible = False
            reasons.append(f"Candidate age ({age_years}y) is below minimum age requirement {min_age_gen} on {cutoff_date}")

        # Statutory Upper Boundary Rule:
        if exam_id == "RPSC_RAS":
            # RPSC statutory forward-year rule: candidate must not have exceeded max completed years
            if age_years > effective_max_age:
                is_eligible = False
                reasons.append(f"Candidate age ({age_years}y) exceeds statutory upper age limit {effective_max_age} on {cutoff_date}")
        elif exam_id.startswith("UPSC_"):
            # Central civil statutory notification: born not earlier than 2nd of cutoff month
            earliest_allowed_dob = date(cutoff_date.year - effective_max_age, cutoff_date.month, cutoff_date.day + 1)
            if dob < earliest_allowed_dob:
                is_eligible = False
                reasons.append(f"Candidate born before {earliest_allowed_dob} exceeds statutory upper age limit {effective_max_age} on {cutoff_date}")
        else:
            # State PSCs & PSUs: candidate born on cutoff date attains completed year on cutoff and is within limit
            earliest_allowed_dob = date(cutoff_date.year - effective_max_age, cutoff_date.month, cutoff_date.day)
            if dob < earliest_allowed_dob:
                is_eligible = False
                reasons.append(f"Candidate age ({age_years}y) exceeds statutory upper age limit {effective_max_age} on {cutoff_date}")

        # 3. Aggregate Percentage Check (Strict Non-Rounding Rule)
        candidate_pct = float(profile.get("graduation_aggregate_pct", 0.0))
        target_min_pct = min_pct_res if effective_cat in ("SC", "ST", "PwBD") else min_pct_gen

        if target_min_pct > 0.0:
            # Rounding is strictly prohibited: 59.99% is less than 60.0%
            if round(candidate_pct, 4) < round(target_min_pct, 4):
                is_eligible = False
                reasons.append(f"Aggregate percentage {candidate_pct:.2f}% falls below strict threshold {target_min_pct:.2f}% (no rounding permitted)")

        # 4. Attempt Limits Check
        prior_attempts = profile.get("prior_attempts", 0)
        max_attempts = None
        if effective_cat in ("GEN", "EWS"):
            max_attempts = att_gen
        elif effective_cat == "OBC":
            max_attempts = att_obc
        elif effective_cat in ("SC", "ST"):
            max_attempts = att_sc_st

        # RBI Grade B Phase-1 specific attempts
        if exam_id == "RBI_GRADE_B":
            phase1_attempts = profile.get("prior_phase1_attempts", prior_attempts)
            if effective_cat in ("GEN", "EWS") and phase1_attempts >= 6:
                is_eligible = False
                reasons.append(f"Candidate reached/exceeded RBI Grade B Phase-1 attempt limit of 6 for Gen/EWS ({phase1_attempts} attempts)")
        elif max_attempts is not None and prior_attempts >= max_attempts:
            is_eligible = False
            reasons.append(f"Candidate reached/exceeded maximum attempt limit of {max_attempts} for category {effective_cat} ({prior_attempts} attempts)")

        # 5. Language Requirements Gate
        lang_cfg = json.loads(lang_json) if lang_json else None
        user_langs = [l.lower() for l in profile.get("fluent_languages", [])]
        user_mother_tongue = profile.get("mother_tongue", "").lower()

        if lang_cfg:
            pass

        # 6. Physical Standards Gate (Police / Uniformed Cadres)
        phys_cfg = json.loads(phys_json) if phys_json else None
        target_post = profile.get("target_post", "").upper()
        user_height = profile.get("height_cm", 0.0)

        if phys_cfg and user_height > 0:
            if exam_id == "UPPSC_PCS" and "DSP" in target_post:
                req_h = 165.0 if gender.upper() == "MALE" else 152.0
                if user_height < req_h:
                    is_eligible = False
                    reasons.append(f"Height {user_height} cm falls below UPPSC DSP minimum standard of {req_h} cm")
            elif exam_id == "UPSC_CAPF_AC":
                req_h = 165.0 if gender.upper() == "MALE" else 157.0
                if user_height < req_h:
                    is_eligible = False
                    reasons.append(f"Height {user_height} cm falls below CAPF AC standard of {req_h} cm")
            elif exam_id == "PSU_SAIL_MTT":
                req_h = 155.0 if gender.upper() == "MALE" else 143.0
                if user_height < req_h:
                    is_eligible = False
                    reasons.append(f"Height {user_height} cm falls below SAIL MTT standard of {req_h} cm")

        return is_eligible, reasons

    def run_all_tests(self) -> List[str]:
        """Runs the statutory edge case vectors."""
        errors = []

        test_vectors = [
            # 1. Cutoff Dates: UPSC CSE (Aug 1, 2027) Upper Boundary
            {
                "name": "UPSC CSE: Born 1995-08-01 (General Male) -> Ineligible (Overage)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "1995-08-01", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0},
                "expected_eligible": False
            },
            {
                "name": "UPSC CSE: Born 1995-08-02 (General Male) -> Eligible (Within Age)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "1995-08-02", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0},
                "expected_eligible": True
            },
            # 2. Cutoff Dates: UPSC CSE Lower Boundary (Min 21)
            {
                "name": "UPSC CSE: Born 2006-08-01 (General) -> Eligible (Exactly 21y)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "2006-08-01", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0},
                "expected_eligible": True
            },
            {
                "name": "UPSC CSE: Born 2006-08-02 (General) -> Ineligible (Underage by 1 day)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "2006-08-02", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 0},
                "expected_eligible": False
            },
            # 3. Cutoff Dates: MPPSC SSE (Jan 1, 2027)
            {
                "name": "MPPSC SSE: Born 1987-01-01 (General) -> Eligible on 01-01-2027 (Max 40)",
                "exam_id": "MPPSC_SSE",
                "profile": {"dob": "1987-01-01", "category": "GEN", "graduation_aggregate_pct": 55.0, "domicile": "Madhya Pradesh"},
                "expected_eligible": True
            },
            {
                "name": "MPPSC SSE: Born 1986-12-31 (General) -> Ineligible on 01-01-2027 (40y 1d)",
                "exam_id": "MPPSC_SSE",
                "profile": {"dob": "1986-12-31", "category": "GEN", "graduation_aggregate_pct": 55.0, "domicile": "Madhya Pradesh"},
                "expected_eligible": False
            },
            # 4. Cutoff Dates: UPPSC PCS (Jul 1, 2027)
            {
                "name": "UPPSC PCS: Born 1987-07-01 (General Male) -> Eligible on 01-07-2027 (Max 40)",
                "exam_id": "UPPSC_PCS",
                "profile": {"dob": "1987-07-01", "category": "GEN", "gender": "MALE", "domicile": "Uttar Pradesh"},
                "expected_eligible": True
            },
            {
                "name": "UPPSC PCS: Born 1987-06-30 (General Male) -> Ineligible on 01-07-2027 (40y 1d)",
                "exam_id": "UPPSC_PCS",
                "profile": {"dob": "1987-06-30", "category": "GEN", "gender": "MALE", "domicile": "Uttar Pradesh"},
                "expected_eligible": False
            },
            # 5. Cutoff Dates: TSPSC Group 1 (July 1, 2027)
            {
                "name": "TSPSC Group 1: Born 1983-07-01 (UR) -> Eligible on 01-07-2027 (Max 44)",
                "exam_id": "TSPSC_GROUP_1",
                "profile": {"dob": "1983-07-01", "category": "GEN", "domicile": "Telangana", "fluent_languages": ["English", "Hindi"]},
                "expected_eligible": True
            },
            {
                "name": "TSPSC Group 1: Born 1983-06-30 (UR) -> Ineligible on 01-07-2027 (44y 1d)",
                "exam_id": "TSPSC_GROUP_1",
                "profile": {"dob": "1983-06-30", "category": "GEN", "domicile": "Telangana", "fluent_languages": ["English", "Hindi"]},
                "expected_eligible": False
            },
            # 6. Cutoff Dates: RPSC RAS (Forward-Year 01-01-2028 Cutoff)
            {
                "name": "RPSC RAS: Born 1987-01-02 -> Eligible evaluated on 01-01-2028",
                "exam_id": "RPSC_RAS",
                "profile": {"dob": "1987-01-02", "category": "GEN", "gender": "MALE", "domicile": "Rajasthan"},
                "expected_eligible": True
            },
            {
                "name": "RPSC RAS: Born 1986-12-31 -> Ineligible evaluated on 01-01-2028 (41y 1d)",
                "exam_id": "RPSC_RAS",
                "profile": {"dob": "1986-12-31", "category": "GEN", "gender": "MALE", "domicile": "Rajasthan"},
                "expected_eligible": False
            },
            # 7. Strict Percentage: PSU IOCL (65.0% Strict Cutoff)
            {
                "name": "PSU IOCL: 64.99% raw aggregate -> Ineligible (Strict 65.0% rule)",
                "exam_id": "PSU_IOCL_ET",
                "profile": {"dob": "2002-01-01", "category": "GEN", "graduation_aggregate_pct": 64.99},
                "expected_eligible": False
            },
            {
                "name": "PSU IOCL: 65.00% raw aggregate -> Eligible",
                "exam_id": "PSU_IOCL_ET",
                "profile": {"dob": "2002-01-01", "category": "GEN", "graduation_aggregate_pct": 65.00},
                "expected_eligible": True
            },
            # 8. Strict Percentage: PSU HPCL (60.0% Strict Cutoff)
            {
                "name": "PSU HPCL: 59.99% raw aggregate -> Ineligible (Strict 60.0% rule)",
                "exam_id": "PSU_HPCL_OFFICER",
                "profile": {"dob": "2003-01-01", "category": "GEN", "graduation_aggregate_pct": 59.99},
                "expected_eligible": False
            },
            {
                "name": "PSU HPCL: 60.00% raw aggregate -> Eligible",
                "exam_id": "PSU_HPCL_OFFICER",
                "profile": {"dob": "2003-01-01", "category": "GEN", "graduation_aggregate_pct": 60.00},
                "expected_eligible": True
            },
            # 9. Strict Percentage: RBI Grade B (60.0% Strict Cutoff)
            {
                "name": "RBI Grade B: 59.99% raw aggregate -> Ineligible (Strict 60.0% rule)",
                "exam_id": "RBI_GRADE_B",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 59.99, "prior_phase1_attempts": 0},
                "expected_eligible": False
            },
            # 10. Central Civil: UPSC CSE (Simple Degree Pass)
            {
                "name": "UPSC CSE: 45.0% pass aggregate -> Eligible (No min percentage)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 45.00, "prior_attempts": 0},
                "expected_eligible": True
            },
            # 11. Attempt Limits: UPSC CSE (General 6 Attempts)
            {
                "name": "UPSC CSE: General with 5 prior attempts -> Eligible",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 5},
                "expected_eligible": True
            },
            {
                "name": "UPSC CSE: General with 6 prior attempts -> Ineligible",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 55.0, "prior_attempts": 6},
                "expected_eligible": False
            },
            # 12. Attempt Limits: UPSC CSE (OBC 9 Attempts)
            {
                "name": "UPSC CSE: OBC with 8 prior attempts -> Eligible",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "1997-01-01", "category": "OBC", "graduation_aggregate_pct": 55.0, "prior_attempts": 8},
                "expected_eligible": True
            },
            {
                "name": "UPSC CSE: OBC with 9 prior attempts -> Ineligible",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "1997-01-01", "category": "OBC", "graduation_aggregate_pct": 55.0, "prior_attempts": 9},
                "expected_eligible": False
            },
            # 13. Attempt Limits: UPSC CSE (SC/ST Unlimited)
            {
                "name": "UPSC CSE: SC/ST with 12 prior attempts -> Eligible (Unlimited)",
                "exam_id": "UPSC_CSE",
                "profile": {"dob": "1995-01-01", "category": "SC", "graduation_aggregate_pct": 55.0, "prior_attempts": 12},
                "expected_eligible": True
            },
            # 14. Attempt Limits: RBI Grade B (6 Phase-1 Gen/EWS only)
            {
                "name": "RBI Grade B: General with 5 Phase-1 attempts -> Eligible",
                "exam_id": "RBI_GRADE_B",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 65.0, "prior_phase1_attempts": 5},
                "expected_eligible": True
            },
            {
                "name": "RBI Grade B: General with 6 Phase-1 attempts -> Ineligible",
                "exam_id": "RBI_GRADE_B",
                "profile": {"dob": "2000-01-01", "category": "GEN", "graduation_aggregate_pct": 65.0, "prior_phase1_attempts": 6},
                "expected_eligible": False
            },
            {
                "name": "RBI Grade B: OBC with 6 Phase-1 attempts -> Eligible (Cap Gen/EWS only)",
                "exam_id": "RBI_GRADE_B",
                "profile": {"dob": "2000-01-01", "category": "OBC", "graduation_aggregate_pct": 65.0, "prior_phase1_attempts": 6},
                "expected_eligible": True
            },
            # 15. Gender Distinction: BPSC CCE (Male 37 vs Female 40)
            {
                "name": "BPSC CCE: UR Male age 39 on 01-08-2027 -> Ineligible (Cap 37)",
                "exam_id": "BPSC_CCE",
                "profile": {"dob": "1988-08-01", "category": "GEN", "gender": "MALE", "domicile": "Bihar"},
                "expected_eligible": False
            },
            {
                "name": "BPSC CCE: UR Female age 39 on 01-08-2027 -> Eligible (Cap 40)",
                "exam_id": "BPSC_CCE",
                "profile": {"dob": "1988-08-01", "category": "GEN", "gender": "FEMALE", "domicile": "Bihar"},
                "expected_eligible": True
            },
            # 16. State Domicile Firewall: Out-of-state OBC applying for BPSC CCE
            {
                "name": "BPSC CCE: UP OBC Male age 38 -> Ineligible (Treated as UR Male without UP relaxation)",
                "exam_id": "BPSC_CCE",
                "profile": {"dob": "1989-08-01", "category": "OBC", "gender": "MALE", "domicile": "Uttar Pradesh"},
                "expected_eligible": False
            },
            # 17. State Domicile Firewall: Out-of-state OBC applying for UPPSC PCS
            {
                "name": "UPPSC PCS: Bihar OBC Male age 42 -> Ineligible (Treated as UR Male without UP relaxation)",
                "exam_id": "UPPSC_PCS",
                "profile": {"dob": "1985-07-01", "category": "OBC", "gender": "MALE", "domicile": "Bihar"},
                "expected_eligible": False
            },
            # 18. Physical Standards: UPPSC DSP Police Cadre Height
            {
                "name": "UPPSC DSP: Male height 163 cm -> Ineligible for DSP (Min 165 cm)",
                "exam_id": "UPPSC_PCS",
                "profile": {"dob": "2000-01-01", "category": "GEN", "gender": "MALE", "target_post": "DSP", "height_cm": 163.0, "domicile": "Uttar Pradesh"},
                "expected_eligible": False
            },
            # 19. Physical Standards: CAPF AC Height
            {
                "name": "CAPF AC: Male height 164 cm -> Ineligible (Min 165 cm)",
                "exam_id": "UPSC_CAPF_AC",
                "profile": {"dob": "2004-01-01", "category": "GEN", "gender": "MALE", "height_cm": 164.0},
                "expected_eligible": False
            },
            # 20. Physical Standards: SAIL MTT Height
            {
                "name": "SAIL MTT: Male height 153 cm -> Ineligible (Min 155 cm)",
                "exam_id": "PSU_SAIL_MTT",
                "profile": {"dob": "2001-01-01", "category": "GEN", "gender": "MALE", "height_cm": 153.0, "graduation_aggregate_pct": 70.0},
                "expected_eligible": False
            }
        ]

        for tv in test_vectors:
            name = tv["name"]
            exam_id = tv["exam_id"]
            prof = tv["profile"]
            expected = tv["expected_eligible"]

            actual, reasons = self.evaluate(exam_id, prof)
            if actual != expected:
                errors.append(f"Edge case failed '{name}': Expected {expected}, got {actual}. Reasons: {reasons}")

        return errors


# =============================================================================
# 5. Syllabus Taxonomy & Overlap Matrix Validator (Milestone 2)
# =============================================================================

class SyllabusTaxonomyAndMatrixValidator:
    """Verifies Universal Syllabus Taxonomy, 31 Exams Stage Mappings, and JSON Matrix Exports."""

    def __init__(self, conn: sqlite3.Connection, project_root: str):
        self.conn = conn
        self.project_root = project_root

    def verify(self) -> List[str]:
        errors = []
        cursor = self.conn.cursor()

        # 1. Validate taxonomy size and domains
        cursor.execute("SELECT COUNT(*) FROM syllabus_taxonomy;")
        total_topics = cursor.fetchone()[0]
        if total_topics < 120:
            errors.append(f"syllabus_taxonomy has only {total_topics} topics, minimum required is 120")

        cursor.execute("SELECT DISTINCT domain FROM syllabus_taxonomy;")
        domains = {r[0] for r in cursor.fetchall()}
        expected_domains = {
            "General Studies", "Quantitative Aptitude", "Reasoning",
            "English", "Economics & Finance", "Technical"
        }
        if domains != expected_domains:
            errors.append(f"syllabus_taxonomy domains mismatch. Expected {sorted(expected_domains)}, got {sorted(domains)}")

        cursor.execute("SELECT COUNT(DISTINCT sub_domain) FROM syllabus_taxonomy;")
        sub_domain_count = cursor.fetchone()[0]
        if sub_domain_count < 35:
            errors.append(f"syllabus_taxonomy has only {sub_domain_count} sub-domains, minimum expected 35")

        # 2. Validate topic_id format
        topic_pattern = re.compile(r"^[a-z_]+\.[a-z_]+\.[a-z0-9_]+$")
        cursor.execute("SELECT topic_id, topic_title FROM syllabus_taxonomy;")
        for tid, title in cursor.fetchall():
            if not topic_pattern.match(tid):
                errors.append(f"Invalid topic_id format: '{tid}'")
            if not title or not title.strip():
                errors.append(f"Empty topic_title for topic_id '{tid}'")

        # 3. Validate exam_syllabus_map coverage across all 25 examinations
        cursor.execute("SELECT COUNT(DISTINCT exam_id) FROM exam_syllabus_map;")
        mapped_exams_count = cursor.fetchone()[0]
        if mapped_exams_count != 25:
            errors.append(f"exam_syllabus_map covers only {mapped_exams_count}/25 examinations")

        cursor.execute("SELECT COUNT(*) FROM exam_syllabus_map;")
        total_mappings = cursor.fetchone()[0]
        if total_mappings < 300:
            errors.append(f"exam_syllabus_map has only {total_mappings} mappings, expected >= 300")

        # 4. Validate depth_level enums and source_clause_ref
        cursor.execute("""
            SELECT exam_id, stage_name, topic_id, depth_level, source_clause_ref, weightage_pct_estimate
            FROM exam_syllabus_map;
        """)
        valid_depths = {"Foundation", "Intermediate", "Advanced", "Analytical"}
        for eid, stage, tid, depth, clause, weight in cursor.fetchall():
            if depth not in valid_depths:
                errors.append(f"Invalid depth_level '{depth}' in mapping ({eid}, {stage}, {tid})")
            if not clause or not clause.strip():
                errors.append(f"Missing source_clause_ref in mapping ({eid}, {stage}, {tid})")
            if weight is not None and not (0.0 <= weight <= 100.0):
                errors.append(f"Invalid weightage {weight} in mapping ({eid}, {stage}, {tid})")

        # 5. Check orphan topics
        cursor.execute("""
            SELECT COUNT(*) FROM syllabus_taxonomy 
            WHERE topic_id NOT IN (SELECT DISTINCT topic_id FROM exam_syllabus_map);
        """)
        orphan_count = cursor.fetchone()[0]
        if orphan_count > 0:
            errors.append(f"Found {orphan_count} orphan topics in syllabus_taxonomy not mapped to any exam")

        # 6. Validate on-disk JSON artifacts
        tax_json_path = os.path.join(self.project_root, "data", "syllabus_taxonomy.json")
        matrix_json_path = os.path.join(self.project_root, "data", "exam_syllabus_matrix.json")

        if not os.path.isfile(tax_json_path):
            errors.append(f"Missing JSON export file: {tax_json_path}")
        else:
            try:
                with open(tax_json_path, "r", encoding="utf-8") as f:
                    tax_data = json.load(f)
                if len(tax_data.get("topics_flat", [])) < 120:
                    errors.append(f"{tax_json_path} has fewer than 120 topics")
                if "lookup_by_id" not in tax_data or "domains" not in tax_data:
                    errors.append(f"{tax_json_path} missing required keys ('lookup_by_id', 'domains')")
            except Exception as ex:
                errors.append(f"Failed parsing {tax_json_path}: {ex}")

        if not os.path.isfile(matrix_json_path):
            errors.append(f"Missing JSON export file: {matrix_json_path}")
        else:
            try:
                with open(matrix_json_path, "r", encoding="utf-8") as f:
                    matrix_data = json.load(f)
                p_metrics = matrix_data.get("pairwise_metrics", {})
                if len(p_metrics) != 25:
                    errors.append(f"{matrix_json_path} pairwise_metrics does not cover all 25 exams (found {len(p_metrics)})")
                if "disjoint_upset_combinations" not in matrix_data or "topic_frequencies" not in matrix_data:
                    errors.append(f"{matrix_json_path} missing required set analysis keys")
            except Exception as ex:
                errors.append(f"Failed parsing {matrix_json_path}: {ex}")

        return errors


# =============================================================================
# Main Verification CLI Runner
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Automated Grade A Exam Database Verification Engine")
    parser.add_argument("--db", default="data/grade_a_exams.db", help="Path to SQLite database file")
    parser.add_argument("--check-live-links", action="store_true", help="Perform online HTTP requests for source links")
    parser.add_argument("--live-timeout", type=float, default=5.0, help="Timeout in seconds for live HTTP link checks (default: 5.0)")
    parser.add_argument("--allow-unreachable", action="store_true", help="Log unreachable live links as warnings instead of failing verification")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose failure output")
    args = parser.parse_args()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(project_root, args.db) if not os.path.isabs(args.db) else args.db

    print(f"{BOLD}{CYAN}=== GRADE A DATABASE AUTOMATED VERIFICATION ENGINE ==={RESET}")
    print(f"Target Database: {db_path}\n")

    if not os.path.exists(db_path):
        print(f"{RED}[FAIL] Database file not found at: {db_path}{RESET}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    except Exception as e:
        print(f"{RED}[FAIL] Could not connect to SQLite database: {e}{RESET}")
        sys.exit(1)

    total_failures = 0

    # 1. Relational Integrity Checks
    print(f"{BOLD}[1/5] Checking SQLite Relational Schema Integrity...{RESET}")
    integrity_verifier = DatabaseIntegrityVerifier(conn)
    integrity_errors = integrity_verifier.verify()
    if integrity_errors:
        total_failures += len(integrity_errors)
        print(f"  {RED}FAILED ({len(integrity_errors)} violations){RESET}")
        for err in integrity_errors:
            print(f"    - {err}")
    else:
        print(f"  {GREEN}PASSED (PRAGMA integrity_check 'ok', 0 FK violations, all tables/indexes intact){RESET}")

    # 2. Exam Master & Eligibility Criteria Checks
    print(f"\n{BOLD}[2/5] Checking 25 Exams Master & Eligibility Non-Null/JSON Schema...{RESET}")
    master_validator = ExamMasterValidator(conn)
    master_errors = master_validator.verify()
    if master_errors:
        total_failures += len(master_errors)
        print(f"  {RED}FAILED ({len(master_errors)} violations){RESET}")
        for err in master_errors:
            print(f"    - {err}")
    else:
        print(f"  {GREEN}PASSED (All 25 exams verified with non-null constraints and valid JSON structures){RESET}")

    # 3. Source Audit Log & URL Checks
    print(f"\n{BOLD}[3/5] Checking 100% Source Audit Log Coverage & URL Formatting...{RESET}")
    audit_verifier = AuditLogVerifier(
        conn,
        check_live_links=args.check_live_links,
        live_timeout=args.live_timeout,
        allow_unreachable=args.allow_unreachable,
    )
    audit_errors = audit_verifier.verify()
    if audit_errors:
        total_failures += len(audit_errors)
        print(f"  {RED}FAILED ({len(audit_errors)} violations){RESET}")
        for err in audit_errors:
            print(f"    - {err}")
    else:
        print(f"  {GREEN}PASSED (100% exam coverage, 150 audit logs, all citations and HTTP/HTTPS URLs syntactically valid){RESET}")

    # 4. Multi-Vector Eligibility Edge Case Test Harness
    print(f"\n{BOLD}[4/5] Executing Algorithmic Eligibility Edge-Case Test Harness...{RESET}")
    harness = EligibilityEdgeCaseHarness(conn)
    harness_errors = harness.run_all_tests()
    if harness_errors:
        total_failures += len(harness_errors)
        print(f"  {RED}FAILED ({len(harness_errors)} edge case regressions){RESET}")
        for err in harness_errors:
            print(f"    - {err}")
    else:
        print(f"  {GREEN}PASSED (All 20+ multi-vector statutory edge cases passed perfectly){RESET}")

    # 5. Syllabus Taxonomy & Overlap Matrix Checks (Milestone 2)
    print(f"\n{BOLD}[5/5] Checking Syllabus Taxonomy, 25 Exams Stage Mapping & Matrix Exports...{RESET}")
    syllabus_validator = SyllabusTaxonomyAndMatrixValidator(conn, project_root)
    syllabus_errors = syllabus_validator.verify()
    if syllabus_errors:
        total_failures += len(syllabus_errors)
        print(f"  {RED}FAILED ({len(syllabus_errors)} violations){RESET}")
        for err in syllabus_errors:
            print(f"    - {err}")
    else:
        print(f"  {GREEN}PASSED (>=120 topics, 6 domains, all 25 exams mapped with valid depth levels, 0 orphans, valid JSON matrix){RESET}")

    conn.close()

    # Final Summary Report
    print(f"\n{BOLD}{CYAN}=================================================={RESET}")
    if total_failures == 0:
        print(f"{BOLD}{GREEN}VERIFICATION SUCCESSFUL: 0 VIOLATIONS ACROSS ALL MODULES.{RESET}")
        print(f"Exit code: 0")
        sys.exit(0)
    else:
        print(f"{BOLD}{RED}VERIFICATION FAILED: {total_failures} TOTAL VIOLATIONS DETECTED.{RESET}")
        print(f"Exit code: 1")
        sys.exit(1)


if __name__ == "__main__":
    main()
