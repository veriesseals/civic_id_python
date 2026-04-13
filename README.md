# 🇺🇸 CivicID — National Identity & Verification System

> A secure, role-based identity platform designed to simulate real-world government infrastructure.

---

## 🧠 Overview

CivicID is a backend system built with Django and Django REST Framework that models a **multi-agency identity and civic management platform**.

It enables structured and secure interaction between government-like domains, including:

- Identity Management
- Birth Registration
- ID Issuance
- Voter Registration
- Law Enforcement Verification
- Audit and Compliance Tracking

The system enforces strict access control, traceability, and data boundaries to reflect real-world backend system design.

---

## 🎯 Project Goals

- Build a centralized identity system
- Enforce **Role-Based Access Control (RBAC)**
- Secure APIs using **JWT authentication**
- Track sensitive operations via **audit logging**
- Support **civic processes (voter registration)**
- Simulate real-world backend architecture across multiple domains

---

## 🏛️ System Roles

| Role | Description |
|------|------------|
| SUPER_ADMIN | Full system access (development/testing) |
| REGISTRAR | Manages birth records |
| DMV | Handles ID applications and issuance |
| LAW_ENFORCEMENT | Performs identity verification |
| AUDITOR | Reviews audit logs |
| ELECTION_OFFICIAL | Manages voter registration |

---

## ⚙️ Tech Stack

- Python 3.12
- Django 5.2.x
- Django REST Framework
- SimpleJWT (Authentication)
- SQLite (Development)
- django-cors-headers

---

## 🔐 Authentication (JWT)

### Obtain Token

POST /api/token/

### Refresh Token

POST /api/token/refresh/
### Usage

---

## 📡 Core API Endpoints

| Endpoint | Description |
|---------|------------|
| `/api/persons/` | Core identity records |
| `/api/birth-records/` | Birth registration |
| `/api/id-applications/` | ID application workflow |
| `/api/issued-ids/` | Issued identification |
| `/api/voter-registrations/` | Voter registration system |
| `/api/law-enforcement-verifications/` | Identity verification |
| `/api/audit-logs/` | System activity logs |

---

## 🗳️ Voter Registration System

The platform includes a **voter registration module** that integrates with identity records.

### Capabilities:
- Links voter registration to verified persons
- Prevents duplicate registrations
- Tracks eligibility status
- Restricts access to election officials
- Logs all registration activity

### Design Principles:
- Identity-first validation
- Role-based access
- Auditability
- Minimal data exposure

---

## 🚓 Law Enforcement Verification

A controlled verification system for identity lookup.

### Features:
- Reason-based verification requests
- Limited data responses
- Automatic association with requesting officer
- Logged for audit review

### Security Model:
- Least-privilege access
- No unrestricted browsing
- Fully auditable

---

## 🔐 Role-Based Access Control (RBAC)

Custom permission classes enforce strict access boundaries:

- Registrar → birth records only
- DMV → applications and ID issuance
- Law enforcement → verification only
- Election officials → voter registration
- Auditor → read-only logs
- Super Admin → full system access

Unauthorized access returns:

---

## 📜 Audit Logging

Tracks system activity including:
- Record creation
- Identity verification
- Voter registration actions

### Current State:
- Manual logging implemented

### Planned Enhancements:
- Automatic logging (middleware/signals)
- Request metadata tracking
- IP logging
- Compliance-level auditing

---

## 🧱 Project Structure

civic_id_python/
├── civicid/              # Project settings
├── accounts/             # Custom user + roles
├── persons/              # Identity data
├── birth_records/        # Birth records
├── id_applications/      # Application workflow
├── issued_ids/           # Issued IDs
├── voter_registration/   # Voter registration system
├── immigration_status/   # Immigration tracking
├── naturalization/       # Naturalization records
├── law_enforcement/      # Verification system
├── audit/                # Logging
├── documents/            # Supporting documents
├── notifications/        # Notifications (in progress)
├── manage.py
├── requirements.txt
└── README.md

---

## 🚧 Project Status

### ✅ Completed
- Core identity models
- JWT authentication
- RBAC system
- API endpoints for core modules
- Law enforcement verification (MVP)
- Voter registration module (MVP)
- Manual audit logging

### 🚧 In Progress
- Automated audit logging
- Permission hardening
- Data exposure control

### 🔮 Planned
- Frontend dashboard
- Java / Spring Boot version
- Docker deployment
- Cloud hosting

---

## 💡 Why This Project Matters

CivicID demonstrates:

- Backend system design at scale
- Role-based architecture (RBAC)
- Secure API development
- Multi-domain data modeling
- Audit-focused engineering
- Real-world workflow simulation

---

## 👨‍💻 Author

** Veries Seals III **  
B.S. Computer Science (Software Engineering)  
Colorado Technical University  

---

## 🚀 Future Vision

CivicID is evolving into a **full-scale identity and civic infrastructure prototype**, designed to simulate:

- cross-agency data sharing
- secure identity + voter registration workflows
- scalable backend systems
- enterprise-grade governance controls

---

> ⚡ Built with real-world system design in mind

