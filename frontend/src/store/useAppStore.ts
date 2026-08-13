import { useState } from 'react';
import { SystemHealth } from '@/types';

export function useAppStore() {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [activeTaskId, setActiveTaskId] = useState<string | null>(null);

  return { health, setHealth, activeTaskId, setActiveTaskId };
}
