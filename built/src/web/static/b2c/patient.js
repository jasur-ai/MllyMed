/**
 * MllyMed B2C — Bemor Portali & Identifikatsiya (OneID & Telefon)
 */

let isUserLoggedIn = false;
let loggedInUser = null;

// Avval saqlangan sessiyani yuklash
try {
  const saved = localStorage.getItem('mllymed_auth_user');
  if (saved) {
    loggedInUser = JSON.parse(saved);
    isUserLoggedIn = true;
  }
} catch (e) {}

// Ismlarning bosh harflaridan deterministik monogramli avatar
function monogramAvatarDataUri(name) {
  let h = 0;
  const str = String(name || 'Sohibjon Sulaymonov');
  for (let i = 0; i < str.length; i++) { h = (Math.imul(h, 31) + str.charCodeAt(i)) | 0; }
  const hue = Math.abs(h) % 360;
  const words = str.trim().split(/\s+/).filter(Boolean);
  const initials = ((words[0] ? words[0][0] : 'S') + (words[1] ? words[1][0] : 'S')).toUpperCase();
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
    + '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
    + '<stop offset="0" stop-color="hsl(' + hue + ',82%,48%)"/><stop offset="1" stop-color="hsl(' + hue + ',76%,32%)"/>'
    + '</linearGradient></defs>'
    + '<rect width="100" height="100" rx="50" fill="url(#g)"/>'
    + '<text x="50" y="64" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="38" font-weight="800" fill="#ffffff">' + initials + '</text>'
    + '</svg>';
  return 'data:image/svg+xml,' + encodeURIComponent(svg);
}

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
    const homeBtn = $('tab-mob-home') || $('tab-mob-drugs');
    if (homeBtn) homeBtn.classList.add('active');
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
  if (title) title.textContent = "Bemor Shaxsiy Profili";
  loadPatientState();
}

function loginWithOneId() {
  isUserLoggedIn = true;
  loggedInUser = {
    name: "Sohibjon Sulaymonov",
    pinfl: "32408996540012",
    passport: "AB 1234567",
    phone: "+998 (90) 123-45-67",
    blood: "II (A) Rh+",
    clinic: "14-sonli shahar oilaviy poliklinikasi (Yunusobod)",
    doctor: "Dr. Karimova Aziza (Terapevt, Oliy toifa)",
    provider: "OneID"
  };
  try { localStorage.setItem('mllymed_auth_user', JSON.stringify(loggedInUser)); } catch (e) {}
  updateNavLoginState();
  showCabinetView();
}

function loginWithPhone(e) {
  if (e) e.preventDefault();
  const phone = $('auth-phone')?.value.trim();
  isUserLoggedIn = true;
  loggedInUser = {
    name: "Sohibjon Sulaymonov",
    pinfl: "32408996540012",
    passport: "AB 1234567",
    phone: phone ? (phone.startsWith('+998') ? phone : '+998 ' + phone) : "+998 (90) 123-45-67",
    blood: "II (A) Rh+",
    clinic: "14-sonli shahar oilaviy poliklinikasi (Yunusobod)",
    doctor: "Dr. Karimova Aziza (Terapevt, Oliy toifa)",
    provider: "OneID (SMS)"
  };
  try { localStorage.setItem('mllymed_auth_user', JSON.stringify(loggedInUser)); } catch (e) {}
  updateNavLoginState();
  showCabinetView();
}

function logoutPatient() {
  isUserLoggedIn = false;
  loggedInUser = null;
  try { localStorage.removeItem('mllymed_auth_user'); } catch (e) {}
  updateNavLoginState();
  showLoginView();
}

