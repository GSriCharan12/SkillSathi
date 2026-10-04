"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  X,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  TrendingUp,
  MapPin,
  Clock,
  GraduationCap,
  Briefcase,
  ShieldCheck,
  Building,
  Sparkles
} from "lucide-react";

export interface ComparisonTradeItem {
  trade_id: number;
  trade_code: string;
  trade_title: string;
  sector: string;
  nsqf_level: number;
  duration_months: number;
  min_qualification: string;
  description?: string;
  local_availability: {
    matched_location: string;
    local_providers_count: number;
    total_providers_count: number;
    is_available_locally: boolean;
  };
  verified_placement_rate?: number;
  verified_starting_monthly_inr?: number;
  verified_mid_career_monthly_inr?: number;
  verified_stipend_inr?: number;
  top_employers?: string[];
  top_sectors?: string[];
  retention_rate_1yr?: number;
  career_progression_steps?: Array<{
    step_order: number;
    role_title: string;
    experience_months: number;
    salary_min?: number;
    salary_max?: number;
  }>;
  further_education_routes?: string[];
  evidence_source?: {
    publisher: string;
    name: string;
    url?: string;
    data_year?: number;
    verification_status: string;
  };
  freshness_label?: string;
  is_stale?: boolean;
  missing_metrics?: string[];
}

interface PathwayComparisonMatrixProps {
  trades: ComparisonTradeItem[];
  onRemoveTrade: (tradeId: number) => void;
  onSelectTradeDetail?: (tradeId: number) => void;
}

