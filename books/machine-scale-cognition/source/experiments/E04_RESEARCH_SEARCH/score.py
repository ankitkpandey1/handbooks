# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib
import re

root = pathlib.Path(__file__).parent
corpus = json.loads((root / "output/corpus.json").read_text())
known = {r["doi"].lower().removeprefix("https://doi.org/") for r in corpus["records"] if r["doi"]}

def dois(text):
    found = re.findall(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", text)
    return {x.rstrip(".,;:)]").lower() for x in found}

for condition in ("b1", "s"):
    text = (root / "output" / f"{condition}.md").read_text()
    cited = dois(text)
    print(json.dumps({
        "condition": condition,
        "word_count": len(text.split()),
        "unique_dois": len(cited),
        "dois_in_frozen_corpus": len(cited & known),
        "dois_outside_frozen_corpus": sorted(cited - known),
        "mentions_falsifier": "falsif" in text.lower(),
        "mentions_boundary": "boundary" in text.lower() or "cannot" in text.lower(),
    }, sort_keys=True))
