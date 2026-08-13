import React from 'react';
import { Badge } from '@/components/ui/Badge';

export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="min-h-screen bg-slate-900 text-slate-100 p-6">
    <div className="max-w-7xl mx-auto space-y-6">
      <header className="flex justify-between items-center border-b border-slate-700 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-cyan-400">EAOS Cybernetic Control Room</h1>
          <p className="text-xs text-slate-400">Feature-Based Next.js Operator Interface</p>
        </div>
        <Badge>● System Active (Zero-Ops)</Badge>
      </header>
      <main>{children}</main>
    </div>
  </div>
);
