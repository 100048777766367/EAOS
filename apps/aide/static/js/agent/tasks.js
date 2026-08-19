export async function submitGatewayTask(command, targetAgent = 'planner') {
  const response = await fetch('/interactions/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command, target_agent: targetAgent }),
  });
  return response.json();
}
