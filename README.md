# Indian Grade A Government Examinations Intelligence Platform (GoI)

An exhaustive research database, verifiable statutory ground-truth audit trail, universal syllabus ontology, and Cloudflare-hosted Vue 3 Progressive Web Application (PWA) with D3.js multi-view set visualizations and multidimensional eligibility profiling across 31 premier Indian Grade A examinations.

[![Live PWA](https://img.shields.io/badge/PWA-grade--a--exams.pages.dev-0284c7?style=flat-square&logo=cloudflare)](https://grade-a-exams.pages.dev)
[![API Edge Worker](https://img.shields.io/badge/API-grade--a--api.workers.dev-f97316?style=flat-square&logo=cloudflare-workers)](https://grade-a-api.priyanshukh1201.workers.dev)
[![D1 Database](https://img.shields.io/badge/D1-grade__a__db-10b981?style=flat-square&logo=sqlite)](https://dash.cloudflare.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)

---

## 🏛️ System Architecture

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
| - /api/v1/syllabus/taxonomy       |   JSON & Sync Protocol    | - Pinia State Stores              |
| - /api/v1/profile/evaluate & sync |                           | - Profile Intake Quiz Engine      |
| Cloudflare D1 Serverless DB       |                           | - D3.js Multi-View Visualizations |
+-----------------------------------+                           +-----------------------------------+
                                                                          |
                                                                          +---> 1. UpSet Overlap Matrix
                                                                          +---> 2. Dynamic Venn (2-4 Sets)
                                                                          +---> 3. Bipartite Force Graph
```

---

## 🚀 Live Deployments

- **Production Frontend PWA**: [https://grade-a-exams.pages.dev](https://grade-a-exams.pages.dev)
- **Cloudflare Edge Worker API**: [https://grade-a-api.priyanshukh1201.workers.dev](https://grade-a-api.priyanshukh1201.workers.dev)
- **Edge D1 Database**: `grade_a_db` (ID: `0a591154-d727-43ba-b8f9-005cb5dc58c6`, Region: `APAC`)

---

## 📊 Exam Coverage (31 Statutory Audits)

### 1. Central Civil & Uniformed Services (8 Exams)
- **UPSC CSE** (Civil Services Examination — IAS, IFS, IPS, IRS)
- **UPSC ESE** (Engineering Services Examination — CE, ME, EE, E&T)
- **UPSC IFoS** (Indian Forest Service)
- **UPSC CAPF (AC)** (Central Armed Police Forces — Assistant Commandants)
- **UPSC CDS** (Combined Defence Services — IMA, INA, AFA, OTA)
- **IAF AFCAT** (Air Force Common Admission Test — Flying & Ground Duty)
- **UPSC CGSE** (Combined Geo-Scientist Examination — GSI / CGWB)
- **UPSC IES/ISS** (Indian Economic Service / Indian Statistical Service)

### 2. Regulatory & Financial Authorities (7 Exams)
- **RBI Grade B** (Officers in Grade B - General / DEPR / DSIM)
- **SEBI Grade A** (Assistant Manager — General, Legal, IT, Engineering)
- **NABARD Grade A** (Assistant Manager in RDBS)
- **IFSCA Grade A** (Assistant Manager — International Financial Services Centres Authority)
- **PFRDA Grade A** (Assistant Manager — Pension Fund Regulatory and Development Authority)
- **SIDBI Grade A** (Assistant Manager — MSME Development Bank of India)
- **India Exim Bank MT** (Management Trainee / Deputy Manager Grade A)

### 3. State Public Service Commissions (10 Exams)
- **UPPSC PCS** (Uttar Pradesh Combined State / Upper Subordinate Services)
- **BPSC CCE** (Bihar Combined Competitive Examination — 70th CCE)
- **MPPSC SSE** (Madhya Pradesh State Service Examination)
- **RPSC RAS/RTS** (Rajasthan Administrative & Subordinate Services)
- **TSPSC Group 1** (Telangana State Public Service Commission Group-1)

### 4. Maharatna & Navratna PSUs via GATE (11 Organizations)
- **ONGC GT** (Oil and Natural Gas Corporation — Graduate Trainee)
- **IOCL Officers** (Indian Oil Corporation Limited — Engineers / Officers)
- **NTPC ET** (National Thermal Power Corporation — Executive Trainee)
- **BHEL ET** (Bharat Heavy Electricals Limited — Engineer Trainee)
- **PGCIL ET** (Power Grid Corporation of India — Executive Trainee)
- **HPCL Officers** (Hindustan Petroleum Corporation Limited)
- **BPCL Officers** (Bharat Petroleum Corporation Limited)
- **SAIL MT (Tech)** (Steel Authority of India — Management Trainee Technical)
- **GAIL ET** (Gas Authority of India Limited — Executive Trainee)
- **Coal India MT** (Coal India Limited — Management Trainee)
- **BARC / NPCIL OCES/DGFS** (Bhabha Atomic Research Centre Scientific Officers)

---

## 🛠️ Repository Layout

```
.
├── data/
│   ├── schema.sql                       # Relational DDL with CHECK constraints & JSON validations
│   ├── grade_a_exams.db                 # Master SQLite 3.38+ database
│   ├── grade_a_exams.json               # Master JSON export of all 31 exams and eligibility
│   ├── syllabus_taxonomy.json           # 192 normalized taxonomy topics across 6 domains
│   └── exam_syllabus_matrix.json        # 1,123 stage-to-topic mapping pairs with depth levels
├── scripts/
│   ├── build_database.py                # Database population compiler
│   ├── verify_database.py               # 0-violation statutory verification suite
│   ├── export_json.py                   # Relational to JSON exporter
│   ├── deploy_cloudflare.sh             # Turnkey automated Cloudflare deployment script
│   └── sync_github.sh                   # Git sync script
├── frontend/                            # Vue 3 + Vite + Tailwind CSS Progressive Web Application
│   ├── src/
│   │   ├── components/visualizations/   # D3.js UpSet Matrix, Edwards-Venn (2-4), Bipartite Force Graph
│   │   ├── services/                    # Eligibility engine, IndexedDB outbox, API worker client
│   │   ├── stores/                      # Pinia stores: exam catalog, syllabus state, user profile
│   │   └── views/                       # Catalog, Syllabus Explorer, Quiz Stepper, Report Card
│   ├── public/                          # PWA manifest, service worker headers, icons
│   └── functions/                       # Cloudflare Pages edge proxy functions
├── worker/                              # Cloudflare Edge Worker API (Hono Framework)
│   ├── src/index.ts                     # REST routes: /exams, /syllabus, /profile/evaluate, /sync
│   ├── migrations/                      # D1 serverless schema and seed migrations
│   └── wrangler.toml                    # Wrangler deployment configuration with D1 bindings
└── tests/
    ├── e2e/                             # Opaque-box requirement-driven test harness (Tiers 1-4)
    └── unit/                            # Component & eligibility edge-case unit test suites
```

---

## ⚡ Quick Start

### 1. Verification of Master SQLite Database
```bash
python3 scripts/verify_database.py --db data/grade_a_exams.db
```

### 2. Run PWA Frontend Locally
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Cloudflare Worker API Locally
```bash
cd worker
npm install
npm run dev
```

### 4. Deploy Live Infrastructure to Cloudflare
```bash
bash scripts/deploy_cloudflare.sh
```

---

## 📜 Statutory Auditability
100% of facts recorded in `source_audit_log` cite:
- Official Notification Document Title & Issuing Ministry / Constitutional Commission
- Gazette of India / State Gazette Reference Numbers
- Exact Statutory Rule and Clause Numbers
- Official Verifiable Download URLs (zero broken links)
