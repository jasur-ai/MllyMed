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
    const btn = $('tab-mob-home');
    if (btn) btn.classList.add('active');
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
  if (typeof updateDockIndicator === 'function') updateDockIndicator();
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
              <img src="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%20120%20120%22%3E%3Cdefs%3E%3ClinearGradient%20id=%22g%22%20x1=%220%22%20y1=%220%22%20x2=%221%22%20y2=%221%22%3E%3Cstop%20offset=%220%22%20stop-color=%22#5eead4%22/%3E%3Cstop%20offset=%221%22%20stop-color=%22#0e7490%22/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect%20width=%22120%22%20height=%22120%22%20rx=%2260%22%20fill=%22url%28#g%29%22/%3E%3Ccircle%20cx=%2260%22%20cy=%2244%22%20r=%2217%22%20fill=%22#ffffff%22%20opacity=%220.96%22/%3E%3Cpath%20d=%22M23%20112c5-25%2021-36%2037-36s32%2011%2037%2036Z%22%20fill=%22#ffffff%22%20opacity=%220.96%22/%3E%3Crect%20x=%2252.5%22%20y=%2278%22%20width=%2215%22%20height=%225.4%22%20rx=%222.7%22%20fill=%22#0e7490%22%20opacity=%220.85%22/%3E%3C/svg%3E" alt="Shifokor avatari" class="cal-doctor-avatar">
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

  animateStatCounters();
  setTimeout(updateDockIndicator, 350);

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

/* ── Toast bildirishnomalar ── */
function showToast(msg, iconName) {
  let root = document.getElementById('toast-root');
  if (!root) {
    root = document.createElement('div');
    root.id = 'toast-root';
    root.className = 'toast-root';
    root.setAttribute('aria-live', 'polite');
    document.body.appendChild(root);
  }
  const el = document.createElement('div');
  el.className = 'toast';
  const ic = typeof window.icon === 'function' ? window.icon(iconName || 'check-circle', 16, 2.2) : '';
  const span = document.createElement('span');
  span.textContent = String(msg == null ? '' : msg);
  el.innerHTML = ic;
  el.appendChild(span);
  root.appendChild(el);
  setTimeout(() => {
    el.classList.add('toast-out');
    setTimeout(() => el.remove(), 320);
  }, 2600);
}

/* ── Statistikalarni count-up bilan jonlantirish ── */
function animateStatCounters() {
  const fmt = n => Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '\u2009');
  document.querySelectorAll('.stat-val[data-count]').forEach(el => {
    const target = parseFloat(el.getAttribute('data-count')) || 0;
    const suffix = el.getAttribute('data-suffix') || '';
    const dur = 1300;
    const t0 = performance.now();
    function frame(t) {
      const k = Math.min(1, (t - t0) / dur);
      const e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(target * e) + suffix;
      if (k < 1) requestAnimationFrame(frame);
      else el.textContent = fmt(target) + suffix;
    }
    requestAnimationFrame(frame);
  });
}

/* ── Mobil dock: aktiv element ostiga sirg'aluvchi ko'rsatkich ── */
function updateDockIndicator() {
  const pill = document.querySelector('.mob-dock-pill');
  if (!pill) return;
  let ind = pill.querySelector('.dock-indicator');
  if (!ind) {
    ind = document.createElement('span');
    ind.className = 'dock-indicator';
    ind.setAttribute('aria-hidden', 'true');
    pill.insertBefore(ind, pill.firstChild);
  }
  const active = pill.querySelector('.dock-item.active');
  if (!active) { ind.style.opacity = '0'; return; }
  ind.style.opacity = '1';
  ind.style.left = active.offsetLeft + 'px';
  ind.style.width = active.offsetWidth + 'px';
}
window.addEventListener('resize', updateDockIndicator);

window.switchMode = switchMode;
window.mobileNavTab = mobileNavTab;
window.onSearchInput = onSearchInput;
window.openNotificationModal = openNotificationModal;
window.closeNotificationModal = closeNotificationModal;
window.showToast = showToast;
window.updateDockIndicator = updateDockIndicator;
