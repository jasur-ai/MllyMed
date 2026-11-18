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
