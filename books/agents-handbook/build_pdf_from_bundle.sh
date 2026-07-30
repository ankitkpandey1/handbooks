#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
OUTPUT="${1:-$ROOT/build/Production_Agent_Engineering_Edition_1.8.pdf}"
mkdir -p "$(dirname "$OUTPUT")"
bash "$ROOT/source/build_pdf.sh" \
  "$ROOT/source/production_agent_engineering_edition_1_8.md" \
  "$ROOT/release/Production_Agent_Engineering_Edition_1.8_Reproducibility_Package.zip" \
  "$OUTPUT"
echo "Built: $OUTPUT"
