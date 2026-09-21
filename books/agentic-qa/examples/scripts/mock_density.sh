#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
# Mock/patch count vs assert count per file; exit 1 above THRESHOLD.
set -euo pipefail
THRESHOLD="${THRESHOLD:-0.5}"
FILES=("$@")
if [ "${#FILES[@]}" -eq 0 ]; then
    FILES=($(git diff --name-only -- '*.py' 2>/dev/null || true))
fi
STATUS=0
PAT='\b(mock|patch|MagicMock|jest\.mock)\b'
for f in "${FILES[@]}"; do
    [ -f "$f" ] || continue
    mocks=$( (grep -Eo "$PAT" "$f" || true) | wc -l)
    asserts=$( (grep -Eo '\bassert\b' "$f" || true) | wc -l)
    read -r ratio over <<< "$(awk -v m="$mocks" -v a="$asserts" \
        -v t="$THRESHOLD" 'BEGIN{
        if(a==0){r=(m>0)?"inf":"0.00";o=(m>0)?1:0}
        else{r=sprintf("%.2f",m/a);o=(m/a>t)?1:0}
        print r, o}')"
    printf '%-30s mocks=%-3s asserts=%-3s ratio=%s\n' \
        "$f" "$mocks" "$asserts" "$ratio"
    [ "$over" -eq 1 ] && STATUS=1
done
exit $STATUS
