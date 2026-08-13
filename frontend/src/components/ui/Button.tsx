import React from 'react';
import { cn } from '@/utils/cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', className, children, ...props }) => {
  const variants = {
    primary: 'bg-cyan-600 hover:bg-cyan-500 text-white',
    secondary: 'bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700',
    danger: 'bg-red-600 hover:bg-red-500 text-white',
  };

  return (
    <button className={cn('px-4 py-2 rounded-lg font-medium transition-colors text-sm', variants[variant], className)} {...props}>
      {children}
    </button>
  );
};
