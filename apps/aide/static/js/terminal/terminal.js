export function mountTerminal(output) {
  output.textContent = '$ uv run uvicorn apps.aide.app.main:app --host 127.0.0.1 --port 6932\nAIDE terminal UI ready; commands execute through governed gateway contracts.';
  return { sessions: [{ id: 'term-1', cwd: 'EAOS', status: 'idle' }] };
}
