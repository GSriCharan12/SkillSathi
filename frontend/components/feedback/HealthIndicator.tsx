"use client";

import React, { useEffect, useState } from "react";
import { Activity, Database, CheckCircle2, AlertCircle, RefreshCw } from "lucide-react";
import { apiClient } from "@/lib/api-client";
import { AppHealth, DatabaseHealth } from "@/types";

export const HealthIndicator: React.FC = () => {
  const [appHealth, setAppHealth] = useState<AppHealth | null>(null);
  const [dbHealth, setDbHealth] = useState<DatabaseHealth | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchHealth = async () => {
    setLoading(true);
    const [appRes, dbRes] = await Promise.all([
      apiClient.getHealth(),
      apiClient.getDatabaseHealth(),
    ]);

    if (appRes.success && appRes.data) {
      setAppHealth(appRes.data);
    }
    if (dbRes.success && dbRes.data) {
      setDbHealth(dbRes.data);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchHealth();
  }, []);

  const isBackendOnline = appHealth !== null && appHealth.status === "healthy";

  return (
    <div className="flex items-center gap-2 text-xs">
      <div
        className={`flex items-center gap-1.5 px-3 py-1 rounded-full border transition-all ${
          isBackendOnline
            ? "bg-[#EBF8F2] border-[#52B788]/30 text-[#2D6A4F]"
            : "bg-[#FEF9EB] border-[#F6C85F]/50 text-[#9A6B00]"
        }`}
        title={`API Health: ${appHealth?.status || "Connecting..."}`}
      >
        <span
          className={`w-2 h-2 rounded-full ${
            isBackendOnline ? "bg-[#52B788] animate-pulse" : "bg-[#F6C85F]"
          }`}
        />
        <span className="font-semibold">
          {isBackendOnline ? "Backend Live" : "API Connecting..."}
        </span>
        {appHealth && (
          <span className="text-[10px] opacity-75 font-mono">
            v{appHealth.version}
          </span>
        )}
      </div>

      <button
        onClick={fetchHealth}
        disabled={loading}
        className="p-1 rounded-full hover:bg-[#14213D]/5 text-[#64748B] transition-colors"
        title="Refresh Status"
      >
        <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
      </button>
    </div>
  );
};
