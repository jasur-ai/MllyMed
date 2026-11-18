/**
 * MllyMed Bemor Portali & Kabinet Moduli
 */

function openPatientModal() {
  const modal = $('patient-modal');
  if (modal) modal.classList.remove('hidden');
  loadPatientState();
}

function closePatientModal() {
  const modal = $('patient-modal');
  if (modal) modal.classList.add('hidden');
}

async function loadPatientState() {
  const apptsEl = $('patient-appts-list');
  const rxsEl = $('patient-rxs-list');
  const patientIdEl = $('patient-id-display');

  if (patientIdEl) patientIdEl.textContent = AppState.sid;

  try {
    const res = await api('/api/state?sid=' + AppState.sid, null, 'patient');
    
    // Qabullar ro'yxati
    let aHtml = '';
    if (!(res.appointments || []).length) {
      aHtml = `<span style="font-size:13px;color:var(--text-muted)">Sizda hali faol qabullar mavjud emas.</span>`;
    } else {
      res.appointments.forEach(a => {
        aHtml += `
          <div style="padding:10px 14px;border:1px solid var(--border-light);border-radius:var(--radius-sm);margin-bottom:8px;font-size:13px;background:#f8fafc">
            Shifokor: <b>${esc(a.doctor_name || a.doctor_id)}</b> (${esc(a.slot)})<br>
            Status: <span class="badge ${a.status === 'confirmed' ? 'badge-local' : 'badge-import'}">${esc(a.status)}</span>
          </div>
        `;
      });
    }
    if (apptsEl) apptsEl.innerHTML = aHtml;

    // Retseptlar ro'yxati
    let rHtml = '';
    if (!(res.prescriptions || []).length) {
      rHtml = `<span style="font-size:13px;color:var(--text-muted)">Sizga hali elektron retsept yozilmagan.</span>`;
    } else {
      res.prescriptions.forEach(r => {
        rHtml += `
          <div style="padding:10px 14px;border:1px solid var(--border-light);border-radius:var(--radius-sm);margin-bottom:8px;font-size:13px;background:#f8fafc">
            Dori XPN: <b>${esc(r.inn)}</b><br>
            Holati: <span class="badge ${r.status === 'dispensed' ? 'badge-local' : 'badge-otc'}">${esc(r.status)}</span>
          </div>
        `;
      });
    }
    if (rxsEl) rxsEl.innerHTML = rHtml;
  } catch (e) {
    if (apptsEl) apptsEl.innerHTML = `<span style="color:#ef4444;font-size:13px">Xato: ${esc(e.message)}</span>`;
  }
}

window.openPatientModal = openPatientModal;
window.closePatientModal = closePatientModal;
window.loadPatientState = loadPatientState;
