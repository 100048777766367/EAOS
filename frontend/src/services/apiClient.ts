import { AgentTaskRequest, AgentTaskResponse, SystemHealth } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchSystemHealth(): Promise<SystemHealth> {
  const res = await fetch(`${API_BASE_URL}/health`);
  if (!res.ok) throw new Error('Không thể nạp trạng thái hệ thống');
  return res.json();
}

export async function delegateAgentTask(req: AgentTaskRequest): Promise<AgentTaskResponse> {
  const res = await fetch(`${API_BASE_URL}/agent/delegate-task`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error('Thất bại khi giao nhiệm vụ cho Agent');
  return res.json();
}

export async function approveAgentTask(taskId: string, decision: 'APPROVED' | 'REJECTED'): Promise<void> {
  await fetch(`${API_BASE_URL}/agent/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: taskId, decision, reason: 'Phê duyệt từ Web UI' }),
  });
}
