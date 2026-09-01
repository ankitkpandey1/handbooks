# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import sys
import time
import urllib.parse
import urllib.request

QUERIES = [
    "solid electrolyte conductivity degradation cycling mechanism",
    "solid state battery interfacial resistance cycling conductivity",
    "solid electrolyte dendrite space charge mechanical degradation",
    "solid electrolyte operando impedance spectroscopy cycling",
]

def abstract(inv):
    if not inv:
        return ""
    pairs = [(pos, word) for word, positions in inv.items() for pos in positions]
    return " ".join(word for _, word in sorted(pairs))

records = {}
for query in QUERIES:
    params = urllib.parse.urlencode({"search": query, "per-page": 50, "select": "id,doi,title,publication_year,cited_by_count,authorships,primary_location,abstract_inverted_index,topics"})
    url = "https://api.openalex.org/works?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "ai-super-reconstruction/1.0 (mailto:research@example.com)"})
    with urllib.request.urlopen(req, timeout=30) as response:
        payload = json.load(response)
    for work in payload["results"]:
        key = work.get("doi") or work["id"]
        item = records.setdefault(key, {
            "id": work["id"], "doi": work.get("doi"), "title": work["title"],
            "year": work.get("publication_year"), "cited_by": work.get("cited_by_count", 0),
            "authors": [a["author"]["display_name"] for a in work.get("authorships", [])[:8]],
            "landing_page": (work.get("primary_location") or {}).get("landing_page_url"),
            "abstract": abstract(work.get("abstract_inverted_index")),
            "topics": [t["display_name"] for t in work.get("topics", [])[:5]],
            "query_families": [],
        })
        item["query_families"].append(query)
    time.sleep(0.2)

out = {
    "retrieval_date": "2026-08-31",
    "queries": QUERIES,
    "unique_count": len(records),
    "records": sorted(records.values(), key=lambda x: (-x["cited_by"], x["title"])),
}
json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
