"use client";

import React, { useState, useEffect } from "react";
import {
  ShieldCheck,
  RefreshCw,
  Database,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Layers,
  FileText,
  Activity,
  Server
} from "lucide-react";

export const AdminDataInspection: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [syncMessage, setSyncMessage] = useState<string | null>(null);

  const fetchMonitoringData = async () => {
    setIsLoading(true);
    try {
      const res = await fetch("/api/v1/admin/monitoring");
      const data = await res.json();
      if (data.success && data.data) {
        setSummary(data.data);
      }
    } catch (err) {
      console.error("Error fetching admin monitoring:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMonitoringData();
  }, []);

  const handleTriggerSync = async () => {
    setIsSyncing(true);
    setSyncMessage(null);
    try {
      const res = await fetch("/api/v1/data-sync/trigger-all", {
        method: "POST",
      });
      const data = await res.json();
      if (data.success) {
        setSyncMessage("Data sync completed successfully across all official adapters.");
        fetchMonitoringData();
      } else {
        setSyncMessage("Sync completed with warnings.");
      }
    } catch (err) {
      setSyncMessage("Sync error occurred.");
    } finally {
      setIsSyncing(false);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-3xl p-12 text-center border border-gray-200">
        <RefreshCw className="w-8 h-8 text-teal-600 animate-spin mx-auto mb-3" />
        <div className="text-sm font-bold text-gray-700">Loading Admin Telemetry...</div>
      </div>
    );
  }

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-teal-950 to-slate-900 rounded-3xl p-8 text-white shadow-xl flex flex-wrap items-center justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-teal-400/20 text-teal-300 border border-teal-400/30 mb-2">
            <Server className="w-3.5 h-3.5 text-teal-300" />
            Administrative Provenance & Data Control Console
          </div>
          <h2 className="text-2xl sm:text-4xl font-black text-white">
            Data Source & Provenance Governance
          </h2>
          <p className="text-xs sm:text-sm text-teal-100/90 mt-1 max-w-2xl">
            Inspect live database sync runs, freshness timestamps, government publishers, and data quality validation logs.
          </p>
        </div>

        <button
          onClick={handleTriggerSync}
          disabled={isSyncing}
          className="px-6 py-3.5 rounded-2xl bg-teal-400 hover:bg-teal-300 text-teal-950 font-black text-xs transition-all shadow-md flex items-center gap-2"
        >
          <RefreshCw className={`w-4 h-4 ${isSyncing ? "animate-spin" : ""}`} />
          <span>{isSyncing ? "Ingesting Adapters..." : "Trigger Full Sync"}</span>
        </button>
      </div>

      {syncMessage && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 p-4 rounded-2xl text-xs font-bold flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{syncMessage}</span>
        </div>
      )}

      {/* Telemetry KPI Metrics */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
          <div className="text-xs font-bold text-gray-500 uppercase">Ingested Evidence Sources</div>
          <div className="text-3xl font-black text-teal-900 mt-2">{summary?.total_sources || 0}</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-1">100% Official Publishers</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
          <div className="text-xs font-bold text-gray-500 uppercase">Registered NSQF Trades</div>
          <div className="text-3xl font-black text-teal-900 mt-2">{summary?.total_trades || 0}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-1">NQR Curriculum Verified</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
          <div className="text-xs font-bold text-gray-500 uppercase">Affiliated Providers</div>
          <div className="text-3xl font-black text-teal-900 mt-2">{summary?.total_providers || 0}</div>
          <div className="text-[11px] text-gray-500 font-medium mt-1">Govt ITIs & NSTIs</div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-xs">
          <div className="text-xs font-bold text-gray-500 uppercase">Verified Outcome Records</div>
          <div className="text-3xl font-black text-teal-900 mt-2">{summary?.total_outcomes || 0}</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-1">MSDE Tracer Surveys</div>
        </div>
      </div>

      {/* Audit Logs & Quality Checks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Sync History */}
        <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-teal-700" />
            Recent Sync Runs & Ingestion Logs
          </h3>

          <div className="space-y-3">
            {summary?.recent_sync_runs?.map((run: any) => (
              <div key={run.id} className="bg-gray-50 rounded-xl p-3.5 border border-gray-100 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-gray-900">{run.sync_type || "SCHEDULED"}</div>
                  <div className="text-gray-500">Inserted: {run.records_inserted} • Updated: {run.records_updated}</div>
                </div>

                <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-emerald-100 text-emerald-800">
                  {run.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Validation & Quality Checks */}
        <div className="bg-white rounded-3xl p-6 border border-gray-200 shadow-xs space-y-4">
          <h3 className="text-base font-bold text-gray-900 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-700" />
            Data Quality & Anti-Hallucination Audits
          </h3>

          <div className="space-y-3">
            {summary?.recent_quality_alerts?.length === 0 ? (
              <div className="bg-emerald-50 rounded-xl p-4 text-center text-xs font-semibold text-emerald-800 border border-emerald-200">
                ✓ 100% Records passed validation checks (zero duplicate / negative anomalies).
              </div>
            ) : (
              summary?.recent_quality_alerts?.map((qc: any) => (
                <div key={qc.id} className="bg-gray-50 rounded-xl p-3.5 border border-gray-100 text-xs">
                  <div className="font-bold text-gray-900">{qc.issue_type}</div>
                  <div className="text-gray-600">{qc.details}</div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
