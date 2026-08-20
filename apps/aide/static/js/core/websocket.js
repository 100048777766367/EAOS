const TERMINAL_STATES = new Set(['completed', 'failed', 'denied']);
const VALID_STATES = new Set(['accepted', 'planning', 'executing', 'verifying', 'completed', 'failed', 'denied']);

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
      if (!VALID_STATES.has(event.lifecycle_state)) return false;
      const key = `${event.task_id}:${event.event_type}:${event.lifecycle_state}:${event.timestamp}:${event.correlation_id || ''}`;
      if (seen.has(key)) return false;
      seen.add(key);
      events.push(event);
      return true;
    },
  };
}

export function connectTaskLifecycle(state, taskId, handlers = {}, options = {}) {
  const buffer = options.buffer || createLifecycleEventBuffer();
  const maxReconnects = options.maxReconnects ?? 2;
  const reconnectDelayMs = options.reconnectDelayMs ?? 250;
  let socket = null;
  let reconnects = 0;
  let closedByClient = false;
  let terminal = false;
  let reconnectTimer = null;

  function cleanup() {
    if (reconnectTimer) clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }

  function open() {
    handlers.onState?.(reconnects > 0 ? 'reconnecting' : 'connecting');
    socket = new WebSocket(taskLifecycleWebSocketUrl(state, taskId));
    socket.addEventListener('open', () => handlers.onState?.('open'));
    socket.addEventListener('message', (event) => {
      const payload = JSON.parse(event.data);
      if (buffer.push(payload)) {
        terminal = TERMINAL_STATES.has(payload.lifecycle_state);
        handlers.onEvent?.(payload, [...buffer.events]);
      }
    });
    socket.addEventListener('error', (event) => handlers.onError?.(event));
    socket.addEventListener('close', (event) => {
      handlers.onState?.(event.code === 1000 ? 'closed' : 'closed');
      handlers.onClose?.(event, [...buffer.events]);
      if (closedByClient || terminal || event.code === 1000 || reconnects >= maxReconnects) return;
      reconnects += 1;
      handlers.onState?.('reconnecting');
      reconnectTimer = setTimeout(open, reconnectDelayMs);
    });
  }

  open();
  return {
    get socket() {
      return socket;
    },
    buffer,
    close() {
      closedByClient = true;
      cleanup();
      socket?.close();
    },
  };
}
