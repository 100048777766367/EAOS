export function mountChat(form, log, state, options = {}) {
  log.innerHTML = '<div class="chat-message">EAOS Copilot consumes Gateway task/chat contracts; no local agent execution.</div>';
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    const command = input.value.trim();
    if (!command) return;
    log.insertAdjacentHTML('beforeend', `<div class="chat-message pending">Gateway request pending: ${command}</div>`);
    options.onSubmitCommand?.(command);
    input.value = '';
  });
  return { endpoint: `${state.api_base_url}/v1/agents/execute`, owner: 'apps/api', localExecution: false };
}
