"""Evidence-gated review analysis. Only reviews obtained lawfully from approved sources.
Review counts are not sales counts. No inferred revenue or CAC.
"""
import collections,datetime,json,re,unicodedata
from urllib.parse import urlparse

ISSUES={
"breaks_or_fails":r"broke|broken|stopped working|defect|faulty|kaputt|defekt|roto|cassé|uszkodzon",
"wrong_size_or_fit":r"too small|too big|does not fit|doesn't fit|zu klein|passt nicht|trop petit|nie pasuje",
"poor_material":r"cheap plastic|flimsy|poor quality|schlechte qualität|mauvaise qualité|mala calidad",
"hard_to_use":r"hard to use|difficult to use|complicated|schwierig|difficile|difícil",
"cleaning_problem":r"hard to clean|difficult to clean|schwer zu reinigen|difficile à nettoyer",
"leaks_or_spills":r"leak|leaking|spilled|undicht|fuite|gotea",
"misleading_claim":r"not as described|doesn't work as advertised|misleading|nicht wie beschrieben",
}
def analyze(reviews):
    seen=set();groups=collections.defaultdict(lambda:{"review_ids":[],"sources":set(),"countries":set(),"verified_buyers":0,"examples":[]})
    valid=0;rejected=0
    for r in reviews:
        required=("review_id","product_family","text","source_url","observed_at","country")
        if not all(r.get(k) for k in required) or urlparse(r.get("source_url","")).scheme not in ("https","http"):
            rejected+=1;continue
        key=(r["source_url"],r["review_id"])
        if key in seen:continue
        seen.add(key);valid+=1
        text=unicodedata.normalize("NFKC",r["text"]).lower()
        for issue,pattern in ISSUES.items():
            if not re.search(pattern,text,re.IGNORECASE):continue
            g=groups[(r["product_family"],issue)]
            g["review_ids"].append(r["review_id"])
            g["sources"].add(urlparse(r["source_url"]).netloc)
            g["countries"].add(r["country"])
            g["verified_buyers"]+=bool(r.get("verified_buyer",False))
            if len(g["examples"])<3:g["examples"].append({"review_id":r["review_id"],"url":r["source_url"],"excerpt":r["text"][:200]})
    results=[]
    for (family,issue),g in groups.items():
        results.append({"product_family":family,"issue":issue,"distinct_reviews":len(g["review_ids"]),"distinct_domains":len(g["sources"]),"countries":sorted(g["countries"]),"verified_buyers":g["verified_buyers"],"examples":g["examples"],"demand_verified":False,"sales_verified":False,"status":"review_complaint_signal_only"})
    return {"accepted_reviews":valid,"rejected_records":rejected,"issue_clusters":sorted(results,key=lambda x:-x["distinct_reviews"])}
def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument("input",help="JSONL from a permissioned review export");p.add_argument("--output",default="data/review_clusters.json");a=p.parse_args()
    with open(a.input,encoding="utf-8") as f:reviews=[json.loads(line) for line in f if line.strip()]
    result=analyze(reviews)
    from pathlib import Path
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"accepted_reviews":result["accepted_reviews"],"issue_clusters":len(result["issue_clusters"])}))
if __name__=="__main__":main()
