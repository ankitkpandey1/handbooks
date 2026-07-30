# __TITLE__

**Tier B** · Edition 0.1.0 · [CC-BY-4.0](../../LICENSE) prose, [Apache-2.0](../../LICENSES/Apache-2.0.txt) code

> One paragraph: what this book is, who it is for, and what a reader will be able to do after
> reading it. Replace this.

## Download

Published editions are on the [releases page](https://github.com/ankitkpandey1/handbooks/releases).
Stable links, always newest edition:

| Format | Link | For |
|---|---|---|
| PDF | [`__SLUG__.pdf`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/__SLUG__.pdf) | reading |
| EPUB | [`__SLUG__.epub`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/__SLUG__.epub) | e-readers |
| HTML | [`__SLUG__.html`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/__SLUG__.html) | the web |
| Markdown | [`__SLUG__.md`](https://github.com/ankitkpandey1/handbooks/releases/latest/download/__SLUG__.md) | agents and LLMs |

## Assurance

**Tier B**: manuscript plus metadata, structurally linted and built to four formats by CI.
This book does not carry the source-contract manifests, reproducibility package or verifier
suite of a Tier A handbook — see [the repo README](../../README.md#what-tier-means) for what
the tiers mean.

Release assets still carry signed build provenance:

```bash
gh attestation verify __SLUG__.pdf --repo ankitkpandey1/handbooks
```

## Build it yourself

```bash
scripts/setup-toolchain.sh
scripts/build-book.sh __SLUG__
```

## Contributing

Errata and claim challenges welcome — see [CONTRIBUTING.md](../../CONTRIBUTING.md).
