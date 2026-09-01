# E04 Result

**Claim level:** `REPRODUCIBLE_INTERNAL` for retrieval/provenance counts; `ASSESSED_INTERNAL` for scientific synthesis
**Outcome boundary:** no experiment was performed and no mechanism was scientifically validated here

The scripted retrieval returned 164 unique DOI-bearing OpenAlex works across four query families; 130 included abstracts and 29 appeared through more than one query family.

B1 used two web searches in its normal agent turn. It produced six mechanism families, four DOI citations, and three strong discriminating experiments in 1,259 words. Crossref contains records for all four cited DOIs. This is a strong baseline, not a straw man.

S received the frozen corpus. It produced 25 unique citations, all present in that corpus, explicit mechanism/evidence/confounder/falsifier structures, boundary conditions, exactly three discriminating experiment cards, and a 12-paper human-review set in 2,151 words. Crossref confirmed 23 records; two requests were rate-limited (HTTP 429), while their OpenAlex DOI records remain in the frozen corpus.

## What changed

S increased auditable evidence coverage and compressed a 164-item retrieval into 12 priority papers. It explicitly distinguished title-only leads from abstract support and surfaced query leakage/dependence. B1 was more concise and scientifically useful than the old proposal assumed.

## Failures and limits

- The S response incorrectly said exact overlap counts could not be recomputed, although per-record query membership was supplied.
- Retrieval queries and corpus were authored for the case; recall against the full literature is unknown.
- DOI existence does not validate claim interpretation.
- No domain expert independently scored the mechanism synthesis.
- B1 had live web access while S had a fixed larger corpus; this intentionally tests workflow access, not pure prompting.

This satisfies an internal demonstration of machine-scale retrieval, provenance compression, and experiment discrimination. It does not establish a correct scientific conclusion or downstream outcome.
