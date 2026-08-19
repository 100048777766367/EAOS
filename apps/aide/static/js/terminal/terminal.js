export function mountTerminal(output) {
  const state = { sessions: [{ id: 'term-1', cwd: 'EAOS', status: 'idle' }], backendExecution: false };
  output.textContent = '$ uv run uvicorn apps.aide.app.main:app --host 127.0.0.1 --port 6932\nTerminal UI ready; execution remains Gateway-owned.';
  return state;
}
