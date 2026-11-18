/**
 * MllyMed B2C — Dori Katalogi & 80% Mahalliy Ekvivalent Tahlili
 */

let currentCategory = '';
let favoritesList = JSON.parse(localStorage.getItem('mllymed_favs') || '[]');
let isFavoritesFilterActive = false;
let drugsViewPage = 1;
let drugsViewCategory = '';

function isFavorite(title) {
  return favoritesList.includes(title);
}

function toggleFavorite(title, event) {
  if (event) event.stopPropagation();
  if (favoritesList.includes(title)) {
    favoritesList = favoritesList.filter(t => t !== title);
  } else {
    favoritesList.push(title);
  }
  localStorage.setItem('mllymed_favs', JSON.stringify(favoritesList));
  updateFavBadge();
  document.querySelectorAll(`.card-fav-btn[data-title="${CSS.escape(title)}"]`).forEach(btn => {
    const active = isFavorite(title);
    btn.classList.toggle('active', active);
    const svg = btn.querySelector('svg');
    if (svg) {
      svg.setAttribute('fill', active ? '#ef4444' : 'none');
      svg.setAttribute('stroke', active ? '#ef4444' : '#94a3b8');
    }
  });
  if (isFavoritesFilterActive) {
    loadDrugsView(true);
  }
}

function updateFavBadge() {
  const dot = $('fav-count-dot');
  if (dot) {
    if (favoritesList.length > 0) dot.classList.remove('hidden');
    else dot.classList.add('hidden');
  }
}

function setCategory(cat, el) {
  currentCategory = cat || '';
  document.querySelectorAll('.category-btn').forEach(b => {
    b.classList.toggle('active', b.getAttribute('data-cat') === currentCategory);
  });
  loadCatalog(true);
}

// «Qidirish» tugmasi — darhol qidirish (debounce'ni kutmasdan)
function doSearchNow() {
  const inp = $('q');
  const mob = $('mob-search-input');
  if (inp && mob && mob.value !== inp.value) {
    // qaysi input aktiv bo'lsa — shuni asos qilib olamiz
    if (document.activeElement === mob) inp.value = mob.value;
    else mob.value = inp.value;
  }
  clearTimeout(window.searchTimer);
  loadCatalog(true);
}

