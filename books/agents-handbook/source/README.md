# Production Agent Engineering in 2026 - Edition 1.7.0 companion package

This archive is embedded in Edition 1.7.0 and distributed separately. It contains the canonical Markdown, deterministic code-block extraction, synthetic evaluation, deferred-approval application contract, source-contract manifest and receipt, environment attestation, exact PDF build/post-processing scripts, PDF text/navigation/binding verifiers, and member checksums.

Run the complete check with Bash; direct execution is also supported because executable mode is preserved in the release ZIP:

```bash
bash run_publication_checks.sh \
  /path/to/Production_Agent_Engineering_2026_Edition_1.7.pdf \
  /path/to/Production_Agent_Engineering_2026_Edition_1.7_Reproducibility_Package.zip \
  /path/to/Publication_Build_Receipt_Edition_1.7.json \
  manifest-only
```

Use `online` instead of `manifest-only` to fetch each pinned upstream source and recompute its Git blob SHA-1. `--require-content-sha256` is available on the source verifier and intentionally fails because expected raw-content SHA-256 values were not captured in this release. That remaining limitation is not reported as a pass.

## Closed publication chain

The package verifies:

```text
canonical Markdown SHA-256
-> deterministic code-block extraction
-> byte-identical code-block manifest
-> Pandoc/XeLaTeX build inputs
-> normalised source-to-PDF text coverage
-> bookmark and internal-link destinations
-> embedded archive byte identity
-> external receipt binding source, archive, and final PDF SHA-256
```

The build receipt is external by design: embedding a receipt containing the final PDF hash would alter that hash and create a circular dependency.

## Environment attestation

`environment_attestation.json` records the exact installed package versions, transitive dependencies, installed-tree SHA-256 values, and SHA-256 values of the build binaries. `requirements.txt` is a readable exact-version projection; This records the observed Linux x86-64 build environment. It is not a reconstructive wheel lock, OCI digest, Nix closure, or equivalent and must not be used as one.

## Deferred approval test boundary

`test_deferred_approval_application_contract.py` tests application hashing, expiry, revalidation, and duplicate suppression. It is not a credentialed Claude SDK defer/resume integration test.
