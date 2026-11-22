"""No-cost problem-signal discovery, not proof of product demand.
Uses public Google News RSS search feeds. No scraping marketplace pages.
"""
import datetime as dt
import hashlib
import json
import pathlib
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT=pathlib.Path("data")
ROOT.mkdir(exist_ok=True)
EVIDENCE=ROOT/"problem_signals.jsonl"
STATE=ROOT/"state.json"
CHECKPOINT=ROOT/"CHECKPOINT.md"
DOMAINS=[
("pet-care","pet owners frustrated product cleaning"),
("footwear","shoe repair complaints consumer"),
("laundry","laundry stains consumer problem"),
("travel","travel luggage passenger complaints"),
("cycling","cyclists recurring maintenance problems"),
("gardening","garden pests tools consumer problems"),
("craft","sewing repair tools frustration"),
("home-insulation","drafty windows energy bill problems"),
("car-care","car interior cleaning problems"),
("office","desk ergonomics home office pain"),
("bathroom","bathroom mold cleaning difficulties"),
("kitchen","food waste kitchen storage complaints"),
("outdoor","camping gear consumer complaints"),
("fitness","home fitness equipment frustration"),
("electronics-care","device cable wear repair complaints"),
("storage","small apartment storage problems"),
("pets-travel","pet travel safety comfort complaints"),
("textiles","clothing pilling repair complaints"),
("furniture","furniture scratches repair problems"),
("hobbies","hobby beginners tools frustrating"),
("sustainability","reusable products complaints durability"),
("seasonal","winter home maintenance problems"),
("beauty-tools","beauty tools cleaning frustrations"),
("mobility","commuter cycling rain complaints"),
("household-safety","household trip hazards prevention"),
("cleaning","hard to clean household surfaces"),
("parenting","parents stroller accessories complaints"),
("accessibility","daily living product usability complaints"),
]
def load_json(path,default):
    try:return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError,ValueError):return default
def collect():
    state=load_json(STATE,{"offset":0,"runs":0})
    seen=set()
    if EVIDENCE.exists():
        for line in EVIDENCE.read_text(encoding="utf-8").splitlines():
            try:seen.add(json.loads(line)["id"])
            except (ValueError,KeyError):pass
    today=dt.datetime.now(dt.timezone.utc).isoformat()
    new=[];errors=[];start=state["offset"]
    for j in range(5):
        category,query=DOMAINS[(start+j)%len(DOMAINS)]
        params=urllib.parse.urlencode({"q":query+" when:30d","hl":"en","gl":"DE","ceid":"DE:en"})
        url="https://news.google.com/rss/search?"+params
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"EUOpportunityResearch/1.0"})
            with urllib.request.urlopen(req,timeout=15) as response:
                xml=response.read(500000)
            root=ET.fromstring(xml)
            for item in root.findall(".//item")[:20]:
                title=item.findtext("title","").strip()
                link=item.findtext("link","").strip()
                published=item.findtext("pubDate","").strip()
                if not title or not link:continue
                identity=hashlib.sha256((title.lower()+"|"+link).encode()).hexdigest()
                if identity in seen:continue
                seen.add(identity)
                new.append({"id":identity,"category":category,"title":title,"source_url":link,"published":published,"observed_at":today,"evidence_type":"news_search_result","demand_confirmed":False,"product_family":None,"verified_product":False,"research_status":"unreviewed_problem_signal"})
        except Exception as exc:errors.append({"category":category,"error":type(exc).__name__})
    if new:
        with EVIDENCE.open("a",encoding="utf-8") as out:
            for row in new:out.write(json.dumps(row,ensure_ascii=False)+"\n")
    state={"offset":(start+5)%len(DOMAINS),"runs":state["runs"]+1,"last_run":today,"last_new_signals":len(new),"last_errors":errors}
    STATE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    CHECKPOINT.write_text("# EU Research Checkpoint\n\nLast run: "+today+"\n\nRuns: "+str(state["runs"])+"\n\nUnique unreviewed problem signals: "+str(len(seen))+"\n\nVerified product families: **0** (this pipeline does not validate products).\n\nLast new signals: "+str(len(new))+"\n\nErrors: "+json.dumps(errors)+"\n\nNews mentions are NOT evidence of demand, sales or profit. Requires human or authorized API validation.\n",encoding="utf-8")
    print(json.dumps({"runs":state["runs"],"new_problem_signals":len(new),"total_signals":len(seen),"errors":errors,"verified_products":0}))
if __name__=="__main__":collect()
