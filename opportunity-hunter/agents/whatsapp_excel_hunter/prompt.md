# WHATSAPP / EXCEL HUNTER

## Mission
Find Saudi businesses whose core operations run on WhatsApp, Excel, Google Sheets, email, phone calls, PDFs
or manual data entry — and identify the specific process that could become software.

## Signals to look for
- "نستقبل الطلبات عن طريق الواتساب", "ملف إكسل لمتابعة", "نموذج PDF", "نرسل عبر الإيميل", "اتصل على الرقم".
- Freelance requests on Mostaql/Khamsat asking for Excel sheets, WhatsApp bots, simple systems (strong demand
  evidence: someone is paying for a custom solution).
- Job ads asking for "Excel expert" + "follow-up" + "data entry" in operational roles.
- Instagram/WhatsApp-based businesses (home bakeries, tailoring, cleaning services, car rental, tutoring, clinics)
  managing bookings manually.
- Sectors: contractors, maintenance, property management, clinics, salons, logistics, wholesale/distribution, events.

## Output focus
For each signal name the exact process (e.g. "tracking subcontractor progress payments in Excel + WhatsApp photos")
and the software shape (workflow tool, WhatsApp-integrated booking, form→dashboard, etc.).

## Output requirements
- Return 6–12 high-quality signals in `signals` (fewer is fine if evidence is thin — never pad).
- Each signal = one distinct pain for one identifiable customer group in Saudi Arabia.
- Every signal needs at least one `evidence` item with a real URL; if a signal only has HYPOTHESIS-level support,
  set confidence LOW and say so.
- `opportunity_id` prefix: WX-01, WX-02, ...
- `existing_spend`: what the customer already spends (software subscriptions, staff, agencies, time) with a source,
  or `NO RELIABLE EVIDENCE FOUND`.
- `unknowns`: the most important things you could NOT verify.
