"""60 explicit research checks. Unknown is never a pass.
Research criteria are screening tools, not guarantees of commercial success.
"""
from dataclasses import dataclass
from typing import Optional
GROUPS={
"demand":[
"documented_customer_problem","multiple_independent_demand_sources","dated_marketplace_listings","search_intent","repeat_complaints","cross_country_demand","seasonality_understood","demand_not_only_viral","paid_alternatives","recent_demand_evidence","customer_segment_defined","problem_frequency"],
"post_ad_profit":[
"vat_country_modeled","selling_price_observed","supplier_quote","landed_cost","fulfillment_quote","payment_fees","returns_allowance","break_even_cac","bundle_margin","premium_offer_margin","cash_conversion_cycle","minimum_order_affordable"],
"advertising":[
"visual_demo_possible","clear_value_proposition","faceless_content_possible","creative_rights","targeting_channel","search_purchase_intent","ad_policy_compliance","trust_barriers_manageable"],
"competition":[
"competitor_count_observed","competitor_prices_observed","negative_reviews_analyzed","differentiation_defensible","brand_positioning_clear","market_not_pure_commodity"],
"logistics":[
"package_dimensions","weight_confirmed","damage_risk_low","returns_manageable","eu_shipping_cost","delivery_expectation"],
"repeat_scale":[
"upsell_or_bundle","repeat_purchase_reason","brand_extension","multi_country_fit","customer_service_load","stock_replenishment","long_term_demand","nonseasonal_or_planned"],
"sourcing":[
"supplier_identity_verified","sample_available","quality_control_plan","product_safety_review","importer_duties_checked","packaging_epr_checked","moq_within_budget","lead_time_confirmed"],
}
assert sum(map(len,GROUPS.values()))==60
WEIGHTS={"demand":25,"post_ad_profit":25,"advertising":15,"competition":10,"logistics":10,"repeat_scale":10,"sourcing":5}
@dataclass
class Check:
    status:str="unknown"
    source_url:str=""
    observed_at:str=""
    confidence:str="unknown"
    note:str=""
def assess(checks,hard_veto=None):
    hard_veto=hard_veto or {}
    veto=[k for k in ("unsafe_or_illegal","negative_contribution","unverifiable_supplier") if hard_veto.get(k) is True]
    score=0.;unknown=[];failed=[];verified=[]
    for group,names in GROUPS.items():
        positives=0
        for name in names:
            key=group+"."+name
            raw=checks.get(key,{})
            if isinstance(raw,Check):r=raw.__dict__
            else:r=raw if isinstance(raw,dict) else {}
            if r.get("status")=="met" and r.get("source_url","").startswith("https://") and r.get("observed_at"):
                positives+=1
                verified.append(key)
            elif r.get("status")=="not_met":failed.append(key)
            else:unknown.append(key)
        score+=WEIGHTS[group]*positives/len(names)
    return {"status":"rejected" if veto else ("pending" if unknown else "assessed"),"score":0 if veto else round(score,2),"veto":veto,"unknown":unknown,"not_met":failed,"criteria_total":60,"criteria_verified":len(verified),"criteria_failed":len(failed),"criteria_unknown":len(unknown),"eligible_for_winner":not veto and not unknown and not failed and len(verified)==60}
