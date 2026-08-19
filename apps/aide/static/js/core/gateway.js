export async function observeGateway() {
  try {
    const response = await fetch('/integrations/gateway/health');
    return await response.json();
  } catch (error) {
    return { target: 'apps/api', status: 'unavailable', detail: String(error) };
  }
}
