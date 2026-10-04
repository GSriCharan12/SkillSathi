"use client";

import React from "react";
import { EvidenceCitation } from "@/types";
import {
  ShieldCheck,
  Building2,
  TrendingUp,
  FileText,
  Calendar,
  IndianRupee,
  GraduationCap,
  Sparkles,
  ExternalLink,
  AlertTriangle,
} from "lucide-react";

interface EvidenceDrawerProps {
  citations: EvidenceCitation[];
  isEvidenceAvailable?: boolean;
  activeTradeTitle?: string;
}

export function EvidenceDrawer({
  citations,
  isEvidenceAvailable = true,
  activeTradeTitle = "Vocational Trade",
}: EvidenceDrawerProps) {
  return (
    <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-5 h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-stone-100 pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-100">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-stone-900 text-sm">Live Verified Evidence</h3>
              <p className="text-xs text-stone-500">Government tracer data & provenance</p>
            </div>
          </div>
          <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded bg-stone-100 text-stone-600 border border-stone-200">
            Zero Hallucination
          </span>
        </div>
      </div>

      {/* Citations List / Missing State */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-1">
        {citations.length === 0 ? (
          <div className="p-5 text-center bg-stone-50 rounded-xl border border-dashed border-stone-200 space-y-3">
            <FileText className="w-8 h-8 text-stone-300 mx-auto" />
            <div>
              <p className="text-xs font-semibold text-stone-700">No Specific Citation Yet</p>
              <p className="text-[11px] text-stone-500 mt-1">
                Ask about salary, job security, placement, or career growth to see verified government records.
              </p>
            </div>
          </div>
        ) : !isEvidenceAvailable ? (
          <div className="p-4 bg-amber-50 rounded-xl border border-amber-200 space-y-2">
            <div className="flex items-center gap-2 text-amber-900 font-semibold text-xs">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Evidence Notice</span>
            </div>
            <p className="text-xs text-amber-800 leading-relaxed">
              Verified government tracer records for this specific combination are not yet published. The AI Counsellor will not invent estimated numbers.
            </p>
          </div>
        ) : (
          citations.map((cite, index) => (
            <div
              key={index}
              className="bg-stone-50 hover:bg-stone-100/80 transition-all rounded-xl p-4 border border-stone-200 space-y-3"
            >
              {/* Citation Title & Publisher */}
              <div className="space-y-1">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-200 inline-flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" />
                    {cite.verification_status.replace(/_/g, " ")}
                  </span>
                  {cite.data_year && (
                    <span className="text-[11px] text-stone-500 flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      Year {cite.data_year}
                    </span>
                  )}
                </div>
                <h4 className="text-xs font-bold text-stone-900 leading-tight">
                  {cite.title}
                </h4>
                <div className="flex items-center gap-1.5 text-[11px] text-stone-500">
                  <Building2 className="w-3.5 h-3.5 text-stone-400" />
                  <span>{cite.publisher || cite.source_name}</span>
                </div>
              </div>

              {/* Data Metrics Grid */}
              <div className="grid grid-cols-2 gap-2 text-xs">
                {cite.starting_salary_min && (
                  <div className="p-2 bg-white rounded-lg border border-stone-200">
                    <div className="text-[10px] text-stone-500 flex items-center gap-1">
                      <IndianRupee className="w-3 h-3 text-emerald-600" />
                      Starting Salary
                    </div>
                    <div className="font-bold text-stone-800 mt-0.5">
                      ₹{cite.starting_salary_min.toLocaleString("en-IN")} - ₹{cite.starting_salary_max?.toLocaleString("en-IN")}/mo
                    </div>
                  </div>
                )}

                {cite.placement_rate !== undefined && (
                  <div className="p-2 bg-white rounded-lg border border-stone-200">
                    <div className="text-[10px] text-stone-500 flex items-center gap-1">
                      <TrendingUp className="w-3 h-3 text-teal-600" />
                      Placement Rate
                    </div>
                    <div className="font-bold text-teal-700 mt-0.5">
                      {cite.placement_rate}%
                    </div>
                  </div>
                )}

                {cite.formal_contract_pct !== undefined && (
                  <div className="p-2 bg-white rounded-lg border border-stone-200">
                    <div className="text-[10px] text-stone-500">Formal Contract</div>
                    <div className="font-bold text-stone-800 mt-0.5">
                      {cite.formal_contract_pct}% (PF/ESI)
                    </div>
                  </div>
                )}

                {cite.retention_rate_1yr !== undefined && (
                  <div className="p-2 bg-white rounded-lg border border-stone-200">
                    <div className="text-[10px] text-stone-500">1-Yr Retention</div>
                    <div className="font-bold text-stone-800 mt-0.5">
                      {cite.retention_rate_1yr}%
                    </div>
                  </div>
                )}
              </div>

              {/* Education Ladder */}
              {cite.education_ladder && (
                <div className="p-2 bg-teal-50/70 rounded-lg border border-teal-100 text-xs">
                  <div className="text-[10px] font-semibold text-teal-900 flex items-center gap-1 mb-1">
                    <GraduationCap className="w-3.5 h-3.5 text-teal-700" />
                    Higher Education Pathway
                  </div>
                  <p className="text-[11px] text-teal-800">
                    {cite.education_ladder}
                  </p>
                </div>
              )}

              {/* Citation Snippet & Provenance */}
              <div className="text-[11px] text-stone-600 bg-white p-2.5 rounded-lg border border-stone-200 italic leading-relaxed">
                "{cite.citation_snippet}"
              </div>
            </div>
          ))
        )}
      </div>

      {/* Trust & Provenance Footer */}
      <div className="border-t border-stone-100 pt-3 text-[11px] text-stone-500 space-y-1">
        <div className="flex items-center gap-1 text-stone-700 font-medium">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
          <span>Statutory Data Integrity Mandate</span>
        </div>
        <p className="text-[10px] text-stone-400 leading-tight">
          All data is ingested via official source adapters (NCVET, DGT, Labour Bureau) with full provenance.
        </p>
      </div>
    </div>
  );
}
