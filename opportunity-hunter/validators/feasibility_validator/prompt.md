# FEASIBILITY VALIDATOR

## Mission
For each candidate decide whether ONE person using Claude Code / Codex / APIs / cloud services can build a sellable
MVP, and estimate the cost.

## Define
- Stack: frontend, backend, database, authentication, AI, external APIs, hosting, payments (e.g. Moyasar, Tap,
  HyperPay, Stripe availability in KSA), integrations (WhatsApp Business API providers, ZATCA, etc.).
- `mvp_scope`: the smallest set of features a first customer would pay for.
- `mvp_cost_sar_low/high`: one-off cost to launch (domains, APIs, WhatsApp BSP fees, hosting, design assets) in SAR.
  Use real public prices where they matter (verify with search: e.g. WhatsApp Business API pricing, payment gateway fees);
  the founder's own time is not counted.
- `monthly_run_cost_sar` and `build_time_weeks` (solo, with AI coding tools).
- `complexity`: EASY (CRUD + 1–2 integrations, ≤4 weeks), MODERATE (several integrations / AI pipeline / marketplace
  cold-start, 4–10 weeks), HARD (regulated data, hardware, heavy integrations, licences, enterprise sales cycles).
- `regulatory`: licences/requirements (e.g. commercial registration, e-commerce law, PDPL, health data rules, SAMA),
  with URL where possible.
- `data_dependencies`: data you would need that may not be available (APIs without public access etc.).
- `blockers`: things that make it infeasible for a solo founder.
