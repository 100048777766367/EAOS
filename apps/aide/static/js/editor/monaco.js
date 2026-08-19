export function mountEditor(host, tabs, statusNode) {
  const files = {
    'apps/aide/app/main.py': 'from apps.aide.app.main import app\n\n# AIDE presentation boundary',
    'apps/aide/templates/workspace.html': '<!-- AIDE workspace template -->',
    'apps/api/app/routers/tasks.py': '# Gateway-owned task lifecycle route',
  };
  const diagnostics = [];
  const state = { active: 'apps/aide/app/main.py', dirty: false, savedAt: null, diagnostics };

  function render() {
    tabs.innerHTML = Object.keys(files)
      .map((file) => `<button class="tab" data-file="${file}" aria-pressed="${file === state.active}">${file.split('/').pop()}</button>`)
      .join('');
    host.textContent = files[state.active] || '';
    host.dataset.activeFile = state.active;
    host.dataset.monacoReady = 'true';
    if (statusNode) statusNode.textContent = `${state.active} · ${state.dirty ? 'modified' : 'saved'} · ${diagnostics.length} diagnostics`;
  }

  function openFile(file) {
    state.active = file;
    if (!(file in files)) {
      files[file] = '';
      diagnostics.splice(0, diagnostics.length, { severity: 'info', message: 'Empty file placeholder; content not loaded from backend.' });
    } else {
      diagnostics.splice(0, diagnostics.length);
    }
    state.dirty = false;
    render();
    return { ...state };
  }

  function markChanged(nextText) {
    files[state.active] = nextText;
    state.dirty = true;
    render();
    return { ...state };
  }

  function markSaved() {
    state.dirty = false;
    state.savedAt = new Date().toISOString();
    render();
    return { ...state, saveContract: 'ui-only:file.save' };
  }

  tabs.addEventListener('click', (event) => {
    const file = event.target?.dataset?.file;
    if (file) openFile(file);
  });
  render();
  return { state, openFile, markChanged, markSaved, diagnostics };
}
