import React from 'react';
import { cn } from '@/utils/cn';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({ className, children, ...props }) => (
  <div className={cn('bg-slate-800 border border-slate-700 rounded-xl p-5', className)} {...props}>
    {children}
  </div>
);
