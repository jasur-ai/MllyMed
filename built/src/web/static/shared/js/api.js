/**
 * MllyMed Frontend — Markazlashgan API Klienti
 * B2C va B2B API marshrutlarini dinamik qo'llab-quvvatlaydi
 */

const $ = id => document.getElementById(id);

const AppState = {
  sid: 'bemor_' + Math.random().toString(36).slice(2, 8),
  role: 'patient',
  activeMode: 'b2c',
  catPage: 1,
  activeB2BTab: 'doctor'
};

// Matndagi BARCHA piktogramma/emoji/bayroq/z-var markerlarini olib tashlaydi.
// (Backend "trust card" javoblarida emoji bo'lishi mumkin — saytda ko'rsatilmaydi.)
const EMOJI_RX = /[\u{1F000}-\u{1FAFF}\u{1F1E6}-\u{1F1FF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{2300}-\u{23FF}\u{2500}-\u{257F}\u{FE00}-\u{FE0F}\u{200D}\u{20E3}]/gu;
function stripEmoji(str) {
  return String(str == null ? '' : str)
    .replace(EMOJI_RX, '')
    .split('\n')
    .map(line => line.replace(/\s{2,}/g, ' ').trim())
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function esc(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function money(som) {
  if (som === null || som === undefined || som === '') return '—';
  const n = Math.round(Number(som));
  if (isNaN(n)) return String(som);
  return n.toLocaleString('uz-UZ') + " so'm";
}

async function api(path, body = null, role = null) {
  const currentRole = role || AppState.role;
  const headers = {
    'X-Role': currentRole,
    'X-User': AppState.sid
  };
  
  const opts = { headers };
  if (body) {
    opts.method = 'POST';
    headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  } else {
    opts.method = 'GET';
  }

  const res = await fetch(path, opts);
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || 'Server xatosi (' + res.status + ')');
  }
  return data;
}

window.$ = $;
window.AppState = AppState;
window.esc = esc;
window.money = money;
window.api = api;
window.stripEmoji = stripEmoji;
