export function mountExplorer(root, options = {}) {
  const files = [
    'apps/aide/app/main.py',
    'apps/aide/templates/workspace.html',
    'apps/aide/static/js/core/websocket.js',
    'apps/api/app/routers/tasks.py',
    'runtime/traces/audit_ledger.jsonl',
  ];
  const state = { files, activeFile: null, loading: false, error: null, empty: files.length === 0 };

  function render() {
    if (state.loading) {
      root.innerHTML = '<li class="tree-state">Loading workspace…</li>';
      return;
    }
    if (state.error) {
      root.innerHTML = `<li class="tree-state error">${state.error}</li>`;
      return;
    }
    if (state.empty) {
      root.innerHTML = '<li class="tree-state empty">No files discovered</li>';
      return;
    }
    root.innerHTML = state.files
      .map((file) => `<li class="tree-item" data-file="${file}" aria-selected="${file === state.activeFile}">${file}</li>`)
      .join('');
  }

  function selectFile(file) {
    state.activeFile = file;
    render();
    if (options.onSelect) options.onSelect(file);
    return { ...state };
  }

  root.addEventListener('click', (event) => {
    const file = event.target?.dataset?.file;
    if (file) selectFile(file);
  });
  render();
  return { state, selectFile, render };
}
