# Real review and marketplace evidence imports

The free news collector produces problem signals only. To evaluate products, import **authorized** marketplace listings to `data/product_candidates.jsonl` and review exports to `data/reviews_import.jsonl`.

Product JSONL example (illustrative schema, NOT a real product):
`{"product_family":"EXAMPLE FAMILY","country":"DE","source_url":"https://example.org/item","observed_at":"2026-11-23","evidence_type":"marketplace_listing"}`

Review JSONL example (illustrative schema, NOT a real review):
`{"product_family":"EXAMPLE FAMILY","country":"DE","review_id":"EXAMPLE","source_url":"https://example.org/review","observed_at":"2026-11-23","text":"Example complaint","verified_buyer":false}`

Never commit private personal data, copied protected review corpora, or API keys. Only use APIs/exports permitted by the source's terms. The pipeline never treats number of listings or reviews as proven sales. Run `python opportunity_pipeline.py`. It writes an evidence-only queue with all 60 criteria unknown until independently checked.
