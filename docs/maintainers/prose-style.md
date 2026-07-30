<!--
SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
SPDX-License-Identifier: CC-BY-4.0
-->
# Prose style, and why not ASD-STE100

## What is enforced

[Vale](https://vale.sh/) with a local house style in [`styles/Handbooks/`](../../styles/Handbooks/).
Vale is markup-aware, which matters here: the manuscripts are roughly a third code, and a
linter that reads Python comments as prose is worse than none.

```bash
scripts/lint-prose.sh                 # every book
scripts/lint-prose.sh <slug>          # one book
scripts/lint-prose.sh <slug> --strict # any alert fails
scripts/verify-book.sh <slug> --prose # structural + prose in one pass
```

| Rule | Level | What it does |
|---|---|---|
| `Terminology` | warning | Blocks marketing register and imprecise substitutes for defined terms |
| `BritishEnglish` | warning | The manuscripts declare `lang: en-GB`; keeps spelling consistent |
| `UnlabelledClaims` | warning | Flags hedges that usually stand in for an evidence label |
| `Overclaiming` | error | Absolutes the repository cannot verify |
| `SentenceLength` | suggestion | Sentences over 45 words |
| `Procedures/SentenceLength` | warning | STE's 20-word cap, **procedural files only** |

Vale is optional and advisory. Errors fail `--strict` runs; on pull requests it reports into
the job summary and never blocks a merge. A style rule that can block a merge gets deleted; one
that informs gets used.

Structural and label checks are separate and *are* enforced — those live in
[`scripts/lint-book.py`](../../scripts/lint-book.py), which also verifies that every substantial
code block carries an authenticity label (currently 81/81 in `agents-handbook`).

## Why not ASD-STE100 conformance

[ASD-STE100](https://www.asd-ste100.org/) Simplified Technical English reached Issue 9 in
January 2025. It pairs 53 writing rules with a controlled dictionary of about 900 approved
words, each with one approved meaning and one part of speech. It is an excellent specification.
It is the wrong specification for most of this repository, for six reasons.

**1. Genre.** STE was developed by AECMA in the 1980s, at the request of the European airline
industry, for aircraft maintenance documentation, and is now used with S1000D. It optimises the
unambiguous execution of a procedure. These handbooks are expository argument: architecture
selection, agency budgets, competing alternatives, trade-offs.

**2. It cannot express calibrated uncertainty.** The books' evidence scheme — *Established*,
*Strong production evidence*, *Emerging evidence*, *Engineering hypothesis*, *Open question* —
is built on graded confidence. STE's rules push toward flat declaratives. An "Engineering
hypothesis" label needs precisely the hedged construction STE removes.

**3. The dictionary constrains the connective tissue, not the jargon.** This is the part usually
got wrong. STE explicitly permits Technical Names and Technical Verbs, so `harness`,
`idempotency` and `linearise` are all fine. The friction is one-approved-meaning-per-word on
general vocabulary — `since`, `as`, `follow`, `provide`, `support`, `consider`, `given` — which
is the machinery of argument.

**4. The sentence caps fragment reasoning.** STE caps procedural sentences at 20 words and
descriptive ones at 25. The manuscripts routinely carry 40–60 word sentences holding a single
conditional claim. Splitting those does not simplify: it fragments one claim into pieces whose
relationship the reader must then reconstruct. Correct for a procedure, harmful for an argument.

**5. No Vale implementation exists.** STE conformance tooling is commercial — Acrolinx,
HyperSTE, Congree, the Oxygen XML add-on. Adopting STE here would mean hand-authoring 53 rules
and ~900 dictionary entries as Vale YAML, and then maintaining them.

**6. Licensing.** The Part 2 dictionary is ASD copyright, distributed under ASD's own terms.
Redistributing it as YAML in a public CC-BY-4.0 repository is an unresolved question, not a
hypothetical one.

**And the reason that should settle it:** conformance could not be verified. This repository's
credibility rests on claiming only what it checks — that is what the tier system is for.
"Written in Simplified Technical English", backed by a hand-rolled partial style, would be
exactly the overclaim the architecture exists to prevent.

## What was taken from STE instead

The transferable core, which is genuinely valuable:

- **One term for one concept** → `Terminology.yml`. This is STE's most portable idea.
- **Sentence-length discipline** → `SentenceLength.yml`, at 45 words rather than 25.
- **Full STE caps for procedures** → `styles/Procedures/`, scoped in `.vale.ini` to
  `books/*/source/procedures/**`. This is where STE genuinely earns its keep: a runbook is read
  under time pressure by someone who did not write it. Put runbooks and step sequences there and
  they get the 20-word cap.
- **Domain vocabulary exemptions** → `styles/config/vocabularies/Handbooks/accept.txt`, which is
  STE's Technical Names idea. Add to it rather than weakening a rule.

## Measure a rule before adding it

Every rule here was measured against the existing 8,600-line manuscript first, and that changed
the design substantially:

| Candidate rule | Hits | Verdict |
|---|---|---|
| `prompt` → "task contract" | 98 | **Dropped.** The books define "prompt" as their own term; Part 5 is titled "prompt engineering" |
| `guardrail` → "invariant/policy/preference" | 56 | **Dropped.** "Guardrails" is a named field of the books' own pattern contract |
| STE 20-word cap on all prose | 247 | **Scoped to procedures only** |
| `clearly` as a hedge | 2 | **Dropped.** Both were "clearly labelled"/"clearly delimited" — adverbs on concrete actions. Vale uses RE2, which has no lookahead, so the uses cannot be separated by pattern |
| bare `fully reproducible` | 1 | **Narrowed** to the artifact claim. The synthetic evaluation genuinely does reproduce exactly |
| `chatbot` → "agent" | 1 | **Dropped.** Used correctly and contrastively |

After tuning: **0 errors, 0 warnings, 8 suggestions** across 181 published pages.

That is the standard to hold. A prose linter that fires 150 times on correct prose gets switched
off, and then it protects nothing. Precision beats coverage.

## Adding the Microsoft or Google styles later

Both are available as Vale packages and both are good. Introduce them **one rule at a time**,
not by adding `BasedOnStyles = Microsoft`, which on an existing manuscript produces thousands of
alerts in a single run and guarantees the tool gets abandoned.

```ini
# .vale.ini — the incremental way
Packages = Microsoft

[*.md]
BasedOnStyles = Handbooks
Microsoft.Contractions = NO
Microsoft.Passive = suggestion    # enable individually, measure, keep or drop
```

Note that adding `Packages` introduces a `vale sync` step and a network dependency in CI. The
house style is deliberately local so that CI cannot break because an upstream style changed.
