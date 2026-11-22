"""Quality gates for evidence-first research. Zero invented products."""
from collections import Counter
from datetime import datetime,timezone
from urllib.parse import urlsplit
import json
from pathlib import Path

REQUIRED={"product_family","country","source_url","observed_at","evidence_type"}
def validate_record(row):
    missing=sorted(k for k in REQUIRED if not row.get(k))
    url=urlsplit(str(row.get("source_url","")))
    if url.scheme!="https" or not url.netloc:missing.append("valid_https_source_url")
    try:
        datetime.fromisoformat(str(row.get("observed_at","")).replace("Z","+00:00"))
    except ValueError:missing.append("valid_observation_date")
    return sorted(set(missing))
def audit(path="data/product_candidates.jsonl"):
    p=Path(path)
    if not p.exists():return {"total_records":0,"valid_evidence_records":0,"unique_product_families":0,"missing_source_records":0,"note":"No candidate dataset exists"}
    records=[];bad=0
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():continue
        try:
            row=json.loads(line)
            if not isinstance(row,dict) or validate_record(row):bad+=1;continue
            records.append(row)
        except (ValueError,TypeError):bad+=1
    families={(r["product_family"].strip().casefold(),r["country"].strip().upper()) for r in records}
    return {"total_records":len(records)+bad,"valid_evidence_records":len(records),"unique_family_country_pairs":len(families),"missing_source_records":bad,"note":"Valid records are NOT proof of sales, demand, or 60-criterion approval"}
if __name__=="__main__":print(json.dumps(audit(),ensure_ascii=False))
