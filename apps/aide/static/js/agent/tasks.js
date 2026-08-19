export const TASK_STATES = {
  idle: 'IDLE',
  submitting: 'SUBMITTING',
  accepted: 'QUEUED',
  planning: 'PLANNING',
  executing: 'EXECUTING',
  verifying: 'VERIFYING',
  completed: 'COMPLETED',
  failed: 'FAILED',
  denied: 'DENIED',
  timeout: 'TIMEOUT',
  cancelled: 'CANCELLED',
};

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

export function renderTaskState(node, gatewayPayload) {
  const payload = gatewayPayload.payload || gatewayPayload;
  const state = TASK_STATES[payload.lifecycle_state] || TASK_STATES.idle;
  node.textContent = `Task ${state}`;
  return state;
}
