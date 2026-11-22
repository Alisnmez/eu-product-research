"""Fail visibly on stale runs and empty evidence; never mistake activity for success."""
import argparse,datetime as dt,json
from pathlib import Path

def check(root="data",now=None):
    root=Path(root)
    now=now or dt.datetime.now(dt.timezone.utc)
    state_path=root/"state.json"
    queue_path=root/"opportunity_queue.json"
    problems=[]
    state={}
    try:state=json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError,ValueError):problems.append("missing_or_invalid_state")
    try:
        last=dt.datetime.fromisoformat(state.get("last_run","").replace("Z","+00:00"))
        if last.tzinfo is None:raise ValueError("naive time")
        age=(now-last).total_seconds()/3600
        if age>3:problems.append("research_stale_over_3_hours")
        if age< -1:problems.append("future_timestamp")
    except ValueError:problems.append("missing_or_invalid_last_run")
    try:
        queue=json.loads(queue_path.read_text(encoding="utf-8"))
        count=len(queue["candidates"])
    except (OSError,ValueError,KeyError,TypeError):count=0;problems.append("missing_or_invalid_opportunity_queue")
    if count==0:problems.append("no_product_candidates")
    if state.get("last_errors"):problems.append("source_fetch_errors")
    return {"status":"healthy" if not problems else "needs_attention","issues":sorted(set(problems)),"runs":state.get("runs",0),"candidate_count":count,"last_run":state.get("last_run"),"note":"Healthy only means operational signals; never means commercially validated products."}
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--root",default="data");a=parser.parse_args()
    result=check(a.root)
    path=Path(a.root)/"HEALTH.md"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("# Research health\n\nStatus: **"+result["status"]+"**\n\nRuns: "+str(result["runs"])+"\n\nCandidate families/countries: "+str(result["candidate_count"])+"\n\nIssues: "+(", ".join(result["issues"]) or "none")+"\n\n"+result["note"]+"\n",encoding="utf-8")
    print(json.dumps(result))
if __name__=="__main__":main()
