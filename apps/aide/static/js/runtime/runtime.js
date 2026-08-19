export function mountRuntime(footer, state) {
  footer.textContent = `● Gateway Unknown | API ${state.api_base_url} | Python | EAOS | WS not-opened`;
  return { health: 'ready', websocket: state.api_ws_url };
}
