/**
 * MllyMed B2B — Shifokor Portali
 * XPN (INN) bo'yicha elektron retsept shakllantirish va raqamli imzolash
 */

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

window.b2bDraftPrescription = b2bDraftPrescription;
