#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUTPUT="${1:-$ROOT/build/Production_Agent_Engineering_2026_Edition_1.7.pdf}"
mkdir -p "$(dirname "$OUTPUT")"
bash "$ROOT/source/build_pdf.sh" \
  "$ROOT/source/production_agent_engineering_2026_edition_1_7.md" \
  "$ROOT/release/Production_Agent_Engineering_2026_Edition_1.7_Reproducibility_Package.zip" \
  "$OUTPUT"
echo "Built: $OUTPUT"
