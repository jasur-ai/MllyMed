/**
 * MllyMed B2C — Bemor Portali & Identifikatsiya (OneID, MyGov, Telefon)
 */

let isUserLoggedIn = false;
let loggedInUser = null;

function openAuthModal() {
  const modal = $('patient-modal');
  if (!modal) return;
  modal.classList.remove('hidden');

  if (isUserLoggedIn) {
    showCabinetView();
  } else {
    showLoginView();
  }
}

function closePatientModal() {
  const modal = $('patient-modal');
  if (modal) modal.classList.add('hidden');
  
  const authBtn = $('tab-mob-auth');
  if (authBtn && authBtn.classList.contains('active')) {
    authBtn.classList.remove('active');
    const drugsBtn = $('tab-mob-drugs');
    if (drugsBtn) drugsBtn.classList.add('active');
  }
}

function showLoginView() {
  const viewLogin = $('auth-view-login');
  const viewCabinet = $('auth-view-cabinet');
  const title = $('modal-auth-title');
  if (viewLogin) viewLogin.classList.remove('hidden');
  if (viewCabinet) viewCabinet.classList.add('hidden');
  if (title) title.textContent = "Tizimga kirish";
}

function showCabinetView() {
  const viewLogin = $('auth-view-login');
  const viewCabinet = $('auth-view-cabinet');
  const title = $('modal-auth-title');
  if (viewLogin) viewLogin.classList.add('hidden');
  if (viewCabinet) viewCabinet.classList.remove('hidden');
  if (title) title.textContent = "Bemor Shaxsiy Kabineti";
  loadPatientState();
}

function loginWithOneId() {
  isUserLoggedIn = true;
  loggedInUser = {
    name: "Sohibjon Sulaymonov",
    id: "JShShIR: 32408990000000",
    provider: "OneID"
  };
  updateNavLoginState();
  showCabinetView();
}

function loginWithMyGov() {
  isUserLoggedIn = true;
  loggedInUser = {
    name: "Sohibjon Sulaymonov",
    id: "MyGov ID: #849201",
    provider: "MyGov.uz"
  };
  updateNavLoginState();
  showCabinetView();
}

function loginWithPhone(e) {
  if (e) e.preventDefault();
  const phone = $('auth-phone')?.value.trim();
  if (!phone || phone.length < 7) {
    alert("Iltimos, telefon raqamingizni to'liq kiriting");
    return;
  }
  isUserLoggedIn = true;
  loggedInUser = {
    name: "Foydalanuvchi (+998 " + phone + ")",
    id: "+998 " + phone,
    provider: "SMS"
  };
  updateNavLoginState();
  showCabinetView();
}

function logoutPatient() {
  isUserLoggedIn = false;
  loggedInUser = null;
  updateNavLoginState();
  showLoginView();
}

function updateNavLoginState() {
  const btn = $('btn-nav-auth');
  if (!btn) return;
  if (isUserLoggedIn) {
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
        <circle cx="12" cy="7" r="4"/>
      </svg>
      Kabinet
    `;
    btn.style.background = "#059669";
  } else {
    btn.innerHTML = `
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
        <polyline points="10 17 15 12 10 7"/>
        <line x1="15" y1="12" x2="3" y2="12"/>
      </svg>
      Kirish
    `;
    btn.style.background = "var(--primary)";
  }

  const mobLabel = $('tab-mob-auth-label');
  if (mobLabel) {
    mobLabel.textContent = isUserLoggedIn ? 'Kabinet' : 'Kirish';
  }

  const mobUser = $('mob-user-display');
  if (mobUser) {
    mobUser.textContent = isUserLoggedIn ? (loggedInUser?.name?.split(' ')[0] || 'Sohibjon') : 'Sohibjon';
  }
}

async function loadPatientState() {
  const apptsEl = $('patient-appts-list');
  const rxsEl = $('patient-rxs-list');
  const patientIdEl = $('patient-id-display');
  const providerBadge = $('patient-provider-badge');

  if (patientIdEl) {
    patientIdEl.textContent = loggedInUser?.name || AppState.sid;
  }
  if (providerBadge) {
    providerBadge.textContent = loggedInUser?.provider || "Tizim";
  }

  try {
    const res = await api('/api/state?sid=' + AppState.sid, null, 'patient');
    
    let aHtml = '';
    if (!(res.appointments || []).length) {
      aHtml = `<span style="font-size:13px;color:var(--text-muted)">Sizda hali faol qabullar mavjud emas.</span>`;
    } else {
      res.appointments.forEach(a => {
        aHtml += `
          <div style="padding:10px 14px;border:1px solid var(--border-light);border-radius:var(--radius-sm);margin-bottom:8px;font-size:13px;background:#f8fafc">
            Shifokor: <b>${esc(a.doctor_name || a.doctor_id)}</b> (${esc(a.slot)})<br>
            Status: <span class="badge ${a.status === 'confirmed' ? 'badge-local' : 'badge-import'}">${esc(a.status)}</span>
          </div>
        `;
      });
    }
    if (apptsEl) apptsEl.innerHTML = aHtml;

    let rHtml = '';
    if (!(res.prescriptions || []).length) {
      rHtml = `<span style="font-size:13px;color:var(--text-muted)">Sizga hali elektron retsept yozilmagan.</span>`;
    } else {
      res.prescriptions.forEach(r => {
        rHtml += `
          <div style="padding:10px 14px;border:1px solid var(--border-light);border-radius:var(--radius-sm);margin-bottom:8px;font-size:13px;background:#f8fafc">
            Dori XPN: <b>${esc(r.inn)}</b><br>
            Holati: <span class="badge ${r.status === 'dispensed' ? 'badge-local' : 'badge-otc'}">${esc(r.status)}</span>
          </div>
        `;
      });
    }
    if (rxsEl) rxsEl.innerHTML = rHtml;
  } catch (e) {
    if (apptsEl) apptsEl.innerHTML = `<span style="color:#ef4444;font-size:13px">Xato: ${esc(e.message)}</span>`;
  }
}

window.openAuthModal = openAuthModal;
window.closePatientModal = closePatientModal;
window.loginWithOneId = loginWithOneId;
window.loginWithMyGov = loginWithMyGov;
window.loginWithPhone = loginWithPhone;
window.logoutPatient = logoutPatient;
window.loadPatientState = loadPatientState;
