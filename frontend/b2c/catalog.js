/**
 * MllyMed B2C — Dori Katalogi & 80% Mahalliy Ekvivalent Tahlili
 */

let currentCategory = '';
// Haqiqiy mahsulot fotolari manifesti (frontend/assets/img/manifest.json) —
// bo'lmasa generativ "pack shot" ko'rsatiladi (oflayn-tez, har doim yaxlit).
window.PACK_IMG = window.PACK_IMG || {};

function getDrugPhotoUrl(p) {
  if (!p) return null;
  if (p.photo_url) return p.photo_url;
  if (!window.PACK_IMG) return null;
  const pid = p.id != null ? String(p.id).replace(/[^a-zA-Z0-9_-]/g, '') : '';
  if (pid && window.PACK_IMG[pid]) return window.PACK_IMG[pid];
  if (p.image_id && window.PACK_IMG[p.image_id]) return window.PACK_IMG[p.image_id];
  const name = (p.name || '').trim();
  if (name && window.PACK_IMG[name]) return window.PACK_IMG[name];
  const nLow = name.toLowerCase();
  if (nLow && window.PACK_IMG[nLow]) return window.PACK_IMG[nLow];
  if (p.canon_inn && window.PACK_IMG[p.canon_inn]) return window.PACK_IMG[p.canon_inn];
  if (p.inn && window.PACK_IMG[p.inn]) return window.PACK_IMG[p.inn];
  // Taniqli brend va mahsulot kalit so'zlari
  const brands = [
    'nurofen', 'нурофен', 'arbidol', 'арбидол', 'kanefron', 'канефрон',
    'orlip', 'орлип', 'enterojermina', 'энтерожермина', 'aprid', 'априд',
    'adaptol', 'адаптол', 'inflyuvak', 'инфлювак', 'korteksin', 'кортексин',
    'semavik', 'семавик', 'tirzetta', 'тирзетта', 'sorbifer', 'сорбифер',
    'sedjaro', 'седжаро', 'fenistil', 'фенистил', 'dufaston', 'дюфастон', 'dyufaston'
  ];
  for (const b of brands) {
    if (nLow.includes(b) && window.PACK_IMG[b]) {
      return window.PACK_IMG[b];
    }
  }
  return null;
}

function refreshRenderedPhotos() {
  try {
    document.querySelectorAll('.product-card').forEach(card => {
      const q = card.getAttribute('data-q') || '';
      const mediaEl = card.querySelector('.card-media');
      if (!mediaEl || mediaEl.querySelector('.pack-photo')) return;
      const photoUrl = getDrugPhotoUrl({ name: q });
      if (photoUrl) {
        const svgEl = mediaEl.querySelector('svg.pack-art');
        if (svgEl) {
          const img = document.createElement('img');
          img.className = 'pack-photo';
          img.src = photoUrl;
          img.alt = q;
          img.loading = 'lazy';
          img.dataset.name = q;
          img.onerror = function () { window.__packFallback(this); };
          svgEl.replaceWith(img);
        }
      }
    });
  } catch (e) {}
}

try {
  fetch('assets/img/manifest.json')
    .then(r => (r.ok ? r.json() : {}))
    .then(m => {
      window.PACK_IMG = (m && typeof m === 'object') ? m : {};
      refreshRenderedPhotos();
    })
    .catch(() => {});
} catch (e) { /* e'tiborsiz */ }

let favoritesList = JSON.parse(localStorage.getItem('mllymed_favs') || '[]');
let isFavoritesFilterActive = false;
let drugsViewPage = 1;
let drugsViewCategory = '';

// Haqiqiy foto yuklanmay qolsa — generativ SVG pack shot bilan almashtirish
window.__packFallback = function (img) {
  try {
    const name = img.getAttribute('data-name') || '';
    const local = img.getAttribute('data-local') === '1' ? true : (img.getAttribute('data-local') === '0' ? false : undefined);
    const div = document.createElement('div');
    div.innerHTML = renderDrugPackSvg(name, local);
    const svg = div.firstElementChild;
    if (svg && img.parentNode) img.parentNode.replaceChild(svg, img);
  } catch (e) {
    img.style.visibility = 'hidden';
  }
};

