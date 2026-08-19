export function telemetryContract(state) {
  return { endpoint: `${state.api_base_url}/telemetry/ingest`, owner: 'apps/api' };
}
