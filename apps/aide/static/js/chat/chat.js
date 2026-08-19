export function mountChat(form, log, state) {
  log.innerHTML = '<div class="chat-message">EAOS Copilot consumes Gateway task/chat contracts; no local agent execution.</div>';
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    log.insertAdjacentHTML('beforeend', `<div class="chat-message pending">Gateway request pending: ${input.value}</div>`);
    input.value = '';
  });
  return { endpoint: `${state.api_base_url}/v1/agents/execute`, owner: 'apps/api', localExecution: false };
}
