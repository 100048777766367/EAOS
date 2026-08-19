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
  if (state === 'denied') return 'governance-denied';
  if (state === 'failed' && payload.error) return 'execution-or-verification-failed';
  if (state === 'completed') return 'verified-complete';
  return 'in-progress';
}

export function renderTaskState(node, gatewayPayload) {
  const payload = gatewayPayload.payload || gatewayPayload;
  const state = TASK_STATES[payload.lifecycle_state] || TASK_STATES.idle;
  node.textContent = `Task ${state}`;
  node.dataset.lifecycleState = payload.lifecycle_state || 'idle';
  node.dataset.terminal = String(TERMINAL_STATES.has(payload.lifecycle_state));
  return state;
}

export function mountTaskUx(nodes, websocketConnector, bootstrapState) {
  const state = { taskId: null, lifecycleState: 'idle', terminal: false, events: [] };

  function renderEvent(event) {
    const item = document.createElement('li');
    item.dataset.eventType = event.event_type;
    item.textContent = `${event.lifecycle_state} · ${event.event_type} · ${event.correlation_id || 'no-correlation'}`;
    nodes.timeline.appendChild(item);
  }

  function applyEvent(event, orderedEvents = []) {
    state.taskId = event.task_id;
    state.lifecycleState = event.lifecycle_state;
    state.terminal = TERMINAL_STATES.has(event.lifecycle_state);
    state.events = orderedEvents;
    nodes.taskId.textContent = event.task_id;
    nodes.currentState.textContent = TASK_STATES[event.lifecycle_state] || event.lifecycle_state;
    nodes.correlation.textContent = event.correlation_id || 'none';
    nodes.evidence.textContent = event.evidence_ref || 'pending';
    nodes.error.textContent = event.error?.message || 'none';
    nodes.governance.textContent = classifyTaskOutcome(event);
    renderEvent(event);
    renderTaskState(nodes.footerTask, event);
  }

  function connect(taskId) {
    nodes.wsState.textContent = 'WS connecting';
    const connection = websocketConnector(bootstrapState, taskId, {
      onState(nextState) {
        nodes.wsState.textContent = `WS ${nextState}`;
      },
      onEvent: applyEvent,
      onError() {
        nodes.wsState.textContent = 'WS error';
      },
      onClose(event) {
        nodes.wsState.textContent = event.code === 1000 ? 'WS terminal closed' : 'WS disconnected';
      },
    });
    return connection;
  }

  return { state, applyEvent, connect };
}
