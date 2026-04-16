# 🇺🇸 CivicID — National Identity & Verification System

> A secure, role-based civic infrastructure platform designed to simulate real-world government systems.

---

## Overview

CivicID is a Django and Django REST Framework backend that models a multi-agency identity and civic management platform. It supports structured interaction across all major civic identity domains — from birth registration to death records, marriage certificates, Social Security, Selective Service, voter registration, and passport issuance.

The platform enforces strict role-based access control, JWT authentication, privacy-aware data design, a permanent tamper-evident audit trail, and person photo management across all modules.

---

## Project Goals

- Build a centralized national identity system
- Enforce role-based access control (RBAC) across all agencies
- Secure APIs with JWT authentication
- Track every sensitive action through an immutable audit log
- Support full civic lifecycle: birth → identity → civic participation → death
- Simulate real-world multi-agency backend architecture
- Display person photos across all relevant modules for visual identity confirmation

---

## System Roles

| Role | Description |
|------|-------------|
| SUPER_ADMIN | Full system access for development and testing |
| REGISTRAR | Birth records, death records, marriage certificates, Social Security, Selective Service |
| DMV | ID applications and issued IDs |
| LAW_ENFORCEMENT | Identity verification lookups (reason required, privacy-first) |
| AUDITOR | Read-only audit log access |
| ELECTIONS | Voter registration, voter ID issuance, felony flag and rights restoration |
| STATE_DEPT | Passport issuance and status management |
| SSA | Social Security Number issuance and management |
| IMMIGRATION | Immigration status tracking and naturalization records |

---

## Tech Stack

- Python 3.12
- Django 5.2.4
- Django REST Framework 3.16.1
- SimpleJWT 5.5.1
- SQLite (development)
- django-cors-headers
- django-filter
- Celery 5.5.3
- Redis 6.4.0
- Pillow 11.3.0
- Gunicorn 23.0.0

---

## Authentication

JWT is used for all protected API access. Tokens are sent via `Authorization: Bearer <token>` and fall back to Django session authentication when the JWT is expired. The `apiFetch()` utility in `civic.js` handles both automatically — all API calls must use `apiFetch()`, never raw `fetch()`.

### Obtain token
`POST /api/token/`

### Refresh token
`POST /api/token/refresh/`

Token lifetimes:
- Access token: **8 hours**
- Refresh token: **1 day**

---

## Core API Domains

| Endpoint | Description |
|----------|-------------|
| `/api/persons/` | Identity registry — PATCH triggers audit-logged change record |
| `/api/birth-records/` | Birth certificate registration |
| `/api/death-records/` | Death certificates — cascades to voter, passport, selective service |
| `/api/marriage-certificates/` | Civil union registry — name changes applied automatically |
| `/api/social-security/` | SSN assignment — SSN write-only, masked on read |
| `/api/selective-service/` | Federal Selective Service registration |
| `/api/person-photos/` | Photo history per person |
| `/api/id-applications/` | DMV ID applications |
| `/api/issued-ids/` | Issued ID credentials |
| `/api/immigration-status/` | Immigration status records |
| `/api/naturalization/` | Naturalization records |
| `/api/voter-registrations/` | Voter registration records |
| `/api/voter-ids/` | Voter ID credentials |
| `/api/passports/` | Passport issuance and management |
| `/api/law-enforcement/verify/` | Privacy-first identity lookup (reason required) |
| `/api/law-enforcement/history/` | Officer's own lookup history |
| `/api/voter/eligibility/` | Eligibility check (citizenship, age, felony gates) |
| `/api/voter/register/` | Register voter + issue voter ID |
| `/api/voter/flag-felony/` | Flag felony conviction, suspend voter ID |
| `/api/voter/restore/` | Restore voting rights, reactivate voter ID |
| `/api/audit-logs/` | Read-only compliance audit trail |
| `/api/token/` | Obtain JWT |
| `/api/token/refresh/` | Refresh JWT |

---

## Key Features

### Identity & Credentialing
- Person records with full demographic data, gender, address, and photo
- Birth record registration (link to existing or create new person simultaneously)
- Naturalization and immigration status tracking
- ID applications and issued credentials
- Passport issuance with days-remaining tracking

### Person Photos
- `Person.photo` stores the current profile photo (`upload_to='person_photos/'`)
- `PersonPhoto` model stores full photo history (`upload_to='person_photos/history/'`)
- Photos are uploaded via `/api/person-photos/` or the Django Admin panel
- Photos display across all modules at a **maximum size of 300×300px**:
  - **Law Enforcement** — large ID card–style frame (300×300) in the result panel; 32×40 thumbnail in lookup history
  - **Persons Registry** — 36×45 thumbnail left of the record ID number
  - **Death Records** — 32×40 thumbnail between Certificate # and Person name
  - **Social Security** — 32×40 thumbnail before the masked SSN column
  - **Selective Service** — 32×40 thumbnail before the Registration # column
