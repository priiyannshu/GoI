#!/usr/bin/env bash
# ==============================================================================
# Indian Grade A Examinations Platform — Turnkey Cloudflare Deployment Script
# ==============================================================================
set -euo pipefail

# 1. Environment & Credentials
export NODE_OPTIONS="${NODE_OPTIONS:-} --dns-result-order=ipv4first"
export CLOUDFLARE_ACCOUNT_ID="913053598d368551936e69dd07298da5"
D1_DB_NAME="grade_a_db"
PAGES_PROJECT="grade-a-exams"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "=== [1/6] Verifying Wrangler Authentication ==="
wrangler whoami

echo "=== [2/6] Ensuring D1 Database '${D1_DB_NAME}' Exists ==="
if ! wrangler d1 list | grep -q "${D1_DB_NAME}"; then
  echo "Creating D1 database ${D1_DB_NAME} in APAC..."
  wrangler d1 create "${D1_DB_NAME}"
else
  echo "D1 database ${D1_DB_NAME} already exists."
fi

echo "=== [3/6] Applying D1 Schema & Seeding Remote Database ==="
echo "Executing 0001_initial_schema.sql..."
wrangler d1 execute "${D1_DB_NAME}" --remote --file="${ROOT_DIR}/worker/migrations/0001_initial_schema.sql" -y

echo "Executing 0002_seed_data.sql..."
wrangler d1 execute "${D1_DB_NAME}" --remote --file="${ROOT_DIR}/worker/migrations/0002_seed_data.sql" -y

echo "=== [4/6] Deploying Cloudflare Worker API (Hono) ==="
cd "${ROOT_DIR}/worker"
if [ ! -d "node_modules" ]; then
  npm install
fi
wrangler deploy

echo "=== [5/6] Building & Deploying Frontend PWA to Cloudflare Pages ==="
cd "${ROOT_DIR}/frontend"
if [ ! -d "node_modules" ]; then
  npm install
fi
npm run build

# Ensure Pages project exists
if ! wrangler pages project list | grep -q "${PAGES_PROJECT}"; then
  echo "Creating Pages project ${PAGES_PROJECT}..."
  wrangler pages project create "${PAGES_PROJECT}" --production-branch main
fi

echo "Deploying frontend dist to Cloudflare Pages..."
wrangler pages deploy dist --project-name "${PAGES_PROJECT}" --commit-dirty=true --branch main

echo "=== [6/6] Verifying Live Production Deployments ==="
API_URL="https://grade-a-api.priyanshukh1201.workers.dev"
PAGES_URL="https://grade-a-exams.pages.dev"

echo "Checking Worker Health (${API_URL}/)..."
curl -fsS "${API_URL}/" | jq .

echo "Checking Worker Exams Count (${API_URL}/api/v1/exams)..."
curl -fsS "${API_URL}/api/v1/exams" | jq '{success: .success, count: .count}'

echo "Checking Pages HTTP Code (${PAGES_URL})..."
curl -s -o /dev/null -w "HTTP Response: %{http_code}\n" "${PAGES_URL}"

echo "Checking Pages API Proxy (${PAGES_URL}/api/v1/exams)..."
curl -fsS "${PAGES_URL}/api/v1/exams" | jq '{success: .success, count: .count}'

echo ""
echo "🎉 DEPLOYMENT COMPLETE & VERIFIED!"
echo "PWA Application URL: ${PAGES_URL}"
echo "REST API Endpoint:   ${API_URL}"