function updateNavLoginState() {
  const btn = $('btn-nav-auth');
  if (btn) {
    if (isUserLoggedIn) {
      btn.innerHTML = `
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
          <circle cx="12" cy="7" r="4"/>
        </svg>
        Profil
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
  }

  const mobLabel = $('tab-mob-auth-label');
  if (mobLabel) {
    mobLabel.textContent = isUserLoggedIn ? 'Profil' : 'Kirish';
  }

  const mobUser = $('mob-user-display');
  if (mobUser) {
    mobUser.textContent = isUserLoggedIn ? (loggedInUser?.name?.split(' ')[0] || 'Sohibjon') : 'Sohibjon';
  }

  const mobAvatar = $('mob-nav-avatar');
  if (mobAvatar && isUserLoggedIn && loggedInUser?.name) {
    mobAvatar.src = monogramAvatarDataUri(loggedInUser.name);
  }
}

async function loadPatientState() {
  const patientIdEl = $('patient-id-display');
  const providerBadge = $('patient-provider-badge');
  const pinflEl = $('profile-pinfl-display');
  const phoneEl = $('profile-phone-display');
  const bloodEl = $('profile-blood-display');
  const clinicEl = $('profile-clinic-display');
  const doctorEl = $('profile-doctor-display');
  const avatarImg = $('profile-avatar-img');
  const apptsEl = $('patient-appts-list');
  const rxsEl = $('patient-rxs-list');

  const u = loggedInUser || {
    name: "Sohibjon Sulaymonov",
    pinfl: "32408996540012",
    passport: "AB 1234567",
    phone: "+998 (90) 123-45-67",
    blood: "II (A) Rh+",
    clinic: "14-sonli shahar oilaviy poliklinikasi (Yunusobod)",
    doctor: "Dr. Karimova Aziza (Terapevt, Oliy toifa)",
    provider: "OneID"
  };

  if (patientIdEl) patientIdEl.textContent = u.name;
  if (providerBadge) providerBadge.innerHTML = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg> ${esc(u.provider || 'OneID')}`;
  if (pinflEl) pinflEl.textContent = `JShShIR: ${u.pinfl} · ${u.passport}`;
  if (phoneEl) phoneEl.textContent = u.phone;
  if (bloodEl) bloodEl.textContent = u.blood || "II (A) Rh+";
  if (clinicEl) clinicEl.textContent = u.clinic;
  if (doctorEl) doctorEl.textContent = u.doctor;
  if (avatarImg) avatarImg.src = monogramAvatarDataUri(u.name);

  // DMED Appts & E-Rxs
  try {
    const res = await api('/api/state?sid=' + AppState.sid, null, 'patient');
    
    // Appointments
    const appts = (res.appointments && res.appointments.length) ? res.appointments : [
      {
        doctor_name: "Dr. Karimova Aziza",
        specialist: "Terapevt",
        clinic_name: "14-sonli poliklinika (Yunusobod)",
        slot: "Ertaga, 10:30 (Xona: 204)",
        ticket: "#A-42",
        status: "confirmed"
      }
    ];

    let aHtml = appts.map(a => `
      <div class="profile-item-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <b style="color:#0f172a;font-size:13px">${esc(a.doctor_name || 'Dr. Karimova')}</b>
            <span style="color:#64748b;font-size:11.5px"> · ${esc(a.specialist || 'Terapevt')}</span>
            <div style="color:#0b69ed;font-weight:700;font-size:12px;margin-top:2px">${esc(a.slot || '10:30')}</div>
          </div>
          <span class="badge ${a.status === 'confirmed' ? 'badge-local' : 'badge-otc'}" style="font-size:10px">
            ${a.status === 'confirmed' ? '✓ Tasdiqlangan' : esc(a.status)}
          </span>
        </div>
        <div style="font-size:11px;color:#94a3b8;margin-top:4px">Talon: <b style="color:#334155">${esc(a.ticket || '#A-42')}</b> · ${esc(a.clinic_name || '14-son poliklinika')}</div>
      </div>
    `).join('');
    if (apptsEl) apptsEl.innerHTML = aHtml;

    // Prescriptions
    const rxs = (res.prescriptions && res.prescriptions.length) ? res.prescriptions : [
      {
        inn: "Paratsetamol 500mg №10",
        date: "16.11.2026",
        status: "Faol (Dorixonadan olish mumkin)",
        doctor: "Dr. Karimova A.",
        lookup_q: "Paratsetamol"
      },
      {
        inn: "Amoksitsillin 500mg №20",
        date: "12.11.2026",
        status: "Berilgan (Dispensed)",
        doctor: "Dr. Karimova A.",
        lookup_q: "Amoksitsillin"
      }
    ];

    let rHtml = rxs.map(r => `
      <div class="profile-item-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start">
          <div>
            <b style="color:#0f172a;font-size:13px">${esc(r.inn || 'Dori')}</b>
            <div style="color:#64748b;font-size:11px;margin-top:2px">Yozilgan sana: ${esc(r.date || '16.11.2026')} · ${esc(r.doctor || 'Shifokor')}</div>
          </div>
          <span class="badge ${r.status.includes('Faol') ? 'badge-local' : 'badge-otc'}" style="font-size:10px">${esc(r.status)}</span>
        </div>
        ${r.lookup_q ? `
          <div style="margin-top:6px;display:flex;justify-content:flex-end">
            <button type="button" class="btn-secondary" style="font-size:11px;padding:3px 8px;border-radius:6px;color:#0b69ed;border-color:#bfdbfe" onclick="closePatientModal();lookup('${esc(r.lookup_q)}')">
              🔍 80% arzon analogini ko'rish
            </button>
          </div>
        ` : ''}
      </div>
    `).join('');
    if (rxsEl) rxsEl.innerHTML = rHtml;

  } catch (e) {
    if (apptsEl) apptsEl.innerHTML = `<span style="color:#ef4444;font-size:12px">Qabullarni yuklab bo'lmadi</span>`;
    if (rxsEl) rxsEl.innerHTML = `<span style="color:#ef4444;font-size:12px">Retseptlarni yuklab bo'lmadi</span>`;
  }
}

// Boshlang'ich yuklanganda nav holatini sinxronlash
document.addEventListener('DOMContentLoaded', () => {
  updateNavLoginState();
});

window.openAuthModal = openAuthModal;
window.closePatientModal = closePatientModal;
window.loginWithOneId = loginWithOneId;
window.loginWithPhone = loginWithPhone;
window.logoutPatient = logoutPatient;
window.loadPatientState = loadPatientState;
