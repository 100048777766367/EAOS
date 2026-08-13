import React from "react";

export interface EAOSButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger";
  children: React.ReactNode;
}

export const EAOSButton: React.FC<EAOSButtonProps> = ({
  variant = "primary",
  children,
  className = "",
  ...props
}) => {
  const baseStyle = "px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2";
  const variants = {
    primary: "bg-cyan-500 hover:bg-cyan-400 text-white focus:ring-cyan-300",
    secondary: "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 focus:ring-slate-500",
    danger: "bg-red-500 hover:bg-red-400 text-white focus:ring-red-300"
  };

  return (
    <button className={`${baseStyle} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
};