- All photo sizes are enforced via inline styles on the injected `<img>` elements, ensuring correct display regardless of browser CSS cache state

### Vital Events
- **Death Records** — filing automatically suspends voter registration, voter ID, passport, and selective service via Django signals
- **Marriage Certificates** — name changes applied automatically to Person records; maiden name preserved; audit logged
- **Person Edits** — every PATCH to a Person record diffs before/after state, requires a typed reason, and writes a permanent audit entry with officer identity and timestamp

### Auto ID Application on Registration
When a new Person record is created (via the API, Django Admin, or any other path), a Django signal fires automatically:
- If the person is **16 years of age or older**, a `FIRST_TIME_ID` application is created with status `DRAFT`
- A DMV officer must review and approve it before an ID is physically issued
- Implemented in `apps/persons/signals.py` using `@receiver(post_save, sender=Person)`
- Signal uses the **model class directly** (not the string form) for reliability

### Social Security
- OneToOne SSN assignment per person
- SSN stored as plain text in dev; write-only in API (only masked display `***-**-1234` returned)
- Access restricted to SSA, REGISTRAR, and SUPER_ADMIN roles

### Selective Service
- Federal law compliance: all males 18–25 required to register (50 U.S.C. § 3802), regardless of citizenship
- Auto-registration via Celery Beat task daily at midnight UTC when a qualifying person turns 18
- Auto-deregistration at age 26 (daily task at 00:30 UTC)
- Manual registration with gender/age validation warnings in UI

### Voter Registration
- Three-gate eligibility: citizenship, age 18+, no active felony
- Automatic voter registration + voter ID issuance on eligibility confirmation
- Felony flagging suspends voter ID immediately
- Rights restoration reactivates registration and voter ID

### Law Enforcement Verification
- Reason required before any data is returned
- Returns minimum-necessary fields: name, DOB, citizenship status, and photo (if on file)
- Every lookup automatically logged to audit trail
- Officers can only view their own history
- `MinimalPersonSerializer` deliberately excludes SSN, address, maiden name, and all other sensitive fields

### Audit & Compliance
- All sensitive actions across every module write to `AuditLog`
- Person edits record: officer, timestamp, reason, and field-level diff (`{from, to}` per field)
- Death record filings, marriage registrations, voter actions, LE lookups all auto-logged
- Read-only via API; no delete endpoint

### Automated Tasks (Celery + Redis)
- **Midnight UTC**: `run_daily_civic_checks` — auto-registers voters and selective service for everyone turning 18 that day
- **00:30 UTC**: `deregister_selective_service_age_26` — removes persons from selective service rolls at age 26

---

## Frontend Pages

| Page | Roles | Description |
|------|-------|-------------|
| `/` | All | Agency selection + secure login |
| `/pages/dashboard/` | All | System-wide stats and recent activity |
| `/pages/persons/` | All (edit: REGISTRAR, DMV, SUPER_ADMIN) | Identity registry with photo thumbnails, edit modal, and audit trail |
| `/pages/birth-records/` | REGISTRAR, SUPER_ADMIN | New record modal: existing person or create new inline; gender field |
| `/pages/death-records/` | REGISTRAR, LAW_ENFORCEMENT, SUPER_ADMIN | File death record with person photo; cascades fire automatically |
| `/pages/marriage/` | REGISTRAR, SUPER_ADMIN | Register marriage; name changes auto-applied |
| `/pages/social-security/` | SSA, REGISTRAR, SUPER_ADMIN | Issue SSN with person photo; masked display |
| `/pages/selective-service/` | REGISTRAR, SUPER_ADMIN | Registry with person photo + manual registration |
| `/pages/id-applications/` | DMV, SUPER_ADMIN | ID application management |
| `/pages/issued-ids/` | DMV, SUPER_ADMIN | Credential status and expiration tracking |
| `/pages/immigration/` | IMMIGRATION, SUPER_ADMIN | Immigration status + naturalization |
| `/pages/voter-registration/` | ELECTIONS, SUPER_ADMIN | Eligibility check, registration, felony flag, rights restoration |
| `/pages/passport/` | STATE_DEPT, SUPER_ADMIN | Passport issuance and status management |
| `/pages/law-enforcement/` | LAW_ENFORCEMENT | Identity lookup portal with 300×300 photo and history thumbnails |
| `/pages/audit/` | AUDITOR, SUPER_ADMIN | Full audit log with action filtering |
| `/pages/administration/` | SUPER_ADMIN | System overview, module links, API reference |

---

## Frontend Architecture

