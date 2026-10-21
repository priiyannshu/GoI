#!/usr/bin/env bash
# ==============================================================================
# Configure Cloudflare API Token for GitHub Actions CI/CD Pipeline
# Repository: priiyannshu/GoI
# ==============================================================================
set -euo pipefail

REPO="priiyannshu/GoI"
ACCOUNT_ID="913053598d368551936e69dd07298da5"

echo "=========================================================="
echo " Cloudflare CI/CD Pipeline Secret Configuration"
echo " Target Repository: ${REPO}"
echo "=========================================================="

# Check if token was passed as an argument, otherwise prompt securely
if [ -n "${1:-}" ]; then
  CF_TOKEN="$1"
else
  read -rsp "Enter your Cloudflare API Token: " CF_TOKEN
  echo ""
fi

# Validation: ensure token is not empty
if [ -z "${CF_TOKEN// }" ]; then
  echo "Error: Token cannot be empty." >&2
  exit 1
fi

echo ""
echo "--> Setting CLOUDFLARE_API_TOKEN secret on GitHub..."
echo -n "${CF_TOKEN}" | gh secret set CLOUDFLARE_API_TOKEN -R "${REPO}"

echo "--> Verifying CLOUDFLARE_ACCOUNT_ID secret..."
echo -n "${ACCOUNT_ID}" | gh secret set CLOUDFLARE_ACCOUNT_ID -R "${REPO}"

echo ""
echo "✓ Secrets successfully configured in GitHub repository!"
echo "Listing repository secrets:"
gh secret list -R "${REPO}"

echo ""
read -rp "Trigger deployment pipeline now? (Y/n): " TRIGGER_DEPLOY
TRIGGER_DEPLOY="${TRIGGER_DEPLOY:-Y}"

if [[ "${TRIGGER_DEPLOY}" =~ ^[Yy]$ ]]; then
  echo ""
  echo "--> Triggering GitHub Actions workflow: deploy.yml..."
  gh workflow run deploy.yml -R "${REPO}" --ref main
  echo ""
  echo "🎉 Deployment triggered! Monitoring workflow run..."
  sleep 3
  gh run list -R "${REPO}" -L 1
  echo ""
  echo "To watch live logs, run:"
  echo "  gh run watch -R ${REPO}"
fi
