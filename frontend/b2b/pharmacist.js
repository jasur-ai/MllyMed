/**
 * MllyMed B2B — Dorixona Dispense Portali
 * Imzolangan retseptlar navbati va bemorga dori tarqatish
 */

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

window.loadB2BPharmacist = loadB2BPharmacist;
window.b2bDispense = b2bDispense;
