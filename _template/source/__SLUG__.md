---
title: "__TITLE__"
subtitle: "One line that tells a reader whether this is for them"
author: "Ankit Kumar Pandey <itsankitkp@gmail.com>"
rights: "Copyright © __YEAR__ Ankit Kumar Pandey. Licensed under CC-BY-4.0."
version: "Edition 0.1.0"
date: "__DATE__"
lang: en-GB
subject: ""
keywords:
  - keyword
documentclass: scrartcl
classoption:
  - paper=a4
  - fontsize=11pt
  - titlepage=true
geometry: margin=0.9in
toc: true
toc-depth: 2
numbersections: false
colorlinks: true
linkcolor: NavyBlue
toccolor: NavyBlue
urlcolor: NavyBlue
mainfont: "Noto Serif"
sansfont: "Noto Sans"
monofont: "DejaVu Sans Mono"
header-includes:
  - |
    \usepackage{microtype}
    \usepackage{xurl}
    \usepackage{booktabs}
    \usepackage{longtable}
    \usepackage{xcolor}
    \definecolor{NavyBlue}{RGB}{18,52,86}
---

# Publication information

**Tier B.** This book is a manuscript plus metadata: it is structurally linted and built to
PDF, EPUB, HTML and single-file Markdown by CI. It does **not** carry the source-contract
manifests, reproducibility package or verifier suite of a Tier A handbook. Do not read it as
though it does.

## Scope and evidence labels

Every claim in this book carries one of these labels. If a claim has no label, treat it as
unverified and open an issue.

- **[measured]** — I ran it and observed this result. The setup is described well enough to
  repeat.
- **[documented]** — stated by primary vendor or project documentation. Cited.
- **[reported]** — stated by a secondary source. Cited, and treated as weaker.
- **[inferred]** — my reasoning from the above. Not observed directly.
- **[opinion]** — a judgement call. Argued, not asserted.

## Code authenticity labels

- **[executed]** — this exact listing was run.
- **[adapted]** — derived from code that was run, edited for the page.
- **[illustrative]** — never run. Shows shape, not behaviour.

## How to read this

Start with the executive summary. Each part stands alone; the parts are ordered by
dependency, not importance.

## Executive summary

Three to six paragraphs. What problem this addresses, what the reader will be able to do
afterwards, and what this book deliberately does not cover.

# Part 1 — __FIRST_PART__

## 1.1 Section

Prose. Keep claims labelled.

```python
# [illustrative]
def example() -> None:
    ...
```

# Edition history

- **0.1.0** (__DATE__) — first draft.
