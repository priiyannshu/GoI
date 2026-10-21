# E2E Test Infra: Indian Grade A Government Examinations Platform

## Test Philosophy
- Opaque-box, requirement-driven. Derived from `ORIGINAL_REQUEST.md` and statutory examination rules, completely independent of implementation internals.
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinatorial Testing + Real-World Workload Testing.

## Feature Inventory (25 Features)
| # | Feature | Source (Requirement) | Tier 1 (>=5) | Tier 2 (>=5) | Tier 3 (Pairwise) | Tier 4 (Workload) |
|---|---------|----------------------|:------------:|:------------:|:-----------------:|:-----------------:|
| 1 | SQLite Master Schema | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 2 | Cluster 1 Research Data | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 3 | Cluster 2 Research Data | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 4 | Cluster 3 Research Data | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 5 | Cluster 4 Research Data | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 6 | Verifiable Fact-Audit Log | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 7 | Data Verification Engine | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 8 | Master JSON Export | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ | ✓ |
| 9 | Universal Syllabus Taxonomy | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 10 | 4-Level Cognitive Depth Scale | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 11 | Exam-Syllabus Stage Mapping | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 12 | Syllabus Export Artifacts | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 13 | Vue 3 + Vite + Tailwind App | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 14 | Offline PWA Service Worker | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 15 | Multidimensional Eligibility Engine | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 16 | Interactive Profile Intake Quiz | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 17 | Eligibility Explanatory Report | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 18 | UpSet Overlap Matrix View | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 19 | Dynamic Venn Diagram View | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 20 | Bipartite Force Network Graph | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 21 | Cross-View State Synchronization | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ | ✓ |
| 22 | Cloudflare Worker Hono API | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 23 | Cloudflare D1 Migrations | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ | ✓ |
| 24 | E2E Test Suite Automation | ORIGINAL_REQUEST AC | 5 | 5 | ✓ | ✓ |
| 25 | Final Acceptance Verification | ORIGINAL_REQUEST AC | 5 | 5 | ✓ | ✓ |

## Test Architecture
- Test Runner: Python pytest & custom runner script `python3 tests/e2e/test_runner.py`
- Pass/Fail semantics: Exit code 0 indicates all tests pass. Non-zero indicates failure.
- Directory layout:
  - `tests/e2e/tier1_feature_coverage.py`
  - `tests/e2e/tier2_boundary_corner.py`
  - `tests/e2e/tier3_pairwise_combinations.py`
  - `tests/e2e/tier4_real_world_scenarios.py`
  - `tests/e2e/test_runner.py`

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Engineering Graduate targeting UPSC ESE, Civil Services (IPS preference), and PSU Direct via GATE | F1, F2, F5, F15, F16, F17, F19, F20 | High |
| 2 | Commerce / MBA Graduate comparing RBI Grade B, SEBI Grade A, and NABARD Grade A overlaps | F1, F3, F9, F11, F15, F18, F19, F21 | High |
| 3 | State PCS Aspirant cross-applying for UPPSC, BPSC, and MPSC with domicile/language barriers | F1, F4, F15, F16, F17, F18, F20 | High |
| 4 | Offline Mobile User taking Profile Intake Quiz, caching catalog, and syncing to Cloudflare D1 | F13, F14, F15, F16, F22, F23 | High |
| 5 | Broad-spectrum General Graduate exploring full Grade A landscape via UpSet and Network graph | F9, F11, F18, F19, F20, F21 | High |

## Coverage Thresholds
- Tier 1: >=5 per feature (Total >= 125 test cases)
- Tier 2: >=5 per feature (Total >= 125 test cases)
- Tier 3: Pairwise coverage of major feature combinations (Total >= 25 test cases)
- Tier 4: Realistic end-to-end application scenarios (Total >= 13 test cases)
- **Minimum Total Test Cases**: ~288 test cases
