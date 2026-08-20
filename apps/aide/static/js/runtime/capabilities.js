export function renderCapabilityRegistry(node, envelope) {
  const payload = envelope?.payload;
  const capabilities = Array.isArray(payload) ? payload : payload?.capabilities || payload?.data || [];
  const status = envelope?.status || 'unavailable';
  const rows = capabilities
    .map(
      (capability) =>
        `<li data-capability-id="${capability.capability_id}" data-capability-status="${capability.status}"><span>${capability.name}</span><strong>${capability.status}</strong></li>`,
    )
    .join('');
  node.innerHTML = `<h3>EAOS Capabilities</h3><p data-capability-registry-status="${status}">Registry ${status}</p><ul>${rows}</ul>`;
  return { status, count: capabilities.length };
}