// Sevimlilarga qo'shganda — rangli zarralar portlashi
function favBurst(x, y, adding) {
  const colors = adding ? ['#ef4444', '#f97316', '#f43f5e', '#fbbf24', '#fb7185'] : ['#94a3b8', '#cbd5e1'];
  for (let i = 0; i < 12; i++) {
    const el = document.createElement('span');
    el.className = 'fx-particle';
    const ang = (Math.PI * 2 * i) / 12 + Math.random() * 0.5;
    const dist = 20 + Math.random() * 36;
    el.style.setProperty('--tx', Math.cos(ang) * dist + 'px');
    el.style.setProperty('--ty', Math.sin(ang) * dist + 'px');
    el.style.background = colors[i % colors.length];
    el.style.left = x + 'px';
    el.style.top = y + 'px';
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 720);
  }
}

function isFavorite(title) {
  return favoritesList.includes(title);
}

function toggleFavorite(title, event) {
  if (event) event.stopPropagation();
  const adding = !favoritesList.includes(title);
  if (adding) {
    favoritesList.push(title);
  } else {
    favoritesList = favoritesList.filter(t => t !== title);
  }
  if (event && typeof event.clientX === 'number' && event.clientX) {
    favBurst(event.clientX, event.clientY, adding);
  }
  if (typeof showToast === 'function') {
    showToast(adding ? "Sevimlilarga qo'shildi" : "Sevimlilardan olib tashlandi", adding ? 'heart' : 'check');
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
      <div class="empty-art">${icon('search', 44, 1.5)}</div>
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
    return `<span class="badge badge-local">${icon('flag', 12, 2.4)} Mahalliy (GMP)</span>`;
  }
  if (isLocal === false) {
    return `<span class="badge badge-import">${icon('globe', 12, 2.2)} Import</span>`;
  }
  return `<span class="badge" style="background:#f1f5f9;color:#64748b">Aniqmas</span>`;
}

/* ═══════════════════════════════════════════════════════════════════
   GENERATIV «PACK SHOT» — har bir dori uchun deterministik, brand-
   konsistent mahsulot ko'rinishi. Arzon Apteka'dagi kabi, lekin har
   bitta mahsulot o'ziga xos (nomdan hash → shakl + palitra).
   Rasmlar tashqi serverdan olinmaydi — Mini App oflayn ham tez.
   Haqiqiy foto kerak bo'lsa: frontend/assets/img/<id>.(png|jpg|webp)
   ══════════════════════════════════════════════════════════════════ */

const PACK_PALETTES = [
  ['#2563eb', '#1e3a8a'], ['#059669', '#064e3b'], ['#7c3aed', '#4c1d95'],
  ['#db2777', '#831843'], ['#ea580c', '#7c2d12'], ['#0891b2', '#164e63'],
  ['#4f46e5', '#312e81'], ['#0f766e', '#134e4a'], ['#b45309', '#451a03'],
  ['#be123d', '#4c0519'], ['#334155', '#0f172a'], ['#0369a1', '#0c2a3f'],
];

function hashStr(str) {
  let h = 1779033703 ^ str.length;
  for (let i = 0; i < str.length; i++) {
    h = Math.imul(h ^ str.charCodeAt(i), 3432918353);
    h = (h << 13) | (h >>> 19);
  }
  h = Math.imul(h ^ (h >>> 16), 2246822507);
  h = Math.imul(h ^ (h >>> 13), 3266489909);
  return (h ^= h >>> 16) >>> 0;
}

let packUid = 0;

function monogramOf(name) {
  const words = String(name || '').toUpperCase().match(/[A-ZА-ЯЁ0-9]+/g) || [];
  if (!words.length) return 'M';
  const w = words[0];
  return (w[0] + (words[1] ? words[1][0] : (w[1] || ''))).slice(0, 2);
}

