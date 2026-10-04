import React from "react";
import { cn } from "@/lib/utils";

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value: number; // 0 to 100
  max?: number;
  variant?: "teal" | "emerald" | "golden" | "coral";
  showLabel?: boolean;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  max = 100,
  variant = "teal",
  showLabel = false,
  className,
  ...props
}) => {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  const variantStyles = {
    teal: "bg-[#2A9D8F]",
    emerald: "bg-[#52B788]",
    golden: "bg-[#F6C85F]",
    coral: "bg-[#F28482]",
  };

  return (
    <div className={cn("w-full space-y-1.5", className)} {...props}>
      {showLabel && (
        <div className="flex justify-between text-xs text-[#243047] font-medium">
          <span>Family Alignment</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-[#14213D]/10">
        <div
          className={cn("h-full transition-all duration-500 ease-out rounded-full", variantStyles[variant])}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
