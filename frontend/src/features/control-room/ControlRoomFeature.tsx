import React, { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { useAgentTask } from './useAgentTask';
import { useSSE } from '@/hooks/useSSE';
import { approveAgentTask } from '@/services/apiClient';

export const ControlRoomFeature: React.FC = () => {
  const [goal, setGoal] = useState('');
  const [capability, setCapability] = useState('packages/knowledge');
  const [autonomy, setAutonomy] = useState<1 | 2 | 3>(2);
  const { taskId, loading, startTask } = useAgentTask();
  const streamSteps = useSSE(taskId);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (goal) startTask(goal, capability, autonomy);
  };

  return (
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <Card className="lg:col-span-4 space-y-4">
        <h2 class="text-lg font-semibold border-b border-slate-700 pb-2">🎯 Giao Việc Cho Agents</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1">Mục tiêu (Goal)</label>
            <textarea value={goal} onChange={(e) => setGoal(e.target.value)} rows={4} className="w-full bg-slate-900 border border-slate-700 rounded-lg p-2 text-sm text-slate-200 outline-none" placeholder="Nhập mục tiêu..." />
          </div>
          <Button type="submit" disabled={loading} className="w-full">
            {loading ? 'Đang gửi...' : '🚀 Thực thi Task'}
          </Button>
        </form>
      </Card>

      <Card className="lg:col-span-8 flex flex-col h-[500px]">
        <h2 className="text-lg font-semibold border-b border-slate-700 pb-2 mb-3">⚡ Live Agent Stream ({taskId || 'Waiting'})</h2>
        <div className="flex-1 bg-slate-950 rounded-lg p-4 font-mono text-xs overflow-y-auto space-y-2">
          {streamSteps.map((step, idx) => (
            <div key={idx} className="text-slate-200">
              <span className="text-cyan-400">[{step.agent}]</span> {step.message}
              {step.agent === 'HITL_REQUIRED' && (
                <div className="mt-2 flex space-x-2">
                  <Button variant="danger" onClick={() => taskId && approveAgentTask(taskId, 'REJECTED')}>Từ chối</Button>
                  <Button variant="primary" onClick={() => taskId && approveAgentTask(taskId, 'APPROVED')}>Chấp thuận</Button>
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