function detectPackForm(t) {
  // HAQIQIY katalog (308 mahsulot) bo'yicha sozlangan aniqlash tartibi
  if (/(inyeks|ukol|ampul|ampola|\binj)/i.test(t)) return 'ampoule';
  if (/(infuz|flakon|vial)/i.test(t)) return 'vial';
  if (/tomchi/i.test(t)) return 'dropper';
  if (/(sirop|suspen|mikstur|eritma)/i.test(t)) return 'syrup';   // og'iz orqali eritma (inyeksiya/infuziya yuqorida tutildi)
  if (/(krem|maz|gel|malham|suratma|surtma)/i.test(t)) return 'tube';
  if (/(kaps|caps)/i.test(t)) return 'capsule';
  if (/(granul|porosh|paket|sachet)/i.test(t)) return 'sachet';
  if (/(inhal|aerozol|sprey|spriy|spray)/i.test(t)) return 'inhaler';
  return 'blister';
}

function renderDrugPackSvg(name, isLocal) {
  const raw = String(name || 'DORI');
  const t = raw.toLowerCase();
  const h = hashStr(raw);
  const [c1, c2] = PACK_PALETTES[h % PACK_PALETTES.length];
  const uid = 'pk' + (packUid++).toString(36) + h.toString(36);
  const mono = esc(monogramOf(raw));
  const seed2 = (h >>> 8) % 97;

  // Mahalliy: yashil GMP chizig'i · Import: kumush-ko'k holografiya (mahsulot kengligida)
  const originBar = (x, w) => {
    if (isLocal !== true && isLocal !== false) return '';
    const fill = isLocal === true ? `url(#${uid}-g)` : `url(#${uid}-h)`;
    return `<rect x="${x}" y="111" width="${w}" height="7" rx="3.5" fill="${fill}"/><rect x="${x + 2}" y="111.6" width="${w - 4}" height="1.2" rx="0.6" fill="#ffffff" opacity="0.55"/>`;
  };

  const defs = `
    <linearGradient id="${uid}-g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#10d68a"/><stop offset="1" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="${uid}-h" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#e2e8f0"/><stop offset="0.45" stop-color="#b8c4d8"/>
      <stop offset="0.55" stop-color="#eef2f8"/><stop offset="1" stop-color="#94a9c4"/>
    </linearGradient>
    <linearGradient id="${uid}-p" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${c1}"/><stop offset="1" stop-color="${c2}"/>
    </linearGradient>
    <linearGradient id="${uid}-foil" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.5" stop-color="#e8edf5"/><stop offset="1" stop-color="#c9d3e4"/>
    </linearGradient>
    <radialGradient id="${uid}-pk" cx="0.38" cy="0.34" r="0.75">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.75" stop-color="#dfe6ef"/><stop offset="1" stop-color="#b7c3d6"/>
    </radialGradient>
    <radialGradient id="${uid}-glass" cx="0.4" cy="0.35" r="0.8">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/><stop offset="0.35" stop-color="${c1}" stop-opacity="0.28"/><stop offset="1" stop-color="${c2}" stop-opacity="0.55"/>
    </radialGradient>
    <linearGradient id="${uid}-syr" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fde9a8"/><stop offset="0.42" stop-color="#f5b73e"/><stop offset="1" stop-color="#d97706"/>
    </linearGradient>
    <linearGradient id="${uid}-shine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/><stop offset="0.28" stop-color="#ffffff" stop-opacity="0.08"/><stop offset="0.6" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>`;

  const shadow = `<ellipse cx="60" cy="106" rx="33" ry="6" fill="#0f1c2e" opacity="0.16"/>`;
  const monoBadge = (x, y, r, fs) => `
    <circle cx="${x}" cy="${y}" r="${r}" fill="#ffffff" opacity="0.92"/>
    <circle cx="${x}" cy="${y}" r="${r}" fill="none" stroke="#ffffff" stroke-opacity="0.6"/>
    <text x="${x}" y="${y + fs * 0.36}" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif"
          font-size="${fs}" font-weight="800" fill="${c2}" letter-spacing="0.5">${mono}</text>`;
  const lines = (x, y, w, tint) => `
    <rect x="${x}" y="${y}" width="${w}" height="3.4" rx="1.7" fill="${tint || '#0f1c2e'}" opacity="0.35"/>
    <rect x="${x}" y="${y + 6.4}" width="${Math.round(w * 0.62)}" height="2.6" rx="1.3" fill="${tint || '#0f1c2e'}" opacity="0.2"/>`;

  const form = detectPackForm(t);
  let art = '';

  if (form === 'blister' || form === 'capsule') {
    // Blister kartochkasi — kumush folga + tabletkalar
    const rows = 3, cols = 4;
    let pills = '';
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const cx = 32 + c * 18.5, cy = 62 + r * 14.5;
        pills += form === 'capsule'
          ? `<g transform="translate(${cx - 7},${cy - 4.4}) rotate(-32)">
               <rect width="15" height="8.8" rx="4.4" fill="${c1}"/>
               <rect width="7.5" height="8.8" rx="4.4" fill="#ffffff" opacity="0.92"/>
               <rect width="15" height="8.8" rx="4.4" fill="none" stroke="#0f1c2e" stroke-opacity="0.15" stroke-width="0.8"/>
             </g>`
          : `<circle cx="${cx}" cy="${cy}" r="6.1" fill="url(#${uid}-pk)" stroke="#9aa7ba" stroke-opacity="0.5" stroke-width="0.7"/>
             <circle cx="${cx - 1.6}" cy="${cy - 1.6}" r="1.9" fill="#ffffff" opacity="0.85"/>`;
      }
    }
    art = `
      <rect x="13" y="14" width="94" height="92" rx="11" fill="url(#${uid}-foil)" stroke="#a7b3c6" stroke-width="1.1"/>
      <path d="M13 25a11 11 0 0 1 11-11h72a11 11 0 0 1 11 11v15H13Z" fill="url(#${uid}-p)"/>
      <path d="M13 25a11 11 0 0 1 11-11h72a11 11 0 0 1 11 11v15H13Z" fill="url(#${uid}-shine)"/>
      ${monoBadge(26.5, 25, 8.6, 9.5)}
      <rect x="40" y="17.5" width="46" height="3.1" rx="1.55" fill="#ffffff" opacity="0.75"/>
      <rect x="40" y="24" width="30" height="2.4" rx="1.2" fill="#ffffff" opacity="0.5"/>
      <line x1="16" y1="46" x2="104" y2="46" stroke="#8b99ad" stroke-width="0.9" stroke-dasharray="3 3" opacity="0.7"/>
      ${pills}
      ${originBar(13, 94)}`;
  } else if (form === 'ampoule' || form === 'vial') {
    const small = form === 'vial';
    art = `
      <rect x="14" y="46" width="92" height="58" rx="9" fill="#ffffff" stroke="#b9c4d4" stroke-width="1.1"/>
      <path d="M14 55a9 9 0 0 1 9-9h74a9 9 0 0 1 9 9v13H14Z" fill="url(#${uid}-p)"/>
      <path d="M14 55a9 9 0 0 1 9-9h74a9 9 0 0 1 9 9v13H14Z" fill="url(#${uid}-shine)"/>
      ${monoBadge(28, 60, 9, 10)}
      <rect x="43" y="53" width="42" height="3" rx="1.5" fill="#ffffff" opacity="0.75"/>
      <rect x="43" y="59.5" width="26" height="2.2" rx="1.1" fill="#ffffff" opacity="0.5"/>
      <g transform="translate(38,26)">
        <path d="M9 0h7v9l3.4 4.6v36a4.4 4.4 0 0 1-4.4 4.4h-5a4.4 4.4 0 0 1-4.4-4.4v-36L9 9Z" fill="url(#${uid}-glass)" stroke="#8fa3bb" stroke-opacity="0.7" stroke-width="0.9"/>
        <rect x="4.6" y="26" width="16" height="${small ? 9 : 13}" fill="${c1}" opacity="0.75"/>
        <line x1="4" y1="22" x2="22" y2="22" stroke="#ffffff" stroke-opacity="0.85" stroke-width="1"/>
      </g>
      <g transform="translate(66,32) scale(0.86)">
        <path d="M9 0h7v9l3.4 4.6v36a4.4 4.4 0 0 1-4.4 4.4h-5a4.4 4.4 0 0 1-4.4-4.4v-36L9 9Z" fill="url(#${uid}-glass)" stroke="#8fa3bb" stroke-opacity="0.7" stroke-width="0.9"/>
        <rect x="4.6" y="26" width="16" height="${small ? 8 : 12}" fill="${c2}" opacity="0.75"/>
      </g>
      ${originBar(14, 92)}`;
  } else if (form === 'syrup') {
    art = `
      <rect x="42" y="8" width="36" height="13" rx="4.5" fill="#22314a"/>
      <rect x="40" y="19" width="40" height="5" rx="2.4" fill="#475569"/>
      <rect x="27" y="24" width="66" height="82" rx="15" fill="url(#${uid}-syr)" stroke="#b45309" stroke-width="1.3"/>
      <rect x="31" y="54" width="58" height="35" rx="4.5" fill="#ffffff" stroke="#e2e8f0"/>
      <path d="M31 58.5a4.5 4.5 0 0 1 4.5-4.5h49a4.5 4.5 0 0 1 4.5 4.5v7H31Z" fill="url(#${uid}-p)"/>
      <text x="60" y="64.6" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="8.2" font-weight="800" fill="#ffffff" letter-spacing="0.6">${mono}</text>
      <line x1="37" y1="76" x2="78" y2="76" stroke="#64748b" stroke-width="2.1" stroke-linecap="round" opacity="0.55"/>
      <line x1="37" y1="82.5" x2="66" y2="82.5" stroke="#94a3b8" stroke-width="1.7" stroke-linecap="round" opacity="0.6"/>
      <line x1="97" y1="40" x2="97" y2="88" stroke="#b45309" stroke-opacity="0.4" stroke-width="1" stroke-dasharray="2 4"/>
      <path d="M29 27a15 15 0 0 1 12-6" stroke="#ffffff" stroke-opacity="0.8" stroke-width="2.4" fill="none" stroke-linecap="round"/>
      ${originBar(27, 66)}`;
  } else if (form === 'tube') {
    art = `
      <path d="M28 10h64l-5.4 15H33.4Z" fill="#94a3b8"/>
      <line x1="36" y1="14.8" x2="84" y2="14.8" stroke="#64748b" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="2.6 3.4"/>
      <path d="M33.4 25h53.2c3.2 22 4.1 44-6.2 56H39.6c-10.3-12-9.4-34-6.2-56Z" fill="#ffffff" stroke="#b9c4d4" stroke-width="1.2"/>
      <path d="M34 27h52c2 10 2.6 19 1.6 27H32.4c-1-8-.4-17 1.6-27Z" fill="url(#${uid}-p)"/>
      <path d="M34 27h52c2 10 2.6 19 1.6 27H32.4c-1-8-.4-17 1.6-27Z" fill="url(#${uid}-shine)"/>
      <text x="60" y="45" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12.5" font-weight="800" fill="#ffffff" letter-spacing="1">${mono}</text>
      <line x1="44" y1="72" x2="76" y2="72" stroke="#64748b" stroke-width="1.8" opacity="0.5" stroke-linecap="round"/>
      <rect x="44" y="81" width="32" height="17" rx="4.2" fill="#334155"/>
      <rect x="44" y="81" width="32" height="4" fill="#ffffff" opacity="0.14"/>
      ${originBar(28, 64)}`;
  } else if (form === 'dropper') {
    art = `
      <circle cx="60" cy="13" r="8.6" fill="#22314a"/>
      <rect x="48" y="18" width="24" height="13" rx="4.5" fill="#334155"/>
      <rect x="54.5" y="29" width="11" height="7" fill="#64748b"/>
      <rect x="28" y="36" width="64" height="68" rx="17" fill="url(#${uid}-syr)" stroke="#b45309" stroke-width="1.3"/>
      <rect x="33" y="60" width="54" height="30" rx="4.5" fill="#ffffff" stroke="#e2e8f0"/>
      <path d="M33 64.5a4.5 4.5 0 0 1 4.5-4.5h45a4.5 4.5 0 0 1 4.5 4.5v6.5H33Z" fill="url(#${uid}-p)"/>
      <text x="60" y="69.8" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="7.6" font-weight="800" fill="#ffffff">${mono}</text>
      <line x1="40" y1="80" x2="80" y2="80" stroke="#64748b" stroke-width="1.8" opacity="0.5" stroke-linecap="round"/>
      ${originBar(28, 64)}`;
  } else if (form === 'sachet') {
    const rot = (seed2 % 9) - 4;
    art = `
      <g transform="translate(60,64) rotate(${-16 + rot}) translate(-24,-30)">
        <rect width="48" height="62" rx="5" fill="${c2}" opacity="0.85"/>
      </g>
      <g transform="translate(60,64) rotate(${14 - rot}) translate(-24,-30)">
        <rect width="48" height="62" rx="5" fill="${c1}" opacity="0.8"/>
      </g>
      <g transform="translate(60,64) translate(-25,-33)">
        <rect width="50" height="66" rx="5.5" fill="url(#${uid}-p)" stroke="#ffffff" stroke-opacity="0.5" stroke-width="1.2"/>
        <path d="M0 8a5.5 5.5 0 0 1 5.5-5.5h39A5.5 5.5 0 0 1 50 8v6H0Z" fill="#ffffff" opacity="0.22"/>
        <path d="M25 0v66" stroke="#0f1c2e" stroke-opacity="0.18" stroke-width="1" stroke-dasharray="3 3"/>
        <text x="25" y="38" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="10.5" font-weight="800" fill="#ffffff" letter-spacing="0.8">${mono}</text>
      </g>
      ${originBar(35, 50)}`;
  } else if (form === 'inhaler') {
    art = `
      <rect x="38" y="10" width="26" height="16" rx="7" fill="#22314a"/>
      <rect x="46" y="26" width="52" height="22" rx="6" fill="#475569"/>
      <rect x="30" y="40" width="66" height="62" rx="12" fill="#ffffff" stroke="#b9c4d4" stroke-width="1.2"/>
      <rect x="30" y="52" width="66" height="26" fill="url(#${uid}-p)"/>
      <rect x="30" y="52" width="66" height="26" fill="url(#${uid}-shine)"/>
      <text x="63" y="69.5" text-anchor="middle" font-family="-apple-system,Segoe UI,Roboto,sans-serif" font-size="12" font-weight="800" fill="#ffffff" letter-spacing="1">${mono}</text>
      <circle cx="63" cy="92" r="4.6" fill="none" stroke="#64748b" stroke-width="1.4"/>
      ${originBar(30, 66)}`;
  }

  return `
    <svg class="pack-art" viewBox="0 0 120 122" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(raw)}">
      <defs>${defs}</defs>
      ${shadow}
      <g>${art}</g>
    </svg>`;
}

