export function mountAgentStatus(node) {
  node.innerHTML = '<div class="contract-card">Agent: awaiting observed Gateway orchestration state</div>';
  return { state: 'unknown', owner: 'apps/api' };
}
