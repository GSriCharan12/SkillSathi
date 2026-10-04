# SkillSathi Data Sources & Ingestion Pipeline
**Smart India Hackathon 2026 | Problem Statement 26241**

---

## 1. Verified Official Data Sources

SkillSathi connects with official Indian vocational education and labor statistical repositories.

| Source Code | Official Source Name | Publisher Ministry / Body | Cadence | Data Elements Captured |
| :--- | :--- | :--- | :--- | :--- |
| **`NCVET_NQR`** | National Qualifications Register | NCVET, Ministry of Skill Development & Entrepreneurship (MSDE) | Monthly | NSQF Levels, entry requirements, training hours, mapped national occupations |
| **`DGT_TRACER_2024`** | National ITI Tracer Study & NAPS Registry | Directorate General of Training (DGT) | Annual / Quarterly | Placement rates (%), NAPS apprenticeship stipends, certified ITI pass-outs |
| **`LABOUR_BUREAU_WAGE`** | Occupational Wage Survey & PLFS | Labour Bureau, Ministry of Labour & Employment (MoLE) | Annual | District/State wage distribution, 10th/50th/90th percentile entry & mid-career earnings |
| **`AICTE_LATERAL_DB`** | Polytechnic & Engineering Lateral Admissions Directory | All India Council for Technical Education (AICTE) | Bi-annual | Lateral entry eligibility into 2nd year Diploma & B.Tech / B.Voc programs under NEP 2020 NCrF |
| **`AISHE_VOCATIONAL`** | All India Survey on Higher Education | Ministry of Education (MoE) | Annual | Higher education progression pathways, community college admissions |

---

## 2. Ingestion Pipeline Architecture

```
+-------------------------------------------------------------------------------+
|                             External Data Feeds                               |
| (NCVET Portal / DGT Tracer CSV / MoLE Wage API / AICTE Lateral Entry Circular)|
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       1. Source Adapter (fetcher)                             |
|  - Rate-limited fetching with exponential backoff                             |
|  - TLS verification, sha256 checksum tracking                                 |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       2. Parser & Normalizer                                  |
|  - Maps regional trade codes to standardized NSQF identifiers                 |
|  - Converts currency metrics to monthly INR                                   |
|  - Cleans state/district spellings (e.g. Warangal Urban/Rural normalization)  |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       3. Validator & Deduplication                            |
|  - Validates placement rates in [0.0, 100.0]                                   |
|  - Enforces non-negative monthly earnings                                     |
|  - Drops duplicate trade-district-year triplets                               |
+---------------------------------------+---------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                       4. Persistence & Audit Log                              |
|  - Records source provenance ID, publisher ministry, and survey year          |
|  - Marks live vs demo records clearly                                         |
+-------------------------------------------------------------------------------+
```

---

## 3. Freshness Classification Standards

SkillSathi categorizes all data into four strictly distinguished tiers:

1. **`LIVE`**: Synced via verified API within the last 30 days.
2. **`FRESH`**: Official survey data verified within the current fiscal year (e.g. 2024–2025).
3. **`STALE`**: Verified data older than 24 months, flagged for re-verification.
4. **`DEMO`**: Clearly marked `[DEMO DATA - Simulation]` records used for platform demonstrations in unmapped districts.
