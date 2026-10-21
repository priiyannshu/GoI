#!/usr/bin/env bash
# ==============================================================================
# Indian Grade A Examinations Platform — GitHub Sync Script
# Target Repository: git@github.com:priiyannshu/GoI.git
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
TARGET_REMOTE="git@github.com:priiyannshu/GoI.git"

cd "${ROOT_DIR}"

echo "=== [1/5] Verifying Git Initialization ==="
if [ ! -d ".git" ]; then
  echo "Initializing git repository on branch main..."
  git init -b main
fi

# Ensure branch is main
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")"
if [ "${CURRENT_BRANCH}" != "main" ]; then
  git branch -M main
fi

echo "=== [2/5] Configuring Git User Identity & Remote ==="
git config user.name "priiyannshu"
git config user.email "priyanshukh1201@gmail.com"

if git remote | grep -q "origin"; then
  git remote set-url origin "${TARGET_REMOTE}"
else
  git remote add origin "${TARGET_REMOTE}"
fi
echo "Configured remote origin -> $(git remote get-url origin)"

echo "=== [3/5] Verifying SSH Connection to GitHub ==="
ssh -T -o BatchMode=yes -o StrictHostKeyChecking=accept-new git@github.com 2>&1 || true

echo "=== [4/5] Staging Clean Tracked Files ==="
git add .
git status --short

echo "=== [5/5] Committing & Pushing to GitHub (main) ==="
if git diff --staged --quiet; then
  echo "No changes staged to commit."
else
  COMMIT_MSG="${1:-feat: Indian Grade A Government Examinations Intelligence Platform}"
  git commit -m "${COMMIT_MSG}"
fi

echo "Pushing branch 'main' to origin (${TARGET_REMOTE})..."
git push -u origin main

echo ""
echo "🎉 GITHUB SYNCHRONIZATION COMPLETE!"
echo "Repository: https://github.com/priiyannshu/GoI"
