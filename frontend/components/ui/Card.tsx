import React from "react";
import { cn } from "@/lib/utils";

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "glass" | "solid" | "subtle" | "bordered";
  interactive?: boolean;
}

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = "glass", interactive = false, children, ...props }, ref) => {
    const variantStyles = {
      glass: "glass-card",
      solid: "bg-white border border-[#14213D]/8 shadow-sm",
      subtle: "bg-[#FFFDF7]/60 border border-[#14213D]/5",
      bordered: "bg-transparent border-2 border-[#14213D]/10",
    };

    const interactiveStyles = interactive
      ? "hover:-translate-y-0.5 hover:shadow-md transition-all duration-200 cursor-pointer"
      : "";

    return (
      <div
        ref={ref}
        className={cn("rounded-2xl p-5 md:p-6", variantStyles[variant], interactiveStyles, className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";
