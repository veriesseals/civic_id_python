// ── CIVIC-ID SHARED UTILITIES ──

const AGENCY_LABELS = {
  SUPER_ADMIN:     'System Administration',
  REGISTRAR:       'Registrar Office',
  DMV:             'DMV Office',
  LAW_ENFORCEMENT: 'Law Enforcement',
  AUDITOR:         'Audit Division',
  IMMIGRATION:     'Immigration Services',
  ELECTIONS:       'Elections Office',
  STATE_DEPT:      'State Department',
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
    'Content-Type':  'application/json',
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
  el.textContent = now.toUTCString().split(' ').slice(4, 5)[0] + ' GMT';
}

// ── NAV MAPS ────────────────────────────────────────────────────
const NAV_LINKS = {
  SUPER_ADMIN: [
    { href: '/pages/dashboard/',          label: 'Dashboard',          key: 'dashboard' },
    { href: '/pages/persons/',            label: 'Persons',            key: 'persons' },
    { href: '/pages/birth-records/',      label: 'Birth Records',      key: 'birth-records' },
    { href: '/pages/id-applications/',    label: 'ID Applications',    key: 'id-applications' },
    { href: '/pages/issued-ids/',         label: 'Issued IDs',         key: 'issued-ids' },
    { href: '/pages/voter-registration/', label: 'Voter Registration', key: 'voter-registration' },
    { href: '/pages/passport/',           label: 'Passports',          key: 'passport' },
    { href: '/pages/audit/',              label: 'Audit Logs',         key: 'audit' },
    { href: '/pages/administration/',     label: 'Administration',     key: 'administration' },
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
  ELECTIONS: [
    { href: '/pages/voter-registration/', label: 'Voter Registration', key: 'voter-registration' },
    { href: '/pages/persons/',            label: 'Persons',            key: 'persons' },
    { href: '/pages/audit/',              label: 'Audit Logs',         key: 'audit' },
  ],
  STATE_DEPT: [
    { href: '/pages/passport/', label: 'Passport Registry', key: 'passport' },
    { href: '/pages/persons/',  label: 'Person Lookup',     key: 'persons' },
  ],
};

// ── HEADER INJECTION ─────────────────────────────────────────────
function injectHeader(activePage) {
  const agency      = getAgency();
  const username    = getUsername();
  const agencyLabel = AGENCY_LABELS[agency] || agency;
  const links       = NAV_LINKS[agency] || NAV_LINKS.SUPER_ADMIN;

  document.body.insertAdjacentHTML('afterbegin', `
    <div class="classification-bar">
      &#9733; &nbsp; UNITED STATES GOVERNMENT &mdash; AUTHORIZED ACCESS ONLY &nbsp; &#9733;
    </div>
    <header class="site-header">
      <div class="header-inner">
        <a href="/pages/dashboard/" class="header-brand">
          <img src="/media/civic_id_2026.png" class="header-logo" alt="CivicID Seal" onerror="this.style.display='none'" />
          <div class="header-title-group">
            <span class="agency-label">United States Government</span>
            <span class="system-name">CIVIC ID</span>
            <span class="system-sub">National Identity &amp; Verification System</span>
          </div>
        </a>
        <div class="header-right">
          <div class="header-badge">
            <span class="badge-role">${agencyLabel}</span>
            <span class="badge-user">${username}</span>
            <span class="badge-time" id="live-clock"></span>
          </div>
          <button onclick="logout()" class="btn-logout">
            <i class="bi bi-box-arrow-right"></i> LOGOUT
          </button>
        </div>
      </div>
    </header>
    <nav class="site-nav">
      <div class="nav-inner">
        ${links.map(l => `
          <a href="${l.href}" class="${activePage === l.key ? 'active' : ''}">${l.label}</a>
        `).join('')}
      </div>
    </nav>
  `);

  setInterval(updateClock, 1000);
  updateClock();
}

// ── HELPERS ──────────────────────────────────────────────────────
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
    INACTIVE: 'pending', SUSPENDED: 'rejected', INELIGIBLE: 'rejected',
    RESTORED: 'active',
  };
  const cls = map[status] || 'pending';
  return `<span class="status-badge ${cls}">${status.replace(/_/g, ' ')}</span>`;
}