# Original User Request

## Initial Request — 2026-10-20T11:19:32Z

Build an exhaustive research database, verifiable ground-truth audit trail, and Cloudflare-hosted Vue 3 Progressive Web Application (PWA) with D3.js set visualizations for all Indian Grade A Government Examinations, eligibility profiling, and 2027 timelines.

Working directory: /home/deadpool/omniverse/grade-A
Integrity mode: benchmark

Reference blueprint: /home/deadpool/.gemini/antigravity-cli/brain/d71215f9-09c7-4e11-b5a8-a89812ab9758/plan.md

## Requirements

### R1. Ground-Truth Data & Verification Engine
Construct a structured SQLite database (`data/grade_a_exams.db`) with accompanying JSON export and verification audit logs. Populate comprehensive research for all Indian Grade A examinations starting with Cluster 1 (UPSC CSE, ESE, CAPF AC, CDS, AFCAT, etc.) and Cluster 2 (RBI Grade B, SEBI Grade A, NABARD Grade A, IFSCA, PFRDA, SIDBI), followed by State PSCs (UPPSC, BPSC, MPSC, etc.) and PSU Executive Trainees via GATE. Every entry must cite the official notification title, official document URL, gazette reference, exact clause number, and 2027 tentative exam cycle.

### R2. Universal Syllabus Taxonomy & Multi-View Set Visualizations
Define a unified, normalized syllabus taxonomy spanning General Studies, Aptitude/Reasoning, Economics/Finance, and Technical streams. Map each audited exam's stages to these taxonomy nodes. In the frontend, implement three synchronized D3.js visualization views:
1. An interactive UpSet-style overlap matrix showing topic membership frequencies across exams.
2. A dynamic pairwise/cluster Venn diagram calculating intersections (A ∩ B) and unique modules for any 2-4 selected exams.
3. A bipartite force-directed network graph linking exam nodes to syllabus topics with cluster physics.

### R3. Cloudflare-Ready Vue 3 PWA & Cloud Profile Engine
Develop an offline-first Vue 3 + Vite + Tailwind CSS Progressive Web Application with service worker caching. Include an interactive user profile intake flow evaluating multidimensional eligibility (DOB vs 2027 cutoffs, category relaxations, educational degrees & percentage thresholds, domicile/state languages, attempt limits, and physical standards). Provide cloud persistence and sync via Cloudflare Workers and D1 database.

## Acceptance Criteria

### Data & Audit Integrity
- [ ] SQLite database passes relational schema validation with foreign keys enabled.
- [ ] 100% of researched exams have direct official notification links and verified clause citations in `source_audit_log`.
- [ ] Automated test script verifies zero broken source links and validates eligibility calculation edge cases (e.g., age on 1 Aug 2027 vs 1 Jan 2027, reservation relaxations).

### Visualizations & Syllabus
- [ ] All three visualization modes (UpSet matrix, Pairwise Venn, Bipartite Graph) render smoothly without SVG errors.
- [ ] Selecting an exam or topic in any view highlights overlapping modules and updates syllabus coverage stats.

### PWA & Cloudflare Integration
- [ ] PWA builds with zero errors (`npm run build`), meets Lighthouse PWA installability requirements, and works offline via cached assets.
- [ ] Profile evaluation engine correctly evaluates user eligibility across all exams with explanatory pass/fail reasons.
- [ ] Cloudflare Worker endpoints and D1 schema migrations successfully deploy and sync profiles.
