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

export function createLifecycleEventBuffer() {
  const seen = new Set();
  const events = [];
  return {
    events,
    push(event) {
      const key = `${event.task_id}:${event.event_type}:${event.timestamp}`;
      if (seen.has(key)) return false;
      seen.add(key);
      events.push(event);
      events.sort((left, right) => String(left.timestamp).localeCompare(String(right.timestamp)));
      return true;
    },
  };
}

export function connectTaskLifecycle(state, taskId, handlers = {}) {
  const socket = new WebSocket(taskLifecycleWebSocketUrl(state, taskId));
  const buffer = createLifecycleEventBuffer();
  socket.addEventListener('open', () => handlers.onState?.('connected'));
  socket.addEventListener('message', (event) => {
    const payload = JSON.parse(event.data);
    if (buffer.push(payload)) handlers.onEvent?.(payload, [...buffer.events]);
  });
  socket.addEventListener('error', (event) => handlers.onError?.(event));
  socket.addEventListener('close', (event) => {
    handlers.onState?.(event.code === 1000 ? 'terminal-closed' : 'disconnected');
    handlers.onClose?.(event, [...buffer.events]);
  });
  return { socket, buffer };
}
