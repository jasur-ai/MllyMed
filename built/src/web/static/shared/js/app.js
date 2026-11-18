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
  document.querySelectorAll('.nav-item-btn').forEach(b => b.classList.remove('active'));
  
  if (tab === 'drugs') {
    const btn = $('tab-mob-drugs');
    if (btn) btn.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
    const popup = $('agent-popup');
    if (popup && !popup.classList.contains('hidden')) {
      popup.classList.add('hidden');
    }
  } else if (tab === 'search') {
    const btn = $('tab-mob-search');
    if (btn) btn.classList.add('active');
    const inp = $('q');
    if (inp) {
      inp.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => inp.focus(), 250);
    }
  } else if (tab === 'ai') {
    const btn = $('tab-mob-ai');
    if (btn) btn.classList.add('active');
    if (typeof toggleAgentPopup === 'function') {
      toggleAgentPopup();
    }
  } else if (tab === 'auth') {
    const btn = $('tab-mob-auth');
    if (btn) btn.classList.add('active');
    if (typeof openAuthModal === 'function') {
      openAuthModal();
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

  const localSelect = $('cat-local');
  if (localSelect) {
    localSelect.addEventListener('change', () => {
      if (typeof loadCatalog === 'function') loadCatalog(true);
    });
  }

  if (typeof loadCatalog === 'function') {
    loadCatalog(true);
  }
});

window.switchMode = switchMode;
window.mobileNavTab = mobileNavTab;
window.onSearchInput = onSearchInput;
window.openNotificationModal = openNotificationModal;
window.closeNotificationModal = closeNotificationModal;
