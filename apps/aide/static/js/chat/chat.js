function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function messageText(payload) {
  if (payload?.error?.message) return payload.error.message;
  if (payload?.output) return payload.output;
  if (payload?.lifecycle_state) return `Task ${payload.lifecycle_state}`;
  return 'Gateway response received without output.';
}

export function mountChat(form, log, state, options = {}) {
  const conversation = [];
  const renderedTerminalTasks = new Set();
  log.innerHTML = '<div class="chat-message">EAOS Copilot sends human requests through Gateway task lifecycle; no local agent execution.</div>';

  function appendMessage(role, text, cssClass = '') {
    const item = document.createElement('div');
    item.className = `chat-message ${cssClass}`.trim();
    item.dataset.role = role;
    item.innerHTML = `<strong>${escapeHtml(role)}:</strong> ${escapeHtml(text)}`;
    log.appendChild(item);
    return item;
  }

  function recordTaskUpdate(payload = {}) {
    const terminal = ['completed', 'failed', 'denied'].includes(payload.lifecycle_state);
    if (!terminal && !payload.error?.message) return null;
    if (terminal && payload.task_id && renderedTerminalTasks.has(payload.task_id)) return null;
    if (terminal && payload.task_id) renderedTerminalTasks.add(payload.task_id);
    const role = payload.error?.message || payload.lifecycle_state === 'failed' || payload.lifecycle_state === 'denied' ? 'EAOS error' : 'EAOS';
    const text = messageText(payload);
    conversation.push({ role, text, task_id: payload.task_id, correlation_id: payload.correlation_id });
    return appendMessage(role, text, payload.error?.message ? 'error' : 'response');
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    const command = input.value.trim();
    if (!command) return;
    conversation.push({ role: 'Human', text: command });
    appendMessage('Human', command, 'pending');
    options.onSubmitCommand?.(command);
    input.value = '';
  });
  return {
    endpoint: `${state.api_base_url}/api/v1/control/execute`,
    owner: 'apps/api',
    localExecution: false,
    conversation,
    recordTaskUpdate,
  };
}
