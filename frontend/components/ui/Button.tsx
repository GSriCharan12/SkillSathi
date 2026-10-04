"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "coral" | "emerald";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed select-none active:scale-[0.98]";

    const sizeStyles = {
      sm: "text-xs px-3 py-1.5 gap-1.5",
      md: "text-sm px-4 py-2.5 gap-2",
      lg: "text-base px-6 py-3.5 gap-2.5",
    };

    const variantStyles = {
      primary:
        "bg-[#14213D] text-[#FFFDF7] hover:bg-[#1E293B] shadow-sm hover:shadow-md focus-visible:ring-[#14213D]",
      secondary:
        "bg-[#2A9D8F] text-white hover:bg-[#238276] shadow-sm hover:shadow focus-visible:ring-[#2A9D8F]",
      emerald:
        "bg-[#52B788] text-white hover:bg-[#40916C] shadow-sm focus-visible:ring-[#52B788]",
      coral:
        "bg-[#F28482] text-white hover:bg-[#E06D6B] shadow-sm focus-visible:ring-[#F28482]",
      outline:
        "border border-[#14213D]/20 bg-white/60 hover:bg-white text-[#243047] hover:border-[#14213D]/40 focus-visible:ring-[#2A9D8F]",
      ghost:
        "text-[#243047] hover:bg-[#14213D]/5 hover:text-[#14213D] focus-visible:ring-[#2A9D8F]",
    };

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, sizeStyles[size], variantStyles[variant], className)}
        {...props}
      >
        {isLoading ? (
          <span className="inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
        ) : (
          leftIcon
        )}
        <span>{children}</span>
        {!isLoading && rightIcon}
      </button>
    );
  }
);

Button.displayName = "Button";
