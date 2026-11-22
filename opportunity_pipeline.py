"""Turn permissioned product/review evidence into auditable research queues.
This is a triage pipeline, NOT a sales forecast.
"""
import argparse,json,re,unicodedata
from pathlib import Path
from urllib.parse import urlsplit
from criteria import assess

def normalize(value):
    return re.sub(r"[^\\w]+"," ",unicodedata.normalize("NFKC",str(value)).casefold(),flags=re.UNICODE).strip()
def valid_https(url):
    u=urlsplit(str(url))
    return u.scheme=="https" and bool(u.netloc)
def read_jsonl(path):
    if not Path(path).exists():return []
    out=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                value=json.loads(line)
                if isinstance(value,dict):out.append(value)
            except json.JSONDecodeError:pass
    return out
def process(products,reviews,assessments=None):
    assessments=assessments or []
    assessment_map={}
    for record in assessments:
        key=(normalize(record.get("product_family","")),str(record.get("country","")).upper())
        if key[0] and key[1]:assessment_map[key]=record
    families={}
    errors=[]
    for i,p in enumerate(products):
        family=normalize(p.get("product_family",""))
        country=str(p.get("country","")).upper()
        url=p.get("source_url","")
        if not family or not country or not valid_https(url) or not p.get("observed_at"):
            errors.append({"type":"invalid_product_evidence","row":i});continue
        key=(family,country)
        entry=families.setdefault(key,{"product_family":p["product_family"],"country":country,"listing_sources":set(),"listing_records":0,"reviews":[],"complaints":{},"demand_confirmed":False,"sales_confirmed":False})
        entry["listing_sources"].add(urlsplit(url).netloc)
        entry["listing_records"]+=1
    seen_reviews=set()
    for i,r in enumerate(reviews):
        family=normalize(r.get("product_family",""))
        country=str(r.get("country","")).upper()
        url=r.get("source_url","")
        review_id=str(r.get("review_id",""))
        if not family or not country or not review_id or not valid_https(url) or not r.get("observed_at") or not r.get("text"):
            errors.append({"type":"invalid_review_evidence","row":i});continue
        identity=(url,review_id)
        if identity in seen_reviews:continue
        seen_reviews.add(identity)
        key=(family,country)
        if key not in families:continue
        families[key]["reviews"].append(r)
    from review_analysis import analyze
    output=[]
    for entry in families.values():
        clusters=analyze(entry["reviews"])["issue_clusters"]
        entry["complaints"]={c["issue"]:c["distinct_reviews"] for c in clusters}
        entry["distinct_review_count"]=len(entry["reviews"])
        entry["independent_listing_domains"]=len(entry["listing_sources"])
        entry["listing_sources"]=sorted(entry["listing_sources"])
        entry["reviews"]=[]
        # Do not promote review volume or listing presence to confirmed demand.
        entry["research_stage"]="review_evidence_present" if entry["distinct_review_count"] else "listing_evidence_only"
        a=assessment_map.get((normalize(entry["product_family"]),entry["country"]),{})
        entry["criteria"]=assess(a.get("checks",{}),a.get("hard_veto",{}))
        output.append(entry)
    output.sort(key=lambda e:(-e["distinct_review_count"],-e["independent_listing_domains"],e["product_family"]))
    return {"candidates":output,"errors":errors,"unique_product_country_pairs":len(output),"demand_verified":0,"sales_verified":0}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--products",default="data/product_candidates.jsonl")
    parser.add_argument("--reviews",default="data/reviews_import.jsonl")
    parser.add_argument("--output",default="data/opportunity_queue.json")
    parser.add_argument("--assessments",default="data/assessments.jsonl")
    a=parser.parse_args()
    result=process(read_jsonl(a.products),read_jsonl(a.reviews),read_jsonl(a.assessments))
    target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"candidates":len(result["candidates"]),"errors":len(result["errors"]),"verified_sales":0}))
if __name__=="__main__":main()