// «Mahalliy GMP» servis kartasi — faqat mahalliy takliflarni ko'rsatadi
function filterLocalProducts() {
  const sel = $('cat-local');
  if (sel) sel.value = 'local';
  loadCatalog(true);
  const toolbar = document.querySelector('.catalog-toolbar');
  if (toolbar) toolbar.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function emptyStateHtml(q, category) {
  const what = q ? `«${esc(q)}»` : (category ? `«${esc(category)}»` : 'Tanlangan filtr');
  return `
    <div class="empty-state">
      <div class="empty-art">🔍</div>
      <h3 class="empty-title">${what} bo'yicha dori topilmadi</h3>
      <p class="empty-sub">Boshqa nom, XPN (INN) yoki ishlab chiqaruvchi bo'yicha urinib ko'ring. Qisqartma yoki imlo xatosini tekshiring.</p>
      <button class="btn-primary btn-empty-clear" onclick="clearSearch()">Qidiruvni tozalash</button>
    </div>`;
}

function skeletonHtml() {
  return Array(6).fill(`
    <div class="skeleton-card" aria-hidden="true">
      <div class="sk-media"></div>
      <div class="sk-line sk-w70"></div>
      <div class="sk-line sk-w50"></div>
      <div class="sk-line sk-w90"></div>
    </div>`).join('');
}

function quickSearch(term) {
  const inp = $('q');
  if (inp) {
    inp.value = term;
    const clearBtn = $('search-clear-btn');
    if (clearBtn) clearBtn.classList.remove('hidden');
    loadCatalog(true);
  }
}

function clearSearch() {
  const inp = $('q');
  const mobInp = $('mob-search-input');
  if (inp) inp.value = '';
  if (mobInp) mobInp.value = '';
  const clearBtn = $('search-clear-btn');
  const mobClearBtn = $('mob-search-clear');
  if (clearBtn) clearBtn.classList.add('hidden');
  if (mobClearBtn) mobClearBtn.classList.add('hidden');
  if (mobInp) mobInp.focus();
  else if (inp) inp.focus();
  loadCatalog(true);
}

function originBadge(isLocal) {
  if (isLocal === true) {
    return `<span class="badge badge-local">🇺🇿 Mahalliy (GMP)</span>`;
  }
  if (isLocal === false) {
    return `<span class="badge badge-import">🌍 Import</span>`;
  }
  return `<span class="badge" style="background:#f1f5f9;color:#64748b">Aniqmas</span>`;
}

function renderDrugPackSvg(title, isLocal) {
  const t = (title || '').toLowerCase();
  const primaryBg = isLocal ? '#059669' : '#0066ff';
  const secondaryBg = isLocal ? '#10b981' : '#38bdf8';

  // Inyeksiya / Ampula
  if (t.includes('ampul') || t.includes('ukol') || t.includes('inyeksiya') || t.includes('eritma inyeksiya')) {
    return `
      <svg class="pack-art" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="18" y="24" width="64" height="84" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
        <rect x="18" y="24" width="64" height="24" rx="8" fill="${primaryBg}"/>
        <g transform="translate(32, 54)">
          <path d="M6 0H10V8L12 12V34H4V12L6 8V0Z" fill="#e2e8f0" stroke="#94a3b8"/>
          <line x1="4" y1="20" x2="12" y2="20" stroke="${primaryBg}" stroke-width="2"/>
        </g>
        <g transform="translate(52, 54)">
          <path d="M6 0H10V8L12 12V34H4V12L6 8V0Z" fill="#e2e8f0" stroke="#94a3b8"/>
          <line x1="4" y1="20" x2="12" y2="20" stroke="${primaryBg}" stroke-width="2"/>
        </g>
      </svg>
    `;
  }

  // Sirop / Suspenziya / Eritma
  if (t.includes('sirop') || t.includes('eritma') || t.includes('tomchi') || t.includes('suspen')) {
    return `
      <svg class="pack-art" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="36" y="8" width="28" height="16" rx="4" fill="#64748b"/>
        <rect x="42" y="24" width="16" height="8" fill="#cbd5e1"/>
        <rect x="22" y="32" width="56" height="82" rx="12" fill="#d97706" fill-opacity="0.25" stroke="#b45309" stroke-width="2"/>
        <rect x="26" y="52" width="48" height="46" rx="4" fill="#ffffff" stroke="#e2e8f0"/>
        <rect x="30" y="58" width="40" height="8" rx="2" fill="${primaryBg}"/>
        <line x1="32" y1="74" x2="68" y2="74" stroke="#94a3b8" stroke-width="2" stroke-linecap="round"/>
        <line x1="32" y1="82" x2="56" y2="82" stroke="#cbd5e1" stroke-width="2" stroke-linecap="round"/>
      </svg>
    `;
  }

  // Maz / Krem / Gel
  if (t.includes('gel') || t.includes('maz') || t.includes('krem') || t.includes('surtma')) {
    return `
      <svg class="pack-art" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M30 18L70 18L64 88L36 88L30 18Z" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>
        <rect x="38" y="88" width="24" height="22" rx="3" fill="#64748b"/>
        <rect x="34" y="32" width="32" height="40" rx="3" fill="${primaryBg}" fill-opacity="0.15"/>
        <rect x="38" y="42" width="24" height="6" rx="2" fill="${primaryBg}"/>
        <line x1="38" y1="56" x2="62" y2="56" stroke="#94a3b8" stroke-width="2"/>
      </svg>
    `;
  }

  // Kapsulalar
  if (t.includes('kaps') || t.includes('caps')) {
    return `
      <svg class="pack-art" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="15" y="24" width="70" height="85" rx="10" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
        <rect x="15" y="24" width="70" height="28" rx="10" fill="${primaryBg}"/>
        <circle cx="70" cy="92" r="6" fill="${secondaryBg}"/>
      </svg>
    `;
  }

  // Standart planshet / tabletka blisteri
  return `
    <svg class="pack-art" viewBox="0 0 100 120" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="12" y="20" width="76" height="88" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
      <path d="M12 28C12 23.6 15.6 20 20 20H80C84.4 20 88 23.6 88 28V46H12V28Z" fill="${primaryBg}"/>
      <line x1="40" y1="33" x2="74" y2="33" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
      <rect x="22" y="58" width="56" height="38" rx="6" fill="#f8fafc" stroke="#e2e8f0"/>
      <circle cx="34" cy="70" r="4.5" fill="#94a3b8"/>
      <circle cx="50" cy="70" r="4.5" fill="#94a3b8"/>
      <circle cx="66" cy="70" r="4.5" fill="#94a3b8"/>
      <circle cx="34" cy="84" r="4.5" fill="#94a3b8"/>
      <circle cx="50" cy="84" r="4.5" fill="#94a3b8"/>
      <circle cx="66" cy="84" r="4.5" fill="#94a3b8"/>
    </svg>
  `;
}

function renderDrugCardHtml(p) {
  const name = p.name || '';
  const favActive = isFavorite(name);
  return `
    <div class="product-card" role="button" tabindex="0" data-q="${esc(name)}"
         onclick="lookup(this.dataset.q)" onkeydown="if(event.key==='Enter'){lookup(this.dataset.q)}">
      <button type="button" class="card-fav-btn ${favActive ? 'active' : ''}" data-title="${esc(name)}" aria-pressed="${favActive}"
              onclick="toggleFavorite(this.dataset.title, event)" title="Sevimlilar">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="${favActive ? '#ef4444' : 'none'}" stroke="${favActive ? '#ef4444' : '#94a3b8'}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
      </button>
      <div class="card-media">
        <span class="card-media-sellers">${p.pharmacies || 1} dorixona</span>
        ${renderDrugPackSvg(name, p.local)}
      </div>
      <div class="card-body">
        <div class="card-badges">
          ${originBadge(p.local)}
          <span class="badge badge-otc">${p.rx ? 'Retseptli' : 'Retsept: Erkin'}</span>
        </div>
        <div class="card-title">${esc(name)}</div>
        ${p.canon_inn ? `<div class="card-inn">XPN: ${esc(p.canon_inn)}</div>` : ''}
        <div class="card-manufacturer">Ishlab chiqaruvchi: <b>${esc(p.manufacturer || '—')}</b></div>
        <div class="card-footer">
          <div class="price-box">
            <span class="price-label">Eng past narx</span>
            <span class="price-val">${money(p.price_from_som)}</span>
          </div>
          <button class="btn-card-action" data-q="${esc(name)}"
                  onclick="event.stopPropagation();lookup(this.dataset.q)">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">
              <path d="M21 21l-4.35-4.35"/>
              <circle cx="11" cy="11" r="7"/>
            </svg>
            <span>Tahlil qilish</span>
          </button>
        </div>
      </div>
    </div>
  `;
}

async function loadCatalog(reset = false) {
  if (reset) AppState.catPage = 1;
  const q = ($('q')?.value || '').trim();
  const loc = $('cat-local')?.value || '';
  const container = $('drug-cards-container');
  const countEl = $('cat-count');
  const moreBtn = $('cat-more');

  if (!container) return;

  // Yuklash holati: skeleton shimmer (reset'da), aks holda "Yuklanmoqda…"
  if (reset) {
    container.innerHTML = skeletonHtml();
  } else if (countEl) {
    countEl.textContent = 'Yuklanmoqda…';
  }

  try {
    let url = `/api/catalog?q=${encodeURIComponent(q)}&local=${encodeURIComponent(loc)}&page=${AppState.catPage}&size=12`;
    if (currentCategory) {
      url += `&category=${encodeURIComponent(currentCategory)}`;
    }
    const res = await api(url);
    const items = res.items || [];
    const total = res.total || 0;
    const size = res.size || 12;
    const pages = Math.max(1, Math.ceil(total / size));

    // Kategoriya chiplariga haqiqiy sonlarni yozish (backend facets)
    if (res.facets && res.facets.categories) {
      document.querySelectorAll('#category-chips .category-btn').forEach(btn => {
        const key = btn.getAttribute('data-cat');
        const span = btn.querySelector('.chip-n');
        if (span) span.textContent = key ? ` (${res.facets.categories[key] || 0})` : '';
      });
    }

    if (countEl) {
      countEl.textContent = currentCategory
        ? `${total} ta — «${currentCategory}»`
        : `${total} ta mahsulot topildi`;
    }
    if (moreBtn) moreBtn.style.display = (res.page >= pages) ? 'none' : 'inline-block';

    // — Bo'sh holat: har doim chiroyli "topilmadi" paneli —
    if (total === 0 && reset) {
      container.innerHTML = emptyStateHtml(q, currentCategory);
      return;
    }

    const html = items.map(p => renderDrugCardHtml(p)).join('');

    if (reset) {
      container.innerHTML = html;
      // Mobilda Bosh sahifadagi 4 ta dori prevyusi
      const mobHomeContainer = $('mob-home-drugs');
      if (mobHomeContainer) {
        const previewItems = items.slice(0, 4);
        mobHomeContainer.innerHTML = previewItems.map(p => renderDrugCardHtml(p)).join('');
      }
    } else {
      container.insertAdjacentHTML('beforeend', html);
    }
    AppState.catPage++;
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-art">⚠️</div>
        <h3 class="empty-title">Katalogni yuklab bo'lmadi</h3>
        <p class="empty-sub">${esc(err.message)}</p>
        <button class="btn-primary btn-empty-clear" onclick="loadCatalog(true)">Qayta urinish</button>
      </div>`;
  }
}

async function lookup(q) {
  if (!q) return;
  const modal = $('detail-modal');
  const modalBody = $('detail-modal-body');
  if (!modal || !modalBody) return;

  modal.classList.remove('hidden');
  modalBody.innerHTML = `
    <div class="detail-loading">
      <div class="spinner" aria-hidden="true"></div>
      <div class="detail-loading-text">MllyMed AI «${esc(q)}» tahlil qilmoqda…</div>
    </div>`;

  try {
    const r = await api(`/api/card?q=${encodeURIComponent(q)}`);

    if (r.status === 'ok' && r.card) {
      const c = r.card;
      const apteka = r.apteka || {};
      const offers = apteka.offers || [];
      const chk = apteka.check || {};
      const grp = c.group || {};
      const localBadge = originBadge(c.local);
      const rxBadge = `<span class="badge badge-otc">${c.rx ? 'Retseptli' : 'Retseptsiz'}</span>`;
      const regBadge = c.reg ? `<span class="badge badge-otc">${esc(c.reg)}</span>` : '';

      // 80% tekshiruvi — 3735-son F09 proxy
      let priceCheck;
      if (chk.holat === 'mos') {
        priceCheck = `<div class="chk chk-ok"><b>✓ 80% tekshiruvi: mos</b><span>Mahalliy eng arzon ${money(chk.mahalliy_eng_arzon)} ≤ chegara ${money(chk.chegara_80)}${chk.farq_foiz != null ? ` · farq ${esc(chk.farq_foiz)}%` : ''}</span></div>`;
      } else if (chk.holat && chk.holat !== "tekshirib bo'lmadi") {
        priceCheck = `<div class="chk chk-warn"><b>⚠ 80% tekshiruvi: ${esc(chk.holat)}</b><span>Mahalliy ${money(chk.mahalliy_eng_arzon)} · import ${money(chk.import_eng_arzon)} · chegara ${money(chk.chegara_80)}</span></div>`;
      } else {
        priceCheck = `<div class="chk chk-na"><b>80% tekshiruvi: aniqlanmadi</b><span>${esc(chk.sabab || "dorixona katalogida ma'lumot yetarli emas")}</span></div>`;
      }

      const offersHtml = offers.length ? offers.map(o => `
        <a class="offer-row" ${o.url ? `href="${esc(o.url)}" target="_blank" rel="noopener"` : ''}>
          <span class="offer-main"><b>${esc(o.name || '—')}</b><span class="offer-meta">${esc(o.seller || 'Dorixona')} · ${o.pharmacies || 1} ta dorixona${o.local === true ? ' · 🇺🇿 mahalliy' : ''}</span></span>
          <span class="offer-price">${money(o.price_from_som)}</span>
        </a>`).join('') : `<p class="muted-note">Dorixona takliflari topilmadi — faqat reyestr ma&#8217;lumoti mavjud.</p>`;

      const groupHtml = (grp.n != null) ? `
        <div class="kpi-grid">
          <div class="kpi"><div class="kpi-v">${grp.n}</div><div class="kpi-l">XPN guruhida jami</div></div>
          <div class="kpi"><div class="kpi-v">${grp.local ?? 0}</div><div class="kpi-l">🇺🇿 Mahalliy</div></div>
          <div class="kpi"><div class="kpi-v">${grp.import ?? 0}</div><div class="kpi-l">🌍 Import</div></div>
          <div class="kpi"><div class="kpi-v">${money(grp.local_min)}</div><div class="kpi-l">Mahalliy eng arzon</div></div>
        </div>` : '';

      modalBody.innerHTML = `
        <div class="detail-head">
          <div class="detail-badges">${localBadge}${rxBadge}${regBadge}</div>
          <h2 class="detail-title">${esc(c.name || q)}</h2>
          <p class="detail-inn">XPN: <b>${esc(c.inn_display || c.inn || '—')}</b>${c.form_uz ? ` · ${esc(c.form_uz)}` : ''}${c.strength ? ` · ${esc(c.strength)}` : ''}</p>
        </div>
        <div class="detail-grid">
          <div class="detail-col">
            <div class="info-box">
              <div>🏢 <b>${esc(c.manufacturer || '—')}</b> · ${esc(c.country || '—')}</div>
              <div>🏷️ ATX <code>${esc(c.atc || '—')}</code> · Reyestr <code>${esc(c.reg || '—')}</code></div>
              <div>📦 ${esc(c.full || c.name || '')}</div>
            </div>
            ${groupHtml}
          </div>
          <div class="detail-col">
            ${priceCheck}
            <h4 class="offers-title">Dorixonalardagi narxlar <span class="offers-n">${apteka.count ?? offers.length} ta taklif</span></h4>
            <div class="offers-list">${offersHtml}</div>
            <p class="muted-note" style="margin-top:8px">${esc(apteka.note || "Narx — eng past taklif (dorixona narxi emas).")}</p>
          </div>
        </div>`;
    } else if (r.status === 'ambiguous') {
      const cands = r.candidates || [];
      modalBody.innerHTML = `
        <div class="amb-wrap">
          <div class="amb-icon">💊</div>
          <h3 class="amb-title">«${esc(q)}» — bir necha variant topiladi</h3>
          <p class="empty-sub">Quyidan aniq mahsulotni tanlang:</p>
          <div class="amb-list">
            ${cands.map(cd => `<button class="amb-item" data-q="${esc(cd.name)}" onclick="lookup(this.dataset.q)">${esc(cd.line || cd.name)}</button>`).join('')}
          </div>
        </div>`;
    } else {
      // status: 'none' (topilmadi) va boshqa kutilmagan holatlar
      modalBody.innerHTML = `
        <div class="empty-state" style="border:none;background:transparent;box-shadow:none">
          <div class="empty-art">🔍</div>
          <h3 class="empty-title">«${esc(q)}» topilmadi</h3>
          <p class="empty-sub">Davlat reyestrida va dorixona katalogida bunday nom yo'q. Boshqa nom yoki XPN (INN) bilan urinib ko'ring.</p>
          <button class="btn-primary btn-empty-clear" onclick="closeDetailModal();clearSearch()">Katalogga qaytish</button>
        </div>`;
    }
  } catch (err) {
    modalBody.innerHTML = `<div style="padding:20px;color:#ef4444">Xatolik: ${esc(err.message)}</div>`;
  }
}

