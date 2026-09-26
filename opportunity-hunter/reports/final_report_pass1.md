# تقرير صائد الفرص — Opportunity Hunter Final Report

- **Run ID:** `full_20260926` — **Mode:** `full` — **Generated:** 2026-09-26 11:32
- **Market:** Saudi Arabia (global research used to find adaptable models)
- **Status:** completed — **Elapsed:** 3031.6s — **Total agent cost:** $23.012

## 0. ملخص التشغيل (Run Statistics)

| المؤشر | القيمة |
|---|---|
| عمليات Agents التي أُطلقت فعليًا (processes incl. retries) | 35 |
| مهام Agents المنفّذة | 35 |
| أنواع Agents المختلفة التي عملت | 20 |
| مهام ناجحة / فاشلة / متخطاة | 35 / 0 / 0 |
| عمليات البحث (WebSearch) | 362 |
| جلب صفحات (WebFetch) | 97 |
| إصابات Cache للبحث | 1 |
| استدعاءات منعها حد الميزانية | 14 |
| الإشارات/الفرص الخام | 101 |
| بعد إزالة التكرار الحرفي | 101 |
| مرشحون دخلوا التحقق (بعد التصفية) | 20 |
| طلبات بحث إضافي (Gap research) | 0 |
| نجت من Killer Agent | 4 |
| رفضها Killer Agent | 16 |
| غير محسومة | 0 |

### الخلاصة التنفيذية

من 20 فكرة تم فحصها، نجت 4 فقط أمام القاتل، وجميعها في قطاع الامتثال التنظيمي والأتمتة الخلفية للمنشآت الصغيرة: فوترة ZATCA المصغرة (C01، أقوى دليل دفع لكن سوق مزدحم)، أتمتة المحاسبة بالذكاء الاصطناعي (C04، أفضل دليل ألم وأضعف منافسة مباشرة)، امتثال حماية البيانات PDPL (C10، أسهل بناءً EASY)، وتشغيل الصيانة الميدانية عبر واتساب (C08، أضعف دليل بين الأربعة). رُفضت 16 فكرة أخرى لوجود منافسين مباشرين رخيصين أو مجانيين (Nitaqat، الحجوزات، السير الذاتية، الفوترة للعمل الحر)، أو حواجز تنظيمية صلبة (SABER، ترخيص التوظيف، واجهات Ejar/Qiwa)، أو غياب دليل دفع. تم رصد 12 جوهرة مخفية من قائمة الانتظار تستحق بحثاً إضافياً، و9 فرص مستقبلية مرتبطة بتحولات تنظيمية قادمة لم يحن وقتها بعد.

## 1. الفرص الذهبية (Golden Opportunities)

### 1. أداة فوترة إلكترونية مصغرة عبر واتساب لأصغر التجار في نطاق ZATCA  
`C01` · **EXISTING_MARKET** · Complexity: **MODERATE** · Evidence quality: **HIGH** · Killer: **SURVIVED**

- **المشكلة (Problem):** التجار الصغار جداً ملزمون بمرحلة 2 من الفوترة الإلكترونية؛ الموجة 24 (30 يونيو 2026) خفضت العتبة إلى 375,000 ريال، مع غرامات 5,000-50,000 ريال لكل مخالفة على منشآت بلا موظفي تقنية معلومات.
- **العميل (Customer):** أصحاب المتاجر الصغيرة والمؤسسات الفردية في نطاق مرحلة 2 من فاتورة
- **لماذا توجد المشكلة (Why it exists):** تنظيم حكومي إلزامي يتوسع تدريجياً ليشمل منشآت أصغر لا تحتمل تعقيد أنظمة ERP كاملة.
- **البدائل الحالية (Existing alternatives):** Qoyod وWafeq وDaftra أنظمة كاملة؛ Fatoora Cloud وFatooraPlus أدوات مخصصة أرخص؛ Zoho مستوى مجاني.
- **الفرصة في السعودية (Saudi opportunity):** شريحة أصغر من عتبة المنافسين الحاليين (تاجر واحد بفواتير قليلة) قد تجد حتى 75-120 ريال شهرياً مرتفعاً أو معقداً.
- **الحل (Solution):** أداة أحادية التاجر عبر واتساب فقط أو تسعير لكل فاتورة، تولّد XML/QR وترسله عبر CSID ذاتي بدون اعتماد رسمي.
- **MVP:** تسجيل عبر sandbox ثم production، محادثة واتساب لإنشاء فاتورة، توليد وإرسال XML+QR، تخزين الأرشيف، تصدير PDF.
- **التقنية (Technology):** Next.js + Node/FastAPI + Postgres (Supabase) + ZATCA Fatoora API + Moyasar + واتساب BSP اختياري.
- **التكلفة التقديرية (Estimated cost):** 500-1,000 ريال بناء؛ تشغيل شهري 150-400 ريال.
- **نموذج الإيرادات (Revenue model):** اشتراك أقل من 60 ريال شهرياً أو تسعير لكل فاتورة.
- **استراتيجية أول عميل (First customer strategy):** مجموعات واتساب التجارية ومنشورات مستقل، تجربة مجانية محدودة لأول 10 تجار.
- **التوسع (Expansion):** إضافة مطابقة مصروفات وتقارير ضريبية، ثم شرائح أكبر قليلاً.
- **الأدلة (Evidence):**
  - [DIRECT] ZATCA حددت الموجة 24 بعتبة 375,000 ريال ومهلة 30 يونيو 2026 — <https://zatca.gov.sa/en/Pages/news_1426.aspx>
  - [DIRECT] لا يوجد اعتماد إلزامي لمزودي الحلول، أي حل متوافق تقنياً مقبول — <https://zatca.gov.sa/en/E-Invoicing/SolutionProviders/Pages/SolutionProvidersDirectory.aspx>
  - [STRONG_INDIRECT] أسعار Qoyod الفعلية 60-600 ريال شهرياً تشمل الفوترة الإلكترونية — <https://www.qoyod.com/en/knowledge-base/qoyod-plans-and-pricing-subscription-tiers-features-add-ons/>
  - [DIRECT] Fatoora Cloud يقدم فوترة من 75 ريال شهرياً بدون إعداد — <https://www.bytesraw.com/fatoora>
- **المنافسون (Competitors):**
  - Qoyod — من 60 ريال شهرياً، فوترة مشمولة <https://www.qoyod.com/en/knowledge-base/qoyod-plans-and-pricing-subscription-tiers-features-add-ons/>
  - Fatoora Cloud — 75 ريال شهرياً، بدون إعداد <https://www.bytesraw.com/fatoora>
  - FatooraPlus — من 99 ريال شهرياً <https://fatooraplus.com/pricing/>
  - Zoho Invoice/Books — مستوى مجاني متوافق <https://www.zoho.com/sa/books/e-invoicing>
- **المخاطر (Risks):**
  - منافسة شديدة من Fatoora Cloud وFatooraPlus وZoho تجعل السعر الرخيص وحده غير كافٍ.
  - أي خطأ في التوقيع الرقمي يعرّض العميل لغرامة حقيقية، عبء مسؤولية كبير على مؤسس منفرد.
  - عدم تأكد استعداد أصغر التجار للدفع الشهري.
- **المجهول (Unknowns):**
  - حجم الشريحة الأصغر من المنافسين الحاليين.
  - تكلفة دعم واتساب BSP عند الحجم.
  - استعداد الدفع تحت 60-75 ريال شهرياً.
- **ما بقي غير مؤكد حسب Killer Agent:**
  - Whether a truly ultra-micro / WhatsApp-only tier priced below SAR60-75/month can achieve sustainable unit economics given payment processing + hosting + support costs
  - Whether Zoho's free tier actually includes ZATCA Phase-2 compliance or only the paid Books tiers do (search results were ambiguous: 'users must be subscribed to the appropriate Zoho Books plan')
  - Real churn/willingness of the smallest merchants to switch from a free/cheap incumbent to a new unbranded solo product
  - Whether ZATCA's evolving wave schedule will require constant compliance-logic maintenance that a solo founder can sustain long-term
- **المصادر (Sources):**
  - <https://zatca.gov.sa/en/Pages/news_1426.aspx>
  - <https://zatca.gov.sa/en/E-Invoicing/SolutionProviders/Pages/SolutionProvidersDirectory.aspx>
  - <https://www.qoyod.com/en/knowledge-base/qoyod-plans-and-pricing-subscription-tiers-features-add-ons/>
  - <https://www.bytesraw.com/fatoora>
  - <https://fatooraplus.com/pricing/>
  - <https://www.zoho.com/sa/books/e-invoicing>

### 2. أداة ذكاء اصطناعي لأتمتة إدخال الفواتير والتسوية المحاسبية  
`C04` · **IMPROVED_MARKET** · Complexity: **MODERATE** · Evidence quality: **MEDIUM** · Killer: **SURVIVED**

- **المشكلة (Problem):** متاجر وشركات صغيرة تنشر باستمرار طلبات مستقل لإدخال فواتير وتسوية بنكية بدلاً من أتمتة العملية.
- **العميل (Customer):** أصحاب متاجر إلكترونية وشركات صغيرة، ومكاتب محاسبة صغيرة
- **لماذا توجد المشكلة (Why it exists):** غياب أداة ذاتية الخدمة بالعربية للمنشآت الصغرى؛ الحل التقني الأقرب موجه للمؤسسات الكبيرة فقط.
- **البدائل الحالية (Existing alternatives):** توظيف متكرر لمستقلين، أو مكاتب محاسبة بسعر 1,500-5,000+ ريال شهرياً، أو أنظمة كاملة لا تستوعب OCR للفواتير الواردة.
- **الفرصة في السعودية (Saudi opportunity):** طلب حي متكرر بلا منافس ذاتي الخدمة يستهدف الشريحة الصغرى بالعربية.
- **الحل (Solution):** استقبال صور/PDF للفواتير وكشوف الحساب، استخراج بذكاء اصطناعي بصري، مطابقة تلقائية، ملخص تسوية شهري.
- **MVP:** رفع مستندات، استخراج LLM vision، مطابقة بقواعد بسيطة، تصدير Excel.
- **التقنية (Technology):** Next.js + FastAPI + Postgres + Claude/GPT-4o vision + Moyasar.
- **التكلفة التقديرية (Estimated cost):** 500-1,000 ريال بناء؛ تشغيل شهري 150-350 ريال.
- **نموذج الإيرادات (Revenue model):** اشتراك أرخص من تكلفة مكتب محاسبة خارجي.
- **استراتيجية أول عميل (First customer strategy):** التواصل مع أصحاب طلبات إدخال فواتير على مستقل وخمسات مباشرة.
- **التوسع (Expansion):** استهداف مكاتب محاسبة كعميل B2B2B، ثم تصدير مباشر لأنظمة قيود/Wafeq.
- **الأدلة (Evidence):**
  - [DIRECT] أكثر من 7 مشاريع مستقلة حية على مستقل لمحاسبة وإدخال فواتير — <https://mostaql.com/project/1193081-%D9%85%D8%AD%D8%A7%D8%B3%D8%A8-%D8%B9%D9%86-%D8%A8%D8%B9%D8%AF>
  - [STRONG_INDIRECT] مكاتب محاسبة تفرض 1,500-5,000+ ريال شهرياً لنفس المهام — <https://www.sovereigngroup.com/saudi-arabia/accounting-and-bookkeeping/>
  - [WEAK] Sanad.ai أداة OCR عربية موجودة لكنها للمؤسسات الكبرى عبر RPA فقط — <https://sanad.ai/>
- **المنافسون (Competitors):**
  - Sanad.ai — OCR عربي موجه للمؤسسات الكبرى عبر RPA <https://sanad.ai/>
  - Wafeq — يُصدر فواتير لكن لا يستوعب فواتير واردة تلقائياً <https://www.wafeq.com/en-sa/e-invoicing-in-saudi-arabia/preparing-for-e-invoicing/best-accounting-software-in-saudi-arabia>
- **المخاطر (Risks):**
  - منافسة سعرية من مستقلين رخيصين جداً بأجور غير معروفة.
  - لا يوجد تحقق من دقة OCR على فواتير عربية فوضوية.
  - حاجز الثقة قد يتطلب مراجعة بشرية ترفع التكلفة.
- **المجهول (Unknowns):**
  - الأسعار الفعلية للمستقلين على هذه المهام.
  - دقة نماذج الرؤية اللغوية على فواتير عربية حقيقية.
  - أثر مرحلة 2 من فاتورة على هذا الألم مستقبلاً.
- **ما بقي غير مؤكد حسب Killer Agent:**
  - Actual SAR rates freelancers charge per Mostaql bookkeeping/invoice-entry gig (never disclosed in any listing found)
  - Real Arabic OCR accuracy achievable with LLM-vision APIs (Claude/GPT-4o) on messy/handwritten Saudi supplier invoices -- untested in this session
  - Whether customers would trust an unsupervised AI tool for VAT-sensitive reconciliation without a human-in-the-loop, which would raise the founder's operating cost/complexity
- **المصادر (Sources):**
  - <https://mostaql.com/project/1193081-%D9%85%D8%AD%D8%A7%D8%B3%D8%A8-%D8%B9%D9%86-%D8%A8%D8%B9%D8%AF>
  - <https://www.sovereigngroup.com/saudi-arabia/accounting-and-bookkeeping/>
  - <https://sanad.ai/>

### 3. أداة SaaS ذاتية الخدمة للامتثال لنظام حماية البيانات الشخصية PDPL  
`C10` · **LOCAL_ADAPTATION** · Complexity: **EASY** · Evidence quality: **MEDIUM** · Killer: **SURVIVED**

