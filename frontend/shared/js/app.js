/**
 * MllyMed Frontend — Asosiy ilova boshqaruvchisi
 * B2C va B2B rejimlari almashinuvi, mobil pastki menyu va bootstrap
 */

function switchMode(mode) {
  AppState.activeMode = mode;
  
  const b2cSec = $('sec-b2c');
  const b2bSec = $('sec-b2b');
  const btnB2C = $('mode-btn-b2c');
  const btnB2B = $('mode-btn-b2b');

  if (mode === 'b2c') {
    if (b2cSec) b2cSec.classList.remove('hidden');
    if (b2bSec) b2bSec.classList.add('hidden');
    if (btnB2C) btnB2C.classList.add('active');
    if (btnB2B) btnB2B.classList.remove('active');
  } else {
    if (b2cSec) b2cSec.classList.add('hidden');
    if (b2bSec) b2bSec.classList.remove('hidden');
    if (btnB2C) btnB2C.classList.remove('active');
    if (btnB2B) btnB2B.classList.add('active');
    if (typeof switchB2BTab === 'function') {
      switchB2BTab(AppState.activeB2BTab);
    }
  }
}

/**
 * Real Mobile App Bottom Navigation Bar boshqaruvi
 */
/**
 * Real Mobile App Bottom Navigation Bar boshqaruvi
 */
