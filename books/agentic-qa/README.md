# Agentic QA

**Tier B** · Edition 2.0.0 · [CC-BY-4.0](../../LICENSE) prose, [Apache-2.0](../../LICENSES/Apache-2.0.txt) code

A practical handbook for engineers who ship with coding agents and want fewer of the agents' bugs to reach production. It shows why agents over-produce tests that cannot fail — mocking the very code under test — and gives the fixes as things you can run: an example repository (in `examples/`) with an agent-style suite and a real one, break-it-on-purpose and mutation scripts, rules to paste into CLAUDE.md, a reviewer prompt for a second agent, a method for agent-run UI campaigns, CI gates, and printable checklists. Every listing was executed; every number is cited.

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