- **المشكلة (Problem):** SDAIA تنفذ PDPL فعلياً (48 قرار إنفاذ خلال عام، غرامات حتى 5 ملايين ريال)؛ أغلب مخالفات المنشآت الصغيرة غياب أساس قانوني وموافقة تسويقية وضمانات تقنية.
- **العميل (Customer):** منشآت صغيرة وشركات ناشئة سعودية بلا وظيفة قانونية داخلية
- **لماذا توجد المشكلة (Why it exists):** أدوات عالمية رخيصة موجودة لكن دعم العربية وتخصيصها لأنماط SDAIA غير مؤكد؛ البدائل المحلية استشارية مكلفة.
- **البدائل الحالية (Existing alternatives):** Enzuzo وCookieHub وTermsFeed عالمية رخيصة؛ SecureLink وGhaim وHala Privacy محلية استشارية.
- **الفرصة في السعودية (Saudi opportunity):** لا يوجد منافس مؤكد يجمع بين عربي أولاً ورخيص ومخصص لأنماط مخالفات SDAIA الفعلية.
- **الحل (Solution):** مولّد سياسة خصوصية بالعربية، إشعار موافقة قابل للتضمين، استبيان رسم خرائط بيانات، قوالب إشعار اختراق.
- **MVP:** استبيان PDPL، توليد سياسة خصوصية تلقائي، أداة موافقة، قوالب تنزيل.
- **التقنية (Technology):** Next.js + Node/Python + Postgres + Claude API + Moyasar.
- **التكلفة التقديرية (Estimated cost):** 500-900 ريال بناء؛ تشغيل شهري 150-250 ريال.
- **نموذج الإيرادات (Revenue model):** اشتراك شهري منخفض حسب حجم البيانات.
- **استراتيجية أول عميل (First customer strategy):** أصحاب متاجر سلة/زد ومجتمعات الشركات الناشئة، تجربة مجانية لأول سياسة خصوصية.
- **التوسع (Expansion):** تغطية قطاعات أكثر تنظيماً، شراكات مع محاسبين ومستشارين صغار.
- **الأدلة (Evidence):**
  - [STRONG_INDIRECT] SDAIA أصدرت 48 قرار إنفاذ، غرامات حتى 5 ملايين ريال — <https://www.globalprivacyblog.com/2026/05/active-enforcement-of-saudi-arabia-privacy-regime-implications-for-businesses/>
  - [WEAK] Enzuzo تقدم صفحة PDPL سعودية من 7-9 دولار شهرياً — <https://www.enzuzo.com/saudi-arabia-pdpl-compliance-software>
- **المنافسون (Competitors):**
  - Enzuzo — صفحة PDPL سعودية، تعريب غير مؤكد <https://www.enzuzo.com/saudi-arabia-pdpl-compliance-software>
  - SecureLink — استشاري محلي مكلف <https://www.securelink.sa/pdpl-compliance-saudi-arabia/>
- **المخاطر (Risks):**
  - أدوات عالمية رخيصة تغطي جزءاً من الوظيفة بالفعل.
  - غير مؤكد استهداف الإنفاذ للمنشآت الصغيرة المحلية بدلاً من الكبيرة.
  - مخاطر تأطير قانوني: يجب توضيح أنها أداة وليست استشارة قانونية.
- **المجهول (Unknowns):**
  - دعم العربية الفعلي في Enzuzo/CookieHub/TermsFeed.
  - أسعار المنافسين المحليين الفعلية.
  - حجم الطلب الفعلي مقابل فجوة الوعي.
- **ما بقي غير مؤكد حسب Killer Agent:**
  - None of the found global competitors (Enzuzo, CookieHub, TermsFeed, privacypolicygenerator.info) were confirmed to have Arabic-language UI or Saudi-specific breach-notification/DPO-workflow depth tied to SDAIA's documented enforcement patterns — this remains the candidate's plausible wedge but is unproven
  - Whether current SDAIA enforcement (48 decisions/year) is concentrated on large/foreign firms vs. small local SMEs, which would affect real urgency/willingness-to-pay for this exact segment
  - No confirmed SAR pricing for any local competitor (Hala Privacy, SecureLink, Ghaim) or evidence of actual customer volume for any player in this space
- **المصادر (Sources):**
  - <https://www.globalprivacyblog.com/2026/05/active-enforcement-of-saudi-arabia-privacy-regime-implications-for-businesses/>
  - <https://www.enzuzo.com/saudi-arabia-pdpl-compliance-software>
  - <https://www.securelink.sa/pdpl-compliance-saudi-arabia/>

### 4. أداة تشغيل ميداني خفيفة عبر واتساب لشركات الصيانة الصغيرة  
`C08` · **LOCAL_ADAPTATION** · Complexity: **MODERATE** · Evidence quality: **LOW** · Killer: **SURVIVED**

- **المشكلة (Problem):** شركات صيانة صغيرة (1-15 فني) تفتقر لتتبع لحظي للفنيين وسجل صيانة موحد وفوترة سريعة، وتعتمد على الهاتف وواتساب غير المنظم.
- **العميل (Customer):** شركات صيانة ومرافق صغيرة (1-15 فني)
- **لماذا توجد المشكلة (Why it exists):** خيارات إما ERP مؤسسي مبالغ فيه، أو منافسون محليون لم يُؤكد جمعهم بين GPS لحظي وواتساب أصلي.
- **البدائل الحالية (Existing alternatives):** Mutflex وSaudiSoftware.co وDaftra محلياً؛ Jobber وHousecall Pro عالمياً دون تعريب.
- **الفرصة في السعودية (Saudi opportunity):** لا يوجد منافس مؤكد يجمع بين GPS لحظي وواتساب أصلي وتسعير موجه لصغار المشغلين.
- **الحل (Solution):** PWA خفيف لتعيين مهام ومتابعتها عبر واتساب، سجل صيانة موحد بالصور، فاتورة تلقائية عند الإتمام.
- **MVP:** إنشاء مهمة وتعيين فني، تحديث حالة عبر واتساب، سجل صيانة بالصور، فاتورة بسيطة.
- **التقنية (Technology):** Next.js PWA + Node/Python + Postgres + WhatsApp Business API + Moyasar.
- **التكلفة التقديرية (Estimated cost):** 600-1,300 ريال بناء؛ تشغيل شهري 300-450 ريال.
- **نموذج الإيرادات (Revenue model):** اشتراك شهري لكل فني، أقل من الأنظمة المؤسسية.
- **استراتيجية أول عميل (First customer strategy):** مجموعات واتساب لشركات التكييف والكهرباء الصغيرة، تجربة مجانية لأول 5-10 فنيين.
- **التوسع (Expansion):** قطاعات ميدانية مشابهة (توصيل، تنظيف) بنفس البنية بعد إثبات الجدوى.
- **الأدلة (Evidence):**
  - [WEAK] Mutflex منافس سعودي بباقات مستخدمين غير محدودين وتجربة مجانية شهرين — <https://mutflex.com/pricing>
  - [STRONG_INDIRECT] Daftra تملك وحدة إدارة مراكز صيانة من الشكوى حتى الفاتورة — <https://www.daftra.com/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D9%85%D8%B1%D8%A7%D9%83%D8%B2-%D8%A7%D9%84%D8%B5%D9%8A%D8%A7%D9%86%D8%A9-%D9%88%D8%A7%D9%84%D8%AF%D8%B9%D9%85-%D8%A7%D9%84%D9%81%D9%86%D9%89/>
  - [WEAK] إحصائية 38% انتشار رقمي وُجدت منسوخة بين موقعين تسويقيين دون مصدر أساسي — <https://multitech.sa/how-hvac-field-service-software-agreements-improve-efficiency-in-saudi-buildings/>
- **المنافسون (Competitors):**
  - Mutflex — منافس سعودي مباشر لشركات التكييف الصغيرة <https://mutflex.com/pricing>
  - Daftra — نظام محاسبة مجاني الفئة الأولى مع وحدة صيانة <https://www.daftra.com/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D9%85%D8%B1%D8%A7%D9%83%D8%B2-%D8%A7%D9%84%D8%B5%D9%8A%D8%A7%D9%86%D8%A9-%D9%88%D8%A7%D9%84%D8%AF%D8%B9%D9%85-%D8%A7%D9%84%D9%81%D9%86%D9%89/>
- **المخاطر (Risks):**
  - منافسون محليون موجودون (Mutflex، Daftra) وإن لم يُؤكد جمعهم بين GPS وواتساب.
  - إحصائية السوق الرئيسية غير موثوقة (منسوخة بين موقعين).
  - دليل الألم الأساسي من مدونة بائع واحد فقط دون تأكيد مستقل.
- **المجهول (Unknowns):**
  - أسعار المنافسين المحليين الفعلية.
  - هل تقدم Daftra GPS لحظي فعلاً؟
  - استعداد صغار المشغلين للتحول من المجاني إلى المدفوع.
- **ما بقي غير مؤكد حسب Killer Agent:**
  - Actual pricing of Mutflex/SaudiSoftware.co/Daftra's maintenance module — not confirmed, needed to know if a cheaper entrant is even possible
  - Whether Daftra's maintenance-center module is oriented toward walk-in repair shops (e.g., device repair) rather than field technicians visiting customer sites — this distinction could preserve or close the wedge
  - True price sensitivity and switching willingness of 1-10 technician operators
  - Whether any competitor already offers real-time GPS/status tracking + WhatsApp-native workflow specifically, which none of the found sources confirmed
- **المصادر (Sources):**
  - <https://mutflex.com/pricing>
  - <https://www.daftra.com/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D9%85%D8%B1%D8%A7%D9%83%D8%B2-%D8%A7%D9%84%D8%B5%D9%8A%D8%A7%D9%86%D8%A9-%D9%88%D8%A7%D9%84%D8%AF%D8%B9%D9%85-%D8%A7%D9%84%D9%81%D9%86%D9%89/>
  - <https://www.getjobber.com/comparison/jobber-vs-housecall-pro/>

## 2. جواهر مخفية (Hidden Gems)

