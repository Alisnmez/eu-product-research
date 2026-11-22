"""Evidence-based opportunity scoring. Unknown is never a pass."""
from dataclasses import dataclass
from typing import Optional

WEIGHTS={"demand":25,"post_ad_profit":25,"advertising":15,"competition":10,"logistics":10,"repeat_scale":10,"sourcing":5}
BLOCKERS={"illegal_or_unsafe","negative_contribution","unverifiable_supplier"}
@dataclass
class Evidence:
    value:Optional[bool]
    url:str=""
    observed_at:str=""
    note:str=""
    confidence:str="unknown"
def evaluate(groups:dict,blockers:dict):
    """Each group contains criterion-name -> Evidence. Score only evidenced positives."""
    veto=[k for k in BLOCKERS if blockers.get(k) is True]
    if veto:return {"status":"rejected","veto":veto,"score":0}
    score=0.0;unknown=[]
    for group,weight in WEIGHTS.items():
        items=groups.get(group,{})
        if not items:unknown.append(group);continue
        confirmed=sum(1 for e in items.values() if e.value is True and e.url and e.observed_at)
        score+=weight*confirmed/len(items)
        unknown.extend(f"{group}.{k}" for k,e in items.items() if e.value is None or (e.value is True and not(e.url and e.observed_at)))
    return {"status":"needs_validation" if unknown else "scored","score":round(score,2),"unknown":unknown}
def unit_economics(price_incl_vat:float,vat_rate:float,landed_cost:float,fulfillment:float,returns_allowance:float,fees:float):
    if price_incl_vat<=0 or vat_rate<0 or min(landed_cost,fulfillment,returns_allowance,fees)<0:raise ValueError("Invalid inputs")
    net_revenue=price_incl_vat/(1+vat_rate)
    break_even_cac=net_revenue-landed_cost-fulfillment-returns_allowance-fees
    return {"net_revenue":round(net_revenue,2),"break_even_cac":round(break_even_cac,2),"viable_before_ads":break_even_cac>0}
