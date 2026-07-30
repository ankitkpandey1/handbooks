#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import fitz
from pypdf import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument("pdf", type=Path)
parser.add_argument("archive", type=Path)
args = parser.parse_args()

reader = PdfReader(str(args.pdf))
attachments = reader.attachments
if args.archive.name not in attachments:
    raise SystemExit(f"embedded archive not found: {args.archive.name}")
items = attachments[args.archive.name]
if not isinstance(items, list):
    items = [items]
expected = hashlib.sha256(args.archive.read_bytes()).hexdigest()
if not any(hashlib.sha256(item).hexdigest() == expected for item in items):
    raise SystemExit("embedded archive bytes do not match external archive")

annotations: list[tuple[int, list[float], bool]] = []
for index, page in enumerate(reader.pages):
    for reference in page.get("/Annots", []):
        annotation = reference.get_object()
        if annotation.get("/Subtype") == "/FileAttachment":
            rect = [float(value) for value in annotation.get("/Rect", [])]
            media = [float(value) for value in page.mediabox]
            valid = (
                len(rect) == 4
                and rect[0] >= media[0]
                and rect[1] >= media[1]
                and rect[2] <= media[2]
                and rect[3] <= media[3]
                and rect[2] > rect[0]
                and rect[3] > rect[1]
            )
            annotations.append((index + 1, rect, valid))
if len(annotations) != 1 or not annotations[0][2]:
    raise SystemExit(f"expected one valid visible file annotation, found {annotations}")

page_number = annotations[0][0]
doc = fitz.open(args.pdf)
try:
    page = doc[page_number - 1]
    text = page.get_text()
    if not page.search_for("Companion reproducibility package"):
        raise SystemExit(f"attachment is not on the companion section page: {page_number}")
    if not (
        "This edition is distributed with and embeds" in text
        or "The archive contains the complete synthetic evaluation" in text
        or "The package verifies:" in text
    ):
        raise SystemExit(
            f"attachment is on a TOC/index occurrence, not the companion section body: {page_number}"
        )
finally:
    doc.close()

print(
    "OK: embedded archive matches SHA-256 and one visible in-page annotation "
    f"is beside the companion section on PDF page {page_number}"
)
