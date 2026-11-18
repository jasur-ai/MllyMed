/**
 * MllyMed B2B Moduli — Shifokor, Dorixona va Zavod Portali
 */

function switchB2BTab(t) {
  AppState.activeB2BTab = t;
  ['doctor', 'pharmacist', 'factory'].forEach(tab => {
    const tabBtn = $('tab-b2b-' + (tab === 'doctor' ? 'dr' : tab === 'pharmacist' ? 'ph' : 'mfg'));
    const tabBox = $('b2b-' + tab + '-box');
    if (tabBtn) tabBtn.classList.toggle('active', tab === t);
    if (tabBox) tabBox.classList.toggle('hidden', tab !== t);
  });

  if (t === 'pharmacist') loadB2BPharmacist();
  if (t === 'factory') loadB2BFactory();
}

async function b2bDraftPrescription() {
  const statusEl = $('dr-b2b-status');
  try {
    const p = $('dr-p')?.value || 'demo';
    const inn = $('dr-inn')?.value;
    if (!inn) {
      alert('Iltimos, XPN tanlang');
      return;
    }
    const res = await api('/api/prescriptions', { patient: p, inn: inn }, 'doctor');
    await api('/api/prescriptions/sign', { id: res.prescription.id }, 'doctor');
    if (statusEl) {
      statusEl.innerHTML = `
        <div style="background:#ecfdf5;border:1px solid #a7f3d0;padding:12px 16px;border-radius:var(--radius-sm);color:#065f46;margin-top:10px">
          ✓ Elektron retsept <b>#${res.prescription.id}</b> muvaffaqiyatli rasmiylashtirildi, raqamli imzolandi va dorixonalarga uzatildi!
        </div>
      `;
    }
  } catch (e) {
    if (statusEl) {
      statusEl.innerHTML = `<div style="color:#ef4444;margin-top:10px">Xatolik: ${esc(e.message)}</div>`;
    }
  }
}

async function loadB2BPharmacist() {
  const queueEl = $('ph-b2b-queue');
  if (!queueEl) return;

  try {
    const res = await api('/api/prescriptions/queue', null, 'pharmacist');
    let html = '';
    (res.items || []).forEach(it => {
      html += `
        <div style="display:flex;justify-content:space-between;align-items:center;padding:14px 18px;border:1px solid var(--border-light);border-radius:var(--radius-md);margin-bottom:12px;background:#f8fafc">
          <div>
            <div style="font-size:14px;font-weight:700;color:var(--text-primary)">Retsept #${esc(it.id)} · XPN: <span style="color:var(--primary)">${esc(it.inn)}</span></div>
            <div style="font-size:12px;color:var(--text-secondary);margin-top:3px">Bemor: <b>${esc(it.patient)}</b> · Shifokor: ${esc(it.doctor)}</div>
          </div>
          <button class="btn-primary" style="padding:7px 18px;font-size:12px" onclick="b2bDispense('${it.id}')">Dori berish (Dispense)</button>
        </div>
      `;
    });
    queueEl.innerHTML = html || `<div style="padding:20px;text-align:center;color:var(--text-muted)">Kutilayotgan retseptlar mavjud emas.</div>`;
  } catch (e) {
    queueEl.innerHTML = `<div style="color:#ef4444;padding:10px">Xato: ${esc(e.message)}</div>`;
  }
}

async function b2bDispense(id) {
  try {
    await api('/api/prescriptions/dispense', { id: id }, 'pharmacist');
    alert('Dori muvaffaqiyatli berildi va kassada ro\'yxatdan o\'tdi!');
    loadB2BPharmacist();
  } catch (e) {
    alert('Xatolik: ' + e.message);
  }
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
window.b2bDraftPrescription = b2bDraftPrescription;
window.loadB2BPharmacist = loadB2BPharmacist;
window.b2bDispense = b2bDispense;
window.loadB2BFactory = loadB2BFactory;
