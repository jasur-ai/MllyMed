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
    autoResizeInput(inp);
    chatSend();
  }
}

function openAgentWithPrompt(q) {
  if (!q) return;
  const popup = $('agent-popup');
  if (popup) {
    popup.classList.remove('hidden');
    const log = $('chat-log');
    if (log) log.scrollTop = log.scrollHeight;
  }
  sendPrompt(q + " tahlili");
}

function autoResizeInput(el) {
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
  const sendBtn = $('chat-send-btn');
  if (sendBtn) {
    if (el.value.trim().length > 0) {
      sendBtn.classList.remove('disabled');
    } else {
      sendBtn.classList.add('disabled');
    }
  }
}

function onChatKeyDown(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    chatSend();
  }
}

function toggleQuickPrompts() {
  const box = $('quick-prompts-box');
  if (box) {
    box.style.display = box.style.display === 'none' ? 'flex' : 'none';
    const log = $('chat-log');
    if (log) log.scrollTop = log.scrollHeight;
  }
}

let speechRec = null;
function toggleSpeechRecognition() {
  const micBtn = $('chat-mic-btn');
  const inp = $('chat-in');
  const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRec) {
    alert("Brauzeringiz ovozli kiritishni qo'llab-quvvatlamaydi.");
    return;
  }
  if (!speechRec) {
    speechRec = new SpeechRec();
    speechRec.lang = 'uz-UZ';
    speechRec.interimResults = false;
    speechRec.onstart = () => {
      micBtn?.classList.add('recording');
    };
    speechRec.onresult = (e) => {
      const phrase = e.results[0][0].transcript;
      if (inp) {
        inp.value = (inp.value ? inp.value + ' ' : '') + phrase;
        autoResizeInput(inp);
      }
    };
    speechRec.onerror = () => {
      micBtn?.classList.remove('recording');
    };
    speechRec.onend = () => {
      micBtn?.classList.remove('recording');
    };
  }
  try {
    speechRec.start();
  } catch (err) {
    speechRec.stop();
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

  // "O'ylamoqda" (AI Thinking) holati — yumshoq nurli fon + jonli 3 ta nuqta + soniyalik taymer
  const typingId = 'typing-' + Date.now();
  const t0 = AI_TIMER_START();
  log.insertAdjacentHTML('beforeend', `
    <div class="bubble bot typing" id="${typingId}" role="status" aria-live="polite">
      <span class="think-dots" aria-hidden="true">
        <span class="tdot"></span>
        <span class="tdot"></span>
        <span class="tdot"></span>
      </span>
      <span class="think-label">MllyMed AI o'ylayapti...</span>
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
      }
      // Pastida harakatlar paneli: vaqt (qancha daqiqa oldin), copy, like, dislike
      const actions = createBotActionsBar(Date.now());
      bubble.appendChild(actions);
      log.scrollTop = log.scrollHeight;
    });
  } catch (e) {
    stopThinking();
    log.insertAdjacentHTML('beforeend', `<div class="bubble bot" style="color:#ef4444">${esc(e.message)}</div>`);
    log.scrollTop = log.scrollHeight;
  }
}

/**
 * Vaqtni nisbiy hisoblash: "Hozirgina", "1 daqiqa oldin", "X daqiqa oldin"
 */
function formatRelativeTime(ts) {
  if (!ts) return "Hozirgina";
  const diffSec = Math.max(0, Math.floor((Date.now() - ts) / 1000));
  if (diffSec < 20) return "Hozirgina";
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin <= 1) return "1 daqiqa oldin";
  if (diffMin < 60) return diffMin + " daqiqa oldin";
  const diffHour = Math.floor(diffMin / 60);
  if (diffHour === 1) return "1 soat oldin";
  if (diffHour < 24) return diffHour + " soat oldin";
  return Math.floor(diffHour / 24) + " kun oldin";
}

/**
 * Bot xabari ostidagi harakatlar panelini yaratish
 */
function createBotActionsBar(timestamp) {
  const bar = document.createElement('div');
  bar.className = 'bot-actions';
  const ts = timestamp || Date.now();
  bar.setAttribute('data-timestamp', String(ts));
  bar.innerHTML = `
    <span class="bot-time">${formatRelativeTime(ts)}</span>
    <div class="bot-action-btns">
      <button type="button" class="bot-act-btn btn-copy" title="Nusxa olish" aria-label="Nusxa olish" onclick="copyBotMsg(this)">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        <span class="copy-lbl">Nusxa</span>
      </button>
      <button type="button" class="bot-act-btn btn-like" title="Foydali" aria-label="Foydali" onclick="rateBotMsg(this, 'like')">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
      </button>
      <button type="button" class="bot-act-btn btn-dislike" title="Foydasiz" aria-label="Foydasiz" onclick="rateBotMsg(this, 'dislike')">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h3a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-3"></path></svg>
      </button>
    </div>
  `;
  return bar;
}

/**
 * Xabardan nusxa olish (Clipboard)
 */
function copyBotMsg(btn) {
  const bubble = btn.closest('.bubble.bot') || btn.closest('#chat-log')?.querySelector('.bubble.bot');
  if (!bubble) return;
  const clone = bubble.cloneNode(true);
  clone.querySelectorAll('.bot-actions, .bubble-foot, .stream-cursor, .quick-chip').forEach(el => el.remove());
  const text = (clone.textContent || '').trim();

  const lbl = btn.querySelector('.copy-lbl');
  const doFeedback = () => {
    btn.classList.add('copied');
    if (lbl) lbl.textContent = 'Olingan';
    setTimeout(() => {
      btn.classList.remove('copied');
      if (lbl) lbl.textContent = 'Nusxa';
    }, 2000);
  };

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(doFeedback).catch(() => fallbackCopy(text, doFeedback));
  } else {
    fallbackCopy(text, doFeedback);
  }
}

function fallbackCopy(text, cb) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    if (typeof cb === 'function') cb();
  } catch (e) {}
  document.body.removeChild(ta);
}

/**
 * Like / Dislike baholash
 */
function rateBotMsg(btn, type) {
  const parent = btn.closest('.bot-action-btns');
  if (!parent) return;
  const likeBtn = parent.querySelector('.btn-like');
  const dislikeBtn = parent.querySelector('.btn-dislike');

  if (type === 'like') {
    const isLiked = likeBtn && likeBtn.classList.contains('active');
    likeBtn?.classList.toggle('active', !isLiked);
    dislikeBtn?.classList.remove('active');
  } else {
    const isDisliked = dislikeBtn && dislikeBtn.classList.contains('active');
    dislikeBtn?.classList.toggle('active', !isDisliked);
    likeBtn?.classList.remove('active');
  }
}

// Barcha xabarlar vaqtini yangilab turish (har 15 soniyada)
function updateAllBotTimes() {
  const allBars = document.querySelectorAll('.bot-actions');
  allBars.forEach((bar, idx) => {
    let raw = bar.getAttribute('data-timestamp');
    let ts = parseInt(raw, 10);
    if (raw === 'initial' || !ts || isNaN(ts) || ts <= 0) {
      // Dastlabki xabarlar uchun tartib bilan daqiqa ajratish (5 daq. oldin, 8 daq. oldin)
      const minutesAgo = Math.max(3, (allBars.length - idx) * 3 + 1);
      ts = Date.now() - minutesAgo * 60 * 1000;
      bar.setAttribute('data-timestamp', String(ts));
    }
    const timeEl = bar.querySelector('.bot-time');
    if (timeEl) {
      timeEl.textContent = formatRelativeTime(ts);
    }
  });
}

// Darhol ishga tushirish va har 15 soniyada takrorlash
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateAllBotTimes);
} else {
  updateAllBotTimes();
}
setInterval(updateAllBotTimes, 15000);

window.toggleAgentPopup = toggleAgentPopup;
window.sendPrompt = sendPrompt;
window.openAgentWithPrompt = openAgentWithPrompt;
window.chatSend = chatSend;
window.autoResizeInput = autoResizeInput;
window.onChatKeyDown = onChatKeyDown;
window.toggleQuickPrompts = toggleQuickPrompts;
window.toggleSpeechRecognition = toggleSpeechRecognition;
window.createBotActionsBar = createBotActionsBar;
window.formatRelativeTime = formatRelativeTime;
window.copyBotMsg = copyBotMsg;
window.rateBotMsg = rateBotMsg;
