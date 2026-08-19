export function mountChat(form, log, state) {
  log.innerHTML = '<div class="chat-message">EAOS Copilot connected to Gateway contracts.</div>';
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = document.getElementById('chat-input');
    log.insertAdjacentHTML('beforeend', `<div class="chat-message">${input.value}</div>`);
    input.value = '';
  });
  return { endpoint: `${state.api_base_url}/v1/agents/execute` };
}
