import { useState } from 'react';
import { delegateAgentTask } from '@/services/apiClient';
import { AutonomyLevel } from '@/types';

export function useAgentTask() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const startTask = async (goal: string, targetCapability: string, autonomyLevel: AutonomyLevel) => {
    setLoading(true);
    try {
      const res = await delegateAgentTask({
        goal,
        target_capability: targetCapability,
        autonomy_level: autonomyLevel,
        author: 'WebOperator',
      });
      setTaskId(res.task_id);
    } finally {
      setLoading(false);
    }
  };

  return { taskId, loading, startTask };
}
