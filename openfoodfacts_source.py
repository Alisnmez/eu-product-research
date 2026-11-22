"""Fetch actual public product catalogue records from Open Food Facts.
Catalogue presence is NOT proof of sales, demand, margin or consumer reviews.
ODbL attribution/share-alike applies; keep this dataset separate from proprietary imports.
"""
import datetime as dt,json,os,time,urllib.parse,urllib.request
from pathlib import Path

BASE="https://world.openfoodfacts.org/api/v2/search"
CATEGORIES=("en:household-products","en:personal-care-products","en:pet-foods","en:beverages")
def extract(payload,observed_at):
    rows=[]
    for p in payload.get("products",[]):
        code=str(p.get("code") or "").strip()
        name=str(p.get("product_name") or "").strip()
        if not code or not name:continue
        countries=p.get("countries_tags") or []
        rows.append({"product_family":name,"country":"EU","source_url":"https://world.openfoodfacts.org/product/"+urllib.parse.quote(code,safe=""),"observed_at":observed_at,"evidence_type":"public_product_catalogue","catalogue":"Open Food Facts","barcode":code,"brand":str(p.get("brands") or ""),"categories_tags":p.get("categories_tags") or [],"countries_tags":countries,"sales_verified":False,"demand_verified":False,"price_verified":False,"license":"ODbL","attribution":"Open Food Facts contributors"})
    return rows
def fetch(category,limit=30):
    query=urllib.parse.urlencode({"categories_tags":category,"page_size":limit,"fields":"code,product_name,brands,categories_tags,countries_tags","json":1})
    request=urllib.request.Request(BASE+"?"+query,headers={"User-Agent":os.environ.get("OFF_USER_AGENT","EUOpportunityResearch/0.1 (contact: project GitHub issues)"),"Accept":"application/json"})
    with urllib.request.urlopen(request,timeout=25) as response:return json.load(response)
def main():
    path=Path("data/openfoodfacts_catalogue.jsonl")
    path.parent.mkdir(parents=True,exist_ok=True)
    seen=set();existing=[]
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                item=json.loads(line);code=item.get("barcode")
                if code and code not in seen:seen.add(code);existing.append(item)
            except (ValueError,TypeError):pass
    today=dt.datetime.now(dt.timezone.utc).isoformat()
    new=[];errors=[]
    for category in CATEGORIES:
        try:
            for row in extract(fetch(category),today):
                if row["barcode"] not in seen:seen.add(row["barcode"]);new.append(row)
        except Exception as exc:errors.append({"category":category,"error":type(exc).__name__})
        time.sleep(7) # respect documented 10 search requests/minute
    path.write_text("".join(json.dumps(row,ensure_ascii=False)+"\n" for row in existing+new),encoding="utf-8")
    Path("data/openfoodfacts_status.json").write_text(json.dumps({"existing":len(existing),"new":len(new),"total":len(existing)+len(new),"errors":errors,"source":BASE,"sales_verified":0,"demand_verified":0},indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"new_real_catalogue_records":len(new),"total":len(existing)+len(new),"errors":errors}))
if __name__=="__main__":main()
