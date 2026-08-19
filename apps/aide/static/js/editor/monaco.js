export function mountEditor(host, tabs) {
  const active = 'apps/aide/app/main.py';
  tabs.innerHTML = `<button class="tab" data-file="${active}">main.py</button>`;
  host.textContent = 'from apps.aide.app.main import app\n\n# Monaco adapter ready inside AIDE boundary';
  host.dataset.monacoReady = 'true';
  return { active, diagnostics: [] };
}
