#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
#
# Regenerates every derived artifact of a Tier A edition, in dependency order, and then runs the
# book's own verifier suite as the gate.
#
#   scripts/regen-edition.sh <slug>
#
# Run after scripts/cut-edition.py has done the text transforms. Needs the full toolchain
# (Pandoc, XeLaTeX, Ghostscript, pdftotext, PyMuPDF), so in practice this runs in CI.
#
# Order matters and is not obvious:
#   code blocks -> environment lock -> manifest hashes -> source checksums -> companion zip
#   -> PDF (embeds the zip) -> build receipt (hashes the PDF) -> bundle manifest -> bundle sums
#
# The companion zip is a member-for-member copy of source/, and source/SHA256SUMS.txt is itself a
# member, so the checksums must be written before the zip is built. The receipt hashes the final
# PDF, so it must come after the PDF. Getting this order wrong produces a bundle that verifies
# locally and fails on a clean checkout.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
META="$REPO/scripts/bookmeta.py"
SLUG="${1:?usage: scripts/regen-edition.sh <slug>}"

BOOK="$REPO/books/$SLUG"
SRC_DIR="$BOOK/source"
[[ -f "$BOOK/book.json" ]] || { echo "error: no such book: $SLUG" >&2; exit 2; }

EDITION="$(python3 "$META" get "$SLUG" edition)"
SRC_REL="$(python3 "$META" get "$SLUG" canonical_source)"
SRC_NAME="$(basename "$SRC_REL")"
CANON_PDF="$(python3 "$META" get "$SLUG" release.canonical_pdf)"
PREFIX="${CANON_PDF%.pdf}"
ED_SHORT="$(echo "$EDITION" | cut -d. -f1,2)"
ZIP_NAME="${PREFIX}_Reproducibility_Package.zip"
RECEIPT_NAME="Publication_Build_Receipt_Edition_${ED_SHORT}.json"
FULLSRC_NAME="${PREFIX}_Full_Source"

for tool in pandoc xelatex gs pdftotext python3; do
  command -v "$tool" >/dev/null 2>&1 || { echo "error: '$tool' missing. Run scripts/setup-toolchain.sh" >&2; exit 3; }
done

echo "==> regenerating $SLUG edition $EDITION"
echo "    manuscript : $SRC_NAME"
echo "    assets     : $PREFIX.*"
mkdir -p "$BOOK/release" "$BOOK/build"

cd "$SRC_DIR"

echo "--> 1/9 manuscript code blocks"
python3 extract_manuscript_code_blocks.py "$SRC_NAME" manuscript_code_blocks.json

echo "--> 2/9 environment attestation and requirements"
python3 generate_environment_lock.py

