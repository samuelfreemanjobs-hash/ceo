#!/usr/bin/env bash
# Open a new spec cycle directory.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SPECS="$REPO_ROOT/specs"

usage() {
  echo "Usage: open-cycle.sh <slug> [title]"
  echo "Example: open-cycle.sh q2-onboarding 'Q2 Onboarding Revamp'"
  exit 1
}

[[ $# -ge 1 ]] || usage

SLUG="$1"
TITLE="${2:-$SLUG}"
DATE="$(date -u +%Y-%m-%d)"
CYCLE_ID="${DATE}-${SLUG}"
DIR="$SPECS/$CYCLE_ID"

if [[ -d "$DIR" ]]; then
  echo "Cycle already exists: $DIR" >&2
  exit 1
fi

mkdir -p "$DIR"

cat > "$DIR/00-brief.md" <<EOF
# Brief: $TITLE

**Cycle:** \`$CYCLE_ID\`
**Opened:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Goal

## Constraints

## Success metrics

EOF

cat > "$DIR/01-research.md" <<EOF
# Research: $TITLE

_Pending._

EOF

cat > "$DIR/02-spec.md" <<EOF
# Spec: $TITLE

## Problem

## Requirements

## Acceptance criteria

EOF

cat > "$DIR/03-tasks.md" <<EOF
# Tasks: $TITLE

| ID | Task | Owner | Status |
|----|------|-------|--------|
| T1 | | | pending |

EOF

echo "Opened cycle: specs/$CYCLE_ID/"
