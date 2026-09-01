# E04 Preregistration — Machine-Scale Scientific Search

**Frozen before corpus retrieval/model output:** 2026-08-31
**Budget position:** experiment 4 of 10
**Question:** What mechanisms explain conductivity loss during cycling in solid-state or solid-electrolyte battery systems, and which three experiments best discriminate leading mechanisms?

## Conditions

- B1: one Luna response from the ordinary question, no supplied corpus.
- S: reproducible OpenAlex retrieval capped at 200 works; query-family expansion; DOI/title deduplication; concept/mechanism extraction; contradiction search; evidence-family clustering; typed mechanism/prediction/experiment objects.

Both model conditions may use the normal Codex harness, but only S receives the frozen retrieved corpus. Tool use is recorded. This is a workflow-access treatment, not a pure model comparison.

## Primary measures

1. cited-source existence in the retrieved/API-verifiable record;
2. number of distinct evidence families with explicit provenance;
3. duplicated/dependent evidence identified;
4. concrete contradictory findings or boundary conditions;
5. experiments with mutually distinguishing predicted observations;
6. human review object size.

## Failure

S fails the required case if it only summarizes titles, cannot expose provenance, produces no discriminating predictions, or requires reading the 200-item corpus manually. This experiment does not validate the scientific mechanisms or downstream experiments.

**Scorer correction after output, before interpretation:** the first DOI regex retained Markdown `:` and `;` suffixes. `score.py` was corrected to strip them. Raw outputs were not changed; this researcher degree of freedom is disclosed.

**Verifier correction:** DOI.org HEAD requests followed redirects to publisher pages; 403 bot blocks were initially misclassified as nonexistent citations. Verification was changed to Crossref record lookup. The failed HEAD output remains in the command history but is superseded by the regenerated `doi_resolution.jsonl`.
