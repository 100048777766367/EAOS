export function mountInspector(node, contracts) {
  const items = contracts.map((item) => `<li>${item.name}: ${item.owner}</li>`);
  node.insertAdjacentHTML(
    'beforeend',
    `<h3>Gateway Contracts</h3><ul>${items.join('')}</ul><dl id="task-inspector"><dt>Task</dt><dd id="inspect-task">none</dd><dt>Lifecycle</dt><dd id="inspect-lifecycle">idle</dd><dt>Governance</dt><dd id="inspect-governance">unknown</dd><dt>Verification</dt><dd id="inspect-verification">pending</dd><dt>Evidence</dt><dd id="inspect-evidence">pending</dd><dt>Runtime</dt><dd id="inspect-runtime">not observed</dd><dt>Correlation</dt><dd id="inspect-correlation">none</dd></dl>`,
  );
  return { selectedResource: null, contracts: contracts.length };
}

export function updateTaskInspector(nodes, payload) {
  nodes.task.textContent = payload.task_id || 'none';
  nodes.lifecycle.textContent = payload.lifecycle_state || 'idle';
  nodes.governance.textContent = payload.governance?.result || payload.governance || 'unknown';
  nodes.verification.textContent = payload.verification?.passed === undefined ? 'pending' : String(payload.verification.passed);
  nodes.evidence.textContent = payload.evidence?.evidence_id || payload.evidence_ref || 'pending';
  nodes.runtime.textContent = payload.output ? 'gateway-output-observed' : 'awaiting-gateway-output';
  nodes.correlation.textContent = payload.correlation_id || 'none';
}