- **أداة تتبع أقساط العملاء (تقسيط)** (`HG01`, UNVALIDATED_LEAD, EASY): بديل لإكسل الملون يدوياً لتتبع الأقساط وتواريخ التحصيل — دليل حي من مستقل على منتج مماثل مبني لعميل حقيقي، ألم متكرر غير مخدوم بأداة SaaS مخصصة. <https://mostaql.com/portfolio/3273292-%D9%86%D8%B8%D8%A7%D9%85-%D8%A5%D9%83%D8%B3%D9%8A%D9%84-%D8%B0%D9%83%D9%8A-%D9%84%D9%85%D8%AA%D8%A7%D8%A8%D8%B9%D8%A9-%D8%A3%D9%82%D8%B3%D8%A7%D8%B7-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D8%A7%D8%A1-%D9%88%D8%A7%D9%84%D8%AA%D8%AD%D8%B5%D9%8A%D9%84-%D8%A7%D9%84%D9%85%D8%A7%D9%84%D9%8A-%D8%A7%D9%84%D8%AF%D9%88%D8%B1%D9%8A>
- **دفتر أستاذ موردين وعملاء رقمي للجملة** (`HG02`, UNVALIDATED_LEAD, EASY): تتبع التوريدات وحسابات العملاء بدلاً من شيتات إكسل مخصصة — طلب مستقل جديد وبورتفوليو منجز فعلياً، دون أداة SaaS رخيصة مخصصة. <https://mostaql.com/portfolio/1864563-%D8%B4%D9%8A%D8%AA-%D8%A7%D9%83%D8%B3%D9%84-%D9%84%D9%85%D8%AA%D8%A7%D8%A8%D8%B9%D8%A9-%D8%A7%D9%84%D8%AA%D9%88%D8%B1%D9%8A%D8%AF%D8%A7%D8%AA-%D9%88%D8%AD%D8%B3%D8%A7%D8%A8%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D8%A7%D8%A1>
- **تطبيق متابعة مندوبي المبيعات الميدانيين** (`HG03`, UNVALIDATED_LEAD, MODERATE): تتبع زيارات المندوبين والطلبات والتحصيل بدلاً من مكالمات هاتفية — منتج منافس (Kashierapp) يثبت النموذج، لكن استهداف صغار الموزعين تحديداً غير مؤكد. <https://mostaql.com/project/216022-%D9%85%D9%88%D9%82%D8%B9-%D8%A5%D8%AF%D8%A7%D8%B1%D8%A9-%D9%85%D9%86%D8%AF%D9%88%D8%A8%D9%8A%D9%86-%D8%A7%D9%84%D9%85%D8%A8%D9%8A%D8%B9%D8%A7%D8%AA> <https://kashierapp.com/%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D8%AC-%D8%A7%D8%AF%D8%A7%D8%B1%D8%A9-%D8%A7%D9%84%D9%85%D9%86%D8%AF%D9%88%D8%A8%D9%8A%D9%86>
- **أداة متابعة طلبات مخصصة للأعمال المنزلية** (`HG04`, UNVALIDATED_LEAD, EASY): تتبع طلبات العملاء ومواعيد الاستلام والتسليم بدلاً من إكسل يدوي — طلب مجتمعي على خمسات وبورتفوليو منجز، شريحة مهملة من أدوات SaaS. <https://mostaql.com/portfolio/1357455-%D8%AA%D8%B5%D9%85%D9%8A%D9%85-%D8%B4%D9%8A%D8%AA-%D8%A7%D9%83%D8%B3%D9%8A%D9%84-%D9%84%D9%85%D8%AA%D8%A7%D8%A8%D8%B9%D9%87-%D8%A7%D9%84%D8%B9%D9%85%D9%84%D8%A7%D8%A1-%D9%88-%D9%85%D9%88%D8%A7%D8%B9%D9%8A%D8%AF-%D8%A7%D9%84%D8%A7%D8%B3%D8%AA%D9%84%D8%A7%D9%85-%D9%88-%D8%A7%D9%84%D8%AA%D8%B3%D9%84%D9%8A%D9%85>
- **أداة تحصيل الديون عبر واتساب** (`HG05`, UNVALIDATED_LEAD, MODERATE): أتمتة رسائل متابعة المستحقات المتأخرة بدلاً من موظف تحصيل يدوي — وظائف تحصيل مفتوحة ومتكررة لدى جهات متعددة تثبت أن الشركات تدفع رواتب فعلية لهذه المهمة. <https://www.linkedin.com/jobs/view/4206999894> <https://www.gulftalent.com/saudi-arabia/jobs/title/credit-and-collection-officer>
- **أداة تصنيف مستندات لمراقبي مستندات المقاولات** (`HG06`, UNVALIDATED_LEAD, MODERATE): أتمتة تنظيم وتوجيه مستندات المشاريع بدلاً من موظف مراقبة مستندات — دليل رواتب فعلي (4,208-9,075 ريال) و75 وظيفة مفتوحة، لكن تعقيد تكامل EDMS أعلى. <https://www.bayt.com/en/saudi-arabia/salaries/jobtitle/document-controller/>
- **أداة مقارنة عروض أسعار الموردين** (`HG07`, UNVALIDATED_LEAD, MODERATE): أتمتة جمع ومقارنة عروض الموردين بدلاً من منسق مشتريات يدوي — 42 وظيفة مفتوحة متزامنة تثبت طلباً واسعاً، لكن خطر استخدام أنظمة ERP كبيرة أصلاً. <https://www.gulftalent.com/saudi-arabia/jobs/title/procurement-coordinator>
- **روبوت رد آلي بالعربية لمراكز الاتصال** (`HG08`, UNVALIDATED_LEAD, MODERATE): تحويل جزء من حجم مكالمات الاستفسارات المتكررة لروبوت ذكاء اصطناعي — أكثر من 2,000 وظيفة خدمة عملاء مفتوحة تثبت حجم الطلب، نسبة الأتمتة الممكنة غير معروفة. <https://www.linkedin.com/jobs/customer-service-jobs-saudi-arabia?trk=amworks_jserp_redirect>
- **وسيط مزامنة حسابات ومخزون بين سلة/زد ونون/أمازون/Odoo** (`HG09`, UNVALIDATED_LEAD, MODERATE): ربط برمجي مخصص لا يغطيه التطبيق الرسمي في متجر التطبيقات — طلب مقترح رسمي على منصة سلة نفسها، وعدة طلبات مستقل منفصلة رغم وجود تطبيقات رسمية. <https://features.salla.sa/ideas/SUG-I-9363>
- **حاسبة ضريبة الأراضي البيضاء** (`HG10`, UNVALIDATED_LEAD, EASY): أداة بسيطة تحسب ضريبة الأرض البيضاء الجديدة لملاك الأراضي الكبيرة — أكثر من 60,000 مالك أرض تلقوا فواتير فعلية، قاعدة عملاء محددة كأداة تسويقية تقود لاستشارات مدفوعة. <https://www.agbi.com/real-estate/2026/01/saudi-arabia-bills-60000-landowners-under-new-tax-rule/>
- **نظام كاشير منخفض التكلفة بديل لـFoodics** (`HG11`, UNVALIDATED_LEAD, HARD): بديل أرخص للمقاهي والمطاعم الصغيرة الناقمة على تكلفة Foodics — منافس (TapFood) يسوّق نفسه صراحة كبديل أرخص، لكن الحاجة لأجهزة كاشير ترفع صعوبة الـMVP. <https://tapfood.net/blog/tapfood-vs-foodics-alternative-saudi-arabia-2026>
- **أداة عرض سعر وعقد وفاتورة ZATCA للمستقلين** (`HG12`, UNVALIDATED_LEAD, MODERATE): نسخة سعودية متوافقة مع فاتورة من أدوات مثل Bonsai/HoneyBook — فجوة ميزات واضحة نظرياً، لكن لا دليل مباشر على طلب فعلي من مستقلين سعوديين. <https://agiled.app/compare/bonsai-vs-honeybook>

## 3. نماذج عالمية قابلة للتكييف (Foreign Models)

- **Jobber** (كندا) <https://www.getjobber.com/comparison/jobber-vs-housecall-pro/> — جدولة الفنيين وإدارة العمل الميداني والفوترة لشركات الخدمات الصغيرة  
  نموذج الإيراد: اشتراك شهري لكل مستخدم من 19 دولار · الوضع في السعودية: لا تعريب مؤكد؛ منافسون محليون جزئيون (Mutflex، Daftra)  
  التكييف: يحتاج تعريب، واتساب أصلي، وتكامل ZATCA، انظر C08 <https://www.getjobber.com/comparison/jobber-vs-housecall-pro/>
- **Enzuzo** (كندا) <https://www.enzuzo.com/saudi-arabia-pdpl-compliance-software> — إدارة موافقة وسياسات خصوصية ذاتية الخدمة، صفحة PDPL سعودية  
  نموذج الإيراد: اشتراك 7-79 دولار مع خطة مجانية · الوضع في السعودية: يخدم السوق تقنياً، دعم العربية غير مؤكد  
  التكييف: الفرصة المحلية C10 تحتاج تعريب كامل وتخصيص لأنماط SDAIA <https://www.enzuzo.com/saudi-arabia-pdpl-compliance-software>
- **Zoho Invoice/Books** (الهند) <https://www.zoho.com/sa/books/e-invoicing> — فوترة مجانية/رخيصة متوافقة مع مرحلة 2 من ZATCA  
  نموذج الإيراد: مستوى مجاني، اشتراكات مدفوعة للمتقدم · الوضع في السعودية: موجود ويخدم السوق مباشرة كمنافس  
  التكييف: منافس مباشر بالفعل، حاجز سعر أساسي لأي بديل، انظر مخاطر C01 <https://www.zoho.com/sa/books/e-invoicing>
- **Bonsai/HoneyBook** (الولايات المتحدة) <https://agiled.app/compare/bonsai-vs-honeybook> — تجميع عرض السعر والعقد والفوترة للمستقلين  
  نموذج الإيراد: اشتراك شهري · الوضع في السعودية: لا تكامل ZATCA مؤكد، فجوة نظرية غير مُختبرة  
  التكييف: يحتاج فاتورة متوافقة وتعريب كامل، انظر HG12 <https://agiled.app/compare/bonsai-vs-honeybook>
- **Clio** (كندا) <https://www.clio.com/manage/> — إدارة ممارسة قانونية شاملة تخدم 400,000+ قانوني عالمياً  
  نموذج الإيراد: اشتراك شهري لكل مستخدم · الوضع في السعودية: لا تواجد أو دعم عربي مؤكد في السعودية  
  التكييف: فرصة نظرية فقط، تفتقر لدليل طلب فعلي من محامين سعوديين <https://www.clio.com/manage/>

## 4. أعمال مملة لكنها مربحة (Boring Businesses)

- **أتمتة تحصيل المستحقات المتأخرة عبر واتساب** — شركات توظف موظفي تحصيل بشكل متكرر لمتابعة الحسابات المتأخرة يدوياً هاتفياً.  
  من يدفع: أقسام مالية لدى شركات لديها ذمم مدينة (إقراض، مرافق، هيئات مدن صناعية) · الدليل: وظائف تحصيل مفتوحة متكررة لدى جهات متعددة، 14 وظيفة في أغسطس 2026 <https://www.gulftalent.com/saudi-arabia/jobs/title/credit-and-collection-officer>
- **تنظيم وتوجيه مستندات مشاريع المقاولات** — شركات مقاولات توظف مراقبي مستندات بدوام كامل لتنظيم وتتبع مستندات المشروع يدوياً.  
  من يدفع: مقاولون واستشاريو بنية تحتية، راتب 4,208-9,075 ريال شهرياً · الدليل: 75 وظيفة مراقب مستندات مفتوحة في ديسمبر 2025 <https://www.bayt.com/en/saudi-arabia/salaries/jobtitle/document-controller/>
- **امتثال الفوترة الإلكترونية الإلزامية ZATCA** — منشآت صغيرة تدخل حديثاً نطاق الالتزام الحكومي بغرامات حقيقية عند عدم الامتثال.  
  من يدفع: أصحاب متاجر صغيرة، بدليل اشتراكات فعلية 60-249 ريال شهرياً لدى Qoyod وWafeq · الدليل: غرامات موثقة 5,000-50,000 ريال، عتبة الموجة 24 منخفضة من يونيو 2026 <https://zatca.gov.sa/en/Pages/news_1426.aspx>
- **إدخال بيانات الفواتير والمحاسبة اليدوية** — منشآت صغيرة تعيد توظيف مستقلين بشكل متكرر لإدخال فواتير يدوياً.  
  من يدفع: أصحاب متاجر صغيرة عبر مستقل، ومكاتب محاسبة بسعر 1,500-5,000+ ريال شهرياً · الدليل: أكثر من 7 طلبات مستقل حية لإدخال فواتير ومحاسبة عن بعد <https://mostaql.com/project/1193081-%D9%85%D8%AD%D8%A7%D8%B3%D8%A8-%D8%B9%D9%86-%D8%A8%D8%B9%D8%AF>

## 5. فرص مستقبلية 1–3 سنوات (Future Opportunities)

> الأدلة الحالية (CURRENT EVIDENCE) منفصلة عن الفرضية (FUTURE HYPOTHESIS). لا شيء هنا حقيقة مؤكدة.

- **أدوات مالية شخصية عبر البنوك المفتوحة** (1-3 سنوات)  
  **CURRENT EVIDENCE:** ساما بدأت ترخيص البنوك المفتوحة في 26 مارس 2026؛ Lean Technologies أول مرخص  
  **FUTURE HYPOTHESIS:** إذا نضج ترخيص البنوك المفتوحة خلال 1-3 سنوات، فسترغب المنشآت الصغيرة في تطبيقات تدفق نقدي مبنية فوق واجهات مرخصة.  
  المحفّز: نضج السوق بمزودين مرخصين بشروط وصول معقولة لمؤسس منفرد <https://spa.gov.sa/en/N2546753>
- **أدوات امتثال لحوكمة الذكاء الاصطناعي SDAIA** (1-2 سنة)  
  **CURRENT EVIDENCE:** الاستشارة العامة أُغلقت مايو 2026 ولم تُعتمد بعد كنظام ملزم حتى اليوم  
  **FUTURE HYPOTHESIS:** إذا اكتملت وأُنفذت سياسة الذكاء الاصطناعي المسؤول كشرط شراء، فسيحتاج بائعو الذكاء الاصطناعي الصغار أدوات تصنيف مخاطر وتوثيق.  
  المحفّز: اعتماد السياسة رسمياً مع نطاق إنفاذ يشمل الشركات الصغيرة <https://digitalpolicyalert.org/event/39093-saudi-data-and-artificial-intelligence-authority-closes-consultation-on-draft-responsible-ai-policy-including-performance-monitoring-requirement>
- **أدوات تشغيل فندقي للمشغلين المستقلين قبل كأس العالم 2034** (3-8 سنوات)  
  **CURRENT EVIDENCE:** السعودية تملك حالياً نحو 500,000 غرفة فقط مقابل خطة إضافة 180,000-230,000 غرفة بحلول 2034  
  **FUTURE HYPOTHESIS:** إذا استمرت خطط بناء 180,000+ غرفة فندقية، فسيحتاج مشغلون مستقلون أدوات تشغيل وإيرادات ميسورة.  
  المحفّز: افتتاح أعداد كبيرة من الفنادق المستقلة فعلياً في المدن الثانوية <https://alphaconsultancy.sa/en/resources/fifa-world-cup-2034-saudi-arabia-business>
- **مطابقة مقاولي الباطن لمشاريع إكسبو 2030 وكأس العالم 2034** (1-3 سنوات)  
  **CURRENT EVIDENCE:** إكسبو 2030 الرياض تخطط لبدء إنشاء المباني الرئيسية الربع الثالث 2026  
  **FUTURE HYPOTHESIS:** إذا تسارعت أعمال البناء الفعلية، فسيواجه مقاولو الباطن الصغار سوق مناقصات مجزأ ونقص عمالة ماهرة.  
  المحفّز: بدء البناء الفعلي على النطاق المعلن مع ظهور حاجة موثقة لتنسيق مقاولي الباطن <https://expo2030.co/briefings/expo-2030-pavilion-timeline/>
- **أداة اختيار فئات التأمين الصحي الإلزامي لأصحاب العمل الصغار** (1-2 سنة)  
  **CURRENT EVIDENCE:** فئات CHI 2026 موثقة (600-12,000 ريال سنوياً حسب الفئة)  
  **FUTURE HYPOTHESIS:** إذا استمر توسع فئات التأمين الصحي، فسيحتاج أصحاب العمل الصغار أداة لاختيار وميزنة الفئة المناسبة.  
  المحفّز: مزيد من توسع متطلبات مجلس الضمان الصحي <https://truescho.com/en/blog/health-insurance-expats-saudi-arabia-2026>
