"""Strict provenance registry: evidence is not proof of a sale.
Only import authorized records. Prevent unverifiable self-asserted claims.
"""
import datetime as dt
import json
from pathlib import Path
from urllib.parse import urlsplit

REQUIRED=("product_family","country","criterion","status","source_url","observed_at","evidence_type")
STATUSES={"met","not_met","unknown"}
def validate(item,now=None):
    now=now or dt.datetime.now(dt.timezone.utc)
    errors=[f"missing_{k}" for k in REQUIRED if not item.get(k)]
    if errors:return errors
    url=urlsplit(str(item["source_url"]))
    if url.scheme!="https" or not url.hostname:errors.append("invalid_source_url")
    if item["status"] not in STATUSES:errors.append("invalid_status")
    try:
        date=dt.datetime.fromisoformat(str(item["observed_at"]).replace("Z","+00:00"))
        if date.tzinfo is None:errors.append("timezone_required")
        elif date>now+dt.timedelta(days=1):errors.append("future_evidence")
    except ValueError:errors.append("invalid_observation_date")
    from criteria import GROUPS
    allowed={g+"."+c for g,items in GROUPS.items() for c in items}
    if item["criterion"] not in allowed:errors.append("unknown_criterion")
    if item["status"]=="met" and not item.get("evidence_note"):
        errors.append("missing_positive_evidence_explanation")
    return errors
def compile_assessments(rows):
    by_key={};rejected=[]
    for i,item in enumerate(rows):
        errors=validate(item)
        if errors:
            rejected.append({"row":i,"errors":errors});continue
        key=(str(item["product_family"]).casefold().strip(),str(item["country"]).upper())
        entry=by_key.setdefault(key,{"product_family":item["product_family"],"country":str(item["country"]).upper(),"checks":{}})
        check={"status":item["status"],"source_url":item["source_url"],"observed_at":item["observed_at"],"confidence":item.get("confidence","unknown"),"note":item.get("evidence_note","")}
        # If multiple records exist, conflicting conclusions must be manually reconciled.
        prior=entry["checks"].get(item["criterion"])
        if prior and prior["status"]!=check["status"]:
            entry["checks"][item["criterion"]]={"status":"unknown","note":"conflicting evidence requires review"}
        elif not prior:entry["checks"][item["criterion"]]=check
    return list(by_key.values()),rejected
def main():
    path=Path("data/criterion_evidence.jsonl")
    rows=[]
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:rows.append(json.loads(line))
                except json.JSONDecodeError:rows.append({})
    records,rejected=compile_assessments(rows)
    output=Path("data/assessments.jsonl")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text("".join(json.dumps(r,ensure_ascii=False)+"\n" for r in records),encoding="utf-8")
    Path("data/evidence_rejections.json").write_text(json.dumps(rejected,indent=2),encoding="utf-8")
    print(json.dumps({"assessment_records":len(records),"rejected_evidence":len(rejected),"source_rows":len(rows)}))
if __name__=="__main__":main()
