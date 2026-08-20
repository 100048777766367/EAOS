export const TASK_STATES = {
  idle: 'IDLE',
  submitting: 'SUBMITTING',
  accepted: 'ACCEPTED',
  planning: 'PLANNING',
  executing: 'EXECUTING',
  verifying: 'VERIFYING',
  completed: 'COMPLETED',
  failed: 'FAILED',
  denied: 'DENIED',
};

export const TERMINAL_STATES = new Set(['completed', 'failed', 'denied']);
export const RUNTIME_STATES = new Set(Object.keys(TASK_STATES));

export function normalizeGatewayPayload(gatewayPayload) {
  return gatewayPayload?.payload || gatewayPayload || {};
}

export function isAcceptedTaskSubmission(result) {
  const payload = normalizeGatewayPayload(result);
  if (result?.status !== 'available') return false;
  if (payload.task_id) return true;
  return payload.status === 'SUCCESS';
}

function submissionErrorMessage(result, payload) {
  return payload?.error?.message || result?.detail || 'Gateway submission failed';
}

function verificationText(payload) {
  if (payload.verification?.passed !== undefined) return payload.verification.passed ? 'passed' : 'failed';
  if (payload.lifecycle_state === 'verifying') return 'running';
  if (payload.lifecycle_state === 'failed' && payload.error?.type === 'VerificationError') return 'failed';
  return 'pending';
}

function evidenceText(payload) {
  return payload.evidence?.evidence_id || payload.evidence_ref || 'pending';
}

export async function submitGatewayTask(command, targetAgent = 'planner') {
  const response = await fetch('/interactions/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command, target_agent: targetAgent }),
  });
  return response.json();
}

export async function readGatewayTask(taskId) {
  const response = await fetch(`/interactions/tasks/${taskId}`);
  return response.json();
}

export function classifyTaskOutcome(payload) {
  const state = payload.lifecycle_state;
  if (state === 'denied') return 'denied';
  if (state === 'failed' && payload.error?.type === 'VerificationError') return 'verification-failed';
  if (state === 'failed') return 'failed';
  if (state === 'completed') return 'completed';
  if (payload.governance?.result) return payload.governance.result;
  return 'unknown';
}

export function renderTaskState(node, gatewayPayload) {
  const payload = normalizeGatewayPayload(gatewayPayload);
  const lifecycleState = RUNTIME_STATES.has(payload.lifecycle_state) ? payload.lifecycle_state : 'idle';
  const state = TASK_STATES[lifecycleState];
  node.textContent = `Task ${state}`;
  node.dataset.lifecycleState = lifecycleState;
  node.dataset.terminal = String(TERMINAL_STATES.has(lifecycleState));
  return state;
}

export function mountTaskUx(nodes, websocketConnector, bootstrapState, observers = {}) {
  const state = {
    taskId: null,
    lifecycleState: 'idle',
    submissionState: 'idle',
    terminal: false,
    events: [],
    connection: null,
    lastPayload: null,
  };

  function notify(payload) {
    observers.onTaskState?.({ ...state, lastPayload: payload });
  }

  function renderEvent(event) {
    const item = document.createElement('li');
    item.dataset.eventType = event.event_type;
    item.dataset.lifecycleState = event.lifecycle_state;
    item.textContent = `${event.lifecycle_state} · ${event.event_type} · ${event.correlation_id || 'no-correlation'}`;
    nodes.timeline.appendChild(item);
  }

  function renderPayload(payload) {
    nodes.taskId.textContent = payload.task_id || state.taskId || 'none';
    nodes.currentState.textContent = TASK_STATES[payload.lifecycle_state] || payload.lifecycle_state || state.submissionState;
    nodes.correlation.textContent = payload.correlation_id || 'none';
    nodes.evidence.textContent = evidenceText(payload);
    nodes.error.textContent = payload.error?.message || 'none';
    nodes.governance.textContent = classifyTaskOutcome(payload);
    if (nodes.verification) nodes.verification.textContent = verificationText(payload);
    renderTaskState(nodes.footerTask, payload);
  }

  function applyEvent(event, orderedEvents = []) {
    if (!RUNTIME_STATES.has(event.lifecycle_state)) return false;
    state.taskId = event.task_id;
    state.lifecycleState = event.lifecycle_state;
    state.submissionState = event.lifecycle_state === 'accepted' ? 'accepted' : state.submissionState;
    state.terminal = TERMINAL_STATES.has(event.lifecycle_state);
    state.events = orderedEvents;
    state.lastPayload = event;
    renderPayload(event);
    renderEvent(event);
    notify(event);
    return true;
  }

  function connect(taskId) {
    if (state.connection?.close) state.connection.close();
    nodes.wsState.textContent = 'WS CONNECTING';
    state.connection = websocketConnector(bootstrapState, taskId, {
      onState(nextState) {
        nodes.wsState.textContent = `WS ${nextState.toUpperCase()}`;
        observers.onWebSocketState?.(nextState);
      },
      onEvent: applyEvent,
      onError(error) {
        nodes.wsState.textContent = 'WS ERROR';
        observers.onWebSocketState?.('error');
        observers.onError?.(error);
      },
      onClose(event) {
        const nextState = event.code === 1000 ? 'closed' : state.terminal ? 'closed' : 'reconnecting';
        nodes.wsState.textContent = `WS ${nextState.toUpperCase()}`;
        observers.onWebSocketState?.(nextState);
      },
    });
    return state.connection;
  }

  async function submit(command, targetAgent = 'planner') {
    state.submissionState = 'submitting';
    nodes.currentState.textContent = TASK_STATES.submitting;
    renderTaskState(nodes.footerTask, { lifecycle_state: 'submitting' });
    notify({ lifecycle_state: 'submitting', task_id: state.taskId });
    const result = await submitGatewayTask(command, targetAgent);
    const payload = normalizeGatewayPayload(result);
    if (!isAcceptedTaskSubmission(result)) {
      state.submissionState = 'failed';
      const errorPayload = {
        task_id: payload.task_id || state.taskId,
        lifecycle_state: payload.lifecycle_state || 'failed',
        error: { message: submissionErrorMessage(result, payload) },
      };
      renderPayload(errorPayload);
      notify(errorPayload);
      return result;
    }
    state.taskId = payload.task_id || state.taskId;
    state.lifecycleState = payload.lifecycle_state || 'accepted';
    state.submissionState = 'accepted';
    const acceptedPayload = { ...payload, task_id: state.taskId, lifecycle_state: state.lifecycleState };
    renderPayload(acceptedPayload);
    if (payload.task_id) connect(payload.task_id);
    notify(acceptedPayload);
    return result;
  }

  if (nodes.form) {
    nodes.form.addEventListener('submit', (event) => {
      event.preventDefault();
      const command = nodes.commandInput.value.trim();
      if (command) submit(command);
    });
  }

  return { state, applyEvent, connect, submit };
}