### Shared Utilities (`civic.js`)
- `apiFetch(path, options)` — authenticated API calls with JWT + CSRF + session fallback. **All API calls must use this function.**
- `injectHeader(activePage)` — renders the header, nav, and clock
- `injectEditModal()` — injects the shared person edit modal
- `statusBadge(status)` — returns a formatted status badge HTML string
- `formatDate(dateStr)` / `formatDateTime(dateStr)` — date formatting helpers

### Shared Styles (`styles.css`)
All component styles live in one shared stylesheet. No page should have an inline `<style>` block. Key component classes:

| Class | Description |
|-------|-------------|
| `.id-photo-frame` | 300×300 ID card photo frame (Law Enforcement result panel) |
| `.id-photo-placeholder` | No-photo icon inside `.id-photo-frame` |
| `.history-thumb` | 32×40 thumbnail for table rows |
| `.person-thumb` | 36×45 thumbnail for persons registry |
| `.id-cell` | Flex wrapper: photo + ID number side-by-side |
| `.result-panel` / `.result-header` | LE result panel structure |
| `.verify-form` / `.required-tag` | LE lookup form |
| `.eligibility-result` | Voter eligibility result box |
| `.restore-form` / `.felony-form` | Voter rights action panels |
| `.tab-btn` / `.tab-btn.active` | Tab filter buttons (gold underline when active) |
| `.action-header-felony` / `.action-header-restore` | Colored action header backgrounds |

### Photo Rendering Pattern
Photos are injected dynamically via JavaScript. All `<img>` tags use explicit inline `width`, `height`, `max-width`, `max-height`, and `object-fit:cover` to enforce correct sizing regardless of CSS cache state. The `onerror` handler uses `this.style.display='none'` only — never `this.outerHTML=...` — to avoid artifact text appearing in the DOM.

---

## Running the Project

### 1. Start Django
```bash
python manage.py runserver
```

### 2. Start Redis (required for Celery)
```bash
brew install redis        # macOS — one time only
brew services start redis
redis-cli ping            # expect: PONG
```

### 3. Start Celery Worker
```bash
celery -A civicid worker --loglevel=info
```

### 4. Start Celery Beat (scheduled tasks)
```bash
celery -A civicid beat --loglevel=info
```

### Media directory setup (one time)
```bash
mkdir -p media/person_photos/history
cp templates/civicid-frontend/media/civic_id_2026.png media/civic_id_2026.png
```

### Create superuser
```bash
python manage.py createsuperuser
```

### Upload a person photo
Photos must currently be uploaded via:
1. **Django Admin** — `/admin/` → Person Photos → Add
2. **API directly** — `POST /api/person-photos/` with `multipart/form-data`

---

## Project Status

### Completed
- Core identity models with full migration history
- JWT authentication + RBAC (9 roles)
- JWT token lifetime: 8hr access / 1 day refresh
- `apiFetch()` utility with JWT + CSRF + session auth fallback (fixes 403 on token expiry)
- Law enforcement verification (privacy-first, audit-logged, photo included)
- Voter registration module (eligibility gates, felony tracking, rights restoration)
- Passport module with days-remaining calculation
- Birth records with inline person creation
- Death records with automatic cascade signals
- Marriage certificates with automatic name change signals
- Social Security registry (SSN masked in API)
- Selective Service registry (federal law compliance)
- Person edit audit logging (field-level diff, officer, timestamp, reason)
- Celery + Redis automated civic tasks (age 18 registration, age 26 deregistration)
- **Person photos** displayed across all 5 modules (LE, Persons, Death Records, Social Security, Selective Service)
- **Photo size capped at 300×300px** with inline style enforcement on all dynamically injected images
- **Auto ID application** on person registration (16+ years → DRAFT `FIRST_TIME_ID` via Django signal)
- Full CSS refactoring — all styles consolidated into `styles.css`, no inline `<style>` blocks in any page
- Full frontend with 16 pages, role-gated navigation
- SSA agency card on login page

### Planned
- Docker deployment
- Cloud hosting
- Java / Spring Boot version
- Full permission hardening (DRF permission classes per role per endpoint)
- Person profile page with linked records view
- Photo upload UI (currently requires Django Admin or direct API call)

---

## Why This Project Matters

CivicID demonstrates:

- Secure, production-grade backend architecture
- Multi-agency role-based system design
- Full civic lifecycle modeling (birth → identity → participation → death)
- Privacy-first API design (law enforcement minimal-data pattern)
- Audit-focused engineering (immutable logs, field-level diffs, officer attribution)
- Signal-driven cascade automation
- Scheduled task automation with Celery and Redis
- Real-world multi-domain data relationships
- Photo management across a multi-module system with consistent display constraints

---

## Author

**Veries Seals III**
B.S. Computer Science (Software Engineering)
Colorado Technical University

---

> Built with real-world system design in mind.