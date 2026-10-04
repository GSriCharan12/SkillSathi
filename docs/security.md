# SkillSathi Security, Privacy & Role-Based Access Control (RBAC)
**Smart India Hackathon 2026 | Problem Statement 26241**

---

## 1. Authentication & Session Security

- **Password Hashing**: Passwords are saved exclusively as salted hashes using Passlib/Bcrypt (`bcrypt` algorithm with work factor 12). Plain passwords are never stored or logged.
- **JWT Authorization**: Stateless `Bearer` token issuance using HMAC-SHA256 (`HS256`) with configurable expiration (`ACCESS_TOKEN_EXPIRE_MINUTES=1440`).
- **CORS Policies**: Explicit origin whitelisting (`ALLOWED_ORIGINS` in `.env`) preventing cross-site scripting vulnerabilities.

---

## 2. Role-Based Access Control (RBAC)

SkillSathi enforces strict role isolation across four personas:

| Role | Access Permissions | Data Boundaries |
| :--- | :--- | :--- |
| **`LEARNER`** | View trades, select interests, participate in family decision room, message AI counsellor | Restricted strictly to own family session and profile |
| **`PARENT`** | Voice family concerns, review verified evidence, view alignment radar, update decision status | Restricted strictly to own authorized family unit |
| **`COUNSELLOR`** | View escalated cases in workstation, claim cases, append family-shared / private notes, link official schemes | Can only view cases assigned to them or unassigned regional open queue |
| **`ADMIN`** | View scheme-level resistance analytics, sync data adapters, trigger audit jobs, export CSV | Sees strictly aggregated telemetry; individual learner/parent names are scrubbed |

---

## 3. Family Privacy & Data Isolation

1. **Family Isolation Barrier**: All decision room reads and updates (`/api/v1/family-decisions/{family_id}`) check that the authenticated user belongs to `family_id`.
2. **Counsellor Private Notes**: Internal case notes marked `COUNSELLOR_PRIVATE` are omitted from family-facing query responses.
3. **Anonymized Telemetry Export**: The Scheme Administrator CSV export endpoint (`/api/v1/admin/analytics/export`) outputs only `Family_Code`, `District`, `Trade`, `Resistance_Score`, and `Resolved_Status`. Names, phone numbers, and raw conversation transcripts are permanently excluded.
4. **SQL Injection Prevention**: All queries utilize SQLAlchemy ORM parameterized statements. Raw SQL string concatenation is strictly prohibited.
