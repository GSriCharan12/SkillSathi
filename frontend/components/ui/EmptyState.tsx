import React from "react";
import { cn } from "@/lib/utils";
import { Button } from "./Button";

export interface EmptyStateProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
  actionLabel?: string;
  onAction?: () => void;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title,
  description,
  icon,
  actionLabel,
  onAction,
  className,
}) => {
  return (
    <div className={cn("flex flex-col items-center justify-center p-8 text-center glass-card rounded-2xl", className)}>
      {icon && (
        <div className="p-3 mb-4 rounded-2xl bg-[#2A9D8F]/10 text-[#2A9D8F]">
          {icon}
        </div>
      )}
      <h3 className="text-base font-semibold text-[#14213D]">{title}</h3>
      <p className="max-w-sm text-xs md:text-sm text-[#64748B] mt-1.5 mb-5">{description}</p>
      {actionLabel && onAction && (
        <Button variant="secondary" size="sm" onClick={onAction}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};
