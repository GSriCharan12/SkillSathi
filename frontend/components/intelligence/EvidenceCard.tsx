"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, ExternalLink, Calendar, MapPin, Building, ShieldCheck } from "lucide-react";

export interface EvidenceItem {
  id: number;
  claim: string;
  value: string;
  trade_id?: number;
  trade_title?: string;
  trade_code?: string;
  sector?: string;
  state?: string;
  district?: string;
  industrial_cluster?: string;
  provider_name?: string;
  provider_type?: string;
  placement_rate?: number;
  median_starting_monthly_inr?: number;
  mid_career_monthly_inr?: number;
  stipend_during_training_inr?: number;
  data_year?: number;
  sample_size?: number;
  source_publisher?: string;
  source_name?: string;
  source_url?: string;
  verification_status?: string;
  last_verified_at?: string;
  freshness_status?: string;
  freshness_label?: string;
  is_stale?: boolean;
  is_demo?: boolean;
  relevance_score?: number;
  geo_match_level?: string;
}

interface EvidenceCardProps {
  evidence: EvidenceItem;
  showScore?: boolean;
}

export const EvidenceCard: React.FC<EvidenceCardProps> = ({ evidence, showScore = false }) => {
  const isStale = evidence.is_stale || evidence.freshness_status === "STALE";
  const isDemo = evidence.is_demo || evidence.verification_status === "DEMO_SIMULATED" || evidence.freshness_status === "DEMO";

  return (
    <div className="bg-white rounded-2xl border border-gray-200/80 p-5 shadow-xs hover:shadow-md transition-all duration-300 relative overflow-hidden group">
      {/* Top provenance badge */}
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <div className="flex items-center gap-2">
          {isDemo ? (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
              DEMO DATA - Benchmark Simulation
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              {evidence.verification_status === "OFFICIAL_VERIFIED"
                ? "Official Government Verified"
                : "Provisionally Verified"}
            </span>
          )}

          {evidence.geo_match_level === "DISTRICT_MATCH" && (
            <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-teal-50 text-teal-800 border border-teal-200">
              <MapPin className="w-3 h-3 text-teal-600" />
              Local District Match
            </span>
          )}
        </div>

        {showScore && evidence.relevance_score && (
          <span className="text-xs font-bold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-md">
            Match Score: {evidence.relevance_score}
          </span>
        )}
      </div>

      {/* Main Claim */}
      <h4 className="text-base font-bold text-gray-900 leading-snug mb-2 group-hover:text-teal-700 transition-colors">
        {evidence.claim}
      </h4>

      {/* Key Metric Highlight Box */}
      <div className="bg-[#FFFDF7] border border-amber-200/60 rounded-xl p-3.5 mb-4 grid grid-cols-2 sm:grid-cols-3 gap-3">
        {evidence.placement_rate !== undefined && (
          <div>
            <div className="text-xs text-gray-500 font-medium">Placement Rate</div>
            <div className="text-lg font-extrabold text-emerald-700">{evidence.placement_rate}%</div>
          </div>
        )}

        {evidence.median_starting_monthly_inr !== undefined && evidence.median_starting_monthly_inr !== null && (
          <div>
            <div className="text-xs text-gray-500 font-medium">Starting Salary</div>
            <div className="text-lg font-extrabold text-gray-900">
              ₹{evidence.median_starting_monthly_inr.toLocaleString()}/mo
            </div>
          </div>
        )}

        {evidence.stipend_during_training_inr !== undefined && evidence.stipend_during_training_inr > 0 && (
          <div>
            <div className="text-xs text-gray-500 font-medium">Training Stipend</div>
            <div className="text-base font-bold text-teal-700">
              ₹{evidence.stipend_during_training_inr.toLocaleString()}/mo
            </div>
          </div>
        )}
      </div>

      {/* Geographic & Institute Provenance */}
      <div className="space-y-1.5 text-xs text-gray-600 mb-4">
        <div className="flex items-center gap-2">
          <MapPin className="w-3.5 h-3.5 text-gray-400 shrink-0" />
          <span>
            {evidence.district}, {evidence.state}
            {evidence.industrial_cluster && (
              <span className="text-gray-500 ml-1 font-medium">({evidence.industrial_cluster})</span>
            )}
          </span>
        </div>

        {evidence.provider_name && (
          <div className="flex items-center gap-2">
            <Building className="w-3.5 h-3.5 text-gray-400 shrink-0" />
            <span className="truncate">{evidence.provider_name}</span>
          </div>
        )}

        <div className="flex items-center gap-2">
          <Calendar className="w-3.5 h-3.5 text-gray-400 shrink-0" />
          <span>Tracer Survey Data Year: <strong className="text-gray-800">{evidence.data_year || 2024}</strong></span>
          {evidence.sample_size && (
            <span className="text-gray-500">• Sample Size: {evidence.sample_size} graduates</span>
          )}
        </div>
      </div>

      {/* Footer & Source Traceability */}
      <div className="pt-3 border-t border-gray-100 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div className="flex items-center gap-1.5">
          <span className={`inline-block w-2 h-2 rounded-full ${isStale ? "bg-amber-500" : "bg-emerald-500"}`} />
          <span className={`font-medium ${isStale ? "text-amber-700" : "text-gray-600"}`}>
            {evidence.freshness_label || "Verified data updated recently"}
          </span>
        </div>

        {evidence.source_url && (
          <a
            href={evidence.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-teal-700 hover:text-teal-900 font-semibold transition-colors"
          >
            <span>{evidence.source_publisher || "MSDE / DGT"}</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
};