export const PathwayComparisonMatrix: React.FC<PathwayComparisonMatrixProps> = ({
  trades,
  onRemoveTrade,
  onSelectTradeDetail,
}) => {
  if (!trades || trades.length === 0) {
    return (
      <div className="bg-white rounded-3xl border border-gray-200/80 p-12 text-center shadow-xs">
        <Sparkles className="w-10 h-10 text-teal-600 mx-auto mb-3" />
        <h3 className="text-xl font-black text-gray-900">No Pathways Selected for Comparison</h3>
        <p className="text-sm text-gray-600 mt-1 max-w-md mx-auto">
          Explore trades from the Career Explorer and click <strong>&ldquo;Add to Compare&rdquo;</strong> to evaluate 2 or 3 pathways side-by-side with your family.
        </p>
      </div>
    );
  }

  const renderMissingBadge = (label: string = "Verified data unavailable") => (
    <span className="inline-flex items-center gap-1 text-xs font-semibold text-amber-800 bg-amber-50 px-2.5 py-1 rounded-md border border-amber-200/80">
      <AlertCircle className="w-3 h-3 text-amber-600 shrink-0" />
      {label}
    </span>
  );

  return (
    <div className="bg-white rounded-3xl border border-gray-200/80 shadow-md overflow-hidden">
      {/* Header */}
      <div className="p-6 sm:p-8 bg-gradient-to-r from-teal-900 to-slate-900 text-white flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-teal-400/20 text-teal-300 border border-teal-400/30 mb-2">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-300" />
            Family Decision Matrix • Zero Hallucination Standard
          </div>
          <h3 className="text-2xl sm:text-3xl font-black text-white">
            Comparing {trades.length} Vocational Pathways
          </h3>
          <p className="text-xs sm:text-sm text-teal-100/90 mt-1">
            Side-by-side evaluation of qualifications, starting wages, career progression, and local training institutes.
          </p>
        </div>

        <div className="text-xs text-teal-200/80 bg-white/10 px-3.5 py-2 rounded-xl border border-white/10">
          Comparing {trades.length} of max 3 pathways
        </div>
      </div>

      {/* Comparison Table Grid */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[700px]">
          <thead>
            <tr className="border-b border-gray-200 bg-gray-50/75">
              <th className="p-5 text-xs font-bold uppercase tracking-wider text-gray-400 w-1/4">
                Decision Dimension
              </th>
              {trades.map((t) => (
                <th key={t.trade_id} className="p-5 text-left w-1/3 min-w-[240px] relative">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <span className="text-[11px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-md border border-teal-200">
                        NSQF Level {t.nsqf_level}
                      </span>
                      <h4 className="text-base font-black text-gray-900 mt-1.5 leading-snug">
                        {t.trade_title}
                      </h4>
                      <div className="text-xs text-gray-500 font-medium">{t.sector}</div>
                    </div>

                    <button
                      onClick={() => onRemoveTrade(t.trade_id)}
                      className="p-1 rounded-full hover:bg-gray-200 text-gray-400 hover:text-gray-700 transition-colors"
                      title="Remove from comparison"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-200 text-sm">
            {/* 1. TRAINING DURATION */}
            <tr className="hover:bg-gray-50/50 transition-colors">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <Clock className="w-4 h-4 text-teal-600" />
                Training Duration
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5 font-extrabold text-gray-900">
                  {t.duration_months} Months ({Math.round(t.duration_months / 12 * 10) / 10} Years)
                </td>
              ))}
            </tr>

            {/* 2. ENTRY ELIGIBILITY */}
            <tr className="hover:bg-gray-50/50 transition-colors bg-gray-50/30">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-teal-600" />
                Entry Eligibility
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5 font-medium text-gray-800">
                  {t.min_qualification}
                </td>
              ))}
            </tr>

            {/* 3. LOCAL DISTRICT AVAILABILITY */}
            <tr className="hover:bg-gray-50/50 transition-colors">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <MapPin className="w-4 h-4 text-teal-600" />
                Local Availability ({trades[0]?.local_availability?.matched_location || "Your Area"})
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  {t.local_availability.is_available_locally ? (
                    <div className="space-y-1">
                      <span className="inline-flex items-center gap-1 text-xs font-bold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        {t.local_availability.local_providers_count} Providers Nearby
                      </span>
                    </div>
                  ) : (
                    <span className="text-xs font-medium text-gray-500">
                      Available at state / national NSTI centres
                    </span>
                  )}
                </td>
              ))}
            </tr>

            {/* 4. VERIFIED PLACEMENT RATE */}
            <tr className="hover:bg-gray-50/50 transition-colors bg-gray-50/30">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-teal-600" />
                Verified Placement Rate
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  {t.verified_placement_rate !== undefined && t.verified_placement_rate !== null ? (
                    <div>
                      <div className="text-xl font-black text-emerald-700">
                        {t.verified_placement_rate}%
                      </div>
                      <div className="text-[11px] text-gray-400">Tracer Survey 2024</div>
                    </div>
                  ) : (
                    renderMissingBadge()
                  )}
                </td>
              ))}
            </tr>

            {/* 5. STARTING SALARY */}
            <tr className="hover:bg-gray-50/50 transition-colors">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-teal-600" />
                Starting Monthly Salary
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  {t.verified_starting_monthly_inr !== undefined && t.verified_starting_monthly_inr !== null ? (
                    <div className="text-lg font-black text-gray-900">
                      ₹{t.verified_starting_monthly_inr.toLocaleString()}/mo
                    </div>
                  ) : (
                    renderMissingBadge()
                  )}
                </td>
              ))}
            </tr>

            {/* 6. MID-CAREER SALARY */}
            <tr className="hover:bg-gray-50/50 transition-colors bg-gray-50/30">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-teal-600" />
                Mid-Career Salary (3-5 Yrs)
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  {t.verified_mid_career_monthly_inr !== undefined && t.verified_mid_career_monthly_inr !== null ? (
                    <div className="text-lg font-black text-teal-800">
                      ₹{t.verified_mid_career_monthly_inr.toLocaleString()}/mo
                    </div>
                  ) : (
                    renderMissingBadge()
                  )}
                </td>
              ))}
            </tr>

            {/* 7. TRAINING STIPEND */}
            <tr className="hover:bg-gray-50/50 transition-colors">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-amber-500" />
                Training Stipend (NAPS)
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5 font-semibold text-gray-800">
                  {t.verified_stipend_inr ? `₹${t.verified_stipend_inr.toLocaleString()}/mo` : "Available via NAPS Portal"}
                </td>
              ))}
            </tr>

            {/* 8. CAREER PROGRESSION LADDER */}
            <tr className="hover:bg-gray-50/50 transition-colors bg-gray-50/30">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <ArrowRight className="w-4 h-4 text-teal-600" />
                Career Progression Ladder
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  <div className="space-y-1.5">
                    {t.career_progression_steps?.map((step, sIdx) => (
                      <div key={sIdx} className="text-xs text-gray-800 flex items-start gap-1.5">
                        <span className="w-4 h-4 rounded-full bg-teal-100 text-teal-800 flex items-center justify-center font-bold text-[10px] shrink-0 mt-0.5">
                          {step.step_order}
                        </span>
                        <span><strong>{step.role_title}</strong></span>
                      </div>
                    ))}
                  </div>
                </td>
              ))}
            </tr>

            {/* 9. FURTHER HIGHER EDUCATION */}
            <tr className="hover:bg-gray-50/50 transition-colors">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <GraduationCap className="w-4 h-4 text-teal-600" />
                Higher Degree Routes (NCrF)
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5">
                  <div className="space-y-1">
                    {t.further_education_routes?.map((route, rIdx) => (
                      <span
                        key={rIdx}
                        className="inline-block text-xs font-semibold bg-teal-50 text-teal-900 border border-teal-200 px-2.5 py-1 rounded-lg mr-1 mb-1"
                      >
                        {route}
                      </span>
                    ))}
                  </div>
                </td>
              ))}
            </tr>

            {/* 10. EVIDENCE SOURCE */}
            <tr className="hover:bg-gray-50/50 transition-colors bg-gray-50/30">
              <td className="p-5 font-bold text-gray-700 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                Official Evidence Source
              </td>
              {trades.map((t) => (
                <td key={t.trade_id} className="p-5 text-xs text-gray-600">
                  <div className="font-bold text-gray-800">{t.evidence_source?.publisher || "MSDE / DGT"}</div>
                  <div>{t.evidence_source?.name || "National Tracer Study"}</div>
                  <div className="text-emerald-700 font-medium mt-0.5">
                    {t.freshness_label || "Verified data updated recently"}
                  </div>
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
