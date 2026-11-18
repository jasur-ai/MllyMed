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
function mobileNavTab(tab) {
  document.querySelectorAll('.dock-item, .island-tab-btn, .nav-item-btn').forEach(b => b.classList.remove('active'));
  
  if (tab === 'drugs' || tab === 'home') {
    const btn = $('tab-mob-drugs') || $('tab-mob-home');
    if (btn) btn.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    const popup = $('agent-popup');
    if (popup && !popup.classList.contains('hidden')) {
      popup.classList.add('hidden');
    }
  } else if (tab === 'rxs') {
    const btn = $('tab-mob-rxs');
    if (btn) btn.classList.add('active');
    if (typeof openAuthModal === 'function') {
      openAuthModal();
    }
  } else if (tab === 'auth') {
    const btn = $('tab-mob-auth');
    if (btn) btn.classList.add('active');
    if (typeof openAuthModal === 'function') {
      openAuthModal();
    }
  } else if (tab === 'ai') {
    if (typeof toggleAgentPopup === 'function') {
      toggleAgentPopup();
    }
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
      if (typeof tg.setHeaderColor === 'function') tg.setHeaderColor('#ffffff');
      if (typeof tg.setBackgroundColor === 'function') tg.setBackgroundColor('#f8fafc');

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
});

window.switchMode = switchMode;
window.mobileNavTab = mobileNavTab;
window.onSearchInput = onSearchInput;
window.openNotificationModal = openNotificationModal;
window.closeNotificationModal = closeNotificationModal;
