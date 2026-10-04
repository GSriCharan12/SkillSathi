"use client";

import React, { useState, useEffect } from "react";
import {
  ProgrammeAnalyticsResponse,
  AdminMonitoringSummary,
} from "@/types";
import { apiClient } from "@/lib/api-client";
import {
  BarChart3,
  TrendingUp,
  MapPin,
  ShieldCheck,
  AlertCircle,
  Download,
  Filter,
  RefreshCw,
  Users,
  Compass,
  FileSpreadsheet,
  Layers,
  ChevronRight,
  Database,
  Building,
  CheckCircle2,
  AlertTriangle,
  Info,
  Calendar,
  Sparkles,
  ArrowUpRight,
  HelpCircle,
} from "lucide-react";

export function AdminProgrammeDashboard() {
  const [data, setData] = useState<ProgrammeAnalyticsResponse | null>(null);
  const [syncSummary, setSyncSummary] = useState<AdminMonitoringSummary | null>(null);
  const [selectedTab, setSelectedTab] = useState<
    "overview" | "concerns" | "resistance" | "geographic" | "trades" | "funnel" | "sync"
  >("overview");

  // Filters
  const [selectedDistrict, setSelectedDistrict] = useState<string>("");
  const [selectedDays, setSelectedDays] = useState<number>(30);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  const loadAnalytics = async () => {
    setIsRefreshing(true);
    try {
      const [analyticsRes, syncRes] = await Promise.all([
        apiClient.getProgrammeAnalytics({
          district: selectedDistrict || undefined,
          days: selectedDays,
        }),
        apiClient.getAdminMonitoring(),
      ]);

      if (analyticsRes.success && analyticsRes.data) {
        setData(analyticsRes.data);
      }
      if (syncRes.success && syncRes.data) {
        setSyncSummary(syncRes.data);
      }
    } catch (err) {
      console.error("Error loading programme analytics:", err);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [selectedDistrict, selectedDays]);

  const handleExportCsv = () => {
    window.open(apiClient.getExportCsvUrl(), "_blank");
  };

  if (isLoading && !data) {
    return (
      <div className="p-16 text-center bg-white rounded-3xl border border-stone-200 shadow-sm animate-pulse space-y-4">
        <BarChart3 className="w-12 h-12 text-teal-600 mx-auto animate-bounce" />
        <p className="text-sm font-semibold text-stone-700">
          Aggregating Programme Telemetry & Resistance Analytics...
        </p>
      </div>
    );
  }

  const overview = data?.overview;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* 1. Executive Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-navy-900 to-slate-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-1 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 text-teal-300 text-xs font-semibold border border-teal-400/30">
                <ShieldCheck className="w-3.5 h-3.5" />
                National Vocational Policy Telemetry & Analytics
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold font-outfit text-white">
                Programme Resistance & Decision Analytics
              </h1>
              <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                Analyzing where and why family resistance to vocational education occurs using verified platform signals.
              </p>
            </div>

            {/* Filter Controls & Export */}
            <div className="flex flex-wrap items-center gap-2.5">
              {/* District Filter */}
              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                className="bg-white/10 text-white border border-white/20 rounded-xl px-3 py-2 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-teal-400"
              >
                <option value="" className="text-stone-900">All Districts</option>
                <option value="Warangal" className="text-stone-900">Warangal District</option>
                <option value="Medchal" className="text-stone-900">Medchal District</option>
                <option value="Hyderabad" className="text-stone-900">Hyderabad District</option>
              </select>

              {/* Time Window */}
              <select
                value={selectedDays}
                onChange={(e) => setSelectedDays(Number(e.target.value))}
                className="bg-white/10 text-white border border-white/20 rounded-xl px-3 py-2 text-xs font-semibold focus:outline-none focus:ring-2 focus:ring-teal-400"
              >
                <option value={7} className="text-stone-900">Last 7 Days</option>
                <option value={30} className="text-stone-900">Last 30 Days</option>
                <option value={90} className="text-stone-900">Last 90 Days</option>
                <option value={365} className="text-stone-900">Last 1 Year</option>
              </select>

              {/* Refresh Button */}
              <button
                type="button"
                onClick={loadAnalytics}
                disabled={isRefreshing}
                className="p-2.5 bg-white/10 hover:bg-white/20 rounded-xl border border-white/20 text-white transition-colors"
                title="Refresh Telemetry"
              >
                <RefreshCw className={`w-4 h-4 ${isRefreshing ? "animate-spin" : ""}`} />
              </button>

              {/* Download CSV */}
              <button
                type="button"
                onClick={handleExportCsv}
                className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition-all shadow-md flex items-center gap-1.5"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Export Anonymized CSV</span>
              </button>
            </div>
          </div>

          {/* KPI Dashboard Metrics Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3 pt-2">
            {[
              { label: "Families Counselled", val: overview?.families_counselled ?? 0, highlight: "text-white" },
              { label: "Active Sessions", val: overview?.active_sessions ?? 0, highlight: "text-teal-400" },
              { label: "High Resistance", val: overview?.high_concern_cases ?? 0, highlight: "text-rose-400" },
              { label: "Counsellor Escalations", val: overview?.counsellor_escalations ?? 0, highlight: "text-amber-400" },
              { label: "Resolved Sessions", val: overview?.resolved_sessions ?? 0, highlight: "text-emerald-400" },
              { label: "Mean Family Alignment", val: `${overview?.average_family_alignment ?? 80}%`, highlight: "text-teal-300" },
            ].map((metric, i) => (
              <div
                key={i}
                className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm space-y-1"
              >
                <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 truncate">
                  {metric.label}
                </div>
                <div className={`text-2xl font-black ${metric.highlight}`}>
                  {metric.val}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 2. Navigation Tabs */}
      <div className="flex border-b border-stone-200 gap-6 text-sm font-semibold text-stone-500 overflow-x-auto no-scrollbar">
        {[
          { id: "overview", label: "Executive Overview", icon: BarChart3 },
          { id: "concerns", label: "Concern Distribution", icon: AlertCircle },
          { id: "resistance", label: "Family Resistance Index", icon: ShieldCheck },
          { id: "geographic", label: "Geographic Hotspots", icon: MapPin },
          { id: "trades", label: "Trade Telemetry", icon: Compass },
          { id: "funnel", label: "Counselling Funnel", icon: TrendingUp },
          { id: "sync", label: "Data Source Provenance", icon: Database },
        ].map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id as any)}
              className={`pb-4 flex items-center gap-2 border-b-2 transition-all whitespace-nowrap ${
                selectedTab === tab.id
                  ? "border-teal-700 text-teal-900 font-bold"
                  : "border-transparent hover:text-stone-900"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>

      {/* 3. Dynamic Tab Content */}

      {/* TAB 1: EXECUTIVE OVERVIEW */}
      {selectedTab === "overview" && data && (
        <div className="space-y-6">
          {/* Transparent Methodology Disclaimer */}
          <div className="p-4 bg-teal-50/70 rounded-2xl border border-teal-200 flex items-start gap-3 text-xs text-teal-950">
            <Info className="w-5 h-5 text-teal-700 shrink-0 mt-0.5" />
            <div>
              <h4 className="font-bold text-sm">Transparent Resistance Measurement Principle</h4>
              <p className="mt-1 text-stone-700 leading-relaxed">
                {data.resistance_methodology}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Top Concerns Summary (Left 6 cols) */}
            <div className="lg:col-span-6 bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-stone-100">
                <h3 className="text-sm font-bold text-stone-900">
                  Top Parental Resistance Categories
                </h3>
                <span className="text-xs text-stone-400">Database Ground Truth</span>
              </div>

              <div className="space-y-3">
                {data.concerns_breakdown.slice(0, 5).map((c) => (
                  <div key={c.category} className="space-y-1.5">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-stone-800">
                        {c.category.replace(/_/g, " ")}
                      </span>
                      <span className="font-semibold text-teal-800">
                        {c.count} concerns ({c.percentage}%)
                      </span>
                    </div>
                    <div className="w-full bg-stone-100 rounded-full h-2.5 overflow-hidden">
                      <div
                        className="bg-teal-600 h-full rounded-full transition-all duration-500"
                        style={{ width: `${Math.max(5, c.percentage)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Geographic Distribution Preview (Right 6 cols) */}
            <div className="lg:col-span-6 bg-white rounded-3xl border border-stone-200 p-6 shadow-sm space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-stone-100">
                <h3 className="text-sm font-bold text-stone-900">
                  District Resistance Concentration
                </h3>
                <span className="text-xs text-stone-400">Hotspot Index</span>
              </div>

              <div className="space-y-3">
                {data.geographic_hotspots.map((h, i) => (
                  <div
                    key={i}
                    className="p-3.5 bg-stone-50 rounded-2xl border border-stone-200 flex items-center justify-between gap-4"
                  >
                    <div>
                      <div className="text-xs font-bold text-stone-900 flex items-center gap-1.5">
                        <MapPin className="w-3.5 h-3.5 text-teal-600" />
                        <span>{h.district}, {h.state}</span>
                      </div>
                      <div className="text-[11px] text-stone-500 mt-0.5">
                        Primary: <strong>{h.primary_concern_category}</strong> • {h.total_families} Families
                      </div>
                    </div>

                    <div className="text-right">
                      <div className="text-xs font-black text-rose-600">
                        {h.avg_resistance_score}/100
                      </div>
                      <div className="text-[10px] text-stone-400">Resistance Index</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: CONCERN DISTRIBUTION ANALYTICS */}
      {selectedTab === "concerns" && data && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                Vocational Resistance Category Analysis
              </h3>
              <p className="text-xs text-stone-500">
                Aggregated distribution across all 8 canonical parental concern categories
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.concerns_breakdown.map((c) => (
              <div
                key={c.category}
                className="p-5 bg-stone-50 rounded-2xl border border-stone-200 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-teal-100 text-teal-900">
                    {c.category.replace(/_/g, " ")}
                  </span>
                  <span className="text-xs font-semibold text-stone-500">
                    Mean Severity: <strong>{c.avg_severity}/10</strong>
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-2 pt-1 text-center">
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400 uppercase">Reported</div>
                    <div className="text-sm font-bold text-stone-900">{c.count}</div>
                  </div>
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400 uppercase">Share</div>
                    <div className="text-sm font-bold text-teal-700">{c.percentage}%</div>
                  </div>
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400 uppercase">Unresolved</div>
                    <div className="text-sm font-bold text-rose-600">{c.unresolved_count}</div>
                  </div>
                </div>

                {c.top_districts.length > 0 && (
                  <div className="text-[11px] text-stone-600">
                    <strong>Concentrated in:</strong> {c.top_districts.join(", ")}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: FAMILY RESISTANCE INDEX TABLE */}
      {selectedTab === "resistance" && data && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                Family Concern & Resistance Index Roster
              </h3>
              <p className="text-xs text-stone-500">
                Anonymized family friction telemetry based strictly on platform interaction signals
              </p>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-stone-50 border-y border-stone-200 text-stone-500 font-bold uppercase tracking-wider text-[10px]">
                <tr>
                  <th className="py-3 px-4">Family Identifier</th>
                  <th className="py-3 px-4">District / State</th>
                  <th className="py-3 px-4">Resistance Score</th>
                  <th className="py-3 px-4">Level</th>
                  <th className="py-3 px-4">Unresolved Concerns</th>
                  <th className="py-3 px-4">Decision State</th>
                  <th className="py-3 px-4">Primary Concern</th>
                  <th className="py-3 px-4">Escalation</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-stone-100">
                {data.resistance_index.map((row) => (
                  <tr key={row.family_id} className="hover:bg-stone-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-bold text-stone-900">{row.family_code}</td>
                    <td className="py-3.5 px-4 text-stone-600">{row.district}, {row.state}</td>
                    <td className="py-3.5 px-4 font-bold text-stone-900">{row.concern_score}</td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          row.resistance_level === "ACUTE" || row.resistance_level === "HIGH"
                            ? "bg-rose-100 text-rose-800"
                            : row.resistance_level === "MODERATE"
                            ? "bg-amber-100 text-amber-800"
                            : "bg-emerald-100 text-emerald-800"
                        }`}
                      >
                        {row.resistance_level}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 font-semibold text-stone-700">{row.unresolved_concerns}</td>
                    <td className="py-3.5 px-4 font-medium text-stone-800">{row.decision_state}</td>
                    <td className="py-3.5 px-4 text-stone-600">{row.primary_concern}</td>
                    <td className="py-3.5 px-4">
                      {row.counsellor_requested ? (
                        <span className="text-amber-700 font-bold">Yes (Active)</span>
                      ) : (
                        <span className="text-stone-400">No</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB 4: GEOGRAPHIC HOTSPOTS */}
      {selectedTab === "geographic" && data && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                District-Level Resistance Concentrations
              </h3>
              <p className="text-xs text-stone-500">
                Targeted intervention zones for vocational outreach schemes
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {data.geographic_hotspots.map((h, i) => (
              <div
                key={i}
                className="p-5 bg-stone-50 rounded-2xl border border-stone-200 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-stone-900 flex items-center gap-1.5">
                    <MapPin className="w-4 h-4 text-teal-700" />
                    <span>{h.district}</span>
                  </h4>
                  <span className="text-xs font-bold text-stone-500">{h.state}</span>
                </div>

                <div className="space-y-1 text-xs text-stone-700">
                  <div className="flex justify-between py-1 border-b border-stone-200/60">
                    <span className="text-stone-500">Resistance Index:</span>
                    <span className="font-bold text-rose-600">{h.avg_resistance_score}/100</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-stone-200/60">
                    <span className="text-stone-500">Primary Friction Point:</span>
                    <span className="font-bold text-stone-900">{h.primary_concern_category}</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-stone-200/60">
                    <span className="text-stone-500">Escalation Rate:</span>
                    <span className="font-semibold text-amber-700">{h.escalation_rate}%</span>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-stone-500">Top Trade Explored:</span>
                    <span className="font-semibold text-teal-800">{h.top_explored_trade}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: TRADE TELEMETRY */}
      {selectedTab === "trades" && data && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                Trade Exploration & Comparison Volume
              </h3>
              <p className="text-xs text-stone-500">
                Telemetry identifying high-interest pathways and trade-specific concerns
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.trade_analytics.map((t) => (
              <div
                key={t.trade_id}
                className="p-5 bg-stone-50 rounded-2xl border border-stone-200 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-[10px] font-bold text-teal-800 uppercase tracking-wider">
                      {t.sector} (NSQF L{t.nsqf_level})
                    </span>
                    <h4 className="text-sm font-bold text-stone-900">{t.trade_title}</h4>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 text-center text-xs">
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400">Explorations</div>
                    <div className="text-sm font-bold text-stone-900">{t.exploration_count}</div>
                  </div>
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400">Comparisons</div>
                    <div className="text-sm font-bold text-teal-700">{t.comparison_count}</div>
                  </div>
                  <div className="p-2 bg-white rounded-xl border border-stone-200">
                    <div className="text-[10px] text-stone-400">Escalations</div>
                    <div className="text-sm font-bold text-amber-700">{t.escalations_count}</div>
                  </div>
                </div>

                <div className="text-[11px] text-stone-600 flex justify-between">
                  <span>Primary Concern: <strong>{t.top_concern_category}</strong></span>
                  <span>Mean Alignment: <strong>{t.average_alignment}%</strong></span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 6: COUNSELLING FUNNEL */}
      {selectedTab === "funnel" && data && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                End-to-End Family Decision Support Funnel
              </h3>
              <p className="text-xs text-stone-500">
                Conversion and friction drop-off rates across actual platform journey stages
              </p>
            </div>
          </div>

          <div className="space-y-4 max-w-2xl mx-auto">
            {data.counselling_funnel.map((stage, idx) => (
              <div key={stage.stage_key} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-bold text-stone-900">
                    Step {idx + 1}: {stage.stage_label}
                  </span>
                  <span className="font-semibold text-teal-900">
                    {stage.count} families ({stage.conversion_pct}%)
                  </span>
                </div>
                <div className="w-full bg-stone-100 rounded-full h-3 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-teal-700 to-emerald-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${Math.max(8, stage.conversion_pct)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 7: DATA SOURCE PROVENANCE & SYNC STATUS */}
      {selectedTab === "sync" && syncSummary && (
        <div className="bg-white rounded-3xl border border-stone-200 p-6 sm:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-stone-100 pb-4">
            <div>
              <h3 className="text-lg font-bold text-stone-900">
                Government Data Source Synchronization Status
              </h3>
              <p className="text-xs text-stone-500">
                Statutory registries ensuring zero hallucination across all counselling layers
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Sources", val: syncSummary.total_sources },
              { label: "Cataloged Trades", val: syncSummary.total_trades },
              { label: "Mapped Providers", val: syncSummary.total_providers },
              { label: "Verified Outcomes", val: syncSummary.total_outcomes },
            ].map((st, i) => (
              <div key={i} className="p-4 bg-stone-50 rounded-2xl border border-stone-200 space-y-1">
                <div className="text-[10px] text-stone-400 uppercase font-bold">{st.label}</div>
                <div className="text-xl font-black text-stone-900">{st.val}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
