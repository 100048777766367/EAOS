export function mountRuntime(footer, state) {
  const runtime = { gateway: 'unknown', websocket: 'not-opened', task: 'idle', api: state.api_base_url };
  footer.textContent = `● Gateway Unknown | API ${runtime.api} | WS ${runtime.websocket} | Task ${runtime.task}`;
  return runtime;
}

export function updateRuntimeFooter(nodes, runtime) {
  nodes.health.textContent = `● Gateway ${runtime.gateway}`;
  nodes.ws.textContent = `WS ${runtime.websocket}`;
  nodes.task.textContent = `Task ${runtime.task}`;
  return runtime;
}
