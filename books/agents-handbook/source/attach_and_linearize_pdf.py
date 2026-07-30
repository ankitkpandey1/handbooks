#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    TextStringObject,
)


def find_companion_heading(pdf: Path) -> tuple[int, fitz.Rect, float]:
    doc = fitz.open(pdf)
    try:
        candidates: list[tuple[int, fitz.Rect, float]] = []
        for index, page in enumerate(doc):
            text = page.get_text()
            body_marker = (
                "This edition is distributed with and embeds" in text
                or "The archive contains the complete synthetic evaluation" in text
                or "The package verifies:" in text
            )
            if not body_marker:
                continue
            for rect in page.search_for("Companion reproducibility package"):
                candidates.append((index, rect, page.rect.height))
        if len(candidates) != 1:
            raise SystemExit(
                f"expected one rendered companion-section heading outside the TOC, found {len(candidates)}"
            )
        return candidates[0]
    finally:
        doc.close()


def run_ghostscript(input_pdf: Path, output_pdf: Path) -> None:
    """Compress and normalise. Runs BEFORE attachment, never after.

    Ghostscript's pdfwrite device is a re-distiller, not a linearizer: it rebuilds the document
    and does not reliably carry /FileAttachment annotations across, even with -dPreserveAnnots
    (true by default in 10.x). Running it after attachment kept the embedded file stream but
    silently dropped the visible paperclip annotation, which verify_embedded_package.py requires.
    Linearisation is therefore done afterwards by qpdf, which rewrites the file structure without
    touching page content or annotations.
    """
    gs = shutil.which("gs")
    if not gs:
        raise SystemExit("Ghostscript is required for the final linearised PDF build")
    command = [
        gs,
        "-q",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.7",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dPreserveAnnots=true",
        f"-sOutputFile={output_pdf}",
        str(input_pdf),
    ]
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def run_qpdf_linearize(input_pdf: Path, output_pdf: Path) -> None:
    """Linearise for fast web view, preserving annotations and the embedded file tree."""
    qpdf = shutil.which("qpdf")
    if not qpdf:
        raise SystemExit("qpdf is required for the final linearised PDF build")
    subprocess.run(
        [qpdf, "--linearize", "--object-streams=generate", str(input_pdf), str(output_pdf)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()

    # Compress first, so Ghostscript never sees the attachment or its annotation.
    compressed = args.output_pdf.with_suffix(".compressed.tmp.pdf")
    run_ghostscript(args.input_pdf, compressed)

    page_index, rect, page_height = find_companion_heading(compressed)
    reader = PdfReader(str(compressed))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    archive_bytes = args.archive.read_bytes()
    archive_name = args.archive.name
    embedded = writer.add_attachment(archive_name, archive_bytes)
    embedded.description = TextStringObject(
        "Edition 1.7 reproducibility and publication-verification package"
    )
    filespec_ref = writer._add_object(embedded.pdf_object)

    # pypdf uses bottom-left PDF coordinates. Keep the paperclip beside the
    # rendered section heading and wholly inside the media box.
    media_right = float(reader.pages[page_index].mediabox.right)
    x = min(float(rect.x1) + 8.0, media_right - 28.0)
    y_top = float(rect.y0) + 2.0
    y = float(page_height) - y_top - 18.0
    annotation = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Annot"),
            NameObject("/Subtype"): NameObject("/FileAttachment"),
            NameObject("/Rect"): ArrayObject(
                [FloatObject(x), FloatObject(y), FloatObject(x + 18), FloatObject(y + 18)]
            ),
            NameObject("/FS"): filespec_ref,
            NameObject("/Name"): NameObject("/Paperclip"),
            NameObject("/Contents"): TextStringObject(f"Open {archive_name}"),
            NameObject("/T"): TextStringObject("Companion reproducibility package"),
            NameObject("/F"): FloatObject(4),
        }
    )
    annotation_ref = writer._add_object(annotation)
    page = writer.pages[page_index]
    if "/Annots" not in page:
        page[NameObject("/Annots")] = ArrayObject()
    page["/Annots"].append(annotation_ref)
    writer._root_object[NameObject("/AF")] = ArrayObject([filespec_ref])

    attached = args.output_pdf.with_suffix(".attached.tmp.pdf")
    linearised = args.output_pdf.with_suffix(".linear.tmp.pdf")
    try:
        with attached.open("wb") as stream:
            writer.write(stream)
        run_qpdf_linearize(attached, linearised)
        linearised.replace(args.output_pdf)
    finally:
        attached.unlink(missing_ok=True)
        linearised.unlink(missing_ok=True)
        compressed.unlink(missing_ok=True)

    digest = hashlib.sha256(archive_bytes).hexdigest()
    print(f"embedded {archive_name} sha256={digest} on PDF page {page_index + 1}")


if __name__ == "__main__":
    main()
