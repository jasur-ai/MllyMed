/**
 * MllyMed AI Floating Triage & Consultation Agent
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

async function chatSend() {
  const inp = $('chat-in');
  const text = (inp?.value || '').trim();
  if (!text) return;
  inp.value = '';

  const log = $('chat-log');
  if (!log) return;

  log.insertAdjacentHTML('beforeend', `<div class="bubble user">${esc(text)}</div>`);
  log.scrollTop = log.scrollHeight;

  try {
    const res = await api('/api/chat', { text: text, sid: AppState.sid }, 'patient');
    let botHtml = `<div class="bubble bot">${esc(res.reply)}`;
    if (res.triage && res.triage.specialist) {
      botHtml += `
        <div style="margin-top:10px;padding-top:8px;border-top:1px dashed var(--border-light)">
          <span class="badge badge-otc" style="cursor:pointer" onclick="lookup('${esc(res.triage.specialist)}')">
            🩺 Yo'naltirish: ${esc(res.triage.specialist)}
          </span>
        </div>
      `;
    }
    botHtml += `</div>`;
    log.insertAdjacentHTML('beforeend', botHtml);
    log.scrollTop = log.scrollHeight;
  } catch (e) {
    log.insertAdjacentHTML('beforeend', `<div class="bubble bot" style="color:#ef4444">${esc(e.message)}</div>`);
  }
}

window.toggleAgentPopup = toggleAgentPopup;
window.chatSend = chatSend;
