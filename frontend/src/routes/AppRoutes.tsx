import React from 'react';
import { ControlRoomFeature } from '@/features/control-room/ControlRoomFeature';
import { KnowledgeFeature } from '@/features/knowledge/KnowledgeFeature';

export const AppRoutes: React.FC = () => (
  <div className="space-y-6">
    <ControlRoomFeature />
    <KnowledgeFeature />
  </div>
);
