# Agentic QA

**Tier B** · Edition 1.0.0 · [CC-BY-4.0](../../LICENSE) prose, [Apache-2.0](../../LICENSES/Apache-2.0.txt) code

A short guide for engineers who ship with coding agents and want fewer of the agents' bugs to reach production. It explains why agents over-produce code and tests and why their own green results are weak evidence, then gives a procedure for locating the truth boundary, measuring what a passing test is worth, and choosing among six ways to verify at volume — from requirement-first unit QA and generator/verifier splits to mutation-guided generation and triangulated browser campaigns. Every rule is derived from how the models are trained and sampled and from the arithmetic of verification, and every number is cited.

## Download

Published editions are on the [releases page](https://github.com/ankitkpandey1/handbooks/releases).
Stable links, always newest edition:

| Format | Link | For |
|---|---|---|
| PDF | [`agentic-qa.pdf`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agentic-qa.pdf) | reading |
| EPUB | [`agentic-qa.epub`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agentic-qa.epub) | e-readers |
| HTML | [`agentic-qa.html`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agentic-qa.html) | the web |
| Markdown | [`agentic-qa.md`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/agentic-qa.md) | agents and LLMs |

## Assurance

**Tier B**: manuscript plus metadata, structurally linted and built to four formats by CI.
This book does not carry the source-contract manifests, reproducibility package or verifier
suite of a Tier A handbook — see [the repo README](../../README.md#what-tier-means) for what
the tiers mean.

Release assets still carry signed build provenance:

```bash
gh attestation verify agentic-qa.pdf --repo ankitkpandey1/handbooks
```

## Build it yourself

```bash
scripts/setup-toolchain.sh
scripts/build-book.sh agentic-qa
```

## Contributing

Errata and claim challenges welcome — see [CONTRIBUTING.md](../../CONTRIBUTING.md).
