export async function loadGatewayContracts() {
  const response = await fetch('/integrations/gateway/contracts');
  return response.json();
}

export async function loadGatewaySnapshot() {
  const response = await fetch('/integrations/gateway/snapshot');
  return response.json();
}
