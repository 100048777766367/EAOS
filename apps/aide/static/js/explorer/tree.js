export function mountExplorer(root) {
  const files = ['apps/aide/app/main.py', 'apps/aide/templates/workspace.html', 'apps/api/app/routers/agents.py', 'runtime/traces/audit_ledger.jsonl'];
  root.innerHTML = files.map((file) => `<li class="tree-item" data-file="${file}">${file}</li>`).join('');
  return files;
}
