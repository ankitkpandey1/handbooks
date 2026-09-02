# One Expert, Machine-Scale Cognition

**Tier B** · Edition 3.0.0 · [CC-BY-4.0](../../LICENSE) prose, [Apache-2.0](../../LICENSES/Apache-2.0.txt) code

> An evidence-bounded field guide for experts using language models to expand checked search,
> computation and comparison. It teaches how to diagnose the binding constraint, design a
> selector before scaling, compress work into a responsible decision and stop when more AI
> work would create review debt rather than value.

## Download

Published editions are on the [releases page](https://github.com/ankitkpandey1/handbooks/releases).
Stable links, always newest edition:

| Format | Link | For |
|---|---|---|
| PDF | [`machine-scale-cognition.pdf`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/machine-scale-cognition.pdf) | reading |
| EPUB | [`machine-scale-cognition.epub`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/machine-scale-cognition.epub) | e-readers |
| HTML | [`machine-scale-cognition.html`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/machine-scale-cognition.html) | the web |
| Markdown | [`machine-scale-cognition.md`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/machine-scale-cognition.md) | agents and LLMs |

## Assurance

**Tier B**: manuscript plus metadata, structurally linted and built to four formats by CI.
This book does not carry the source-contract manifests, reproducibility package or verifier
suite of a Tier A handbook — see [the repo README](../../README.md#what-tier-means) for what
the tiers mean.

The bundled E01–E10 artifacts have a local content checker. It verifies the experiment
counts and retained scorer outputs cited by the manuscript; it does not bind release files
to source or establish real-world productivity.

Release assets still carry signed build provenance:

```bash
gh attestation verify machine-scale-cognition.pdf --repo ankitkpandey1/handbooks
```

## Build it yourself

```bash
scripts/setup-toolchain.sh
scripts/build-book.sh machine-scale-cognition
books/machine-scale-cognition/verify_experiments.sh
```

## Contributing

Errata and claim challenges welcome — see [CONTRIBUTING.md](../../CONTRIBUTING.md).
