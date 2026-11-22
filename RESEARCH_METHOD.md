# Research standard: evidence before product recommendations

## Goal
Identify product-family × target-country × offer combinations suitable for a new brand with €1,000–€3,000 capital, no influencer network, and no professional ad production. No claim of a high probability of success without measured customer acquisition and unit economics.

## Funnel
1. **Problem discovery** across >=25 domains. News is a lead only, not demand proof. Avoid overfocusing on familiar gadgets.
2. **Demand triangulation:** dated marketplace listings, independently sourced customer reviews, query trends, repeat customer complaints, competing product availability, and, if obtainable, transaction/volume evidence. Review counts do not equal sales.
3. **Negative-review mining:** collect permitted review exports with original URLs, dates, languages, verified buyer flags, star ratings, and product-family identity. Deduplicate exact review IDs and repeated text. Separate delivery complaints from product failures. Count independent domains and countries. Translate with language metadata, retaining originals. Do not manufacture reviews.
4. **Gap identification:** recurring functional complaints + evidence of paid alternatives + plausible manufacturable fix; distinguish problems solvable by packaging/instructions from true product redesign.
5. **Marketability:** assess faceless demo feasibility, value proposition clarity, content rights, trust barriers, branded differentiation, customer search intent, seasonality, substitutes and channel suitability.
6. **Unit economics:** calculate net-of-VAT selling price, landed cost, EU fulfillment, returns, processing fees, shipping, expected refunds, and break-even CAC. Model country × single/bundle/premium. Do not invent supplier quotations, conversion rates, CAC, or demand.
7. **Compliance veto:** GPSR, REACH, category-specific CE obligations if applicable, packaging EPR, importer/responsible-person duties, safety recalls, claims. Unknown = pending legal review.
8. **Validation:** 60 checks with proof URL, observation date, confidence and status (met/not met/unknown). Only observed positive evidence scores. Reject unsafe/non-compliant and negative unit-economics candidates.
9. **Small-budget market tests:** interview customers, request supplier samples and quotes, test landing pages and price acceptance, measure real CAC and returns before stock commitments.
10. **Outputs:** 2,000 unique product families discovery goal; shortlist 100, 20 deep studies, top 3 only after evidence supports. Maintain checkpoints and do not inflate counts.

## References
- Harvard Business School Jobs-to-be-Done: https://online.hbs.edu/blog/post/jobs-to-be-done-examples
- Baymard customer review research: https://baymard.com/research-articles/respond-to-negative-user-reviews
- Northwestern Spiegel Research Center: https://spiegel.medill.northwestern.edu/how-online-reviews-influence-sales/
- EU Safety Gate: https://ec.europa.eu/safety-gate/screen/pages/obligationsForBusinesses

## Limits
GitHub Actions scheduled workflows are best-effort, not guaranteed at exact intervals. The free crawler currently captures news search results, NOT actual marketplace reviews, sales data or validated products. The review-analysis module accepts permissioned JSONL exports; source integrations are not configured. No paid API keys or prohibited scraping are presumed.
