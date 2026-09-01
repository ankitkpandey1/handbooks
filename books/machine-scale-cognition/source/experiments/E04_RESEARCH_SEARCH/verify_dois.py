# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib
import re
import urllib.parse
import urllib.request

root = pathlib.Path(__file__).parent
for condition in ("b1", "s"):
    text = (root / "output" / f"{condition}.md").read_text()
    values = sorted({x.rstrip(".,;:)]").lower() for x in re.findall(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", text)})
    for doi in values:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
        req = urllib.request.Request(url, headers={"User-Agent": "ai-super-reconstruction/1.0 (mailto:research@example.com)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                status = response.status
                payload = json.load(response)
                final = payload.get("message", {}).get("URL", response.url)
        except Exception as exc:
            status = getattr(exc, "code", None)
            final = str(exc)
        print(json.dumps({"condition": condition, "doi": doi, "status": status, "crossref_record": bool(status and status < 400), "target": final}))
