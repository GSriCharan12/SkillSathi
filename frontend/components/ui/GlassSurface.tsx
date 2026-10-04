import React from "react";
import { cn } from "@/lib/utils";

export interface GlassSurfaceProps extends React.HTMLAttributes<HTMLDivElement> {
  level?: "hero" | "panel" | "subtle";
}

export const GlassSurface = React.forwardRef<HTMLDivElement, GlassSurfaceProps>(
  ({ className, level = "panel", children, ...props }, ref) => {
    const levelStyles = {
      hero: "glass-panel rounded-3xl p-6 md:p-8",
      panel: "glass-card rounded-2xl p-5 md:p-6",
      subtle: "glass-pill rounded-xl p-3 md:p-4",
    };

    return (
      <div ref={ref} className={cn(levelStyles[level], className)} {...props}>
        {children}
      </div>
    );
  }
);

GlassSurface.displayName = "GlassSurface";
