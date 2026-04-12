# 🇺🇸 CivicID — National Identity & Verification System (Django Build)

CivicID is a backend-focused system designed to simulate a modern, secure, and 
privacy-aware identity platform that enables controlled communication between 
government agencies.

This project explores how identity data could be structured, protected, and 
accessed across agencies such as:
- Registrars (birth records)
- DMV (ID issuance)
- Law Enforcement (verification)
- Auditors (accountability)

---

## 🎯 Project Goals
- Build a centralized identity system
- Enforce strict role-based access control (RBAC)
- Implement secure authentication (JWT)
- Ensure auditability of all sensitive actions
- Design privacy-first law enforcement access
- Simulate real-world government workflows

---

## 🧱 Tech Stack
- Python 3.12
- Django 5.2.4
- Django REST Framework 3.16.1
- SimpleJWT 5.5.1
- SQLite (development)
- django-cors-headers
- django-filter

---

## ⚙️ Core Features

### 🔐 Authentication
- JWT-based authentication
- Token issuance & refresh endpoints
- Protected API routes — all endpoints require a valid token

### 👤 Identity Management
- Person records
- Birth records
- ID applications and issuance
- Immigration status tracking
- Naturalization records

### 🏛️ Role-Based Access Control (RBAC)
| Role | Access Level |
|---|---|
| SUPER_ADMIN | Full system access |
| REGISTRAR | Birth records and naturalization |
| DMV | ID applications and issued IDs |
| LAW_ENFORCEMENT | Verification API only |
| AUDITOR | Read-only audit log access |

### 🚓 Law Enforcement Verification API
- Reason-based identity lookup (reason required on every request)
- Minimal data exposure (privacy-first design)
- Full audit tracking of every request
- No unrestricted data browsing
- Officers can only view their own lookup history

### 📜 Audit Logging
- Tracks all sensitive actions across the system
- Every LE lookup is automatically logged
- Supports compliance, accountability, and traceability

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip
- Git

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/civic_id_python.git
cd civic_id_python
```

**2. Create and activate a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Apply database migrations:**
```bash
python manage.py migrate
```

**5. Create a superuser (admin account):**
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username and password.

**6. Start the development server:**
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 🔑 Authentication

All API endpoints require a valid JWT token. Here's how to get one:

**Obtain a token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Response:**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Refresh an expired token:**
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

**Use your token on all requests:**
```bash
curl http://127.0.0.1:8000/api/persons/ \
  -H "Authorization: Bearer your_access_token"
```

---

## 📡 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Persons
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/persons/` | List all persons |
| POST | `/api/persons/` | Create a new person |
| GET | `/api/persons/{id}/` | Retrieve a person |
| PUT | `/api/persons/{id}/` | Update a person |
| DELETE | `/api/persons/{id}/` | Delete a person |

### Birth Records
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/birth-records/` | List all birth records |
| POST | `/api/birth-records/` | Create a birth record |
| GET | `/api/birth-records/{id}/` | Retrieve a birth record |
| PUT | `/api/birth-records/{id}/` | Update a birth record |
| DELETE | `/api/birth-records/{id}/` | Delete a birth record |

### ID Applications
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/id-applications/` | List all applications |
| POST | `/api/id-applications/` | Submit a new application |
| GET | `/api/id-applications/{id}/` | Retrieve an application |
| PUT | `/api/id-applications/{id}/` | Update an application |
| DELETE | `/api/id-applications/{id}/` | Delete an application |

### Issued IDs
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/issued-ids/` | List all issued IDs |
| POST | `/api/issued-ids/` | Issue a new ID |
| GET | `/api/issued-ids/{id}/` | Retrieve an issued ID |
| PUT | `/api/issued-ids/{id}/` | Update an issued ID |

### Immigration Status
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/immigration-status/` | List all statuses |
| POST | `/api/immigration-status/` | Create a status record |
| GET | `/api/immigration-status/{id}/` | Retrieve a status |
| PUT | `/api/immigration-status/{id}/` | Update a status |

### Naturalization Records
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/naturalization/` | List all records |
| POST | `/api/naturalization/` | Create a record |
| GET | `/api/naturalization/{id}/` | Retrieve a record |
| PUT | `/api/naturalization/{id}/` | Update a record |

### Audit Logs (Read-Only)
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/audit-logs/` | List all audit logs |
| GET | `/api/audit-logs/{id}/` | Retrieve a specific log |

### 🚓 Law Enforcement API
> Requires `LAW_ENFORCEMENT` role. All requests are automatically logged.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/law-enforcement/verify/` | Submit a verification request |
| GET | `/api/law-enforcement/history/` | View your own lookup history |

**Verification request body:**
```json
{
    "person": 1,
    "reason": "Suspect in active investigation case #12345"
}
```

**Response (minimal data only):**
```json
{
    "id": 1,
    "requested_by": 3,
    "person": 1,
    "person_details": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1990-05-15",
        "citizenship_status": "CITIZEN"
    },
    "reason": "Suspect in active investigation case #12345",
    "status": "COMPLETED",
    "requested_at": "2026-04-12T18:30:00Z"
}
```

---

## 🧪 Testing with Postman

1. Download and install [Postman](https://www.postman.com/)
2. Create a new collection called `CivicID`
3. Add a `POST` request to `http://127.0.0.1:8000/api/token/`
4. Set the body to `raw` / `JSON` and enter your credentials
5. Copy the `access` token from the response
6. On all other requests add a header: `Authorization: Bearer your_token`

---

## 🛠️ Admin Panel

Access the Django admin interface at: