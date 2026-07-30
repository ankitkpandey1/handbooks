#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,datetime,subprocess
from pathlib import Path
import fitz
R=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser(); ap.add_argument('pdf',type=Path); ap.add_argument('archive',type=Path); ap.add_argument('output',type=Path); a=ap.parse_args()
cm=json.loads((R/'canonical_source_manifest.json').read_text()); src=R/cm['source_filename']; d=fitz.open(a.pdf)
inputs=['build_pdf.sh','attach_and_linearize_pdf.py','environment_attestation.json','requirements.txt','pandoc_defaults.yaml','verify_pdf_binding.py','verify_pdf_navigation.py','verify_pdf_text_layer.py']
r={'schema_version':'production-agent-engineering/publication-build-receipt/v2','edition':'1.8.0','generated_at':datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec='seconds'),'canonical_source':{'filename':src.name,'sha256':sha(src)},'reproducibility_archive':{'filename':a.archive.name,'sha256':sha(a.archive)},'final_pdf':{'filename':a.pdf.name,'sha256':sha(a.pdf),'pages':d.page_count,'bookmarks':len(d.get_toc(simple=True)),'links':sum(len(p.get_links()) for p in d),'linearized':bool(d.is_fast_webaccess)},'build_inputs':{n:sha(R/n) for n in inputs},'build_command':f'bash build_pdf.sh {src.name} {a.archive.name} {a.pdf.name}','tool_versions':{'pandoc':subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0],'xelatex':subprocess.check_output(['xelatex','--version'],text=True).splitlines()[0]},'attestation':{'type':'unsigned-local-build-receipt','signed':False,'note':'Cryptographic release signing requires an external immutable release mechanism.'},'circularity_boundary':'External receipt generated after final PDF; not embedded because embedding changes the PDF hash.'}
a.output.write_text(json.dumps(r,indent=2)+'\n'); print(a.output)
