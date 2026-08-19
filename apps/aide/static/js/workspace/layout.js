export function enableWorkspaceLayout(shell) {
  shell.dataset.resizablePanes = 'enabled';
  return { responsive: true, resizablePanes: true };
}
