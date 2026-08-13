export type AutonomyLevel = 1 | 2 | 3;

export interface AgentTaskRequest {
  goal: string;
  target_capability: string;
  autonomy_level: AutonomyLevel;
  author: string;
}

export interface AgentTaskResponse {
  task_id: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  message: string;
}

export interface AgentStreamStep {
  time: string;
  agent: string;
  message: string;
}

export interface SystemHealth {
  status: string;
  version: str;
  governance: string;
  doctor_score: number;
}
