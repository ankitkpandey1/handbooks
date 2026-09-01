# E09 Preregistration — Reproducibly Selected Held-Out Transfer

**Frozen before draw:** 2026-08-31
**Budget position:** experiment 9 of 10

The candidate tasks are stored in `candidates.json`. Selection computes SHA-256 of `docs/02_REQUIREMENTS.md`, converts the first 16 hexadecimal digits to an integer, and takes modulo candidate count. `select.py` prints the digest, index, and selected task. The draw happens only after these files exist.

B1 receives the selected ordinary request. S receives the same request plus the research-derived constraint/selector field card. One Luna call per condition. Assessment: differentiated first action, scalable workload, external selector, bounded human review, authority/stop boundary, and unsupported claims. This probes transfer only; it cannot validate the downstream domain outcome.
