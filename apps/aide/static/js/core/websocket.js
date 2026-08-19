export function taskLifecycleWebSocketUrl(state, taskId) {
  const base = (state.api_ws_url || '').replace(/\/$/, '');
  return `${base}/api/v1/tasks/${taskId}/events`;
}

export function describeWebSocketContract(state) {
  return {
    endpoint: `${state.api_ws_url}/api/v1/tasks/{task_id}/events`,
    purpose: 'Gateway-owned task lifecycle, verification, evidence, and error events',
  };
}

export function connectTaskLifecycle(state, taskId, onEvent, onClose) {
  const socket = new WebSocket(taskLifecycleWebSocketUrl(state, taskId));
  socket.addEventListener('message', (event) => onEvent(JSON.parse(event.data)));
  socket.addEventListener('close', () => {
    if (onClose) onClose();
  });
  return socket;
}
