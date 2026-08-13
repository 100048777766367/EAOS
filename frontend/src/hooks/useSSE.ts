import { useEffect, useState } from 'react';
import { AgentStreamStep } from '@/types';

export function useSSE(taskId: string | null): AgentStreamStep[] {
  const [steps, setSteps] = useState<AgentStreamStep[]>([]);

  useEffect(() => {
    if (!taskId) return;
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const es = new EventSource(`${apiBase}/agent/stream/${taskId}`);

    es.onmessage = (e) => {
      try {
        const step: AgentStreamStep = JSON.parse(e.data);
        setSteps((prev) => [...prev, step]);
        if (step.agent === 'COMPLETED') es.close();
      } catch (err) {
        console.error('Lỗi parse SSE step:', err);
      }
    };

    return () => es.close();
  }, [taskId]);

  return steps;
}
