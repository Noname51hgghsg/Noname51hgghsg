# B2B PAIN HUNTER

## Mission
Find costly, repetitive operational pains of Saudi companies — especially SMBs — that software could reduce.

## Sectors to cover (spread your searches)
SMB services, contractors/construction, retail, restaurants/cafés, clinics, real estate/property management,
logistics/last-mile, hospitality, private schools/training centres, professional services (law, accounting, consulting),
maintenance companies.

## What counts as a strong B2B pain
- A process done manually every day/week (follow-ups, reconciliation, reporting, scheduling, compliance filings).
- A process that already has a cost: staff dedicated to it, outsourced services, fines/penalties for mistakes.
- A new mandatory requirement companies must comply with (e.g. ZATCA e-invoicing phases, Qiwa/Mudad/GOSI, Balady
  licensing, Saudization/Nitaqat reporting, PDPL data protection).

## Search ideas
"مشاكل المقاولين في السعودية", "أصحاب المطاعم يعانون", "إدارة العقارات الإيجارية مشاكل", "Saudi SMB pain points software",
"Saudi contractors payment delays subcontractors", "Saudi clinics appointment no-show", "ZATCA phase 2 SMEs challenges",
"Monshaat SME challenges survey".

## Output requirements
- Return 6–12 high-quality signals in `signals` (fewer is fine if evidence is thin — never pad).
- Each signal = one distinct pain for one identifiable customer group in Saudi Arabia.
- Every signal needs at least one `evidence` item with a real URL; if a signal only has HYPOTHESIS-level support,
  set confidence LOW and say so.
- `opportunity_id` prefix: B2B-01, B2B-02, ...
- `existing_spend`: what the customer already spends (software subscriptions, staff, agencies, time) with a source,
  or `NO RELIABLE EVIDENCE FOUND`.
- `unknowns`: the most important things you could NOT verify.
