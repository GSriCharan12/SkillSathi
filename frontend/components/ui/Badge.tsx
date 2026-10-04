import React from "react";
import { cn } from "@/lib/utils";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "teal" | "emerald" | "coral" | "golden" | "lavender" | "outline";
  size?: "sm" | "md";
}

export const Badge: React.FC<BadgeProps> = ({
  className,
  variant = "default",
  size = "md",
  children,
  ...props
}) => {
  const sizeStyles = {
    sm: "text-[11px] px-2 py-0.5 font-medium",
    md: "text-xs px-2.5 py-1 font-semibold",
  };

  const variantStyles = {
    default: "bg-[#14213D]/10 text-[#14213D] border border-[#14213D]/15",
    teal: "bg-[#E8F5F3] text-[#2A9D8F] border border-[#2A9D8F]/25",
    emerald: "bg-[#EBF8F2] text-[#2D6A4F] border border-[#52B788]/30",
    coral: "bg-[#FDF0F0] text-[#D05353] border border-[#F28482]/30",
    golden: "bg-[#FEF9EB] text-[#B8860B] border border-[#F6C85F]/40",
    lavender: "bg-[#F3F0FC] text-[#5E50A1] border border-[#DCD6F7]/60",
    outline: "border border-neutral-300 text-[#243047] bg-white/70",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full transition-colors",
        sizeStyles[size],
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
};
