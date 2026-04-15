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
  SSA:             'Social Security Administration',
};

const API_BASE = 'http://127.0.0.1:8000/api';

function getToken()    { return localStorage.getItem('civic_access'); }
function getAgency()   { return localStorage.getItem('civic_agency') || 'SUPER_ADMIN'; }
function getUsername() { return localStorage.getItem('civic_username') || 'user'; }

function logout() { localStorage.clear(); window.location.href = '/'; }

function authHeaders() {
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${getToken()}` };
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

// ── NAV MAPS ─────────────────────────────────────────────────────
const NAV_LINKS = {
  SUPER_ADMIN: [
    { href: '/pages/dashboard/',          label: 'Dashboard',         key: 'dashboard' },
    { href: '/pages/persons/',            label: 'Persons',           key: 'persons' },
    { href: '/pages/birth-records/',      label: 'Birth Records',     key: 'birth-records' },
    { href: '/pages/death-records/',      label: 'Death Records',     key: 'death-records' },
    { href: '/pages/marriage/',           label: 'Marriage',          key: 'marriage' },
    { href: '/pages/id-applications/',    label: 'ID Applications',   key: 'id-applications' },
    { href: '/pages/issued-ids/',         label: 'Issued IDs',        key: 'issued-ids' },
    { href: '/pages/voter-registration/', label: 'Voter Reg',         key: 'voter-registration' },
    { href: '/pages/passport/',           label: 'Passports',         key: 'passport' },
    { href: '/pages/social-security/',    label: 'Social Security',   key: 'social-security' },
    { href: '/pages/selective-service/',  label: 'Selective Service', key: 'selective-service' },
    { href: '/pages/audit/',              label: 'Audit Logs',        key: 'audit' },
    { href: '/pages/administration/',     label: 'Administration',    key: 'administration' },
  ],
  REGISTRAR: [
    { href: '/pages/dashboard/',         label: 'Dashboard',         key: 'dashboard' },
    { href: '/pages/persons/',           label: 'Persons',           key: 'persons' },
    { href: '/pages/birth-records/',     label: 'Birth Records',     key: 'birth-records' },
    { href: '/pages/death-records/',     label: 'Death Records',     key: 'death-records' },
    { href: '/pages/marriage/',          label: 'Marriage',          key: 'marriage' },
    { href: '/pages/social-security/',   label: 'Social Security',   key: 'social-security' },
    { href: '/pages/selective-service/', label: 'Selective Service', key: 'selective-service' },
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
  SSA: [
    { href: '/pages/social-security/', label: 'SSN Registry',  key: 'social-security' },
    { href: '/pages/persons/',         label: 'Person Lookup', key: 'persons' },
    { href: '/pages/audit/',           label: 'Audit Logs',    key: 'audit' },
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
        ${links.map(l => `<a href="${l.href}" class="${activePage === l.key ? 'active' : ''}">${l.label}</a>`).join('')}
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
  return new Date(dateStr).toLocaleString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
}

function statusBadge(status) {
  const map = {
    ACTIVE:'active', PENDING:'pending', VERIFIED:'verified', REJECTED:'rejected',
    REVOKED:'revoked', COMPLETED:'verified', DRAFT:'pending', SUBMITTED:'pending',
    APPROVED:'active', ISSUED:'verified', UNDER_REVIEW:'pending', EXPIRED:'rejected',
    REPLACED:'revoked', DENIED:'rejected', CITIZEN:'verified', PERMANENT_RESIDENT:'active',
    VISA_HOLDER:'pending', INACTIVE:'pending', SUSPENDED:'rejected', INELIGIBLE:'rejected',
    RESTORED:'active', DECEASED:'rejected', DEREGISTERED:'revoked', EXEMPT:'pending',
    MALE:'verified', FEMALE:'active', OTHER:'pending',
    NATURAL:'pending', ACCIDENT:'pending', HOMICIDE:'rejected', SUICIDE:'rejected',
    UNDETERMINED:'pending', UNDOCUMENTED_ALIEN:'rejected',
  };
  const cls = map[status] || 'pending';
  return `<span class="status-badge ${cls}">${(status||'').replace(/_/g,' ')}</span>`;
}

// ── SHARED PERSON EDIT MODAL ──────────────────────────────────────
let _editPersonId = null;

function openEditModal(personId) {
  _editPersonId = personId;
  apiFetch(`/persons/${personId}/`).then(p => {
    const m = document.getElementById('editPersonModal');
    if (!m) { alert('Edit modal not found on this page.'); return; }
    m.querySelector('#edit-first').value       = p.first_name || '';
    m.querySelector('#edit-middle').value      = p.middle_name || '';
    m.querySelector('#edit-last').value        = p.last_name || '';
    m.querySelector('#edit-gender').value      = p.gender || 'OTHER';
    m.querySelector('#edit-dob').value         = p.date_of_birth || '';
    m.querySelector('#edit-city').value        = p.place_of_birth_city || '';
    m.querySelector('#edit-state').value       = p.place_of_birth_state || '';
    m.querySelector('#edit-country').value     = p.place_of_birth_country || 'USA';
    m.querySelector('#edit-citizenship').value = p.citizenship_status || 'CITIZEN';
    m.querySelector('#edit-street').value      = p.address_street || '';
    m.querySelector('#edit-addr-city').value   = p.address_city || '';
    m.querySelector('#edit-addr-state').value  = p.address_state || '';
    m.querySelector('#edit-addr-zip').value    = p.address_zip || '';
    m.querySelector('#edit-reason').value      = '';
    m.querySelector('#edit-person-error').style.display   = 'none';
    m.querySelector('#edit-person-success').style.display = 'none';
    new bootstrap.Modal(m).show();
  });
}

function submitPersonEdit() {
  if (!_editPersonId) return;
  const m = document.getElementById('editPersonModal');
  const reason = m.querySelector('#edit-reason').value.trim();
  if (!reason) {
    m.querySelector('#edit-person-error').style.display = 'flex';
    m.querySelector('#edit-error-msg').textContent = 'A reason for the edit is required.';
    return;
  }
  const payload = {
    first_name:             m.querySelector('#edit-first').value.trim(),
    middle_name:            m.querySelector('#edit-middle').value.trim() || null,
    last_name:              m.querySelector('#edit-last').value.trim() || null,
    gender:                 m.querySelector('#edit-gender').value,
    date_of_birth:          m.querySelector('#edit-dob').value,
    place_of_birth_city:    m.querySelector('#edit-city').value.trim(),
    place_of_birth_state:   m.querySelector('#edit-state').value.trim() || null,
    place_of_birth_country: m.querySelector('#edit-country').value.trim() || 'USA',
    citizenship_status:     m.querySelector('#edit-citizenship').value,
    address_street:         m.querySelector('#edit-street').value.trim() || null,
    address_city:           m.querySelector('#edit-addr-city').value.trim() || null,
    address_state:          m.querySelector('#edit-addr-state').value.trim() || null,
    address_zip:            m.querySelector('#edit-addr-zip').value.trim() || null,
    _edit_reason:           reason,
  };
  apiFetch(`/persons/${_editPersonId}/`, { method: 'PATCH', body: JSON.stringify(payload) })
    .then(() => {
      m.querySelector('#edit-person-error').style.display   = 'none';
      m.querySelector('#edit-person-success').style.display = 'flex';
      setTimeout(() => {
        bootstrap.Modal.getInstance(m).hide();
        if (typeof loadPersons === 'function') loadPersons();
        if (typeof loadData === 'function') loadData();
      }, 1200);
    })
    .catch(err => {
      m.querySelector('#edit-person-error').style.display = 'flex';
      m.querySelector('#edit-error-msg').textContent = `Save failed: ${err.message}`;
    });
}

// ── SHARED EDIT MODAL HTML (inject into body) ─────────────────────
function injectEditModal() {
  document.body.insertAdjacentHTML('beforeend', `
  <div class="modal fade" id="editPersonModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header" style="background:var(--cobalt-deeper);border-bottom:2px solid var(--gold);">
          <h5 class="modal-title" style="font-family:var(--font-display);letter-spacing:2px;color:white;font-size:14px;">
            <i class="bi bi-pencil-square me-2"></i>EDIT PERSON RECORD
          </h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body" style="padding:24px;">
          <div class="alert-banner warning mb-3" style="font-size:12px;">
            <i class="bi bi-exclamation-triangle"></i>
            All edits are permanently logged with timestamp, officer, and reason.
          </div>
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">First Name *</label>
              <input type="text" class="form-control-gov" id="edit-first" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Middle Name</label>
              <input type="text" class="form-control-gov" id="edit-middle" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Last Name</label>
              <input type="text" class="form-control-gov" id="edit-last" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Gender</label>
              <select class="form-control-gov" id="edit-gender">
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
                <option value="OTHER">Other / Not Specified</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">Date of Birth *</label>
              <input type="date" class="form-control-gov" id="edit-dob" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Citizenship</label>
              <select class="form-control-gov" id="edit-citizenship">
                <option value="CITIZEN">Citizen</option>
                <option value="PERMANENT_RESIDENT">Permanent Resident</option>
                <option value="VISA_HOLDER">Visa Holder</option>
                <option value="UNDOCUMENTED_ALIEN">Undocumented Alien</option>
                <option value="OTHER">Other</option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="form-label">City of Birth *</label>
              <input type="text" class="form-control-gov" id="edit-city" />
            </div>
            <div class="col-md-4">
              <label class="form-label">State of Birth</label>
              <input type="text" class="form-control-gov" id="edit-state" />
            </div>
            <div class="col-md-4">
              <label class="form-label">Country of Birth</label>
              <input type="text" class="form-control-gov" id="edit-country" />
            </div>
            <div class="col-12"><hr style="border-color:var(--light-gray);margin:4px 0;" /></div>
            <div class="col-md-6">
              <label class="form-label">Street Address</label>
              <input type="text" class="form-control-gov" id="edit-street" placeholder="123 Main St" />
            </div>
            <div class="col-md-2">
              <label class="form-label">City</label>
              <input type="text" class="form-control-gov" id="edit-addr-city" />
            </div>
            <div class="col-md-2">
              <label class="form-label">State</label>
              <input type="text" class="form-control-gov" id="edit-addr-state" />
            </div>
            <div class="col-md-2">
              <label class="form-label">ZIP</label>
              <input type="text" class="form-control-gov" id="edit-addr-zip" />
            </div>
            <div class="col-12">
              <label class="form-label" style="color:var(--danger);">Reason for Edit <span style="color:var(--danger);">*</span></label>
              <textarea class="form-control-gov" id="edit-reason" rows="2"
                placeholder="e.g. Correcting typographical error in date of birth per official birth certificate scan #BR-2026-0042"></textarea>
              <div style="font-size:11px;color:var(--text-muted);margin-top:4px;">
                This reason will be permanently recorded in the audit log with your credentials and a timestamp.
              </div>
            </div>
          </div>
          <div class="alert-banner danger mt-3" id="edit-person-error" style="display:none;">
            <i class="bi bi-exclamation-triangle"></i><span id="edit-error-msg">Error</span>
          </div>
          <div class="alert-banner info mt-3" id="edit-person-success" style="display:none;">
            <i class="bi bi-check-circle"></i>Record updated and change logged successfully.
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-secondary" data-bs-dismiss="modal">Cancel</button>
          <button type="button" class="btn-primary" onclick="submitPersonEdit()">
            <i class="bi bi-save me-1"></i>Save &amp; Log Change
          </button>
        </div>
      </div>
    </div>
  </div>`);
}