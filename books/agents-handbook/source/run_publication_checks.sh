#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
PDF="${1:-}"
ARCHIVE="${2:-}"
RECEIPT="${3:-}"
MODE="${4:-manifest-only}"
if [[ -z "$PDF" || ! -f "$PDF" || -z "$ARCHIVE" || ! -f "$ARCHIVE" || -z "$RECEIPT" || ! -f "$RECEIPT" ]]; then
  echo "usage: bash $0 /path/to/Edition_1.7.pdf /path/to/Edition_1.7_Reproducibility_Package.zip /path/to/Publication_Build_Receipt_Edition_1.7.json [manifest-only|online]" >&2
  exit 2
fi
python "$ROOT/verify_release_metadata.py"
if [[ "$MODE" == "online" ]]; then python "$ROOT/verify_source_contract_manifest.py"; elif [[ "$MODE" == "manifest-only" ]]; then python "$ROOT/verify_source_contract_manifest.py" --manifest-only; else echo "invalid mode: $MODE" >&2; exit 2; fi
python "$ROOT/verify_manuscript_examples.py"
python "$ROOT/verify_companion_references.py"
python "$ROOT/verify_section_numbering.py"
python "$ROOT/verify_edition_history.py"
python "$ROOT/test_deferred_approval_application_contract.py"
python "$ROOT/reproduce_qa_evaluation.py" "$ROOT/qa_eval_synthetic_trials.csv" --grader "$ROOT/qa_eval_synthetic_grader_audit.csv" --failure "$ROOT/qa_eval_synthetic_failure_injection.csv" --json > "$ROOT/qa_eval_synthetic_results.reproduced.json"
python - "$ROOT" <<'PY'
import json,sys
from pathlib import Path
r=Path(sys.argv[1]); a=json.loads((r/'qa_eval_synthetic_results.json').read_text()); b=json.loads((r/'qa_eval_synthetic_results.reproduced.json').read_text())
if a!=b: raise SystemExit('evaluation results do not reproduce')
print('OK: evaluation results reproduce exactly')
PY
python "$ROOT/verify_pdf_text_layer.py" "$PDF"
python "$ROOT/verify_pdf_binding.py" "$PDF"
python "$ROOT/verify_pdf_navigation.py" "$PDF"
python "$ROOT/verify_embedded_package.py" "$PDF" "$ARCHIVE"
python "$ROOT/verify_build_receipt.py" "$PDF" "$ARCHIVE" "$RECEIPT"
python - "$ROOT" <<'PY'
import sys
from pathlib import Path
r=Path(sys.argv[1])
for p in r.glob('*.py'): compile(p.read_text(),str(p),'exec')
print('OK: companion Python sources compile in memory; no bytecode generated')
PY
(cd "$ROOT" && sha256sum -c SHA256SUMS.txt)
