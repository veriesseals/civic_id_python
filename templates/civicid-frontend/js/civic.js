// ── CIVIC-ID SHARED UTILITIES ──
// All paths are absolute so they work whether served by Django
// at http://127.0.0.1:8000/ or opened directly as a file.

const AGENCY_LABELS = {
  SUPER_ADMIN: 'System Administration',
  REGISTRAR: 'Registrar Office',
  DMV: 'DMV Office',
  LAW_ENFORCEMENT: 'Law Enforcement',
  AUDITOR: 'Audit Division',
  IMMIGRATION: 'Immigration Services',
};

const API_BASE = 'http://127.0.0.1:8000/api';

function getToken()    { return localStorage.getItem('civic_access'); }
function getAgency()   { return localStorage.getItem('civic_agency') || 'SUPER_ADMIN'; }
function getUsername() { return localStorage.getItem('civic_username') || 'user'; }

function logout() {
  localStorage.clear();
  window.location.href = '/';
}

function authHeaders() {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`
  };
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...authHeaders(), ...(options.headers || {}) }
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function updateClock() {
  const el = document.getElementById('live-clock');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toUTCString().split(' ').slice(4, 5)[0] + ' UTC';
}

// ── NAV MAPS ────────────────────────────────────────────────────
// All hrefs are absolute Django URL paths (/pages/dashboard/ etc.)
const NAV_LINKS = {
  SUPER_ADMIN: [
    { href: '/pages/dashboard/',      label: 'Dashboard',       key: 'dashboard' },
    { href: '/pages/persons/',        label: 'Persons',         key: 'persons' },
    { href: '/pages/birth-records/',  label: 'Birth Records',   key: 'birth-records' },
    { href: '/pages/id-applications/',label: 'ID Applications', key: 'id-applications' },
    { href: '/pages/issued-ids/',     label: 'Issued IDs',      key: 'issued-ids' },
    { href: '/pages/audit/',          label: 'Audit Logs',      key: 'audit' },
  ],
  REGISTRAR: [
    { href: '/pages/dashboard/',     label: 'Dashboard',     key: 'dashboard' },
    { href: '/pages/birth-records/', label: 'Birth Records', key: 'birth-records' },
    { href: '/pages/persons/',       label: 'Persons',       key: 'persons' },
  ],
  DMV: [
    { href: '/pages/dashboard/',       label: 'Dashboard',       key: 'dashboard' },
    { href: '/pages/id-applications/', label: 'ID Applications', key: 'id-applications' },
    { href: '/pages/issued-ids/',      label: 'Issued IDs',      key: 'issued-ids' },
    { href: '/pages/persons/',         label: 'Persons',         key: 'persons' },
  ],
  LAW_ENFORCEMENT: [
    { href: '/pages/law-enforcement/', label: 'Verify Identity',   key: 'law-enforcement' },
    { href: '/pages/audit/',           label: 'My Lookup History', key: 'audit' },
  ],
  AUDITOR: [
    { href: '/pages/audit/',     label: 'Audit Logs', key: 'audit' },
    { href: '/pages/dashboard/', label: 'Dashboard',  key: 'dashboard' },
  ],
  IMMIGRATION: [
    { href: '/pages/immigration/', label: 'Immigration Status', key: 'immigration' },
    { href: '/pages/persons/',     label: 'Persons',            key: 'persons' },
  ],
};

// ── HEADER INJECTION ────────────────────────────────────────────
function injectHeader(activePage) {
  const agency      = getAgency();
  const username    = getUsername();
  const agencyLabel = AGENCY_LABELS[agency] || agency;
  const links       = NAV_LINKS[agency] || NAV_LINKS.SUPER_ADMIN;

  document.body.insertAdjacentHTML('afterbegin', `
    <div style="background:#001040;color:#E8C97A;text-align:center;font-family:'Oswald',sans-serif;font-size:10px;letter-spacing:4px;padding:5px 0;border-bottom:1px solid rgba(201,168,76,0.4);">
      ★ &nbsp; UNITED STATES GOVERNMENT — AUTHORIZED ACCESS ONLY &nbsp; ★
    </div>
    <header style="background:linear-gradient(135deg,#002060 0%,#0047AB 60%,#1565C0 100%);padding:0;position:sticky;top:0;z-index:1000;box-shadow:0 4px 20px rgba(0,0,0,0.3);border-bottom:3px solid #C9A84C;">
      <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 32px;max-width:1400px;margin:0 auto;">
        <a href="/pages/dashboard/" style="display:flex;align-items:center;gap:16px;text-decoration:none;">
          <img src="/media/civic_id_2026.png" style="width:55px;height:55px;filter:brightness(0) invert(1);object-fit:contain;" alt="CivicID Seal" onerror="this.style.display='none'" />
          <div>
            <div style="font-family:'Oswald',sans-serif;font-size:10px;letter-spacing:3px;color:#E8C97A;">United States Government</div>
            <div style="font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;color:white;letter-spacing:1px;">CIVIC ID</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.5);letter-spacing:1px;">National Identity &amp; Verification System</div>
          </div>
        </a>
        <div style="display:flex;align-items:center;gap:20px;">
          <div style="text-align:right;">
            <div style="background:#C9A84C;color:#002060;font-family:'Oswald',sans-serif;font-size:10px;font-weight:600;letter-spacing:2px;padding:3px 10px;border-radius:2px;text-transform:uppercase;">${agencyLabel}</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.65);margin-top:3px;">${username}</div>
            <div id="live-clock" style="font-size:11px;color:#E8C97A;font-family:'Oswald',sans-serif;letter-spacing:1px;"></div>
          </div>
          <button onclick="logout()" style="background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.25);color:white;font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:1.5px;padding:8px 16px;border-radius:3px;cursor:pointer;">
            <i class="bi bi-box-arrow-right me-1"></i> LOGOUT
          </button>
        </div>
      </div>
    </header>
    <nav style="background:#003080;border-bottom:1px solid rgba(201,168,76,0.3);">
      <div style="max-width:1400px;margin:0 auto;padding:0 32px;display:flex;gap:4px;">
        ${links.map(l => `
          <a href="${l.href}" style="font-family:'Oswald',sans-serif;font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:${activePage===l.key?'white':'rgba(255,255,255,0.65)'};text-decoration:none;padding:12px 16px;display:block;border-bottom:3px solid ${activePage===l.key?'#C9A84C':'transparent'};background:${activePage===l.key?'rgba(255,255,255,0.08)':'transparent'};transition:all 0.2s;">
            ${l.label}
          </a>`).join('')}
      </div>
    </nav>
  `);

  setInterval(updateClock, 1000);
  updateClock();
}

// ── HELPERS ─────────────────────────────────────────────────────
function formatDate(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function formatDateTime(dateStr) {
  if (!dateStr) return '—';
  return new Date(dateStr).toLocaleString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
}

function statusBadge(status) {
  const map = {
    ACTIVE: 'active', PENDING: 'pending', VERIFIED: 'verified',
    REJECTED: 'rejected', REVOKED: 'revoked', COMPLETED: 'verified',
    DRAFT: 'pending', SUBMITTED: 'pending', APPROVED: 'active',
    ISSUED: 'verified', UNDER_REVIEW: 'pending', EXPIRED: 'rejected',
    REPLACED: 'revoked', DENIED: 'rejected', CITIZEN: 'verified',
    PERMANENT_RESIDENT: 'active', VISA_HOLDER: 'pending',
  };
  const cls = map[status] || 'pending';
  return `<span class="status-badge ${cls}">${status.replace(/_/g, ' ')}</span>`;
}