function renderDrugCardHtml(p, idx) {
  const name = p.name || '';
  const favActive = isFavorite(name);
  const hue = (typeof hashStr === 'function' ? hashStr(name) : 215) % 360;
  const delay = (typeof idx === 'number' ? Math.min(idx, 12) : 0) * 45;
  const photoUrl = getDrugPhotoUrl(p);
  const localAttr = p.local === true ? '1' : (p.local === false ? '0' : '');
  const media = photoUrl
    ? `<img class="pack-photo" src="${esc(photoUrl)}" alt="${esc(name)}" loading="lazy" data-name="${esc(name)}" data-local="${localAttr}" onerror="window.__packFallback(this)">`
    : renderDrugPackSvg(name, p.local);
  return `
    <div class="product-card" role="button" tabindex="0" data-q="${esc(name)}" style="--d:${delay}ms"
         onclick="lookup(this.dataset.q)" onkeydown="if(event.key==='Enter'){lookup(this.dataset.q)}">
      <div class="card-media" style="--ph:${hue}">
        <div class="card-media-top">
          <span class="card-media-sellers">${icon('store', 12, 2.2)} ${p.pharmacies || 1} dorixona</span>
          <button type="button" class="card-fav-btn ${favActive ? 'active' : ''}" data-title="${esc(name)}" aria-pressed="${favActive}"
                  onclick="toggleFavorite(this.dataset.title, event)" title="Sevimlilar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="${favActive ? '#ef4444' : 'none'}" stroke="${favActive ? '#ef4444' : '#94a3b8'}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </button>
        </div>
        ${media}
      </div>
      <div class="card-body">
        <div class="card-badges">
          ${originBadge(p.local)}
          <span class="badge badge-otc">${p.rx ? 'Retseptli' : 'Retsept: Erkin'}</span>
        </div>
        <div class="card-title">${esc(name)}</div>
        ${p.canon_inn ? `<div class="card-inn">XPN: ${esc(p.canon_inn)}</div>` : ''}
        <div class="card-manufacturer">Ishlab chiqaruvchi: <b>${esc(p.manufacturer || '—')}</b></div>
        <div class="card-divider"></div>
        <div class="card-footer">
          <div class="price-box">
            <span class="price-label">ENG PAST NARX</span>
            <span class="price-val">${money(p.price_from_som)}</span>
          </div>
          <button type="button" class="btn-card-action" data-q="${esc(p.canon_inn || name)}"
                  onclick="event.stopPropagation();openAgentWithPrompt(this.dataset.q)" title="MllyMed AI bilan tahlil qilish">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="7"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
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

    const html = items.map((p, i) => renderDrugCardHtml(p, i)).join('');

    if (reset) {
      container.innerHTML = html;
      // Mobilda Bosh sahifadagi 4 ta dori prevyusi (haqiqiy fotosuratli mahsulotlar)
      const mobHomeContainer = $('mob-home-drugs');
      if (mobHomeContainer) {
        const photoItems = items.filter(p => getDrugPhotoUrl(p) || p.photo_url);
        const restItems = items.filter(p => !getDrugPhotoUrl(p) && !p.photo_url);
        const previewItems = [...photoItems, ...restItems].slice(0, 4);
        mobHomeContainer.innerHTML = previewItems.map((p, i) => renderDrugCardHtml(p, i)).join('');
      }
    } else {
      container.insertAdjacentHTML('beforeend', html);
    }
    AppState.catPage++;
  } catch (err) {
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-art">${icon('alert-triangle', 44, 1.5)}</div>
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
        priceCheck = `<div class="chk chk-ok"><b>${icon('check-circle', 14, 2.3)} 80% tekshiruvi: mos</b><span>Mahalliy eng arzon ${money(chk.mahalliy_eng_arzon)} ≤ chegara ${money(chk.chegara_80)}${chk.farq_foiz != null ? ` · farq ${esc(chk.farq_foiz)}%` : ''}</span></div>`;
      } else if (chk.holat && chk.holat !== "tekshirib bo'lmadi") {
        priceCheck = `<div class="chk chk-warn"><b>${icon('alert-triangle', 14, 2.3)} 80% tekshiruvi: ${esc(chk.holat)}</b><span>Mahalliy ${money(chk.mahalliy_eng_arzon)} · import ${money(chk.import_eng_arzon)} · chegara ${money(chk.chegara_80)}</span></div>`;
      } else {
        priceCheck = `<div class="chk chk-na"><b>80% tekshiruvi: aniqlanmadi</b><span>${esc(chk.sabab || "dorixona katalogida ma'lumot yetarli emas")}</span></div>`;
      }

      const offersHtml = offers.length ? offers.map(o => `
        <a class="offer-row" ${o.url ? `href="${esc(o.url)}" target="_blank" rel="noopener"` : ''}>
          <span class="offer-main"><b>${esc(o.name || '—')}</b><span class="offer-meta">${esc(o.seller || 'Dorixona')} · ${o.pharmacies || 1} ta dorixona${o.local === true ? ' · mahalliy GMP' : ''}</span></span>
          <span class="offer-price">${money(o.price_from_som)}</span>
        </a>`).join('') : `<p class="muted-note">Dorixona takliflari topilmadi — faqat reyestr ma&#8217;lumoti mavjud.</p>`;

      const groupHtml = (grp.n != null) ? `
        <div class="kpi-grid">
          <div class="kpi"><div class="kpi-v">${grp.n}</div><div class="kpi-l">XPN guruhida jami</div></div>
          <div class="kpi"><div class="kpi-v">${grp.local ?? 0}</div><div class="kpi-l">${icon('flag', 14, 2.2)} Mahalliy</div></div>
          <div class="kpi"><div class="kpi-v">${grp.import ?? 0}</div><div class="kpi-l">${icon('globe', 14, 2)} Import</div></div>
          <div class="kpi"><div class="kpi-v">${money(grp.local_min)}</div><div class="kpi-l">Mahalliy eng arzon</div></div>
        </div>` : '';

      const detailPhotoUrl = getDrugPhotoUrl({ id: c.id, name: c.name || q, inn: c.inn });
      const detailShot = detailPhotoUrl
        ? `<img class="pack-photo" src="${esc(detailPhotoUrl)}" alt="${esc(c.name || q)}" style="max-height:100px;object-fit:contain" onerror="this.outerHTML=renderDrugPackSvg('${esc(c.name || q)}', ${c.local})">`
        : renderDrugPackSvg(c.name || q, c.local);

      modalBody.innerHTML = `
        <div class="detail-head">
          <div class="detail-head-tx">
            <div class="detail-badges">${localBadge}${rxBadge}${regBadge}</div>
            <h2 class="detail-title">${esc(c.name || q)}</h2>
            <p class="detail-inn">XPN: <b>${esc(c.inn_display || c.inn || '—')}</b>${c.form_uz ? ` · ${esc(c.form_uz)}` : ''}${c.strength ? ` · ${esc(c.strength)}` : ''}</p>
          </div>
          <div class="detail-shot" aria-hidden="true">${detailShot}</div>
        </div>
        <div class="detail-grid">
          <div class="detail-col">
            <div class="info-box">
              <div class="info-row">${icon('building', 14)} <span><b>${esc(c.manufacturer || '—')}</b> · ${esc(c.country || '—')}</span></div>
              <div class="info-row">${icon('tag', 14)} <span>ATX <code>${esc(c.atc || '—')}</code> · Reyestr <code>${esc(c.reg || '—')}</code></span></div>
              <div class="info-row">${icon('package', 14)} <span>${esc(c.full || c.name || '')}</span></div>
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
          <div class="amb-icon">${icon('pill', 40, 1.6)}</div>
          <h3 class="amb-title">«${esc(q)}» — bir necha variant topiladi</h3>
          <p class="empty-sub">Quyidan aniq mahsulotni tanlang:</p>
          <div class="amb-list">
            ${cands.map(cd => `<button class="amb-item" data-q="${esc(cd.name)}" onclick="lookup(this.dataset.q)">${esc((typeof stripEmoji === 'function') ? stripEmoji(cd.line || cd.name) : (cd.line || cd.name))}</button>`).join('')}
          </div>
        </div>`;
    } else {
      // status: 'none' (topilmadi) va boshqa kutilmagan holatlar
      modalBody.innerHTML = `
        <div class="empty-state" style="border:none;background:transparent;box-shadow:none">
          <div class="empty-art">${icon('search', 44, 1.5)}</div>
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
    document.body.classList.add('drugs-page-active');
    document.body.style.overflow = 'hidden';
    updateFavBadge();
    loadDrugsView(true);
  }
}

function closeAllDrugsView() {
  const view = $('all-drugs-view');
  if (view) {
    view.classList.add('hidden');
    document.body.classList.remove('drugs-page-active');
    document.body.style.overflow = '';
  }
  const homeBtn = $('tab-mob-home');
  if (homeBtn) {
    document.querySelectorAll('.dock-item').forEach(b => b.classList.remove('active'));
    homeBtn.classList.add('active');
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
            <div class="fav-empty-ic">${icon('heart', 44, 1.5)}</div>
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

    const html = items.map((p, i) => renderDrugCardHtml(p, i)).join('');
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
