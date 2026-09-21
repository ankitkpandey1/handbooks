#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
# Usage: prove_it_fails.sh <test_file> <source_file>
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
TEST_FILE="$1"; SRC_FILE="$2"
cp "$SRC_FILE" "$SRC_FILE.orig"
trap 'mv "$SRC_FILE.orig" "$SRC_FILE"' EXIT
echo "== baseline run =="
python -m pytest -q "$TEST_FILE" \
    || { echo "baseline failing, abort"; exit 2; }

if grep -q '>=' "$SRC_FILE"; then
    sed -i '0,/>=/{s/>=/>/}' "$SRC_FILE"; echo "mutated: '>=' -> '>'"
elif grep -q ' - ' "$SRC_FILE"; then
    sed -i '0,/ - /{s/ - / + /}' "$SRC_FILE"; echo "mutated: '-' -> '+'"
else
    echo "no mutable operator found"; exit 2
fi

echo "== mutant run =="
if python -m pytest -q "$TEST_FILE"; then
    echo "RESULT: suite did NOT notice the mutant (still green)"
else
    echo "RESULT: suite noticed the mutant (went red)"
fi
