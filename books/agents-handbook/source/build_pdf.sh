#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
SOURCE="${1:-$ROOT/production_agent_engineering_2026_edition_1_7.md}"
ARCHIVE="${2:-$ROOT/Production_Agent_Engineering_2026_Edition_1.7_Reproducibility_Package.zip}"
OUTPUT="${3:-$ROOT/Production_Agent_Engineering_2026_Edition_1.7.pdf}"
RAW="${OUTPUT%.pdf}.raw.pdf"

pandoc --defaults "$ROOT/pandoc_defaults.yaml" "$SOURCE" -o "$RAW"
python "$ROOT/attach_and_linearize_pdf.py" "$RAW" "$ARCHIVE" "$OUTPUT"
rm -f "$RAW"
