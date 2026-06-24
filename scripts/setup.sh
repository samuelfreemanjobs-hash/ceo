#!/usr/bin/env bash
# setup.sh — one-time bootstrap for the business stack
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> Creating output directories"
mkdir -p docs/marketing/{offers,proposals,landing-pages,campaigns,content,funnels,decisions,reports,research/profiles,research/alerts}
mkdir -p scheduler-agent/data

echo "==> Installing marketing-dept"
(cd marketing-dept && pip install -q -e .)

echo "==> Installing scheduler-agent deps"
pip install -q -r scheduler-agent/requirements.txt

echo "==> Optional: production scheduler deps (Google Calendar, Redis)"
echo "    pip install -r scheduler-agent/requirements-production.txt"

echo "==> Env templates"
for f in .env.example marketing-dept/.env.example scheduler-agent/.env.example; do
  [[ -f "$f" ]] && echo "    $f"
done
echo "    Copy and add ANTHROPIC_API_KEY before running agents."

echo "==> Regenerating agent indexes"
if [[ -x .github/utils/generate-indexes.sh ]]; then
  .github/utils/generate-indexes.sh
fi

echo ""
echo "Done. Next: edit docs/marketing/BRAND-PROFILE.md"
echo "Then: docs/marketing/GETTING-STARTED.md"
