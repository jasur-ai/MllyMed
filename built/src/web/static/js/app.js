/**
 * MllyMed Frontend Application Bootstrap
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
    switchB2BTab(AppState.activeB2BTab);
  }
}

// Qidiruv kechiktiruvchi (Debounce)
let searchTimer = null;
function onSearchInput() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    loadCatalog(true);
  }, 280);
}

document.addEventListener('DOMContentLoaded', () => {
  // Qidiruv kiritish tinglovchisi
  const searchInput = $('q');
  if (searchInput) {
    searchInput.addEventListener('input', onSearchInput);
  }

  // Filtr o'zgarishi
  const localSelect = $('cat-local');
  if (localSelect) {
    localSelect.addEventListener('change', () => loadCatalog(true));
  }

  // Boshlang'ich katalog yuklash
  loadCatalog(true);
});

window.switchMode = switchMode;
window.onSearchInput = onSearchInput;
