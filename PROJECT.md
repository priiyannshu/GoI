# Project: Indian Grade A Government Examinations Intelligence Platform

## Architecture
An exhaustive research database, verifiable ground-truth audit trail, universal syllabus ontology, and Cloudflare-hosted Vue 3 Progressive Web Application (PWA) with D3.js multi-view set visualizations and multidimensional eligibility profiling for all Indian Grade A examinations.

```
+---------------------------------------------------------------------------------------------------+
|                                   DATA LAYER (SQLite Master)                                      |
| data/grade_a_exams.db (exams, eligibility_criteria, syllabus_taxonomy, exam_syllabus_map,        |
|                         source_audit_log, user_profiles)                                          |
| scripts/verify_database.py (verifies foreign keys, links, 2027 timelines, clause citations)       |
+---------------------------------------------------------------------------------------------------+
                                                  |
                  +-------------------------------+-------------------------------+
                  |                                                               |
                  v                                                               v
+-----------------------------------+                           +-----------------------------------+
|    CLOUDFLARE EDGE INFRASTRUCTURE |                           |          VUE 3 PWA FRONTEND       |
| worker/ (Cloudflare Worker API)   |                           | frontend/ (Vite + Vue 3 + Tailwind|
| - /api/v1/exams                   | <=======================> | - Offline Service Worker (Workbox)|
| - /api/v1/syllabus                |   JSON & Sync Protocol    | - Pinia State Stores              |
| - /api/v1/profile/evaluate & sync |                           | - Profile Intake Quiz Engine      |
| Cloudflare D1 Serverless DB       |                           | - D3.js Multi-View Visualizations |
+-----------------------------------+                           +-----------------------------------+
                                                                          |
                                                                          +---> 1. UpSet Overlap Matrix
                                                                          +---> 2. Pairwise/Cluster Venn (2-4)
                                                                          +---> 3. Bipartite Force Graph
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | SQLite Master Schema | Relational DDL with foreign keys, JSON validation, and indexes | M1_DATA_ENGINE | Survey Miner 2 |
| 2 | Cluster 1 Research Data | 8 Central All-India & Uniformed services (UPSC CSE, ESE, IFoS, CAPF AC, CDS, AFCAT, CGSE, IES/ISS) with URLs, gazettes, clauses | M1_DATA_ENGINE | Survey Miner 1 |
| 3 | Cluster 2 Research Data | 7 Premier Regulatory/Financial bodies (RBI Gr B, SEBI Gr A, NABARD Gr A, IFSCA Gr A, PFRDA Gr A, SIDBI Gr A, EXIM Bank MT) | M1_DATA_ENGINE | Survey Miner 1 |
| 4 | Cluster 3 Research Data | 10 State PSCs (UPPSC, BPSC, MPSC, MPPSC, RPSC, TNPSC, APPSC, TSPSC, WBPSC, KPSC) with language/domicile rules | M1_DATA_ENGINE | Survey Miner 2 |
| 5 | Cluster 4 Research Data | 11 Maharatna/Navratna PSUs (ONGC, IOCL, NTPC, BHEL, PGCIL, HPCL, BPCL, SAIL, GAIL, Coal India, BARC/NPCIL) with GATE disciplines | M1_DATA_ENGINE | Survey Miner 2 |
| 6 | Verifiable Fact-Audit Log | `source_audit_log` with 100% notification links, gazette numbers, and clause citations | M1_DATA_ENGINE | Survey Miner 1 & 2 |
| 7 | Data Verification Engine | Automated test suite validating relational schema, zero broken links, and edge cases | M1_DATA_ENGINE | Survey Miner 2 |
| 8 | Master JSON Export | Automated extraction of SQLite database into `data/grade_a_exams.json` | M1_DATA_ENGINE | Survey Miner 2 |
| 9 | Universal Syllabus Taxonomy | Normalized hierarchy across 6 domains (GS, Quant, Reasoning, English, Econ-Fin, Tech) with canonical IDs | M2_SYLLABUS_TAXONOMY | Survey Explorer 3 |
| 10 | 4-Level Cognitive Depth Scale | Foundation, Intermediate, Advanced, Analytical cognitive levels per stage mapping | M2_SYLLABUS_TAXONOMY | Survey Explorer 3 |
| 11 | Exam-Syllabus Stage Mapping | Relational mapping of all 36 exams' stages and papers to taxonomy nodes | M2_SYLLABUS_TAXONOMY | Survey Explorer 3 |
| 12 | Syllabus Export Artifacts | Bundled JSON matrix and taxonomy for frontend visualization pipelines | M2_SYLLABUS_TAXONOMY | Survey Explorer 3 |
| 13 | Vue 3 + Vite + Tailwind App | Responsive modern PWA application shell with clean dark/light theme | M3_PWA_PROFILE_ENGINE | Survey Explorer 3 |
| 14 | Offline PWA Service Worker | Workbox caching strategy (Stale-While-Revalidate for data, Cache-First for assets) | M3_PWA_PROFILE_ENGINE | Survey Explorer 3 |
| 15 | Multidimensional Eligibility Engine | Pure TypeScript engine evaluating 2027 cutoffs, categories, degrees, percentages, attempts, physical standards | M3_PWA_PROFILE_ENGINE | Survey Explorer 3 |
| 16 | Interactive Profile Intake Quiz | Multi-step interactive wizard collecting DOB, category, academic history, domicile, and physical specs | M3_PWA_PROFILE_ENGINE | Survey Explorer 3 |
| 17 | Eligibility Explanatory Report | Comprehensive report card showing eligible, conditionally eligible, and ineligible exams with reasons and citations | M3_PWA_PROFILE_ENGINE | Survey Explorer 3 |
| 18 | UpSet Overlap Matrix View | Interactive D3.js UpSet plot showing intersection sizes and combination dots across selected exams | M4_D3_VISUALIZATIONS | Survey Explorer 3 |
| 19 | Dynamic Venn Diagram View | Interactive 2, 3, and 4-set Venn diagrams (Edwards-Venn ellipses for 4 sets) with region selection | M4_D3_VISUALIZATIONS | Survey Explorer 3 |
| 20 | Bipartite Force Network Graph | D3 force-directed graph linking exam nodes to syllabus topics with cluster physics and depth stroke styling | M4_D3_VISUALIZATIONS | Survey Explorer 3 |
| 21 | Cross-View State Synchronization | Pinia store synchronizing active exams, hovered topics, and filtered combinations across all 3 views | M4_D3_VISUALIZATIONS | Survey Explorer 3 |
| 22 | Cloudflare Worker Hono API | Serverless REST API providing exam catalog, syllabus queries, and profile evaluation endpoints | M5_CLOUDFLARE_EDGE | Survey Explorer 3 |
| 23 | Cloudflare D1 Database Migrations | D1 SQLite schema migrations and profile synchronization endpoints | M5_CLOUDFLARE_EDGE | Survey Explorer 3 |
| 24 | E2E Testing Suite (Tiers 1-4) | Opaque-box requirement-driven test harness covering >=11 × N test cases across all features | E2E_TESTING_TRACK | Plan Blueprint & Req |
| 25 | Final E2E Pass & Hardening (Tier 5)| 100% pass of E2E test suite followed by adversarial white-box coverage hardening | M6_FINAL_E2E | Plan Blueprint & Req |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| E2E | E2E_TESTING_TRACK | Opaque-box test harness & test suite (Tiers 1-4), publish TEST_READY.md | none | IN_PROGRESS |
| M1 | M1_DATA_ENGINE | SQLite schema, 36 exams data, source_audit_log, verification script, JSON export | none | IN_PROGRESS |
| M2 | M2_SYLLABUS_TAXONOMY | Universal taxonomy ontology, cognitive depth, stage mappings for 36 exams | M1 | PLANNED |
| M3 | M3_PWA_PROFILE_ENGINE | Vue 3 + Vite + Tailwind PWA, Workbox offline caching, eligibility engine, intake quiz | M1 | PLANNED |
| M4 | M4_D3_VISUALIZATIONS | UpSet matrix, dynamic Venn (2-4), Bipartite force graph, Pinia synchronization | M2, M3 | PLANNED |
| M5 | M5_CLOUDFLARE_EDGE | Cloudflare Workers Hono API, D1 migrations, profile sync endpoints, wrangler config | M1, M3 | PLANNED |
| M6 | M6_FINAL_E2E | 100% E2E test pass (Tiers 1-4) + Tier 5 adversarial coverage hardening | M1-M5, E2E | PLANNED |

## Interface Contracts

### 1. Data Layer ↔ Consumers (`data/grade_a_exams.json` & SQLite)
- **SQLite Database Path**: `data/grade_a_exams.db`
- **JSON Export Path**: `data/grade_a_exams.json`
- **Schema Entities**:
  - `exams`: `{ exam_id: string, title: string, short_code: string, category: string, administering_body: string, frequency: string, official_website: string, latest_official_notification_url: string, latest_gazette_ref: string, tentative_timeline_2027: object, description: string }`
  - `eligibility_criteria`: `{ exam_id: string, cutoff_reference_date_rule: string, min_age_gen: number, max_age_gen: number, relaxations_json: object, min_education_level: string, accepted_disciplines: string[], min_aggregate_percentage_gen: number, min_aggregate_percentage_reserved: number, final_year_students_allowed: boolean, attempt_limit_gen: number|null, attempt_limit_obc: number|null, attempt_limit_sc_st: number|null, domicile_restrictions: string[]|null, language_requirements: object|null, physical_standards: object|null, source_citation_clause: string }`
  - `source_audit_log`: `{ audit_id: string, exam_id: string, fact_type: string, official_document_title: string, document_date: string, clause_or_page_number: string, official_download_link: string, archive_link: string|null, verifier_notes: string }`

### 2. Syllabus Taxonomy ↔ Visualizations (`data/syllabus_taxonomy.json` & `exam_syllabus_matrix.json`)
- `syllabus_taxonomy`: Array of `{ topic_id: string, domain: string, sub_domain: string, topic_title: string, description: string }`
  - `topic_id` format: `[domain].[sub_domain].[topic_slug]`
- `exam_syllabus_map`: Array of `{ exam_id: string, stage_name: string, topic_id: string, depth_level: 'Foundation'|'Intermediate'|'Advanced'|'Analytical', is_optional: boolean, weightage_pct_estimate?: number, source_clause_ref: string }`

### 3. Eligibility Engine ↔ Frontend Profile Quiz & Worker API (`src/services/eligibilityEngine.ts`)
- `evaluateEligibility(profile: UserProfileInput, rule: ExamEligibilityRule, examYear?: number): EligibilityVerdict`
- `UserProfileInput`: `{ dob: string, gender: string, category: string, is_ex_serviceman: boolean, ex_service_years: number, graduation_degree: string, graduation_discipline: string, graduation_aggregate_pct: number, is_final_year: boolean, state_domicile: string, fluent_languages: string[], height_cm: number, chest_cm?: number, chest_expansion_cm?: number, has_color_blindness: boolean, prior_attempts: Record<string, number> }`
- `EligibilityVerdict`: `{ exam_id: string, status: 'ELIGIBLE' | 'CONDITIONALLY_ELIGIBLE' | 'INELIGIBLE', reasons: string[], relaxations_applied: string[], statutory_citation: string }`

### 4. Cloudflare Worker API ↔ PWA Client
- `GET /api/v1/exams`: Returns list of all exams and 2027 timelines.
- `GET /api/v1/exams/:id`: Returns complete exam profile and eligibility rules.
- `GET /api/v1/syllabus/taxonomy`: Returns full normalized syllabus taxonomy.
- `GET /api/v1/syllabus/matrix`: Returns exam-topic mapping matrix.
- `POST /api/v1/profile/evaluate`: Accepts `UserProfileInput`, returns verdicts for all exams.
- `POST /api/v1/profile/sync`: Stores user profile in D1 with encrypted/hashed `user_id`.

## Code Layout
```
/home/deadpool/omniverse/grade-A
├── data/
│   ├── schema.sql
│   ├── grade_a_exams.db
│   ├── grade_a_exams.json
│   ├── syllabus_taxonomy.json
│   └── exam_syllabus_matrix.json
├── scripts/
│   ├── build_database.py
│   ├── verify_database.py
│   └── export_json.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── public/
│   └── src/
│       ├── main.ts
│       ├── App.vue
│       ├── router/
│       ├── stores/
│       │   ├── useExamMasterStore.ts
│       │   ├── useSyllabusVisualizationStore.ts
│       │   └── useUserProfileStore.ts
│       ├── components/
│       │   ├── common/
│       │   ├── visualizations/
│       │   │   ├── UpsetMatrixView.vue
│       │   │   ├── VennDiagramView.vue
│       │   │   ├── BipartiteGraphView.vue
│       │   │   └── SyllabusSyncToolbar.vue
│       │   └── quiz/
│       │       ├── QuizStepper.vue
│       │       └── ...
│       ├── views/
│       │   ├── HomeView.vue
│       │   ├── SyllabusExplorerView.vue
│       │   ├── ProfileQuizView.vue
│       │   └── ExamCatalogView.vue
│       └── services/
│           ├── eligibilityEngine.ts
│           ├── apiWorkerClient.ts
│           └── indexedDbStorage.ts
├── worker/
│   ├── wrangler.toml
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   └── index.ts
│   └── migrations/
│       └── 0001_initial_schema.sql
└── tests/
    ├── e2e/
    │   ├── test_runner.py
    │   ├── tier1_feature_coverage.py
    │   ├── tier2_boundary_corner.py
    │   ├── tier3_pairwise_combinations.py
    │   └── tier4_real_world_scenarios.py
    └── unit/
```
