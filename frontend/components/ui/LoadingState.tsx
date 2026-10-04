import React from "react";
import { cn } from "@/lib/utils";

export interface LoadingStateProps {
  message?: string;
  className?: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = "Gathering verified vocational insights...",
  className,
}) => {
  return (
    <div className={cn("flex flex-col items-center justify-center p-8 text-center", className)}>
      <div className="relative flex items-center justify-center w-12 h-12 mb-4">
        <div className="absolute w-12 h-12 border-4 border-[#2A9D8F]/20 rounded-full animate-ping" />
        <div className="w-10 h-10 border-3 border-[#2A9D8F] border-t-transparent rounded-full animate-spin" />
      </div>
      <p className="text-sm font-medium text-[#243047]">{message}</p>
      <p className="text-xs text-[#64748B] mt-1">Connecting learner aspirations with family security</p>
    </div>
  );
};
