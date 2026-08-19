export function readBootstrapState() {
  const node = document.getElementById('aide-state');
  return JSON.parse(node?.textContent || '{}');
}
