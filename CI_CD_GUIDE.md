# Automated CI/CD Pipeline Guide: Cloudflare Deployment

This guide explains the automated Continuous Integration and Continuous Deployment (CI/CD) pipeline for the **Indian Grade A Examinations Intelligence Platform (GoI)**, configured via GitHub Actions in [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

Whenever code is pushed to the `main` branch on GitHub, the pipeline automatically tests, migrates the database, and deploys both the Cloudflare Worker API and the Cloudflare Pages Frontend PWA.

---

## 🏗️ Architecture & Pipeline Stages

```
   Git Push to `main` (or Pull Request)
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 1: Build & Quality Gate                           │
│ - Node.js 20 & Python 3.11 environment setup            │
│ - Frontend: TypeScript check (vue-tsc) & Vite PWA build │
│ - Worker: TypeScript type-check (tsc)                   │
│ - Node.js eligibility & bipartite adversarial suites    │
│ - Python database & boundary test suites                │
│ - Pre-compiled `dist` artifact uploaded for deployment  │
└───────────────────────────┬─────────────────────────────┘
                            │ (Only runs on push to main or manual trigger)
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 2: Deploy Cloudflare Worker API                   │
│ - Authenticates with `CLOUDFLARE_API_TOKEN`             │
│ - Applies pending remote D1 migrations (idempotent)     │
│ - Deploys Hono REST API Worker (`grade-a-api`)          │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 3: Deploy Frontend PWA to Cloudflare Pages        │
│ - Downloads validated build artifact from Stage 1       │
│ - Deploys assets and Edge Proxy functions to Pages      │
│   Project: `goi` (Branch: `main`)                       │
└───────────────────────────┬─────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│ Stage 4: Post-Deployment Smoke Verification             │
│ - Verifies Worker root health and `/api/v1/exams`       │
│ - Verifies Cloudflare Pages HTTP status                 │
│ - Verifies Cloudflare Pages reverse proxy routing       │
│ - Runs live candidate auth and D1 persistence probes    │
└─────────────────────────────────────────────────────────┘
```

---

## 🔑 1. Cloudflare API Token Setup

To enable GitHub Actions to deploy to Cloudflare, you need a Cloudflare API Token with permissions to manage Workers, Pages, and D1.

### Step-by-Step Instructions:

1. Log into your [Cloudflare Dashboard](https://dash.cloudflare.com).
2. Click your profile icon in the top right corner and navigate to **My Profile** > **API Tokens**.
3. Click **Create Token**.
4. You can use the **Edit Cloudflare Workers** template, or select **Create Custom Token** and configure:
   - **Token name**: `GitHub-Actions-GoI-Deploy`
   - **Permissions**:
     - `Account` — `Workers Scripts` — **Edit**
     - `Account` — `Cloudflare Pages` — **Edit**
     - `Account` — `D1` — **Edit**
     - `User` — `Memberships` — **Read**
   - **Account Resources**:
     - `Include` — `All accounts` (or select your account `priyanshukh1201@gmail.com` / `913053598d368551936e69dd07298da5`)
   - **TTL / Expiration**: Set according to your security policy (or leave permanent).
5. Click **Continue to summary**, review, and click **Create Token**.
6. **Copy the generated API token** (Cloudflare will only display it once).

---

## ⚙️ 2. Configure GitHub Repository Secrets

Configure the credentials in your GitHub repository so GitHub Actions can authenticate with Cloudflare:

1. Open your GitHub repository: [https://github.com/priiyannshu/GoI](https://github.com/priiyannshu/GoI)
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Under **Repository secrets**, click **New repository secret**.
4. Add the following secret:
   - **Name**: `CLOUDFLARE_API_TOKEN`
   - **Secret**: Paste the token copied from Step 1.
   - Click **Add secret**.
5. *(Optional)* Add `CLOUDFLARE_ACCOUNT_ID`:
   - **Name**: `CLOUDFLARE_ACCOUNT_ID`
   - **Secret**: `913053598d368551936e69dd07298da5`
   - *(Note: If this is omitted, the workflow automatically falls back to your project account ID defined in `worker/wrangler.toml`)*.

---

## 🚀 3. How Deployments Trigger

### Automatic Deployment on Code Push:
Whenever changes are pushed to `main`:
```bash
git add .
git commit -m "feat: enhance eligibility rules and UI"
git push origin main
```
GitHub Actions detects the push event, runs all tests and builds, applies database migrations, deploys the Worker and Pages, and executes verification smoke tests.

### Pull Requests:
When a pull request is opened or updated targeting `main`, the **Build & Quality Gate** job runs automatically:
- Validates Vue TypeScript types (`vue-tsc --noEmit`)
- Compiles Vite PWA
- Validates Worker TypeScript types (`tsc --noEmit`)
- Runs all unit and adversarial test suites
- **Does not deploy** to production, ensuring pull requests are safely vetted before merging.

### Manual One-Click Deployment (`workflow_dispatch`):
1. In your GitHub repository, click the **Actions** tab.
2. Select **CI/CD Pipeline - Cloudflare Deployment** from the left sidebar.
3. Click **Run workflow**, choose `Branch: main`, and click **Run workflow**.

---

## 🧪 4. Test Matrix & Automated Verification

The workflow enforces a zero-regression policy before any code reaches production:

| Test Group | Runner | Target |
| :--- | :--- | :--- |
| **Vue TypeScript Compilation** | `vue-tsc --noEmit` | `frontend/src/**/*.vue`, `*.ts` |
| **Worker TypeScript Compilation** | `tsc --noEmit` | `worker/src/**/*.ts` |
| **Statutory Eligibility Suite** | `node` | 35 test cases covering age cutoffs, percentages, category relaxations |
| **Bipartite Physics Graph Suite** | `node` | 10 adversarial force simulation & coordinate safety tests |
| **Relational Database Integrity** | `python3` | Schema foreign keys, 2027 timelines, clause citations |
| **Edge Boundary & Fuzzing Probes** | `python3` | Leap years, non-rounding float boundaries, BiDi strings |
| **Live Candidate Auth & Sync** | `python3` | End-to-end PIN registration, unique ID generation, D1 persistence |

---

## 🌐 5. Production Endpoints

| Component | Target URL | Managed By |
| :--- | :--- | :--- |
| **Production PWA** | [https://goi-6hi.pages.dev](https://goi-6hi.pages.dev) | Cloudflare Pages |
| **Worker REST API** | [https://grade-a-api.priyanshukh1201.workers.dev](https://grade-a-api.priyanshukh1201.workers.dev) | Cloudflare Workers |
| **Edge Database** | `grade_a_db` (`0a591154-d727-43ba-b8f9-005cb5dc58c6`) | Cloudflare D1 |

---

## 🛠️ 6. Troubleshooting

- **Authentication Error (`Authentication error [code: 10000]`)**:
  - Verify that `CLOUDFLARE_API_TOKEN` is correctly set in GitHub Repository Secrets.
  - Ensure the token has `Workers Scripts:Edit`, `Cloudflare Pages:Edit`, and `D1:Edit` permissions.
- **D1 Migration Failures**:
  - Migrations in `worker/migrations/` must be sequentially numbered (e.g., `0001_initial_schema.sql`, `0002_seed_data.sql`, `0003_candidate_auth.sql`).
  - All migrations are idempotent (`CREATE TABLE IF NOT EXISTS`, `INSERT OR REPLACE`).
- **Pages Deployment Mismatch**:
  - Ensure the Pages project name in `.github/workflows/deploy.yml` matches `goi`.
