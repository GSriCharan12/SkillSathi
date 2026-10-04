"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, leftIcon, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);

    return (
      <div className="w-full space-y-1.5">
        {label && (
          <label htmlFor={inputId} className="block text-xs font-semibold text-[#243047]">
            {label}
          </label>
        )}
        <div className="relative flex items-center">
          {leftIcon && (
            <div className="absolute left-3.5 pointer-events-none text-neutral-400">
              {leftIcon}
            </div>
          )}
          <input
            id={inputId}
            ref={ref}
            className={cn(
              "w-full rounded-xl border bg-white/80 px-3.5 py-2.5 text-sm text-[#243047] placeholder:text-neutral-400 focus:bg-white focus:outline-none focus:ring-2 transition-all",
              leftIcon && "pl-10",
              error
                ? "border-[#F28482] focus:ring-[#F28482]/20"
                : "border-[#14213D]/12 focus:border-[#2A9D8F] focus:ring-[#2A9D8F]/15",
              className
            )}
            {...props}
          />
        </div>
        {error && <p className="text-xs text-[#D05353]">{error}</p>}
        {hint && !error && <p className="text-xs text-neutral-500">{hint}</p>}
      </div>
    );
  }
);

Input.displayName = "Input";
