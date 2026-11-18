/**
 * MllyMed Web API Client
 * Bemor, Shifokor, Farmatsevt va Admin rollari uchun markazlashgan API interfeysi
 */

const $ = id => document.getElementById(id);

const AppState = {
  sid: 'bemor_' + Math.random().toString(36).slice(2, 8),
  role: 'patient',
  catPage: 1,
  activeMode: 'b2c',
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
