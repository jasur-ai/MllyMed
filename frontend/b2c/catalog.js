/**
 * MllyMed B2C — Dori Katalogi & 80% Mahalliy Ekvivalent Tahlili
 */

let currentCategory = '';

function setCategory(cat, el) {
  currentCategory = cat;
  document.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
  if (el) el.classList.add('active');
  loadCatalog(true);
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
  if (inp) {
    inp.value = '';
    const clearBtn = $('search-clear-btn');
    if (clearBtn) clearBtn.classList.add('hidden');
    inp.focus();
    loadCatalog(true);
  }
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

async function loadCatalog(reset = false) {
  if (reset) AppState.catPage = 1;
  const q = ($('q')?.value || '').trim();
  const loc = $('cat-local')?.value || '';
  const container = $('drug-cards-container');
  const countEl = $('cat-count');
  const moreBtn = $('cat-more');

  if (!container) return;

  try {
    let url = `/api/catalog?q=${encodeURIComponent(q)}&local=${loc}&page=${AppState.catPage}&size=12`;
    if (currentCategory) {
      url += `&category=${encodeURIComponent(currentCategory)}`;
    }
    const res = await api(url);
    if (countEl) countEl.textContent = `${res.total} ta mahsulot topildi`;
    if (moreBtn) moreBtn.style.display = (res.page >= res.pages) ? 'none' : 'inline-block';

    let html = '';
    res.items.forEach(p => {
      html += `
        <div class="product-card" onclick="lookup('${esc(p.title)}')">
          <div class="card-media">
            <span class="card-media-sellers">${p.sellers_count || 1} dorixona</span>
            ${renderDrugPackSvg(p.title, p.local)}
          </div>
          <div class="card-body">
            <div class="card-badges">
              ${originBadge(p.local)}
              <span class="badge badge-otc">Retsept: Erkin</span>
            </div>
            <div class="card-title">${esc(p.title)}</div>
            ${p.canon_inn ? `<div class="card-inn">XPN: ${esc(p.canon_inn)}</div>` : ''}
            <div class="card-manufacturer">Ishlab chiqaruvchi: <b>${esc(p.manufacturer || 'O\'zbekiston')}</b></div>
            <div class="card-footer">
              <div class="price-box">
                <span class="price-label">Eng past narx</span>
                <span class="price-val">${money(p.price_from_som)}</span>
              </div>
              <button class="btn-card-action" onclick="event.stopPropagation();lookup('${esc(p.title)}')">
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
    });

    if (reset) container.innerHTML = html;
    else container.insertAdjacentHTML('beforeend', html);
    AppState.catPage++;
  } catch (err) {
    container.innerHTML = `<p style="color:#ef4444;padding:20px">Xatolik: ${esc(err.message)}</p>`;
  }
}

async function lookup(q) {
  if (!q) return;
  const modal = $('detail-modal');
  const modalBody = $('detail-modal-body');
  if (!modal || !modalBody) return;

  modal.classList.remove('hidden');
  modalBody.innerHTML = `<div style="text-align:center;padding:40px;color:var(--text-secondary)">Dori tahlil qilinmoqda...</div>`;

  try {
    const r = await api(`/api/card?q=${encodeURIComponent(q)}`);
    if (r.status === 'card') {
      const c = r.card || {};
      const pchk = r.price_check || {};
      const locals = r.local_alternatives || [];
      const offers = r.offers || [];

      modalBody.innerHTML = `
        <div class="detail-header-row" style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:20px;border-bottom:1px solid #e2e8f0;padding-bottom:16px">
          <div>
            <div style="display:flex;gap:6px;margin-bottom:8px">
              ${originBadge(c.local)}
              <span class="badge badge-otc">Davlat reestr: ${esc(c.number || 'Mavjud')}</span>
            </div>
            <h2 style="font-size:20px;font-weight:800;color:var(--text-primary)">${esc(c.name || q)}</h2>
            <p style="font-size:13.5px;color:var(--primary);margin-top:2px">XPN: <b>${esc(c.inn || '—')}</b> · Shakli: ${esc(c.form || '—')}</p>
          </div>
          <div style="text-align:right">
            <span style="font-size:11px;color:var(--text-muted);text-transform:uppercase;font-weight:600">Referent Narx</span>
            <div style="font-size:22px;font-weight:800;color:var(--primary)">${money(c.price_ref_som)}</div>
            <span style="font-size:11.5px;color:var(--text-muted)">Chegara narx: ${money(c.price_limit_som)}</span>
          </div>
        </div>

        <div class="detail-grid-layout" style="display:grid;grid-template-columns:1.2fr 1fr;gap:20px">
          <div>
            <div style="background:#f8fafc;padding:14px;border-radius:12px;border:1px solid #e2e8f0;font-size:13px;line-height:1.7;margin-bottom:16px">
              <div>🏢 Ishlab chiqaruvchi: <b>${esc(c.producer || '—')}</b> (${esc(c.country || '—')})</div>
              <div>🏷️ ATX kodi: <code>${esc(c.atc || '—')}</code></div>
              <div>⏳ Yaroqlilik: ${esc(c.expire || '—')}</div>
            </div>

            <h4 style="font-size:14px;font-weight:700;margin-bottom:10px">Tavsiya etilgan mahalliy analoglar:</h4>
            ${!locals.length ? '<p style="font-size:12.5px;color:var(--text-muted)">Mahalliy analoglar topilmadi.</p>' : locals.map(l => `
              <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f1f5f9;font-size:13px">
                <div><b>${esc(l.title)}</b><br><span style="font-size:11.5px;color:var(--text-muted)">${esc(l.manufacturer || 'Mahalliy')}</span></div>
                <div style="font-weight:700;color:var(--primary)">${money(l.price_from_som)}</div>
              </div>
            `).join('')}
          </div>

          <div>
            <div style="background:#ecfdf5;padding:14px;border-radius:12px;border:1px solid #a7f3d0;margin-bottom:16px">
              <span class="badge badge-local">${esc(pchk.holat || 'Tekshirildi')}</span>
              <p style="font-size:12.5px;margin-top:6px;color:#065f46">${esc(pchk.izoh || '80% mahalliy ekvivalent narx talablari asosida tekshirildi.')}</p>
            </div>

            <h4 style="font-size:14px;font-weight:700;margin-bottom:10px">Dorixonalardagi narxlar:</h4>
            ${!offers.length ? '<p style="font-size:12.5px;color:var(--text-muted)">Dorixona takliflari topilmadi.</p>' : offers.map(o => `
              <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #f1f5f9;font-size:13px">
                <div><b>${esc(o.title)}</b><br><span style="font-size:11px;color:var(--text-muted)">${o.sellers_count || 1} ta dorixona</span></div>
                <div style="font-weight:700;color:var(--text-primary)">${money(o.price_from_som)}</div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    } else if (r.status === 'emergency') {
      modalBody.innerHTML = `
        <div style="background:#fef2f2;border:2px solid #fecaca;padding:22px;border-radius:16px">
          <h3 style="color:#b91c1c;font-size:17px;margin-bottom:8px">🚨 DIQQAT: FAVQULODDA HOLAT (103)</h3>
          <p style="color:#7f1d1d;font-size:14px;line-height:1.6">${esc(r.reply)}</p>
          <div style="margin-top:16px"><a href="tel:103" class="btn-primary" style="background:#dc2626">Darhol 103 ga qo'ng'iroq qilish</a></div>
        </div>
      `;
    } else {
      modalBody.innerHTML = `<div style="padding:20px;text-align:center;color:var(--text-secondary)">${esc(r.reply || 'Bu so\'rov bo\'yicha dori topilmadi.')}</div>`;
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
window.quickSearch = quickSearch;
window.originBadge = originBadge;
window.renderDrugPackSvg = renderDrugPackSvg;
window.loadCatalog = loadCatalog;
window.lookup = lookup;
window.closeDetailModal = closeDetailModal;