- **تطبيق حالة شحن للسيارات الكهربائية** (2-4 سنوات)  
  **CURRENT EVIDENCE:** نحو 1,200 شاحن عام مركّز في الرياض وجدة ونيوم؛ إطلاق Ceer مخطط الربع الرابع 2026  
  **FUTURE HYPOTHESIS:** إذا تسارع تبني السيارات الكهربائية من أقل من 1% حالياً، فسيحتاج ملاك جدد تطبيقاً لحالة الشواحن في المدن الثانوية.  
  المحفّز: نمو ملموس في مبيعات السيارات الكهربائية يتجاوز تغطية الشواحن الحالية <https://saudimarketresearchconsulting.com/insights/articles/closing-the-charging-gap-saudi-arabia-ev-charging-infrastructure-gap-and-the-2026-operator-opportunity>
- **أدوات حوكمة خفيفة للشركات العائلية الصغيرة** (2-5 سنوات)  
  **CURRENT EVIDENCE:** 59% من الشركات العائلية السعودية بلا خطة تعاقب واضحة، 23% من المؤسسين فوق 55  
  **FUTURE HYPOTHESIS:** إذا استمرت موجة كبار السن من المؤسسين دون خطط تعاقب رسمية، فسيحتاج الشركات العائلية الصغيرة أدوات حوكمة ميسورة.  
  المحفّز: ظهور طلب فعلي موثق على أدوات رقمية بدلاً من مستشارين بشريين فقط <https://knowledge.insead.edu/family-business/saudi-arabia-tackles-succession-decades>

## 6. الفرص المرفوضة (Rejected by Killer Agent)

> هذا القسم لتعرف ما الذي **لا يجب** أن تضيّع وقتك عليه.

### ❌ C02 — Nitaqat/Saudization profession-level compliance dashboard

- **المشكلة:** The April 2026 Nitaqat overhaul made compliance materially harder for SMEs: mandatory Qiwa authentication, abolished Yellow tier, profession-specific quotas across 269 roles, and rising minimum-wage thresholds to count toward quota — a company can look compliant overall yet violate at department level, risking Red-tier status that blocks work-permit issuance, visas and government contracts. A parallel Qiwa employment-contract documentation mandate (85% by Apr 2026, 90% by Jun 2026) ties directly into Nitaqat credit.
- **[MAJOR] STRONG_COMPETITOR:** A direct, purpose-built competitor already exists and does exactly what this candidate proposes: SaudizationMeter offers Nitaqat band calculation, what-if hiring scenarios, custom alerts, an audit log, and multi-company support, with live tiered pricing ($30/mo Starter, $80/mo Pro, $400/mo Enterprise) and a free calculator as a lead magnet -- this is not a hypothetical incumbent, it is the exact product concept already shipped. <https://www.saudizationmeter.com/pricing> <https://www.jisr.net/en/hr-tools/nitaqat-calculator>
- **[MAJOR] DATA_UNAVAILABLE:** The core value proposition (auto-syncing Qiwa employee/profession data instead of manual re-entry) depends on API access that does not appear to exist for independent third-party developers. Research on Qiwa/government-platform integration confirms most Saudi government services 'do not allow for direct integration with external entities through APIs; instead, it allows for data import and export' -- meaning any new tool, like the existing SaudizationMeter, is reduced to a manual-entry calculator, not a true automation layer. <https://origami.sa/en/blog/saudi-government-platform-integration-qiwa-gosi-mudad-zatca/>
- **الخلاصة:** A near-identical direct competitor (SaudizationMeter) already exists with live paid tiers doing exactly what this candidate proposes, and the core differentiator (automated data sync vs. manual re-entry) is undermined because Saudi government platforms do not appear to expose third-party APIs, only import/export -- both a strong competitive and a technical/product-value blocker.

### ❌ C03 — Multi-portal HR/government compliance reminder tool (Qiwa/Mudad/GOSI/Muqeem/iqama)

- **المشكلة:** HR/admin staff at SMEs repeat the same actions across disconnected government portals (Qiwa, Mudad, GOSI, Muqeem) for every employee event — contract updates, iqama/visa renewals, GOSI registration, wage-file uploads — re-entering the same data multiple times. Iqama renewals are frequently delayed/neglected by employers (fines, labor disputes); Mudad now covers all private employers with 10/15-day delay alerts and a 20-day inspection trigger; dedicated 'Government Relations Coordinator' roles exist specifically to manage this manually.
- **[MAJOR] DATA_UNAVAILABLE:** The central pitch -- eliminating duplicate manual data entry across Qiwa/Mudad/GOSI/Muqeem -- requires API/automated access that does not exist for independent developers. Confirmed again in this session: Saudi government platforms mostly restrict third parties to data import/export, not live API integration, and the candidate's own feasibility_validator already concluded 'without government-portal API access, the tool cannot actually eliminate duplicate data entry (its core pitch).' <https://origami.sa/en/blog/saudi-government-platform-integration-qiwa-gosi-mudad-zatca/>
- **[MAJOR] WEAK_PAIN:** Once stripped of automated sync, the product becomes a manual-entry reminder/checklist tool that must compete directly against free tools SMEs already use for this purpose (Google Calendar, Notion, Excel spreadsheets), and there is no evidence any SME has ever paid specifically for a standalone reminder-only product in this category -- only full, much pricier HCM suites (Jisr ~SAR16-17/employee/month) or human hires (Government Relations Coordinators) show real spend. <https://www.jisr.net/plans>
- **الخلاصة:** The product's core value proposition depends on government-portal API access that does not appear to exist for third parties, reducing it to a manual-entry reminder tool that competes against free calendar/spreadsheet workarounds -- with no evidence anyone has ever paid specifically for that narrower, less valuable product.

### ❌ C05 — WhatsApp/AI booking & no-show reduction for small clinics and salons

- **المشكلة:** Small clinics, salons and single-practitioner service businesses lose revenue to appointment no-shows and mismanaged WhatsApp/notebook bookings; documented no-show rates in Saudi outpatient departments range 11-73% depending on department; missed inbound calls cause lost bookings; salon/spa owners on marketplace platforms like Fresha pay a 20% commission on top of a subscription fee, cutting into thin margins.
- **[FATAL] STRONG_COMPETITOR:** The exact proposed product already exists, live, from a local vendor: Watily offers a WhatsApp-native, no-per-booking-commission, Arabic-first booking + automated reminder system explicitly for both salons AND clinics, priced from SAR49-149/month with no setup fee. This is not a distant analog -- it is essentially the candidate's proposed solution already shipped and commercialized. Beyond Watily, at least four more local/regional competitors serve the identical niche (OJlinker, Hajzak, Bookforme, Salonaty), plus free alternatives (Tawqiti's free booking page, Medicakare's free clinic-management tool) further compress any remaining price wedge, leaving no credible gap for a new solo entrant beyond 'be even cheaper than SAR49/month,' which is unsustainable given WhatsApp Cloud API/BSP messaging costs alone. <https://watily.com/booking-system/ar/> <https://ojlinker.com.sa/> <https://tawqiti.com/industries/salons> <https://www.bookforme.com/ar/business-types/salon>
- **الخلاصة:** This is the most crowded candidate found: a local incumbent (Watily) already sells almost exactly the proposed product (Arabic-first, WhatsApp-native, no-commission booking+reminders for salons and clinics) at SAR49-149/month, alongside four more local/regional competitors and two free alternatives -- leaving no credible wedge for a new solo entrant with the same generic positioning.

### ❌ C06 — Delivery address validation & COD-failure reduction for e-commerce merchants

