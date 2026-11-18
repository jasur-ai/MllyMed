/**
 * MllyMed B2B — Mahalliy Ishlab Chiqaruvchi Zavod & Regulyator Tahlil Portali
 * Bozor qamrovi, 80% narx pariteti va audit jurnali
 */

function switchB2BTab(t) {
  AppState.activeB2BTab = t;
  ['doctor', 'pharmacist', 'factory'].forEach(tab => {
    const tabBtn = $('tab-b2b-' + (tab === 'doctor' ? 'dr' : tab === 'pharmacist' ? 'ph' : 'mfg'));
    const tabBox = $('b2b-' + tab + '-box');
    if (tabBtn) tabBtn.classList.toggle('active', tab === t);
    if (tabBox) tabBox.classList.toggle('hidden', tab !== t);
  });

  if (t === 'pharmacist' && typeof loadB2BPharmacist === 'function') loadB2BPharmacist();
  if (t === 'factory') loadB2BFactory();
}

async function loadB2BFactory() {
  const metricsEl = $('factory-metrics');
  const auditEl = $('factory-audit');

  try {
    const an = await api('/api/analytics', null, 'admin');
    if (metricsEl) {
      metricsEl.innerHTML = `
        <div style="background:#f8fafc;padding:16px 20px;border-radius:var(--radius-md);border:1px solid var(--border-light)">
          <div style="font-size:12px;color:var(--text-muted);font-weight:600">JAMI XPN TURLARI</div>
          <div style="font-size:26px;font-weight:800;color:var(--primary);margin-top:4px">${an.coverage?.total_inn || 2941}</div>
        </div>
        <div style="background:#f8fafc;padding:16px 20px;border-radius:var(--radius-md);border:1px solid var(--border-light)">
          <div style="font-size:12px;color:var(--text-muted);font-weight:600">MAHALLIY EKVIVALENTLI XPN</div>
          <div style="font-size:26px;font-weight:800;color:#059669;margin-top:4px">${an.coverage?.local_inn_count || 158}</div>
        </div>
        <div style="background:#f8fafc;padding:16px 20px;border-radius:var(--radius-md);border:1px solid var(--border-light)">
          <div style="font-size:12px;color:var(--text-muted);font-weight:600">80% QOIDASIGA MOSLIK</div>
          <div style="font-size:26px;font-weight:800;color:#0284c7;margin-top:4px">${an.parity?.percent_compliant || 78}%</div>
        </div>
      `;
    }

    const au = await api('/api/audit', null, 'admin');
    if (auditEl) {
      let rows = '';
      (au.items || []).slice(0, 10).forEach(l => {
        rows += `
          <div style="padding:10px 0;border-bottom:1px solid var(--border-light);font-size:12.5px;display:flex;justify-content:space-between">
            <div><b>[${esc(l.action)}]</b> ${esc(l.details || '')}</div>
            <span style="color:var(--text-muted)">${esc(l.ts || '')}</span>
          </div>
        `;
      });
      auditEl.innerHTML = rows || `<div style="color:var(--text-muted)">Audit yozuvlari mavjud emas.</div>`;
    }
  } catch (e) {
    if (metricsEl) metricsEl.innerHTML = `<span style="color:#ef4444">Xato: ${esc(e.message)}</span>`;
  }
}

window.switchB2BTab = switchB2BTab;
window.loadB2BFactory = loadB2BFactory;
