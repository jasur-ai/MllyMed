/**
 * MllyMed AI — Suzuvchi Triaj va Tibbiy Skrining Agenti
 * Xalqaro daraja (ChatGPT/Siri-klass): oqim (typewriter) javob,
 * jonli taymerli "o'ylayapti" holati, qizil bayroq → 103 tez yordam.
 */

const AI_TIMER_START = () => Date.now();

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

/**
 * Matnni "oqim" effekti bilan chiqaradi — foydalanuvchi javobni
 * bir zumda emas, silliq yozilayotgandek ko'radi.
 */
function streamTextInto(el, fullText, done) {
  const text = String(fullText || '');
  const total = text.length;
  // Uzoq javoblar tezroq, qisqalari tabiiy sur'atda
  const perTick = Math.max(1, Math.round(total / 110));
  let i = 0;
  el.textContent = '';
  const cursor = document.createElement('span');
  cursor.className = 'stream-cursor';
  const tick = setInterval(() => {
    i = Math.min(total, i + perTick);
    el.textContent = text.slice(0, i);
    el.appendChild(cursor.cloneNode());
    const log = $('chat-log');
    if (log) log.scrollTop = log.scrollHeight;
    if (i >= total) {
      clearInterval(tick);
      el.textContent = text;
      if (typeof done === 'function') done();
    }
  }, 16);
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

  // "O'ylayapti" holati — jonli taymer + to'lqin bar animatsiyasi
  const typingId = 'typing-' + Date.now();
  const t0 = AI_TIMER_START();
  log.insertAdjacentHTML('beforeend', `
    <div class="bubble bot typing" id="${typingId}" role="status" aria-live="polite">
      <span class="think-wave" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>
      <span class="think-label">MllyMed AI o'ylayapti</span><span class="think-dots" aria-hidden="true"><i>.</i><i>.</i><i>.</i></span>
      <b class="think-s">0s</b>
    </div>`);
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

    // QIZIL BAYROQ — darhol, to'liq, katta 103 tugmasi bilan
    const cleanReply = (typeof stripEmoji === 'function') ? stripEmoji(res.reply || '') : String(res.reply || '');
    if (res.stage === 'emergency') {
      log.insertAdjacentHTML('beforeend', `
        <div class="bubble emergency" role="alert">
          <div class="emg-band">${icon('alert-triangle', 16, 2.4)} QIZIL BAYROQ — SHOSHILINCH HOLAT</div>
          <div class="emg-reply">${esc(cleanReply)}</div>
          <a class="emg-call-btn" href="tel:103">${icon('phone', 26, 2.2)}<span><small>Tez yordam</small><b>103 — qo'ng'iroq qiling</b></span></a>
          <div class="emg-note">${icon('info', 12, 2.2)} Operator bilan gaplashing va manzilni aniq ayting. Telefonni o'chirmang.</div>
        </div>`);
      log.scrollTop = log.scrollHeight;
      return;
    }

    // Oddiy javob — oqim (typewriter) effekti bilan
    const bubble = document.createElement('div');
    bubble.className = 'bubble bot streaming';
    const body = document.createElement('span');
    body.className = 'stream-text';
    bubble.appendChild(body);
    log.appendChild(bubble);

    streamTextInto(body, cleanReply, () => {
      bubble.classList.remove('streaming');
      const specialist = res.triage && res.triage.specialist ? ((typeof stripEmoji === 'function') ? stripEmoji(res.triage.specialist) : res.triage.specialist) : '';
      if (specialist) {
        const foot = document.createElement('div');
        foot.className = 'bubble-foot';
        foot.innerHTML = `<button type="button" class="badge badge-otc triage-chip" onclick="quickSearch('${esc(specialist)}')">${icon('stethoscope', 13, 2.1)} Yo'naltirish: ${esc(specialist)}</button>`;
        bubble.appendChild(foot);
        log.scrollTop = log.scrollHeight;
      }
    });
  } catch (e) {
    stopThinking();
    log.insertAdjacentHTML('beforeend', `<div class="bubble bot" style="color:#ef4444">${esc(e.message)}</div>`);
    log.scrollTop = log.scrollHeight;
  }
}

window.toggleAgentPopup = toggleAgentPopup;
window.sendPrompt = sendPrompt;
window.chatSend = chatSend;
