#!/usr/bin/env python3
"""
E2E Test Runner for Indian Grade A Government Examinations Platform.
Discovers and executes all 5 test tiers, logs individual test results,
and returns exit code 0 when all tests pass, or exit code 1 if any fail.
"""

import argparse
import datetime
import importlib
import json
import os
import sys
import time
import unittest
from typing import Any, Dict, List, Optional, Tuple

# Ensure project root is in sys.path for direct script execution
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ANSI Terminal Color Constants
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

TIER_MODULES = {
    1: {
        "name": "Tier 1: Isolated Feature Coverage",
        "module": "tests.e2e.tier1_feature_coverage",
        "description": "Happy-path functional verification across all 25 platform features."
    },
    2: {
        "name": "Tier 2: Boundary, Corner Case & Negative Testing",
        "module": "tests.e2e.tier2_boundary_corner",
        "description": "Statutory cutoff boundaries, non-rounding percentages, attempt limits, and physical standard gates."
    },
    3: {
        "name": "Tier 3: Pairwise Combinatorial Interactions",
        "module": "tests.e2e.tier3_pairwise_combinations",
        "description": "Combinatorial matrix tests across social categories, academic disciplines, and service types."
    },
    4: {
        "name": "Tier 4: Real-World Application Scenarios",
        "module": "tests.e2e.tier4_real_world_scenarios",
        "description": "High-complexity end-to-end workload simulations reflecting realistic candidate user journeys."
    },
    5: {
        "name": "Tier 5: Adversarial Hardening & Acceptance",
        "module": "tests.e2e.tier5_adversarial_hardening",
        "description": "White-box security hardening, SQLi resistance, precision tolerances, and D3 physics stability."
    }
}


class DetailedResultCollector(unittest.TestResult):
    """Custom test result collector capturing individual test outcomes, timings, and failures."""

    def __init__(self, verbose: bool = False):
        super().__init__()
        self.verbose = verbose
        self.records: List[Dict[str, Any]] = []
        self._test_start_time: float = 0.0

    def startTest(self, test: unittest.TestCase):
        super().startTest(test)
        self._test_start_time = time.time()

    def addSuccess(self, test: unittest.TestCase):
        super().addSuccess(test)
        duration = time.time() - self._test_start_time
        test_id = test.id()
        self.records.append({
            "test_id": test_id,
            "status": "PASS",
            "duration": duration,
            "error": None
        })
        if self.verbose:
            print(f"  {GREEN}✓ PASS{RESET} {test_id} ({duration:.4f}s)")

    def addFailure(self, test: unittest.TestCase, err):
        super().addFailure(test, err)
        duration = time.time() - self._test_start_time
        test_id = test.id()
        msg = self._exc_info_to_string(err, test)
        self.records.append({
            "test_id": test_id,
            "status": "FAIL",
            "duration": duration,
            "error": msg
        })
        print(f"  {RED}✗ FAIL{RESET} {test_id} ({duration:.4f}s)")

    def addError(self, test: unittest.TestCase, err):
        super().addError(test, err)
        duration = time.time() - self._test_start_time
        test_id = test.id()
        msg = self._exc_info_to_string(err, test)
        self.records.append({
            "test_id": test_id,
            "status": "ERROR",
            "duration": duration,
            "error": msg
        })
        print(f"  {RED}⚠ ERROR{RESET} {test_id} ({duration:.4f}s)")

    def addSkip(self, test: unittest.TestCase, reason: str):
        super().addSkip(test, reason)
        duration = time.time() - self._test_start_time
        test_id = test.id()
        self.records.append({
            "test_id": test_id,
            "status": "SKIP",
            "duration": duration,
            "error": reason
        })
        if self.verbose:
            print(f"  {YELLOW}○ SKIP{RESET} {test_id} (Reason: {reason})")


def run_tier(tier_num: int, tier_info: Dict[str, Any], verbose: bool = False, feature_filter: Optional[str] = None) -> Tuple[unittest.TestSuite, DetailedResultCollector, float]:
    """Loads and executes a single test tier module."""
    module_name = tier_info["module"]
    module = importlib.import_module(module_name)
    loader = unittest.TestLoader()

    if feature_filter:
        pattern = f"*f{int(feature_filter):02d}*" if feature_filter.isdigit() else f"*{feature_filter}*"
        suite = loader.loadTestsFromName(module_name)
        # Filter suite by feature pattern
        filtered_tests = []
        for test_case in suite:
            if isinstance(test_case, unittest.TestSuite):
                for t in test_case:
                    if feature_filter.lower() in t.id().lower():
                        filtered_tests.append(t)
            elif feature_filter.lower() in test_case.id().lower():
                filtered_tests.append(test_case)
        suite = unittest.TestSuite(filtered_tests)
    else:
        suite = loader.loadTestsFromModule(module)

    collector = DetailedResultCollector(verbose=verbose)
    start_time = time.time()
    suite.run(collector)
    elapsed = time.time() - start_time

    return suite, collector, elapsed