- **المشكلة:** Saudi last-mile delivery for SME e-commerce suffers failure rates reported up to 40% (vs ~15% in UAE), driven by inability to locate addresses and cash-on-delivery cancellations; from 1 Jan 2026 all parcel shipments must carry a validated National Address/short code, with SAR 5,000 fines for non-compliant postal providers and rejection risk for shipments without it. Many merchants and customers don't have accurate, validated National Address data on file.
- **[FATAL] STRONG_COMPETITOR:** The two target distribution platforms (Salla and Zid) already natively require/validate the National Address short-code at checkout for free, built into the core product every merchant already uses. On top of that, at least two dedicated third-party address-validation plugins already exist and are live/installable: Saudi Address Pro (WordPress + Shopify App Store, works with Salla, explicitly 'TGA 2026 Ready', 60-day free trial with unlimited validations) and Quiqup KSA Address Validator (Shopify App Store). This satisfies the FATAL bar: cheap/free, well-localized (Arabic, Saudi-specific), well-distributed (built into the merchant's own platform or listed in the app stores merchants already browse), and serving the exact niche, leaving no credible wedge for the 'validate National Address at checkout' value proposition as described. <https://salasa.co/blog/national-address-mandate-2026-a-full-faq-guide-for-merchants-consumers/> <https://saudiaddresspro.com/> <https://wordpress.org/plugins/saudi-address-pro/> <https://apps.shopify.com/quiqup-ksa-address-validator> <https://help.zid.sa/national-address/>
- **[MINOR] WEAK_PAIN:** The only clearly unaddressed remaining wedge identified by the dossier itself (a pre-dispatch WhatsApp COD-cancellation-risk confirmation flow) is a different, unvalidated product idea from the one actually proposed and scoped (an address-validation plugin) — no direct evidence was found that merchants would pay specifically for that narrower workflow. 
- **الخلاصة:** Killed on STRONG_COMPETITOR: Salla and Zid already natively enforce/validate National Address at checkout for free, and at least two dedicated third-party plugins (Saudi Address Pro, Quiqup KSA Address Validator) are already live in the app stores merchants use. No credible wedge remains for the address-validation value proposition as described.

### ❌ C07 — Micro-landlord / small property management tool (rent, Ejar, maintenance)

- **المشكلة:** Small independent landlords and boutique property managers (2-20 units) rely on paper records, Excel sheets and ad-hoc phone/WhatsApp reminders to track rental contracts, chase late rent and manage maintenance requests, with no unified system linking Ejar contracts, collections and maintenance; Western PM platforms (Buildium, AppFolio) lack EJAR/ZATCA integration and Arabic UI, forcing manual workarounds.
- **[MAJOR] REGULATORY:** Direct Ejar API access — the candidate's stated core differentiator ('layered on Ejar contract data') — is gated behind Saudi Commercial Registration, REGA developer-or-property-manager registration, PDPL compliance certification, and a technical security assessment. This is a multi-step accreditation process, not a self-serve API key, and was independently re-confirmed via a fresh search in this session. It directly contradicts the 'easy MVP' framing and forces the realistic MVP down to manual/CSV data entry — a much weaker, easily-copied product. <https://logiolegion.com/blogs/ejar-api-integration-software-development-saudi-arabia> <https://rega.gov.sa/en/rega-services/platforms/ejar/>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** The clearest direct demand evidence in the dossier (5+ independent Mostaql/Khamsat freelance requests) shows the exact target segment's revealed preference is to pay a one-off freelancer for an Excel/Access file rather than adopt recurring SaaS. Payment_validator confirmed only PARTIAL payment evidence, entirely from adjacent agency/portfolio-scale players (Osool, RConcept), with no confirmed instance of a 2-20 unit independent landlord paying for recurring software. <https://mostaql.com/project/916062-%D9%85%D9%84%D9%81-%D8%A7%D9%83%D8%B3%D9%84-%D9%84%D9%85%D8%AA%D8%A7%D8%A8%D8%B9%D8%A9-%D8%AA%D8%AD%D8%B5%D9%8A%D9%84-%D8%A7%D9%84%D8%A7%D9%8A%D8%AC%D8%A7%D8%B1%D8%A7%D8%AA> <https://www.osool.estate/en>
- **الخلاصة:** Rejected on two MAJOR grounds: (1) the stated Ejar-integration differentiator is blocked behind a multi-step REGA/CR/PDPL accreditation gate, not a quick API signup, forcing a much weaker manual-entry MVP; and (2) the strongest direct demand evidence available (freelance Excel requests) shows the exact target segment prefers one-off cheap tools over recurring SaaS, with no confirmed micro-landlord-segment SaaS payment found.

### ❌ C09 — SABER import-certificate assistant for small importers/dropshippers

- **المشكلة:** Since 1 October 2025, a SABER shipment certificate is mandatory for ALL imports into Saudi Arabia — including previously-exempt 'unregulated' products — with no clearance possible without it, causing delays and storage fees. Small/solo importers and e-commerce dropshippers who previously imported low-risk goods without any certificate are newly and abruptly affected.
- **[FATAL] REGULATORY:** A SABER Shipment/Product Certificate of Conformity can legally only be issued by a SASO-accredited/notified Certification Body holding independent ISO/IEC 17065:2012 accreditation via the Saudi Accreditation Center (SAAC). All confirmed players in this space (TÜV SÜD, SGS, QIMA, Verger Group) are established international/regional certification firms, not solo operators. A solo founder cannot obtain this accreditation within a 500-1,000 SAR budget or a short timeframe; the only feasible role is a thin document-prep/referral front-end for an accredited partner, which is a fundamentally weaker business than the one proposed. <https://www.sanyogconformity.com/saso-saber-certification/> <https://www.tuvsud.com/en-ae/services/product-certification/saso-saber-product-certification-in-saudi-arabia> <https://www.qima.com/consumer-products/certifications/saso-conformity>
- **[MAJOR] STRONG_COMPETITOR:** At least 8-10 established certification/consultancy agencies (Adnovs, Fahes, Tabseer, Verger Group, Instacertify, Export2Gulf, Atoney, XDS Solutions, Markek, plus international accredited bodies) already actively market and sell SABER filing/consultancy services with SEO-optimized content targeting exactly the queries a small importer would search, on top of an already-cheap, fixed government fee (~SAR 350-575), leaving very thin margin for a pure software/document-prep layer. <https://verger-group.com/what-is-the-cost-of-a-saber-certificate-in-2025/> <https://instacertify.com/saber>
- **الخلاصة:** Rejected: certificate issuance is legally restricted to ISO/IEC 17065-accredited bodies (a multi-year, expensive accreditation a solo founder cannot obtain), and the achievable fallback (a document-prep/referral layer) would compete in an already-saturated field of 8-10+ established agencies over an already-cheap, fixed government fee — leaving no viable path to a defensible, solo-buildable business as described.

### ❌ C11 — Social-seller formalization onboarding wizard (Maroof/CR)

- **المشكلة:** The Saudi E-Commerce Law requires anyone selling online — including via a plain website, app, or social-media account — to register a commercial registration and obtain Maroof certification, disclose full pre-purchase information, honor a 7-day return right, localize data storage, and integrate ZATCA e-invoicing once above the VAT threshold — formalizing a large previously-informal population of Instagram/Snapchat/WhatsApp sellers, with penalties up to SAR 1 million.
- **[MAJOR] WEAK_PAIN:** The mandatory core legal step this product wraps (Maroof registration) is confirmed by Maroof's own official account to be free and to take only seconds with a few steps — undercutting the premise that social-media sellers need a paid guided wizard to get through it. The heavier compliance items (CR, ZATCA Fatoorah, 7-day return disclosures) are real, but the flagship 'Maroof onboarding' hook of the product is demonstrably already trivial per the regulator itself. <https://twitter.com/maroof_sa/status/814795734864248834?lang=ar> <https://manayr.com/%D8%B7%D8%B1%D9%8A%D9%82%D8%A9-%D8%A7%D9%84%D8%AA%D8%B3%D8%AC%D9%8A%D9%84-%D9%81%D9%8A-%D9%85%D8%B9%D8%B1%D9%88%D9%81/>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** No demand evidence was found anywhere (freelance marketplaces, forums) for a paid all-in-one formalization wizard specifically. The only paid analogues found are cheap human facilitation agencies for the underlying free/near-free government paperwork (Maroof cert ~75 SAR via Lahint, CR issuance ~200 SAR via agencies) — evidence people pay humans for a small annoying task, not that they would buy a SaaS product for it. The dossier's own payment_validator independently reached the same PARTIAL/unproven conclusion. <https://lahint.sa/ar/services/issuance-of-maarouf-certificate>
- **الخلاصة:** Killed on two MAJOR, evidence-backed grounds: the flagship mandatory step (Maroof) is officially free and near-instant per Maroof's own account, and no evidence of demand for a paid wizard product (vs. cheap human facilitation of adjacent paperwork) was found anywhere.

### ❌ C12 — AI product-listing generator for Salla/Zid merchants

- **المشكلة:** Salla/Zid e-commerce merchants repeatedly hire freelancers to manually upload products and write product descriptions to their online stores — a recurring, bulk data-entry task with documented existing spend (~200 per batch, currency unconfirmed).
- **[FATAL] STRONG_COMPETITOR:** A direct AI competitor (ListaPro.ai) already exists live, paid, and positively reviewed, distributed through both Salla's and Shopify's official app stores — the exact discovery channel this candidate would need. It performs near-identical AI product-listing creation (from barcodes/images) plus multi-channel/inventory sync, with flexible subscription pricing. Additionally, Salla's own first-party 'Store Tools – AI Describer' app is embedded directly in the merchant dashboard merchants already use, giving zero-friction, trusted incumbency on top of the third-party competitor. Two independent, already-distributed players covering the same job leaves no credible wedge for a solo founder entering head-on with the same 'AI generates Arabic listings' pitch. <https://apps.salla.sa/en/app/1532783652> <https://listapro.ai/pricing/> <https://apps.shopify.com/lista-pro> <https://apps.salla.sa/en/app/709062167>
- **الخلاصة:** FATAL STRONG_COMPETITOR: a live, paid, reviewed AI listing app (ListaPro) already occupies this exact niche in both Salla's and Shopify's official app stores, compounded by Salla's own native AI Describer tool — leaving no credible wedge for the product as currently scoped.

### ❌ C13 — Progress-payment (mustakhlas) tracking tool for contractors/subcontractors

- **المشكلة:** Contractors and subcontractors face chronic delays receiving payment against progress certificates (مستخلصات), creating cash-flow squeezes; they currently track % completion, amounts due and deductions in manual Excel sheets, using WhatsApp to send photos of completed work as proof for owner/consultant approval, sometimes commissioning freelancers to build custom mustakhlas trackers.
- **[MAJOR] STRONG_COMPETITOR:** At least six dedicated Saudi/Arabic contractor ERP or accounting products already explicitly market مستخلصات (progress-payment certificate) tracking features: Daftra, Bonyan ERP, Buildo, Orchida Soft, Sdeed, and BuildERP (muqawil-erp.com, which has a dedicated 'إدارة المستخلصات' product page). This is a considerably more crowded space than the candidate's original framing suggested. <https://muqawil-erp.com/progress-claims/> <https://bonyan-erp.com/ar/blog/contractor-payment-certificates-how-to-calculate-and-track-them-without-confusion>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** Free مستخلص Excel templates are already abundant and actively distributed — including by an ERP vendor itself (Daftra) as a free lead-generation template, plus multiple standalone free-template sites — matching exactly the manual Excel workaround this candidate targets. Given the candidate's own open question ('would contractors pay for tracking vs. just wanting faster payment') and evidence that the real crisis driver is late owner/government payment orders (not a documentation gap — a named official body reported ~70% of certificates lacked a payment order), a lightweight paid tracker does not address the root cause and competes against free substitutes for the documentation side. <https://www.daftra.com/templates/%D9%86%D9%85%D9%88%D8%B0%D8%AC-%D9%85%D8%B3%D8%AA%D8%AE%D9%84%D8%B5-%D9%85%D9%82%D8%A7%D9%88%D9%84%D8%A7%D8%AA> <https://www.droosmep.com/2024/10/contracting-invoice-excel-sheet-sample.html> <https://www.argaam.com/ar/article/articledetail/id/502380>
- **الخلاصة:** Killed on two MAJOR grounds: a more crowded competitive field of established مستخلصات-tracking ERPs than originally assessed, plus strong evidence that free Excel templates already satisfy the documentation workaround while the real driver of the pain (~70% of certificates lack a payment order, per an official body) is a payment/financing problem no tracking software fixes.

### ❌ C14 — Arabic/Gulf-dialect transcription & meeting-minutes tool

- **المشكلة:** Saudi/Gulf clients pay per-hour for manual Arabic audio transcription (meetings, interviews, lectures) via freelance marketplaces, despite modern ASR tools existing — implying a quality gap or unawareness of AI alternatives for Gulf-dialect audio.
- **[FATAL] STRONG_COMPETITOR:** Munsit is a live, dedicated Gulf/Saudi-dialect (explicitly Najdi and Hijazi) Arabic speech-to-text and meeting-notes product with published, self-serve, pay-as-you-go pricing starting at roughly $0.129 per audio hour (~$8/month for ~100 minutes) — dramatically cheaper than the ~$5/audio-hour freelancer rate this candidate is built to undercut. It ships mobile apps on Google Play and the App Store, claims #1 ranking on the HuggingFace open Arabic ASR leaderboard, and offers structured meeting notes (speakers, action items, Arabic summary) matching this candidate's exact proposed feature set. This leaves essentially no price, feature, or distribution wedge for a solo founder entering head-on. <https://munsit.com/> <https://munsit.com/blog/introducing-munsit-the-first-arabic-speech-to-text-app-built-for-you> <https://play.google.com/store/apps/details?id=com.munsit.android>
- **الخلاصة:** FATAL STRONG_COMPETITOR: Munsit already is the exact proposed product — a live, cheap, self-serve, Saudi/Gulf-dialect-tuned Arabic transcription and meeting-notes tool with mobile app distribution — undercutting the candidate's own price-vs-freelancer value proposition by roughly 40x.

### ❌ C15 — Freelancer invoicing + VAT/ZATCA compliance tool for وثيقة العمل الحر holders

- **المشكلة:** Freelance-document holders are confused about VAT/ZATCA obligations (when to register, how to issue compliant e-invoices as income grows), and also experience buyers delaying payment after delivery of work with no easy way to enforce/track it.
- **[MAJOR] STRONG_COMPETITOR:** The core invoice-generation feature this product is built around is already commoditized and free: multiple ZATCA/VAT-compliant invoice generators are available at no cost (arabtoolbox's own generator is explicitly advertised as free; ALZERP, Fatorli, Fatoora.app similarly free), and free وثيقة العمل الحر invoice templates are also readily available. The underlying وثيقة العمل الحر document itself is also confirmed free to obtain, with VAT only applying above 375,000 SAR/year (a threshold most freelancers likely never cross). <https://arabtoolbox.com/tools/vat-invoice-generator> <https://fawater.net/templates/%D9%81%D8%A7%D8%AA%D9%88%D8%B1%D8%A9-%D8%B9%D9%85%D9%84-%D8%AD%D8%B1>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** The dossier's own payment_validator, after searching for payment evidence, explicitly concluded willingness-to-pay for this specific niche tool is 'PARTIAL at best, weighted toward NO,' and found no evidence at all that anyone pays for the payment-delay/reminder-tracking half of the proposed product — the one differentiator not already covered by free tools or the platform-native (free) Khamsat/Mostaql escrow mechanism. <https://khamsat.com/community/general/387001-%D9%85%D8%B4%D8%A7%D9%83%D9%84-%D8%AA%D8%A3%D8%AE%D8%B1-%D8%A7%D9%84%D9%85%D8%B4%D8%AA%D8%B1%D9%89-%D9%81%D9%89-%D8%A7%D9%84%D8%AF%D9%81%D8%B9-%D8%A8%D8%B9%D8%AF-%D8%A7%D9%86%D8%AA%D9%87%D8%A7%D8%A1-%D8%A7%D9%84%D8%AE%D8%AF%D9%85%D8%A9>
- **الخلاصة:** Killed on two MAJOR grounds: the core invoicing feature is already free and commoditized across multiple tools, and the dossier's own payment validation concluded willingness-to-pay is weighted toward NO with zero evidence anyone pays for the proposed payment-reminder differentiator.

### ❌ C16 — AI-assisted Saudi-market CV/cover-letter generator

- **المشكلة:** Job seekers in the Saudi market actively pay freelancers/services (from ~$5 up to full packages) to write professional CVs tailored to Saudi job applications, rather than write their own.
- **[FATAL] STRONG_COMPETITOR:** NoorCV is a genuinely free (no premium tier, no hidden costs, no credit card ever) bilingual AR/EN AI resume builder explicitly built for Gulf professionals with Saudi-specific fields (visa status, nationality) and real user testimonials confirming actual usage/job outcomes. This is not a hypothetical competitor — it is free, well-localized, and serves the exact same customer (Saudi/Gulf job seeker wanting an AI-assisted bilingual CV) as the candidate. Combined with StylingCV, Hash Resume, Seera AI (all bilingual, Saudi-facing) and the fact that ChatGPT itself does this task for free, the core 'AI CV builder for Saudi market' concept has no scarcity value. The candidate's only proposed wedge (deep Saudi GOV-sector tailoring, WhatsApp delivery) is unverified and speculative, not evidenced. <https://noorcv.com/> <https://ai.stylingcv.com/saudi-arabia> <https://lambacv.com/>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** The human-freelancer segment of this exact market is already commoditized down to $5/CV on Khamsat (confirmed live gig), and multiple fully free AI tools exist with real testimonials. The proposed 10-30 SAR one-time fee sits in a very thin margin band squeezed between free (NoorCV/ChatGPT) and $5 human freelancers, with no proof buyers will choose a paid AI tool over either free option. <https://khamsat.com/writing/resume-writing/676212-%D8%B9%D9%85%D9%84-%D8%B3%D9%8A%D8%B1%D8%A9-%D8%B0%D8%A7%D8%AA%D9%8A%D8%A9-%D8%A7%D8%AD%D8%AA%D8%B1%D8%A7%D9%81%D9%8A%D8%A9-%D9%85%D9%82%D8%A7%D8%A8%D9%84-5-%D8%AF%D9%88%D9%84%D8%A7%D8%B1> <https://noorcv.com/>
- **الخلاصة:** Killed primarily on STRONG_COMPETITOR: a fully free, well-localized, real-usage-confirmed Gulf/Saudi bilingual AI CV builder (NoorCV) already exists alongside several other free/cheap tools, squeezing out room for a paid entrant at the proposed 10-30 SAR price point, compounded by an already-commoditized $5 freelancer market (NO_WILLINGNESS_TO_PAY).

### ❌ C17 — Multi-domain AI consumer/tenant complaint-drafting assistant

- **المشكلة:** Consumers and tenants repeatedly have real grievances — gym membership refund refusals, landlord non-registration/rent-freeze disputes on Ejar, MoC-flagged online-store return/exchange violations, delayed/lost shipments — but find official complaint channels (CST, REGA/Najiz, Balagh Tijari, Consumer Protection Association) confusing enough to sustain a whole cottage industry of paid law-firm content explaining how to file each type of complaint.
- **[MAJOR] REGULATORY:** The candidate's own feasibility validator flagged HIGH severity risk under Nizam al-Muhamah (Law Practice System): drafting formal complaint/legal text for consumers risks being characterized as unauthorized legal practice, which is restricted to licensed Bar-registered lawyers. Across FOUR different dispute domains (rental, gym, e-commerce, delivery) each with evolving rules, a solo non-lawyer founder faces real exposure and a nontrivial content-accuracy maintenance burden with no legal training. <https://sba.gov.sa/wp-content/uploads/2022/05/%D9%86%D8%B8%D8%A7%D9%85-%D8%A7%D9%84%D9%85%D8%AD%D8%A7%D9%85%D8%A7%D8%A9-%D9%88%D9%84%D8%A7%D9%8A%D9%94%D8%AD%D8%AA%D9%87-%D8%A7%D9%84%D8%AA%D9%86%D9%81%D9%8A%D8%B0%D9%8A%D8%A9.pdf>
- **[MAJOR] STRONG_COMPETITOR:** At least three funded, actively-distributed Arabic AI legal-assistant apps already operate in Saudi Arabia and substantially overlap this exact use-case. Adel alone has 500,000 downloads and a 4.6-star rating (663 ratings), searches 70,000+ Saudi legal documents, and drafts contracts/legal documents. Shwra and Waddah AI add further overlapping coverage (lawsuit drafting, AI-to-lawyer routing). None of these is a cheap/free give-away, but their scale of real usage means a solo founder entering the same 'AI helps you with a legal/complaint problem' space faces an uphill distribution battle against apps with a multi-year head start and six-figure download counts. <https://apps.apple.com/sa/app/adel-your-legal-assistant/id6695754708> <https://shwra.ai/en>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** The underlying government complaint channels this tool would sit on top of (Najiz, Ejar, CST, Balagh Tijari, CPA) are entirely free. The candidate's own payment_validator found NO direct evidence anyone pays specifically for complaint-drafting/document-generation — only adjacent, unrelated evidence (general lawyer consultations at 100-1500 SAR, B2B AI-legal tools sold to lawyers, not consumers). <https://portalservices.cst.gov.sa/E-Services/Complaint/ComplaintFAQ.aspx> <https://www.ejar.sa/en/help>
- **الخلاصة:** Three independent MAJOR risks stack up: real unauthorized-practice-of-law exposure across four evolving legal domains for a non-lawyer solo founder, direct overlap with three already-scaled Arabic legal-AI apps (Adel: 500K downloads), and no evidence of payment for complaint-drafting specifically when the underlying government channels are free.

### ❌ C18 — Musaned domestic-worker recruitment dispute assistant

- **المشكلة:** Households recruiting domestic workers through recruitment offices repeatedly face disputes: offices exceeding the agreed timeframe (often 90+30 days), delivering non-matching workers, refusing deposit refunds, demanding informal fees, or refusing replacement after a worker runs away, forcing families to file formal Musaned complaints.
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** The candidate's own payment_validator explicitly concluded 'no direct evidence anyone pays for a Musaned-specific dispute-help tool.' The official Musaned/HRSD complaint channel is free, government-run, and was recently updated (2025) to shorten resolution times, further reducing the pain a paid tool would need to solve. Only adjacent evidence exists: general legal consultation fees unrelated to this specific workflow. <https://www.musaned.com.sa/ar/faqs/hiring-laborers> <https://www.hrsd.gov.sa/media-center/news/793639>
- **[MAJOR] SMALL_MARKET:** The candidate's own competition_validator explicitly rated this market_state as WEAK_MARKET, noting the niche 'sits between a recently-improved free government process and general-purpose Arabic legal-AI apps that likely already handle this informally,' and that Musaned's 2025 update reportedly reduced resolution time to 3-5 business days, which may have already resolved much of the underlying navigation difficulty this tool targets. <https://www.arrajol.com/content/395665/>
- **الخلاصة:** Two MAJOR, evidence-backed reasons from the dossier's own validators: no proof of willingness to pay against a free, recently-improved government channel, and the competition validator's own WEAK_MARKET assessment. The niche is real but too thin and too adjacent to an already-free, already-improving official process to sustain a paid solo product.

### ❌ C19 — SDAIA Responsible AI compliance assistant for AI/SaaS vendors

- **المشكلة:** SDAIA's Responsible AI Policy (public consultation opened April 2026) would, if finalized, require AI vendors selling to government/regulated sectors to classify their systems into risk tiers (critical/high/limited/low) with documentation, testing and monitoring obligations — a compliance burden small Saudi AI/SaaS vendors cannot fill with in-house legal teams.
- **[FATAL] REGULATORY:** Fresh search confirms the SDAIA Responsible AI Policy consultation closed 3 May 2026 and, as of the most recent available information, 'has not yet been finalized' — nearly five months after consultation close and with today's date (26 Sept 2026) well past that, there is still no binding law, no confirmed enforcement scope, and no confirmed timeline. Building a compliance product against a policy that may still change materially (or never be finalized on a knowable schedule) is premature market timing, not a licence problem per se, but functionally blocks any real near-term customer urgency. <https://digitalpolicyalert.org/event/39093-saudi-data-and-artificial-intelligence-authority-closes-consultation-on-draft-responsible-ai-policy-including-performance-monitoring-requirement> <https://www.spa.gov.sa/en/N2551533>
- **[MAJOR] NO_WILLINGNESS_TO_PAY:** No evidence of any Saudi small/mid AI or SaaS vendor paying for SDAIA-specific compliance tooling today. The only confirmed willingness-to-pay data point is global enterprise-tier AI-governance platforms (Credo AI, $30K-150K+/year) serving large multinationals like Mastercard and McKinsey — an entirely different customer segment and price point than 'small Saudi AI/SaaS vendors,' the candidate's stated target. <https://co-aims.com/blog/credo-ai-review-2026-compliance-officers>
- **[MAJOR] FOUNDER_MISFIT:** The candidate's own feasibility validator explicitly flagged that 'B2B compliance tooling typically requires buyer trust/credibility that an unknown solo founder lacks, especially for government-adjacent risk products; enterprise sales cycles are long' — a direct admission that this business model does not fit a solo founder's realistic go-to-market capability, independent of the regulatory timing issue. 
- **الخلاصة:** This is explicitly a FUTURE_HYPOTHESIS resting on an unfinalized draft regulation (confirmed still not finalized via fresh search, ~5 months after consultation closed), with no current Saudi SME paying customer and a B2B trust/credibility mismatch for a solo unknown founder — multiple independent reasons to reject now, though it could be revisited once the policy is actually finalized and enforcement scope is known.

### ❌ C20 — Subcontractor/skilled-labour matching for Expo 2030 / World Cup 2034 construction

- **المشكلة:** If Expo 2030 (excavation/main works from Q3 2026) and World Cup 2034 construction ramp up as scheduled, small/mid subcontractors and skilled tradespeople will likely face a fragmented, opaque tender/subcontracting market and acute shortages of certified project managers, engineers and skilled labour (Dubai Expo 2020 peaked at 30,000+ onsite contractors), creating demand for tools to match verified subcontractors/workers to giga-project tenders and track compliance documentation.
- **[FATAL] REGULATORY:** Fresh search confirms that providing recruitment/labor-matching services without an MHRSD license is a serious violation carrying fines of SR200,000 (1st offense), SR220,000 (2nd) and SR250,000 (3rd) in Saudi Arabia. A platform that matches individual skilled tradespeople/workers to paid work opportunities plausibly falls within this licensing regime, which is exactly the kind of 'hard licence' the founder constraints explicitly instruct to avoid. <https://saudigazette.com.sa/article/664621/saudi-arabia/saudi-arabia-cracks-down-on-unlicensed-recruitment-services-with-fines-up-to-sr250000> <https://www.hrsd.gov.sa/en/%D8%AA%D9%86%D8%B8%D9%8A%D9%85-%D8%B9%D9%85%D9%84%D9%8A%D8%A7%D8%AA-%D8%A7%D9%84%D8%AA%D9%88%D8%B8%D9%8A%D9%81>
- **[FATAL] FOUNDER_MISFIT:** The candidate's own feasibility validator explicitly concluded solo_founder_feasible: false, rating complexity HARD due to a classic two-sided marketplace cold-start problem (needing both trusted certified-subcontractor supply and main-contractor demand simultaneously) in an industry that is relationship-driven and pre-qualification-based, not open-marketplace-based — an environment where an unknown solo founder has no credibility or existing relationships to break in. 
- **[MAJOR] STRONG_COMPETITOR:** Saudi Arabia already has multiple dedicated, Arabic-native subcontractor/tender-matching platforms (Batengate, Muqawalatgate, Contractor.sa) plus an authority-backed incumbent (Scavo, backed by the Saudi Contractors Authority) and a regional procurement platform (ProTenders) already covering the tender-discovery/subcontractor-connection layer this candidate targets. <https://scavo.sa/>
- **الخلاصة:** Two independent FATAL reasons: a plausible MHRSD recruitment/labor-matching licensing requirement carrying fines up to SR250,000 (exactly the 'hard licence' type founder constraints flag to avoid), and the dossier's own feasibility validator already concluding solo_founder_feasible: false due to an unwinnable two-sided marketplace cold-start problem in a relationship-driven, pre-qualification-based industry — compounded by several already-established Arabic-native competitor platforms.

## 7. قابلية بناء MVP (Buildability of surviving opportunities)

| ID | الفرصة | Complexity | MVP cost (SAR) | Monthly (SAR) | Build (weeks) | Solo? | Someone pays now? | Market |
|---|---|---|---|---|---|---|---|---|
| C10 | PDPL compliance self-serve SaaS for SMEs | **EASY** | 500–900 | ~150-250 SAR (hosting + Claude API usage) | 3-5 | True | PARTIAL | COMPETITIVE |
| C01 | ZATCA e-invoicing (Fatoora) compliance micro-tool for micro/small merchants | **MODERATE** | 500–1000 | ≈150-400 SAR (hosting/DB + optional WhatsApp BSP fees; scales with invoice volume; Moyasar has no fixed monthly fee, only the 2.5% transaction cut) | 6-8 | True | YES | COMPETITIVE |
| C04 | AI-assisted bookkeeping, reconciliation & invoice-data-entry automation for micro-SMEs | **MODERATE** | 500–1000 | ≈150-350 SAR (hosting + pay-per-page OCR/LLM vision API costs, scales with document volume) | 6-9 | True | YES | WEAK_MARKET |
| C08 | Lightweight field-service management for micro maintenance/facilities companies | **MODERATE** | 600–1300 | ~300-450 SAR (hosting ~100 SAR + WhatsApp BSP ~200 SAR + optional Maps API usage) | 5-7 | True | PARTIAL | WEAK_MARKET |

> الأولوية لفرص **EASY** ثم **MODERATE**.

## 8. قائمة الانتظار (Backlog — لم تدخل التحقق)

- Vetted tutor marketplace with transparent pricing — _Crowded space (My Teacher, معلم السعودية, 3oloomonline, mo3alemon, hamadacademy already operating); weak evidence on actual willingness to pay a platform fee on top of tutor rate._ (S017, S097)
- Home maintenance (AC/plumbing/electrical) booking marketplace — _Fragmented but already has funded competitors (Serve, GARO); weak evidence and unclear differentiation path for a solo founder._ (S016)
- Madrasati parent companion/notification app — _Madrasati is login-gated (technically risky/hard to build against); weak evidence parents would pay for a convenience layer on a free mandatory government platform._ (S018)
- Vehicle document/fine reminder app (Istimara, insurance) — _Absher already shows this information for free if users check; weak monetization evidence and no API confirmed for pulling personal data._ (S020)
- Pet services aggregator/marketplace — _Weak evidence throughout, unverified market size (pet ownership rate not confirmed), low severity._ (S022)
- Wedding/event vendor comparison platform — _Low frequency (one-off purchase per family), weak evidence, existing directory (zafaf.net) may already capture demand._ (S023)
- Hidden telecom VAS subscription-charge detector — _Thin monetization potential (small per-charge amounts), and CST regulatory pressure may shrink this pain over time._ (S025)
- Multi-platform real-estate listing syndication for small brokers — _Weak evidence on contract terms/pricing and existing agency size affected; unclear differentiation vs existing CRM tools._ (S028)
- Installment-plan tracker for retail/service businesses — _Single-agent evidence only (whatsapp_excel_hunter), weak on willingness to pay recurring SaaS vs one-time Excel; possible overlap with regulated BNPL rules if touching payment collection._ (S031)
- Supplier/customer ledger tracker for wholesale/retail — _Single-agent evidence, weak differentiation from existing lightweight accounting tools already on the market._ (S035)
- Wholesale field sales rep (مندوبين) tracking app — _Weak evidence on incumbent (MEST/Kashier) pricing and unclear size of underserved micro-distributor segment._ (S034)
- Home-based tailoring/custom-order tracking mini-app — _Small niche market, weak evidence, customers show a preference for one-off freelance builds over recurring subscriptions._ (S036)
- WhatsApp-native collections/dunning workflow tool — _Weak evidence on company-size threshold that would adopt vs. existing ERP AR modules; regulatory constraints on automated debt-collection messaging unresearched._ (S042)
- AI document intake/classification tool for construction document controllers — _Weak evidence on whether target contractors already pay for Aconex/Procore-class EDMS; unclear minimum contractor size for adoption._ (S045)
- Supplier RFQ/quote-comparison tool for procurement coordinators — _Weak evidence; risk that target companies already use ERP procurement modules (SAP Ariba) making a point tool redundant._ (S046)
- Arabic FAQ/status-check deflection bot for call centers — _Weak evidence on what fraction of call volume is truly deflectable; likely competes with enterprise CCaaS platforms already in use._ (S047)
- Bilingual proposal+contract+ZATCA-invoice tool for freelancers/consultants — _No direct complaint evidence, purely inferred from a feature gap versus Bonsai/HoneyBook; overlaps partially with C15 freelancer tool._ (S050)
- Legal practice management SaaS for solo Saudi lawyers — _Unknown market size and unverified whether solo lawyers even use software vs. manual/paper processes; no evidence of demand._ (S053)
- Low-cost ZATCA-compliant POS alternative to Foodics — _Foodics is a dominant, well-resourced incumbent; requires POS hardware/infrastructure which raises MVP difficulty above the founder's preferred EASY/MODERATE tier._ (S054)
- Analytics/inventory add-on for Salla/Zid lower-tier merchants — _Weak evidence; likely that merchants simply upgrade Salla/Zid plans rather than buy a separate add-on._ (S055)
- School admin tool bridging duplicate Noor/Madrasati data entry — _Weak evidence (single vendor blog anecdote), true scale of the problem beyond marketing claims not established._ (S057)
- Flat-fee bundled accounting+POS+payroll for small retailers (Qoyod alternative) — _Pricing evidence sourced from a competitor's marketing comparison, not verified; low confidence in real switching willingness._ (S058)
- No-code starter bundle (booking+store+content) for multi-service entrepreneurs — _Based on a single anecdotal freelance project posting; unclear if this is a recurring pattern._ (S060)
- E-commerce accounting/marketplace integration middleware (Odoo/Noon/Amazon connectors) — _Evidence sourced primarily from a single agent (gap_hunter); biggest unknown is whether Noon/Amazon.sa even expose usable seller-side APIs, which is unverified and could make this unbuildable._ (S061, S062, S066)
- WhatsApp-to-any-POS/booking middleware for small service businesses — _Overlaps with C05 booking-tool cluster; unclear whether businesses want an unbundled WhatsApp-only layer vs. a full suite._ (S065)
- NPHIES ICD-10-AM/ACHI coding-assist AI for hospital claims — _Requires deep healthcare-data handling (PDPL, hospital EMR/HIS integration), which is a HARD MVP well beyond solo-founder/500-1000 SAR budget constraints per the agent's own note._ (S071)
- AI contract-review tool for commercial/employment contracts — _Significant unauthorized-practice-of-law risk in Saudi Arabia; no direct first-hand complaint evidence, only inferred from a feature gap._ (S074)
- White Land and Vacant Property Tax calculator — _Very niche customer base (owners of ≥5,000 m² parcels), low frequency (annual, one-time check), unclear if a structured zone-rate dataset is publicly buildable from._ (S082)
- Affordable hotel-ops/revenue-management SaaS for independent hotels (World Cup 2034) — _FUTURE_HYPOTHESIS; global hotel-ops SaaS market (Cloudbeds, Mews) is crowded, unclear localization gap size, and delivery pace vs. 2034 deadline uncertain._ (S086)
- Open-banking-powered SME cash-flow/personal finance app — _FUTURE_HYPOTHESIS; unclear whether building any app touching financial account data triggers its own licensing requirement even without holding a SAMA licence directly._ (S088)
- CHI health-insurance tier comparison/compliance tool for SME HR — _FUTURE_HYPOTHESIS; insurance brokers may already offer this comparison for free, reducing willingness to pay._ (S089)
- Employer-childcare nursery matching + Qurrah subsidy tool — _FUTURE_HYPOTHESIS; exact employer-size threshold/enforcement mechanism for the childcare mandate is unclear, and Qurrah may already include a matching tool._ (S090)
- Booking/itinerary tool for independent tour guides ahead of tourism growth — _FUTURE_HYPOTHESIS; unclear whether independent guides can legally operate without a licensed DMC, and international OTAs may already fill this niche._ (S091)
- Crowdsourced EV charger-status app + EV-service marketplace — _FUTURE_HYPOTHESIS; global apps like PlugShare may already have adequate Saudi coverage, and EV adoption pace is uncertain._ (S092)
- Lightweight family-business succession/governance SaaS — _FUTURE_HYPOTHESIS; unclear whether small family-business owners would trust software vs. wanting a human advisor for sensitive ownership matters._ (S093)
- End-of-service benefit (مكافأة نهاية الخدمة) dispute checker — _Low frequency (one-time event per employee), existing free calculators (Jisr/ZenHR/Bayzat, GOSI FAQ) already partly serve this need._ (S098)
- School bus real-time tracking for smaller private schools — _Established incumbent (Busway) already serves this; B2B2C sales cycle (selling to schools) is a harder go-to-market for a solo founder than direct-to-consumer or self-serve B2B._ (S101)

**مستبعدة مبكرًا من Consolidator:**
- S006: This is a structural labor-market/sponsorship-regulation constraint (نقل كفالة), not a software-solvable gap; the originating agent itself flagged it as 'closer to a structural labor-market constraint' with no direct driver complaint evidence found.
- S039: Independent event guest-list/RSVP management is already well served by named dedicated competitors (ضيفان/Dhaifan, مناسبتي) with low frequency and low severity; no clear differentiation opportunity for a solo entrant per the originating agent's own assessment.

## 9. قيود البحث (Research Limitations)

### قيود النظام
- WebSearch هو محرك البحث المدمج في Claude Code (فهرس مركزه الولايات المتحدة)؛ تغطية المحتوى العربي/السعودي المحلي أقل من Google في السعودية.
- منصات X و TikTok و LinkedIn و Instagram و Snapchat تتطلب تسجيل دخول غالبًا؛ استُخدم فقط ما يظهر في نتائج البحث العامة، ولم يتم تجاوز أي حماية.
- لا توجد مفاتيح APIs مدفوعة (SerpAPI / Google / X API)؛ جميع البيانات من صفحات عامة.
- تقييمات الوكلاء (تصنيف الأدلة، التعقيد، التكلفة) هي أحكام نموذج لغوي مبنية على المصادر المذكورة، وليست دراسات سوق ميدانية.
- لم يتم التواصل مع أي عميل أو شركة؛ لم تُختبر رغبة الدفع مباشرة — هذه أول خطوة يجب أن يقوم بها المؤسس.
- الروابط المذكورة شوهدت من قبل الوكلاء أثناء التشغيل، لكن صفحات الويب تتغير؛ تحقق من الأسعار قبل الاعتماد عليها.

### قيود أبلغ عنها الوكلاء

- problem_hunter: WebFetch tool failed for all attempted URLs in this session ('proxy refused the connection') — all evidence below is based on WebSearch result snippets only, not on directly fetched/verified page content; claims are labeled 'per search snippet' accordingly.
- problem_hunter: Reddit content (r/saudiarabia, r/riyadh) did not surface in Google-indexed search results for any of the site:reddit.com queries tried — likely limited indexing; could not directly observe Reddit complaint threads.
- problem_hunter: Search budget (12/12) was exhausted before domains like school registration (Noor), traffic-fine disputes, and neighbor/noise complaints could be explored in depth — these were touched but evidence was too thin (official pages only, no complaint threads) to include as standalone signals.
- problem_hunter: No pricing pages were fetched, so existing_spend amounts are mostly 'NO RELIABLE EVIDENCE FOUND' even where paid vendors clearly exist.
- problem_hunter: X/TikTok/Instagram/LinkedIn content was not directly accessible; only what appeared in Google search snippets was used (e.g., one TikTok/X result for Absher FAQs, not used as evidence).
- b2b_hunter: All 4 WebFetch attempts in this session failed with 'proxy refused the connection' — could not verify any page beyond what appeared in WebSearch snippets. This means every evidence item is based on search-snippet text only, not full-page verification.
- b2b_hunter: Search budget (12) was used entirely on WebSearch; no fetch-based cross-checking of pricing pages, government portals, or primary regulation text was possible.
- b2b_hunter: Found no Saudi-specific data on restaurant no-show rates/fees (search only returned global/UAE data), so no restaurant no-show signal was included despite it being a suggested sector.
- b2b_hunter: Could not access Mostaql/Khamsat freelance-request listings directly (search returned vendor SEO pages instead of actual freelance job posts), so direct demand-signal evidence from those platforms is missing.
- b2b_hunter: No pricing data (SAR figures customers currently pay) was found with strong evidence for most signals — existing_spend fields are mostly marked LOW confidence or NO RELIABLE EVIDENCE FOUND.
- b2b_hunter: Government portal accessibility (Qiwa, ZATCA Fatoora, Ejar) for third-party API integration by a solo founder was not verified — a key feasibility unknown for several signals.
- b2c_hunter: All 6 WebFetch attempts failed (proxy refused connection / budget exhausted before any page content could actually be retrieved), so every piece of evidence in this run is based on WebSearch snippets only, not full-page verification — evidence_type was downgraded to WEAK across the board to reflect this, per the evidence discipline rules.
- b2c_hunter: Could not verify actual prices, review counts/ratings, or download numbers for any app mentioned (Madrasati, gym apps, VetWay, Fustog, Mqadi, Serve, etc.) because fetches were unavailable.
- b2c_hunter: X/TikTok/Reddit/Instagram content is largely login-gated or returned no Saudi-specific threads in the searches run; consumer complaint volume for several signals (gym refunds, Ejar registration, domestic worker fraud) could not be quantified.
- b2c_hunter: 12/12 web searches and 6/6 web fetches were used; no further verification possible within this session's budget.
- b2c_hunter: Dropped a grocery price-comparison signal after finding 3 existing free apps (Fustog, Mqadi, Pricena) already serving this need with no clear monetization gap for a new solo entrant — judged too saturated to include as a strong opportunity.
- b2c_hunter: Dropped a domestic-worker-fraud-verification idea as too speculative (only government warning articles found, no evidence of a paid product gap).
- complaint_hunter: All 6 WebFetch attempts in this session failed with 'proxy refused the connection', so every claim in this run is based on WebSearch tool result snippets/synthesis rather than a personally-verified full page fetch; where this matters, evidence_type has been downgraded (WEAK) and noted in the summary.
- complaint_hunter: Search budget (12) was exhausted before I could run planned follow-up queries on: existing Saudi vehicle-history-report competitors (relevant to CMP-03), Jahez/HungerStation food-delivery complaint volume, and exact CST telecom-complaint statistics breakdown.
- complaint_hunter: site:reddit.com/r/saudiarabia search returned no on-topic results — Reddit content on this specific topic was not indexed/surfaced for this query wording; did not get to retry with alternate phrasing.
- complaint_hunter: X/TikTok/Instagram complaint threads are login-gated and were not accessible; only what surfaced in Google-style search snippets was used.
- complaint_hunter: No Arabic-language pricing evidence was found for any of the law-firm 'file a complaint' consultation services referenced in CMP-04/CMP-06, so existing_spend for those signals remains unverified beyond the fact that paid legal services around these pains exist.
- whatsapp_excel_hunter: Search budget (12) was fully exhausted; a 13th planned query on delivery/driver tracking for small logistics businesses could not be run.
- whatsapp_excel_hunter: Both attempted WebFetch calls (to mostaql.com and khamsat.com pages) failed with 'proxy refused the connection' — could not verify exact page content, dates, or freelance job prices beyond search-result snippets.
- whatsapp_excel_hunter: No exact prices/dates could be confirmed for any Mostaql/Khamsat listing cited (all marked 'unknown' date and NO RELIABLE EVIDENCE FOUND for cost) — evidence is snippet-level (STRONG_INDIRECT/DIRECT per the snippet itself, but unverified at source).
- whatsapp_excel_hunter: Could not check Reddit (r/saudiarabia, r/riyadh) or Twitter/X complaints directly within budget — coverage relied on Mostaql/Khamsat freelance requests and vendor marketing pages.
- whatsapp_excel_hunter: Sectors not explored due to budget limits: car rental, home bakeries/food businesses, small logistics/last-mile delivery, gyms/tutoring — plausible WX signals may exist there but were not verified.
- whatsapp_excel_hunter: Could not confirm whether cited Mostaql/Khamsat listings are recent (2024-2026) or older, since fetch to view posting dates failed.
- jobs_signal_hunter: All WebFetch attempts in this session failed with 'proxy refused the connection', so no job postings or salary pages could be directly fetched/confirmed beyond search-engine snippets — every claim below is 'per search snippet' evidence (STRONG_INDIRECT/WEAK), not DIRECT page verification.
- jobs_signal_hunter: No access to gated LinkedIn full job descriptions, Bayt full listings, or Jadarat government listings beyond snippet text.
- jobs_signal_hunter: Could not verify actual salary figures for most roles (HR coordinator, collections officer, government relations coordinator, procurement coordinator, call center agent) — only Document Controller and Quantity Surveyor had usable salary snippets.
- jobs_signal_hunter: Mostaql/Khamsat searches surfaced limited Saudi-specific (vs pan-Arab/Egypt) freelance demand; hard to isolate Saudi-only signal from broader Arabic freelance market.
- jobs_signal_hunter: Reached the 12-search budget before covering leasing-coordinator and quantity-surveyor pain points as deeply as HR/collections/document-controller; those two are underdeveloped and were dropped from final signals for lack of strong evidence.
- jobs_signal_hunter: No forum/Reddit-level complaint evidence gathered in this run; signals rely entirely on job-board listing volume and salary data as proxies for pain, per this agent's mandate.
- foreign_model_hunter: WebFetch tool failed for every attempted URL in this session ('proxy refused the connection') — including Fresha pricing, Yarn.com.sa PMS comparison, ZATCA solution providers directory, and Jobber/Housecall Pro comparison pages. All evidence below therefore relies on WebSearch result snippets rather than directly fetched/verified page content, which is reflected in downgraded evidence_type (mostly WEAK/STRONG_INDIRECT) and lower confidence scores.
- foreign_model_hunter: Search budget was exhausted at 14/14 queries; the 15th query ('بديل Clio السعودية') returned a budget-exhausted error and was not executed as a separate search — evidence for FM-06 relies only on the earlier Clio query.
- foreign_model_hunter: Several categories investigated (restaurant inventory — dominated by Foodics; employee attendance/scheduling — served by Bayzat/Jisr/Daftra; dental clinic management — served by Dentolize/DentoSoft/Cloudpital; gym management — already used via global tools in KSA/UAE per search) appeared to already have adequate local or regional solutions, so they were deliberately excluded as signals rather than forced into weak opportunities.
- foreign_model_hunter: No Arabic-language forum/Reddit/Mostaql/Khamsat complaint threads were found or examined directly for any of these categories within the search budget — all 'pain' signals are inferred from competitor/localization-gap analysis rather than first-hand user complaints, which is the weakest form of pain evidence per the evidence discipline rules.
- foreign_model_hunter: Could not verify actual Saudi pricing, customer counts, or spend for any of the foreign tools (Bonsai, HoneyBook, Clio, Podium, Birdeye, Mindbody, GymMaster) specifically in the Saudi market — all customer/revenue figures found are global, not KSA-specific.
- competition_hunter: All 6 WebFetch attempts failed with 'proxy refused the connection' errors, exhausting the fetch budget with zero successful fetches — every claim below relies on WebSearch result snippets/AI summaries rather than directly verified page content, which is lower-confidence than normal DIRECT evidence.
- competition_hunter: No access to G2/Capterra actual review text, app store review counts, or Reddit/X threads with direct user complaints — could not confirm complaint volume or recency for Foodics, Jisr, Qoyod, or Salla/Zid.
- competition_hunter: Could not verify current pricing pages directly (Qoyod, Wafeq, Foodics, Salla, Zid) since fetches failed; all pricing figures are as reported by third-party comparison blogs (some of which are competitors, i.e. potentially biased).
- competition_hunter: Several vendor 'pain point' descriptions (school Noor duplication, Ejar renewal pain) come from marketing blogs of companies selling the very solution to that pain, which is a conflict-of-interest source and only WEAK evidence.
- competition_hunter: No Arabic-language Reddit/forum complaint threads were surfaced in the searches actually run; Arabic queries returned mostly SEO/comparison content rather than user complaints.
- competition_hunter: 12/12 search budget and 6/6 fetch budget fully used; could not cross-check or deepen any single finding further.
- gap_hunter: WebFetch tool failed with 'proxy refused the connection' for every attempted fetch in this session (3 attempts), so all evidence below is based on WebSearch result snippets only, not verified full-page content — this is flagged per-claim as WEAK evidence and noted explicitly.
- gap_hunter: Web search budget (12 queries) was exhausted before I could run planned searches on NPHIES/insurance-claims integration pain and direct job-board evidence (Bayt/LinkedIn) for Salla/Zid API developer hiring demand — these lines of inquiry are not covered in the signals.
- gap_hunter: Mostaql/Khamsat project pages could not be opened to see actual budgets, full briefs, or client responses (only titles/snippets from search results were visible), so demand strength (how much money actually changes hands) is under-verified.
- gap_hunter: Shipping-company integration (SMSA/Aramex) with Salla/Zid appears to already be natively solved via official help-center articles found in this session, so it was excluded as a live opportunity rather than forced into a signal.
- gap_hunter: Could not verify whether Noon.com or Amazon.sa expose any public seller APIs — GAP-06 is speculative and should be treated as the weakest signal in this set pending API-availability confirmation.
- gap_hunter: No direct consumer/business complaint threads (Reddit, X, forums) were found for the Qiwa/Mudad/GOSI sync pain (GAP-04) — evidence there is vendor-blog content only, not a demonstrated freelancer/complaint market.
- ai_opportunity_hunter: All 6 WebFetch attempts in this session failed with 'proxy refused the connection' — could not verify pricing pages, full article stats, or exact posting dates on primary sources (Mostaql projects, NPHIES rejection article, Wafeq, Dello.ai). All evidence for this reason relies on WebSearch snippets only, explicitly marked 'per search snippet' where relevant.
- ai_opportunity_hunter: Reached the 12-search budget limit; did not get to explore additional candidate families (e.g. tender/RFQ generation depth, meeting-minutes-specific enterprise demand, Arabic customer-support ticket classification) as thoroughly as desired.
- ai_opportunity_hunter: Could not confirm exact freelancer/vendor prices for most signals (Mostaql/Khamsat listings typically hide budgets behind login or require fetch, which failed) — existing_spend is mostly marked as unconfirmed or NO RELIABLE PRICE EVIDENCE FOUND.
- ai_opportunity_hunter: Could not verify PDPL/health-data or unauthorized-practice-of-law regulatory constraints directly from official .gov.sa sources within budget — these remain flagged as unknowns.
- ai_opportunity_hunter: No access to X/TikTok/LinkedIn/Instagram content (login-gated), so signals rely on Mostaql/Khamsat/Google-indexed vendor pages only.
- market_change_hunter: All WebFetch calls failed this session ('proxy refused the connection'), so every claim is sourced from search-result snippets only, not from directly fetched/verified pages — summaries note this where relevant.
- market_change_hunter: Search budget (12) was fully exhausted before I could verify existing-solution pricing (e.g., Qoyod/Fatora subscription costs) or find dedicated SaaS tools for White Land Tax and PDPL compliance in the Saudi market specifically.
- market_change_hunter: Could not verify via primary government sources (only via secondary law-firm/vendor blogs and news aggregators) for most regulatory details — dates and thresholds should be re-confirmed against official ZATCA/MHRSD/SDAIA/MoMaH/TGA pages before acting.
- market_change_hunter: Freelance permit (العمل الحر) research did not surface strong pain/complaint evidence — it appears to be a low-friction, largely automated government service, so it was not included as a standalone signal.

### فحص الروابط (URL integrity check)

✅ كل الروابط في الأقسام التجميعية مصدرها وكلاء البحث في هذا التشغيل (لم يُضف المُجمِّع روابط جديدة).

## 10. سجل تنفيذ الوكلاء (Agent Execution Log — proof of real runs)

كل صف = مهمة Agent نُفّذت كعملية مستقلة `claude -p` (PID وsession مستقلان). السجل الكامل: `logs/full_20260926/run.log` · النصوص الكاملة: `results/full_20260926/transcripts/`

| # | Agent | Task | Stage | Status | Attempts | PID | Session | Start | Dur (s) | Searches | Fetches | Cache hits | Cost $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | jobs_signal_hunter | jobs_signal_hunter | discovery | ok | 1 | 2285 | b10c5c55 | 10:42:01 | 154.2 | 12 | 5 | 0 | 0.511 |
| 2 | b2c_hunter | b2c_hunter | discovery | ok | 1 | 2281 | b10c5c55 | 10:42:01 | 201.4 | 12 | 6 | 0 | 0.584 |
| 3 | problem_hunter | problem_hunter | discovery | ok | 1 | 2280 | b10c5c55 | 10:42:01 | 222.4 | 12 | 6 | 0 | 0.590 |
| 4 | b2b_hunter | b2b_hunter | discovery | ok | 1 | 2282 | b10c5c55 | 10:42:01 | 223.9 | 12 | 4 | 0 | 0.587 |
| 5 | whatsapp_excel_hunter | whatsapp_excel_hunter | discovery | ok | 1 | 2284 | b10c5c55 | 10:42:01 | 245.5 | 12 | 2 | 0 | 0.648 |
| 6 | complaint_hunter | complaint_hunter | discovery | ok | 1 | 2283 | b10c5c55 | 10:42:01 | 259.1 | 12 | 6 | 0 | 0.633 |
| 7 | foreign_model_hunter | foreign_model_hunter | discovery | ok | 1 | 2968 | b10c5c55 | 10:44:36 | 250.8 | 14 | 4 | 0 | 0.678 |
| 8 | gap_hunter | gap_hunter | discovery | ok | 1 | 3188 | b10c5c55 | 10:45:44 | 220.0 | 12 | 3 | 0 | 0.604 |
| 9 | ai_opportunity_hunter | ai_opportunity_hunter | discovery | ok | 1 | 3222 | b10c5c55 | 10:45:45 | 221.1 | 12 | 5 | 0 | 0.610 |
| 10 | competition_hunter | competition_hunter | discovery | ok | 1 | 3100 | b10c5c55 | 10:45:23 | 257.9 | 12 | 6 | 0 | 0.623 |
| 11 | future_opportunity_hunter | future_opportunity_hunter | discovery | ok | 1 | 3431 | b10c5c55 | 10:46:21 | 211.1 | 10 | 3 | 0 | 0.515 |
| 12 | market_change_hunter | market_change_hunter | discovery | ok | 1 | 3356 | b10c5c55 | 10:46:07 | 250.1 | 12 | 3 | 0 | 0.621 |
| 13 | individual_problem_hunter | individual_problem_hunter | discovery | ok | 1 | 3794 | b10c5c55 | 10:48:46 | 210.5 | 12 | 5 | 0 | 0.598 |
| 14 | consolidator | consolidator | dedup | ok | 1 | 4087 | b10c5c55 | 10:52:17 | 396.0 | 0 | 0 | 0 | 0.699 |
| 15 | payment_validator | batch1 | validation | ok | 1 | 4388 | b10c5c55 | 10:58:53 | 158.5 | 11 | 2 | 0 | 0.557 |
| 16 | evidence_validator | batch1 | validation | ok | 1 | 4386 | b10c5c55 | 10:58:53 | 178.1 | 11 | 0 | 0 | 0.588 |
| 17 | payment_validator | batch2 | validation | ok | 1 | 4391 | b10c5c55 | 10:58:53 | 179.7 | 14 | 6 | 0 | 0.624 |
| 18 | evidence_validator | batch2 | validation | ok | 1 | 4390 | b10c5c55 | 10:58:53 | 236.5 | 14 | 3 | 0 | 0.720 |
| 19 | evidence_validator | batch3 | validation | ok | 1 | 4389 | b10c5c55 | 10:58:53 | 237.4 | 14 | 4 | 0 | 0.694 |
| 20 | evidence_validator | batch4 | validation | ok | 1 | 4387 | b10c5c55 | 10:58:53 | 256.9 | 11 | 2 | 0 | 0.594 |
| 21 | payment_validator | batch3 | validation | ok | 1 | 5092 | b10c5c55 | 11:01:32 | 148.4 | 13 | 4 | 0 | 0.575 |
| 22 | payment_validator | batch4 | validation | ok | 1 | 5162 | b10c5c55 | 11:01:51 | 153.2 | 10 | 2 | 0 | 0.491 |
| 23 | competition_validator | batch1 | validation | ok | 1 | 5194 | b10c5c55 | 11:01:53 | 243.2 | 11 | 1 | 0 | 0.725 |
| 24 | competition_validator | batch2 | validation | ok | 1 | 5406 | b10c5c55 | 11:02:50 | 280.2 | 12 | 3 | 0 | 0.760 |
| 25 | feasibility_validator | batch1 | validation | ok | 1 | 5735 | b10c5c55 | 11:04:00 | 229.2 | 8 | 0 | 1 | 0.540 |
| 26 | feasibility_validator | batch2 | validation | ok | 1 | 5841 | b10c5c55 | 11:04:25 | 243.6 | 9 | 0 | 0 | 0.576 |
| 27 | competition_validator | batch3 | validation | ok | 1 | 5440 | b10c5c55 | 11:02:51 | 342.6 | 14 | 4 | 0 | 0.908 |
| 28 | feasibility_validator | batch3 | validation | ok | 1 | 6035 | b10c5c55 | 11:05:56 | 208.9 | 7 | 1 | 0 | 0.428 |
| 29 | competition_validator | batch4 | validation | ok | 1 | 5542 | b10c5c55 | 11:03:10 | 386.8 | 14 | 5 | 0 | 0.893 |
| 30 | feasibility_validator | batch4 | validation | ok | 1 | 6239 | b10c5c55 | 11:07:30 | 215.1 | 6 | 0 | 0 | 0.418 |
| 31 | killer_agent | r1_batch4 | killer | ok | 1 | 6498 | b10c5c55 | 11:11:05 | 143.2 | 4 | 0 | 0 | 0.443 |
| 32 | killer_agent | r1_batch1 | killer | ok | 1 | 6496 | b10c5c55 | 11:11:05 | 200.2 | 8 | 0 | 0 | 0.662 |
| 33 | killer_agent | r1_batch2 | killer | ok | 1 | 6499 | b10c5c55 | 11:11:05 | 220.8 | 7 | 0 | 0 | 0.635 |
| 34 | killer_agent | r1_batch3 | killer | ok | 1 | 6497 | b10c5c55 | 11:11:05 | 236.2 | 8 | 2 | 0 | 0.667 |
| 35 | synthesizer | synthesizer | synthesis | ok | 1 | 6951 | b10c5c55 | 11:15:01 | 1051.6 | 0 | 0 | 0 | 2.012 |

### أزمنة المراحل

- 1_DISCOVERY: 615.7s
- 2_DEDUPLICATION: 396.1s
- 3_VALIDATION: 731.9s
- 4_KILLER_ROUND_1: 236.3s
- 5_GAP_DETECTION_R1: 0.0s
- 8_SYNTHESIS: 1051.6s

## 11. المنهجية (Methodology)

Discovery (13 agents بالتوازي) → Deduplication (كود + Consolidator agent) → Evidence/Payment/Competition/Feasibility validators (بالتوازي على دفعات) → Killer Agent → Gap detection → Gap Researcher (بحث إضافي) → Killer final round → Opportunity Synthesizer → هذا التقرير. التفاصيل في `README.md`.