function closeDetailModal() {
  const modal = $('detail-modal');
  if (modal) modal.classList.add('hidden');
}

window.setCategory = setCategory;
window.doSearchNow = doSearchNow;
window.filterLocalProducts = filterLocalProducts;
window.quickSearch = quickSearch;
window.originBadge = originBadge;
window.renderDrugPackSvg = renderDrugPackSvg;
window.loadCatalog = loadCatalog;
window.lookup = lookup;
window.closeDetailModal = closeDetailModal;

/**
 * ══════════════════════════════════════════════════════════════
 * REAL MOBILE APP: TO'LIQ DORILAR BO'LIMI VA SEVIMLILAR TIZIMI
 * ══════════════════════════════════════════════════════════════
 */
function openAllDrugsView() {
  const view = $('all-drugs-view');
  if (view) {
    view.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    updateFavBadge();
    loadDrugsView(true);
  }
}

function closeAllDrugsView() {
  const view = $('all-drugs-view');
  if (view) {
    view.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

let drugsViewTimer = null;
function onDrugsViewSearchInput() {
  const inp = $('drugs-view-search');
  const clearBtn = $('drugs-view-clear');
  if (clearBtn) {
    if (inp && inp.value.trim().length > 0) clearBtn.classList.remove('hidden');
    else clearBtn.classList.add('hidden');
  }
  clearTimeout(drugsViewTimer);
  drugsViewTimer = setTimeout(() => {
    loadDrugsView(true);
  }, 260);
}

function clearDrugsViewSearch() {
  const inp = $('drugs-view-search');
  const clearBtn = $('drugs-view-clear');
  if (inp) {
    inp.value = '';
    inp.focus();
  }
  if (clearBtn) clearBtn.classList.add('hidden');
  loadDrugsView(true);
}

function setCategoryMob(cat, el) {
  drugsViewCategory = cat;
  document.querySelectorAll('.cat-pill-mob').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
  loadDrugsView(true);
}

function toggleFavoritesFilter() {
  isFavoritesFilterActive = !isFavoritesFilterActive;
  const btn = $('btn-drugs-fav');
  if (btn) btn.classList.toggle('active', isFavoritesFilterActive);
  loadDrugsView(true);
}

async function loadDrugsView(reset = false) {
  if (reset) drugsViewPage = 1;
  const grid = $('drugs-view-grid');
  const countEl = $('drugs-view-count');
  const moreBtn = $('drugs-view-more');
  if (!grid) return;

  const q = ($('drugs-view-search')?.value || '').trim();
  const loc = drugsViewCategory === 'local' ? 'local' : '';
  const cat = drugsViewCategory === 'local' ? '' : drugsViewCategory;

  try {
    let url = `/api/catalog?q=${encodeURIComponent(q)}&local=${loc}&page=${drugsViewPage}&size=12`;
    if (cat) url += `&category=${encodeURIComponent(cat)}`;
    const res = await api(url);

    let items = res.items || [];
    if (isFavoritesFilterActive) {
      items = items.filter(p => favoritesList.includes(p.name));
      if (countEl) countEl.textContent = `Sevimlilar: ${items.length} ta dori`;
      if (moreBtn) moreBtn.style.display = 'none';

      if (items.length === 0) {
        grid.innerHTML = `
          <div style="grid-column:1/-1;text-align:center;padding:50px 20px;background:#ffffff;border-radius:20px;border:1px solid #e2e8f0;margin:10px 0">
            <div style="font-size:44px;margin-bottom:10px">❤️</div>
            <h4 style="font-size:16px;font-weight:800;color:#0f172a;margin-bottom:6px">Sevimlilar ro'yxati bo'sh</h4>
            <p style="font-size:13px;color:#64748b;max-width:280px;margin:0 auto">Istalgan dori kartochkasidagi yurakcha belgisini bosib, uni sevimlilarga qo'shishingiz mumkin.</p>
          </div>
        `;
        return;
      }
    } else {
      if (countEl) countEl.textContent = `${res.total} ta dori vositasi mavjud`;
      const pages = Math.max(1, Math.ceil((res.total || 0) / (res.size || 12)));
      if (moreBtn) moreBtn.style.display = (res.page >= pages) ? 'none' : 'inline-block';
    }

    const html = items.map(p => renderDrugCardHtml(p)).join('');
    if (reset) grid.innerHTML = html;
    else grid.insertAdjacentHTML('beforeend', html);
    drugsViewPage++;
  } catch (err) {
    grid.innerHTML = `<p style="grid-column:1/-1;color:#ef4444;padding:20px">Xatolik: ${esc(err.message)}</p>`;
  }
}

function loadMoreDrugsView() {
  loadDrugsView(false);
}

window.openAllDrugsView = openAllDrugsView;
window.closeAllDrugsView = closeAllDrugsView;
window.onDrugsViewSearchInput = onDrugsViewSearchInput;
window.clearDrugsViewSearch = clearDrugsViewSearch;
window.setCategoryMob = setCategoryMob;
window.toggleFavoritesFilter = toggleFavoritesFilter;
window.loadMoreDrugsView = loadMoreDrugsView;
window.toggleFavorite = toggleFavorite;
window.isFavorite = isFavorite;