echo "--> 3/9 canonical source manifest hashes"
python3 - "$SRC_NAME" <<'PY'
import hashlib, json, sys
from pathlib import Path
src = sys.argv[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
p = Path('canonical_source_manifest.json')
m = json.loads(p.read_text())
m['source_filename'] = src
m['source_sha256'] = sha(src)
m['extractor_sha256'] = sha(m['extractor_filename'])
m['code_block_manifest_sha256'] = sha(m['code_block_manifest_filename'])
p.write_text(json.dumps(m, indent=2) + '\n')
print(f"    source_sha256={m['source_sha256'][:16]}...")
PY

echo "--> 4/9 source checksums"
# Every file in source/ except the checksum file itself. Sorted for a deterministic result.
rm -f SHA256SUMS.txt
find . -maxdepth 1 -type f ! -name SHA256SUMS.txt -printf '%f\n' | LC_ALL=C sort \
  | xargs sha256sum > SHA256SUMS.txt
echo "    $(wc -l < SHA256SUMS.txt) files"

echo "--> 5/9 companion reproducibility package"
rm -f "$BOOK/release/$ZIP_NAME"
# Flat archive, members sorted, timestamps normalised so the same inputs give the same bytes.
python3 - "$BOOK/release/$ZIP_NAME" <<'PY'
import sys, zipfile
from pathlib import Path
out = Path(sys.argv[1])
members = sorted(p for p in Path('.').iterdir() if p.is_file())
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in members:
        info = zipfile.ZipInfo(p.name, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, p.read_bytes())
print(f"    {len(members)} members -> {out.name}")
PY

echo "--> 6/9 PDF (Pandoc + XeLaTeX, then attach and linearise)"
bash build_pdf.sh "$SRC_NAME" "$BOOK/release/$ZIP_NAME" "$BOOK/release/$CANON_PDF"

echo "--> 7/9 external build receipt"
python3 generate_build_receipt.py \
  "$BOOK/release/$CANON_PDF" "$BOOK/release/$ZIP_NAME" "$BOOK/release/$RECEIPT_NAME"

echo "--> 8/9 bundle manifest and full-source archive"
cd "$BOOK"
python3 - "$FULLSRC_NAME" "$EDITION" "$SRC_REL" <<'PY'
import hashlib, json, os, sys, zipfile
from pathlib import Path

bundle_name, edition, canonical_source = sys.argv[1], sys.argv[2], sys.argv[3]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

# Everything in the bundle except the manifest, the checksum file, and the archive we are about
# to create -- those three either describe the bundle or are derived from it.
skip_names = {'FULL_SOURCE_MANIFEST.json', 'SHA256SUMS.txt'}
files = []
for p in sorted(Path('.').rglob('*')):
    if not p.is_file():
        continue
    rel = p.relative_to('.').as_posix()
    if rel in skip_names or rel.endswith('_Full_Source.zip'):
        continue
    if '__pycache__' in rel or rel.startswith('build/'):
        continue
    files.append({
        'path': rel,
        'bytes': p.stat().st_size,
        'sha256': sha(p),
        'executable': bool(p.stat().st_mode & 0o111),
    })

release = {}
for entry in files:
    name = Path(entry['path']).name
    if entry['path'].startswith('release/'):
        if name.endswith('.pdf'):
            release['pdf'] = {'path': entry['path'], 'sha256': entry['sha256']}
        elif name.endswith('Reproducibility_Package.zip'):
            release['reproducibility_package'] = {'path': entry['path'], 'sha256': entry['sha256']}
        elif name.startswith('Publication_Build_Receipt'):
            release['build_receipt'] = {'path': entry['path'], 'sha256': entry['sha256']}

manifest = {
    'schema_version': 'production-agent-engineering/full-source-bundle/v1',
    'edition': edition,
    'bundle_name': bundle_name,
    'canonical_source': canonical_source,
    'build_entrypoint': 'build_pdf_from_bundle.sh',
    'verification_entrypoint': 'verify_release.sh',
    'release': release,
    'file_count_excluding_manifest_and_checksum': len(files),
    'files': files,
}
Path('FULL_SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f"    manifest: {len(files)} files, release keys {sorted(release)}")

# Bundle-level checksums, over every distributed file except the checksum file itself.
lines = [f"{e['sha256']}  {e['path']}" for e in files]
lines.append(f"{sha(Path('FULL_SOURCE_MANIFEST.json'))}  FULL_SOURCE_MANIFEST.json")
lines.sort(key=lambda line: line.split('  ', 1)[1])
Path('SHA256SUMS.txt').write_text('\n'.join(lines) + '\n')
print(f"    SHA256SUMS.txt: {len(lines)} entries")

# Full-source archive, mirroring the bundle under a single top-level directory.
zip_path = Path(f'{bundle_name}.zip')
zip_path.unlink(missing_ok=True)
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for rel in ['FULL_SOURCE_MANIFEST.json', 'SHA256SUMS.txt'] + [e['path'] for e in files]:
        info = zipfile.ZipInfo(f'{bundle_name}/{rel}', date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, Path(rel).read_bytes())
    for d in ('build/', 'release/'):
        z.writestr(zipfile.ZipInfo(f'{bundle_name}/{d}', date_time=(2026, 1, 1, 0, 0, 0)), b'')
print(f"    {zip_path.name}")
PY

# The archive is itself a distributed file, so it belongs in the bundle checksums.
sha256sum "$FULLSRC_NAME.zip" | sed "s| .*| $FULLSRC_NAME.zip|" >> SHA256SUMS.txt
LC_ALL=C sort -k2 -o SHA256SUMS.txt SHA256SUMS.txt

echo "--> 9/9 verification gate"
cd "$REPO"
bash scripts/verify-book.sh "$SLUG"

echo
echo "==> edition $EDITION regenerated and verified"
