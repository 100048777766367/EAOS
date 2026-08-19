export function describeWebSocketContract(state) {
  return {
    endpoint: state.api_ws_url,
    owner: 'apps/api',
    status: 'not-opened',
    purpose: 'chat, agent, task, execution, runtime, evidence, telemetry events',
  };
}