function mobileNavTab(tab) {
  document.querySelectorAll('.dock-item, .island-tab-btn, .nav-item-btn').forEach(b => b.classList.remove('active'));
  
  if (tab === 'home') {
    const btn = $('tab-mob-home');
    if (btn) btn.classList.add('active');
    
    // Boshqa ochiq oynalarni yopish
    if (typeof closeAllDrugsView === 'function') closeAllDrugsView();
    closeCalendarModal();
    if (typeof closePatientModal === 'function') closePatientModal();
    closeNotificationModal();
    const popup = $('agent-popup');
    if (popup && !popup.classList.contains('hidden')) {
      popup.classList.add('hidden');
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else if (tab === 'drugs') {
    if (typeof closePatientModal === 'function') closePatientModal();
    closeCalendarModal();
    closeNotificationModal();
    if (typeof openAllDrugsView === 'function') openAllDrugsView();
  } else if (tab === 'rxs' || tab === 'calendar') {
    const btn = $('tab-mob-rxs');
    if (btn) btn.classList.add('active');
    
    if (typeof closeAllDrugsView === 'function') closeAllDrugsView();
    if (typeof closePatientModal === 'function') closePatientModal();
    closeNotificationModal();
    const popup = $('agent-popup');
    if (popup && !popup.classList.contains('hidden')) {
      popup.classList.add('hidden');
    }
    openCalendarModal();
  } else if (tab === 'auth' || tab === 'profile') {
    const btn = $('tab-mob-auth');
    if (btn) btn.classList.add('active');
    
    closeCalendarModal();
    closeNotificationModal();
    const popup = $('agent-popup');
    if (popup && !popup.classList.contains('hidden')) {
      popup.classList.add('hidden');
    }
    if (typeof openAuthModal === 'function') {
      openAuthModal();
    }
  } else if (tab === 'ai' || tab === 'support') {
    openSupportChat();
  }
}

/**
 * Kalendar modali
 */
async function openCalendarModal() {
  const modal = $('calendar-modal');
  if (modal) modal.classList.remove('hidden');
  loadCalendarAppointments();
}

async function loadCalendarAppointments() {
  const container = $('cal-appointments-list');
  if (!container) return;
  try {
    const res = await api('/api/b2c/calendar?sid=' + (window.AppState ? AppState.sid : 'demo'), null, 'patient');
    if (res && res.appointments && res.appointments.length > 0) {
      let html = '';
      res.appointments.forEach(a => {
        const docName = a.doctor_name || (a.doctor_id === 'd01' ? 'Dr. A. Karimova' : (a.doctor_id === 'd02' ? 'Dr. B. Toshpulatov' : 'Dr. Mutaxassis'));
        const specName = a.specialist === 'terapevt' ? 'Terapevt shifokor' : (a.specialist || 'Shifokor');
        const slotClean = (a.slot || '').replace('T', ' ');
        const clinicName = a.doctor_id === 'd01' ? '1-son shahar poliklinikasi' : 'Markaziy Poliklinika';
        const isConfirmed = a.status === 'confirmed';

        html += `
          <div class="cal-card-appt" style="margin-bottom:10px">
            <div class="cal-appt-row">
              <img src="https://images.unsplash.com/photo-1594824813587-08e64c239327?w=120&auto=format&fit=crop&q=80" alt="Doctor" class="cal-doctor-avatar">
              <div class="cal-appt-meta">
                <div style="display:flex;justify-content:space-between;align-items:center">
                  <b style="font-size:14.5px;color:#0f172a">${esc(docName)}</b>
                  <span class="badge ${isConfirmed ? 'badge-local' : 'badge-otc'}" style="font-size:10px">${isConfirmed ? 'Tasdiqlangan' : 'Kutilmoqda'}</span>
                </div>
                <div style="font-size:12px;color:#64748b;margin:2px 0">${esc(specName)}</div>
                <div style="font-size:11.5px;color:#0b69ed;display:flex;align-items:center;gap:4px">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12 6 12 12 16 14"/>
                  </svg>
                  <b>${esc(slotClean)}</b> · ${esc(clinicName)}
                </div>
              </div>
            </div>
            <div class="cal-appt-btns">
              <button class="cal-btn-sec" onclick="closeCalendarModal();openAuthModal()">Navbat holati</button>
              <button class="cal-btn-prim" onclick="closeCalendarModal();lookup('Paratsetamol')">Dori retsepti</button>
            </div>
          </div>
        `;
      });
      container.innerHTML = html;
    }
  } catch (err) {
    console.log('Calendar fetch err:', err);
  }
}

function closeCalendarModal() {
  const modal = $('calendar-modal');
  if (modal) modal.classList.add('hidden');
  
  const calBtn = $('tab-mob-rxs');
  if (calBtn && calBtn.classList.contains('active')) {
    calBtn.classList.remove('active');
    const homeBtn = $('tab-mob-home') || $('tab-mob-drugs');
    if (homeBtn) homeBtn.classList.add('active');
  }
}

/**
 * Support (MllyMed AI) to'liq chat ochish
 */
function openSupportChat() {
  closeCalendarModal();
  if (typeof closePatientModal === 'function') closePatientModal();
  closeNotificationModal();
  
  const popup = $('agent-popup');
  if (!popup) return;
  
  popup.classList.remove('hidden');
  
  const stream = $('chat-log');
  if (stream) {
    setTimeout(() => { stream.scrollTop = stream.scrollHeight; }, 100);
  }
  const inp = $('chat-in');
  if (inp) {
    setTimeout(() => { inp.focus(); }, 250);
  }
}

/**
 * Bildirishnomalar modali
 */
function openNotificationModal() {
  const modal = $('notification-modal');
  if (modal) modal.classList.remove('hidden');
}

function closeNotificationModal() {
  const modal = $('notification-modal');
  if (modal) modal.classList.add('hidden');
}

let searchTimer = null;
function onSearchInput() {
  const inp = $('q');
  const clearBtn = $('search-clear-btn');
  if (clearBtn) {
    if (inp && inp.value.trim().length > 0) {
      clearBtn.classList.remove('hidden');
    } else {
      clearBtn.classList.add('hidden');
    }
  }

  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    if (typeof loadCatalog === 'function') loadCatalog(true);
  }, 280);
}

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = $('q');
  if (searchInput) {
    searchInput.addEventListener('input', onSearchInput);
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        clearTimeout(searchTimer);
        if (typeof loadCatalog === 'function') loadCatalog(true);
      }
    });
  }

  const mobSearch = $('mob-search-input');
  if (mobSearch && searchInput) {
    mobSearch.addEventListener('input', (e) => {
      searchInput.value = e.target.value;
      onSearchInput();
      const clearBtn = $('mob-search-clear');
      if (clearBtn) {
        if (e.target.value.trim().length > 0) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }
    });
    mobSearch.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        clearTimeout(searchTimer);
        if (typeof loadCatalog === 'function') loadCatalog(true);
      }
    });
  }

  const localSelect = $('cat-local');
  if (localSelect) {
    localSelect.addEventListener('change', () => {
      if (typeof loadCatalog === 'function') loadCatalog(true);
    });
  }

  if (typeof loadCatalog === 'function') {
    loadCatalog(true);
  }

  // Telegram Mini App (TMA) Native Avto-Moslashuv
  if (window.Telegram && window.Telegram.WebApp) {
    try {
      const tg = window.Telegram.WebApp;
      tg.ready();
      tg.expand();
      if (typeof tg.enableClosingConfirmation === 'function') {
        tg.enableClosingConfirmation();
      }
      if (typeof tg.setHeaderColor === 'function') tg.setHeaderColor('#eef3fb');
      if (typeof tg.setBackgroundColor === 'function') tg.setBackgroundColor('#eef3fb');

      if (tg.initDataUnsafe && tg.initDataUnsafe.user) {
        const u = tg.initDataUnsafe.user;
        const fullName = [u.first_name, u.last_name].filter(Boolean).join(' ') || u.username || 'Foydalanuvchi';
        window.telegramUser = {
          id: u.id,
          name: fullName,
          username: u.username,
          photo_url: u.photo_url
        };
        // Shaxsiy kabinetga avtomatik biriktirish
        if (typeof isUserLoggedIn !== 'undefined' && !isUserLoggedIn) {
          isUserLoggedIn = true;
          loggedInUser = {
            name: fullName + (u.username ? ` (@${u.username})` : ''),
            id: `Telegram ID: ${u.id}`,
            provider: 'Telegram'
          };
          const patientDisplay = $('patient-id-display');
          const badge = $('patient-provider-badge');
          if (patientDisplay) patientDisplay.textContent = loggedInUser.name;
          if (badge) badge.textContent = 'Telegram';
          const mobLabel = $('tab-mob-auth-label');
          if (mobLabel) mobLabel.textContent = 'Kabinet';
        }
      }
    } catch (tgErr) {
      console.log('TG WebApp auto-init warning:', tgErr);
    }
  }

  // URL Deep Linklar (tab=calendar, q=...)
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get('tab');
    if (tabParam === 'calendar' || window.location.hash === '#calendar') {
      setTimeout(() => {
        if (typeof mobileNavTab === 'function') mobileNavTab('calendar');
      }, 200);
    } else if (tabParam === 'auth' || tabParam === 'profile') {
      setTimeout(() => {
        if (typeof mobileNavTab === 'function') mobileNavTab('auth');
      }, 200);
    }

    const qParam = urlParams.get('q');
    if (qParam) {
      const qInp = $('q');
      if (qInp) {
        qInp.value = qParam;
        setTimeout(() => {
          if (typeof loadCatalog === 'function') loadCatalog(true);
        }, 200);
      }
    }
  } catch (linkErr) {
    console.log('URL deep link err:', linkErr);
  }
});

window.switchMode = switchMode;
window.mobileNavTab = mobileNavTab;
window.onSearchInput = onSearchInput;
window.openNotificationModal = openNotificationModal;
window.closeNotificationModal = closeNotificationModal;
