import React from 'react';
import { cn } from '@/utils/cn';

export const Badge: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className }) => (
  <span className={cn('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-500/10 text-cyan-400 border border-cyan-500/20', className)}>
    {children}
  </span>
);
