# Production Agent Engineering - Edition 1.7 full source bundle

This archive contains the complete materials supplied for building, inspecting, and validating Edition 1.8.0.

## Directory layout

- `source/` - canonical Markdown, Pandoc/XeLaTeX build configuration, PDF post-processing code, evaluation data, source-contract manifests, and all publication verifiers.
- `release/` - the published PDF, the exact companion archive embedded in the PDF, and the external publication build receipt.
- `build/` - default destination for a locally rebuilt PDF. It is intentionally empty in the distributed archive.
- `build_pdf_from_bundle.sh` - one-command local build wrapper.
- `verify_release.sh` - one-command verification wrapper for the supplied release artefacts.
- `FULL_SOURCE_MANIFEST.json` - machine-readable bundle inventory and release hashes.
- `SHA256SUMS.txt` - SHA-256 for every distributed file except the checksum file itself.

## Build the PDF

Required system tools:

- Pandoc 3.1.11.1 or a compatible release;
- XeLaTeX / XeTeX with the LaTeX packages used by Pandoc's generated document;
- Python 3.13 or a compatible release;
- Python dependencies pinned in `source/requirements.txt`.

Run:

```bash
bash build_pdf_from_bundle.sh
```

The default output is:

```text
build/Production_Agent_Engineering_Edition_1.8.pdf
```

To choose another path:

```bash
bash build_pdf_from_bundle.sh /absolute/path/to/output.pdf
```

The build performs two stages:

1. Pandoc converts the canonical Markdown using `source/pandoc_defaults.yaml` and XeLaTeX.
2. `source/attach_and_linearize_pdf.py` embeds the exact companion archive and linearises the final PDF.

The exact publication command recorded by the release receipt is:

```bash
bash build_pdf.sh production_agent_engineering_edition_1_8.md Production_Agent_Engineering_Edition_1.8_Reproducibility_Package.zip Production_Agent_Engineering_Edition_1.8.pdf
```

## Verify the supplied release

Run all offline checks:

```bash
bash verify_release.sh
```

This uses `manifest-only` source-contract verification and then checks release metadata, manuscript examples, companion references, section numbering, edition history, deferred-approval application contracts, synthetic evaluation reproduction, PDF text extraction, source-to-PDF binding, navigation, embedded-archive identity, build-receipt fields, Python syntax, and member checksums.

To fetch pinned upstream sources and recompute Git blob SHA-1 values:

```bash
bash verify_release.sh online
```

Online verification requires network access to the pinned GitHub source URLs.

## Reproducibility boundary

`source/environment_attestation.json` records the observed build environment, installed-tree hashes, and build-binary hashes. It is an environment attestation, not a reconstructive wheel lock, OCI image digest, or Nix/Guix closure. A byte-identical PDF is therefore not guaranteed on a different platform or dependency closure. The release checks instead validate the canonical source, build inputs, text/navigation properties, embedded archive, and external receipt.

The PDF is searchable and its navigation has been validated, but it is not tagged and is not PDF/UA certified.
