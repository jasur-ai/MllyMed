/**
 * MllyMed AI — Suzuvchi Triaj va Tibbiy Skrining Agenti
 */

function toggleAgentPopup() {
  const popup = $('agent-popup');
  if (!popup) return;
  popup.classList.toggle('hidden');
  if (!popup.classList.contains('hidden')) {
    const input = $('chat-in');
    if (input) input.focus();
  }
}

function sendPrompt(text) {
  const inp = $('chat-in');
  if (inp) {
    inp.value = text;
    chatSend();
  }
}

async function chatSend() {
  const inp = $('chat-in');
  const text = (inp?.value || '').trim();
  if (!text) return;
  inp.value = '';

  const log = $('chat-log');
  if (!log) return;

  log.insertAdjacentHTML('beforeend', `<div class="bubble user">${esc(text)}</div>`);
  log.scrollTop = log.scrollHeight;

  // "O'ylamoqda" (AI Thinking) holati — fon yo'q, nurli shimmer + jonli soniyalik taymer
  const typingId = 'typing-' + Date.now();
  const t0 = Date.now();
  log.insertAdjacentHTML('beforeend', `
    <div class="bubble bot typing" id="${typingId}" role="status" aria-live="polite">
      <span class="think-spark" aria-hidden="true">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
          <path d="M12 2L14.4 9.6L22 12L14.4 14.4L12 22L9.6 14.4L2 12L9.6 9.6L12 2Z" fill="url(#sparkGrad)"/>
          <defs>
            <linearGradient id="sparkGrad" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
              <stop stop-color="#0b69ed"/>
              <stop offset="1" stop-color="#38bdf8"/>
            </linearGradient>
          </defs>
        </svg>
      </span>
      <span class="think-label">O'ylamoqda…</span>
      <b class="think-s">0s</b>
    </div>
  `);
  log.scrollTop = log.scrollHeight;

  const thinkTimer = setInterval(() => {
    const secEl = document.querySelector('#' + typingId + ' .think-s');
    if (secEl) secEl.textContent = Math.floor((Date.now() - t0) / 1000) + 's';
  }, 1000);
  const stopThinking = () => {
    clearInterval(thinkTimer);
    const typingEl = $(typingId);
    if (typingEl) typingEl.remove();
  };

  try {
    const res = await api('/api/chat', { text: text, sid: AppState.sid }, 'patient');
    stopThinking();

    let botHtml = `<div class="bubble bot">${esc(res.reply)}`;
    if (res.stage === 'emergency') {
      botHtml = `
        <div class="bubble warning">
          <div style="font-weight:800;color:#b91c1c;margin-bottom:4px">🚨 QIZIL BAYROQ — 103 GA QO'NG'IROQ QILING</div>
          ${esc(res.reply)}
          <div style="margin-top:10px">
            <a href="tel:103" class="btn-primary" style="background:#dc2626;display:inline-block;padding:6px 16px;font-size:12px;text-decoration:none">103 ga qo'ng'iroq qilish</a>
          </div>
        </div>
      `;
    } else if (res.triage && res.triage.specialist) {
      botHtml += `
        <div style="margin-top:10px;padding-top:8px;border-top:1px dashed var(--border-light)">
          <span class="badge badge-otc" style="cursor:pointer" onclick="quickSearch('${esc(res.triage.specialist)}')">
            🩺 Yo'naltirish: ${esc(res.triage.specialist)}
          </span>
        </div>
      `;
    }
    botHtml += `</div>`;
    log.insertAdjacentHTML('beforeend', botHtml);
    log.scrollTop = log.scrollHeight;
  } catch (e) {
    stopThinking();
    log.insertAdjacentHTML('beforeend', `<div class="bubble bot" style="color:#ef4444">${esc(e.message)}</div>`);
  }
}

window.toggleAgentPopup = toggleAgentPopup;
window.sendPrompt = sendPrompt;
window.chatSend = chatSend;
