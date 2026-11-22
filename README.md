# EU Product Research

Independent evidence-first research project. Does not access or modify DalamanWay.

Research specification: 2,000 unique candidate product families across 25+ problem domains and European markets; 60 criteria with explicit unknowns; no invented sales, CAC or profitability.

## Status
Repository scaffold only. Live data collection is NOT deployed. Approved product-level feeds and a persistent database are needed before any product counts can be verified.

Run `python -m unittest discover -v` and `python engine.py status`. `python engine.py run` checks only explicitly enabled and permission-confirmed sources. Do not count fetched pages as products.

See `render.yaml` for an isolated deployment proposal. Review pricing before creating resources.