def print_banner():
    banner = f"""
{CYAN}========================================================================================
   INDIAN GRADE A GOVERNMENT EXAMINATIONS INTELLIGENCE PLATFORM
   Comprehensive Opaque-Box E2E Test Suite Harness (Tiers 1 - 5)
========================================================================================{RESET}
"""
    print(banner)


def main() -> int:
    parser = argparse.ArgumentParser(description="Grade A Examinations Platform E2E Test Runner")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "5", "all"], default="all", help="Target test tier to execute (default: all)")
    parser.add_argument("--feature", type=str, default=None, help="Filter tests by feature key (e.g. f01, f15, upset)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose per-test execution logging")
    parser.add_argument("--json", type=str, default=None, help="Optional output path to export test results in JSON format")

    args = parser.parse_args()

    print_banner()

    target_tiers = [1, 2, 3, 4, 5] if args.tier == "all" else [int(args.tier)]
    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_skipped = 0
    overall_start_time = time.time()

    tier_summaries: List[Dict[str, Any]] = []
    all_records: List[Dict[str, Any]] = []

    for t_num in target_tiers:
        t_info = TIER_MODULES[t_num]
        print(f"\n{BOLD}{BLUE}[EXECUTING TIER {t_num}]{RESET} {BOLD}{t_info['name']}{RESET}")
        print(f"  {WHITE}{t_info['description']}{RESET}\n")

        suite, collector, elapsed = run_tier(t_num, t_info, verbose=args.verbose, feature_filter=args.feature)

        passed = len(collector.records) - len(collector.failures) - len(collector.errors) - len(collector.skipped)
        failed = len(collector.failures)
        errors = len(collector.errors)
        skipped = len(collector.skipped)
        total = len(collector.records)

        total_passed += passed
        total_failed += failed
        total_errors += errors
        total_skipped += skipped
        all_records.extend(collector.records)

        tier_summaries.append({
            "tier": t_num,
            "name": t_info["name"],
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "duration": elapsed
        })

        color = GREEN if (failed == 0 and errors == 0) else RED
        print(f"\n  {BOLD}Tier {t_num} Outcome:{RESET} {color}{passed}/{total} Passed{RESET} ({elapsed:.3f}s)")
        if failed > 0 or errors > 0:
            print(f"  {RED}Failures: {failed}, Errors: {errors}{RESET}")

    overall_elapsed = time.time() - overall_start_time
    total_tests = total_passed + total_failed + total_errors + total_skipped

    # Summary Report Table
    print(f"\n{CYAN}{'='*88}{RESET}")
    print(f"{BOLD}TIER-BY-TIER COVERAGE SUMMARY{RESET}")
    print(f"{CYAN}{'='*88}{RESET}")
    print(f"{'Tier':<8} {'Name':<42} {'Total':<8} {'Passed':<8} {'Failed':<8} {'Time (s)':<10}")
    print(f"{'-'*88}")
    for ts in tier_summaries:
        status_col = GREEN if ts["failed"] == 0 and ts["errors"] == 0 else RED
        print(f"Tier {ts['tier']:<3} {ts['name']:<42} {ts['total']:<8} {status_col}{ts['passed']:<8}{RESET} {ts['failed'] + ts['errors']:<8} {ts['duration']:<10.3f}")
    print(f"{'-'*88}")
    pass_pct = (total_passed / total_tests * 100) if total_tests > 0 else 0.0
    print(f"{BOLD}{'TOTAL':<51} {total_tests:<8} {GREEN if total_failed == 0 and total_errors == 0 else RED}{total_passed:<8}{RESET} {total_failed + total_errors:<8} {overall_elapsed:<10.3f}{RESET}")
    print(f"{CYAN}{'='*88}{RESET}")

    if total_failed == 0 and total_errors == 0 and total_tests > 0:
        print(f"\n{BOLD}{GREEN}🎉 ALL {total_tests} E2E TESTS PASSED SUCCESSFULLY! (Pass Rate: {pass_pct:.1f}%){RESET}\n")
    else:
        print(f"\n{BOLD}{RED}❌ E2E TEST SUITE RUN COMPLETED WITH FAILURES (Pass Rate: {pass_pct:.1f}%){RESET}\n")

    # JSON Report Export
    if args.json:
        report_data = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "overall_status": "PASS" if (total_failed == 0 and total_errors == 0) else "FAIL",
            "total_tests": total_tests,
            "passed": total_passed,
            "failed": total_failed,
            "errors": total_errors,
            "skipped": total_skipped,
            "pass_rate_pct": round(pass_pct, 2),
            "elapsed_seconds": round(overall_elapsed, 4),
            "tier_summaries": tier_summaries,
            "records": all_records
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        print(f"Detailed execution report saved to: {args.json}")

    return 0 if (total_failed == 0 and total_errors == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
