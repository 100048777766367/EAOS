import React from 'react';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';

export const KnowledgeFeature: React.FC = () => (
  <Card>
    <div className="flex justify-between items-center mb-4">
      <h2 className="text-lg font-semibold">📚 Topology Tri Thức Doanh Nghiệp</h2>
      <Badge>Active Nodes: 42</Badge>
    </div>
    <p className="text-sm text-slate-400">Bản đồ liên kết ngữ nghĩa giữa các tri thức EAOS.</p>
  </Card>
);
