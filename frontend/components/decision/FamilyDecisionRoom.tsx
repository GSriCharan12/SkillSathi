"use client";

import React, { useState, useEffect } from "react";
import {
  FamilyDecisionRoomSnapshot,
  Trade,
} from "@/types";
import { apiClient } from "@/lib/api-client";
import {
  Users,
  GraduationCap,
  ShieldCheck,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Briefcase,
  TrendingUp,
  Bookmark,
  Calendar,
  Headphones,
  Check,
  ChevronRight,
  ArrowRight,
  MessageSquare,
  Clock,
  Heart,
  FileText,
  Building,
} from "lucide-react";

interface FamilyDecisionRoomProps {
  familyId?: number;
  onExploreTrades?: () => void;
  onRequestCounselling?: () => void;
}

const DECISION_STATES = [
  { id: "EXPLORING", label: "Exploring Trades", desc: "Browsing pathways" },
  { id: "DISCUSSING", label: "Family Discussion", desc: "Evaluating trade-offs" },
  { id: "COMPARING", label: "Comparing Options", desc: "Side-by-side analysis" },
  { id: "NEEDS_COUNSELLING", label: "Counsellor Help", desc: "Expert 1-on-1 guidance" },
  { id: "INFORMED", label: "Informed State", desc: "All facts verified" },
  { id: "DECISION_MADE", label: "Consensus Reached", desc: "Agreed action plan" },
];

export function FamilyDecisionRoom({
  familyId = 1,
  onExploreTrades,
  onRequestCounselling,
}: FamilyDecisionRoomProps) {
  const [snapshot, setSnapshot] = useState<FamilyDecisionRoomSnapshot | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [activeTab, setActiveTab] = useState<"perspectives" | "concerns" | "evidence" | "counsellor">("perspectives");
  const [isUpdating, setIsUpdating] = useState(false);

  const fetchSnapshot = async () => {
    setIsLoading(true);
    try {
      const res = await apiClient.getFamilyDecisionSnapshot(familyId);
      if (res.success && res.data) {
        setSnapshot(res.data);
      }
    } catch (err) {
      console.error("Failed to load Family Decision Room snapshot:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchSnapshot();
  }, [familyId]);

  const handleStateChange = async (newState: string) => {
    if (!snapshot || isUpdating) return;
    setIsUpdating(true);
    try {
      const res = await apiClient.updateFamilyDecisionState(familyId, {
        decision_status: newState,
        selected_trade_id: snapshot.selected_trade?.id,
        learner_agreed: newState === "INFORMED" || newState === "DECISION_MADE" ? true : snapshot.learner_agreed,
        parent_agreed: newState === "INFORMED" || newState === "DECISION_MADE" ? true : snapshot.parent_agreed,
      });
      if (res.success && res.data) {
        setSnapshot(res.data);
      }
    } catch (err) {
      console.error("Error updating decision state:", err);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleResolveConcern = async (concernId: number) => {
    try {
      const res = await apiClient.resolveFamilyConcern(familyId, {
        concern_id: concernId,
        resolution_notes: "Addressed during joint family evidence review.",
      });
      if (res.success && res.data) {
        setSnapshot(res.data);
      }
    } catch (err) {
      console.error("Error resolving concern:", err);
    }
  };

  if (isLoading && !snapshot) {
    return (
      <div className="p-12 text-center bg-white rounded-3xl border border-stone-200 shadow-sm animate-pulse space-y-4">
        <Users className="w-10 h-10 text-teal-600 mx-auto animate-bounce" />
        <p className="text-sm font-semibold text-stone-700">
          Loading Family Decision Room & Perspective Matrix...
        </p>
      </div>
    );
  }

  if (!snapshot) {
    return (
      <div className="p-8 text-center bg-white rounded-3xl border border-stone-200 shadow-sm space-y-3">
        <AlertCircle className="w-8 h-8 text-amber-600 mx-auto" />
        <p className="text-sm font-bold text-stone-900">Family Session Not Found</p>
        <p className="text-xs text-stone-500">Please select an authorized family room.</p>
      </div>
    );
  }

  const currentStateIdx = DECISION_STATES.findIndex((s) => s.id === snapshot.decision_status);

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* 1. Header Banner & Decision Stepper */}
      <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-teal-950 text-white rounded-3xl p-6 sm:p-8 shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/20 border border-teal-400/30 text-teal-300 text-xs font-semibold">
                <Users className="w-3.5 h-3.5" />
                Family Room: {snapshot.family_code}
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold font-outfit text-white">
                {snapshot.family_name || "Family Decision Room"}
              </h1>
              <p className="text-xs sm:text-sm text-stone-300">
                Shared family perspective hub for {snapshot.location_label || "Telangana"}
              </p>
            </div>

            {/* Alignment Score Badge */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/15 flex items-center gap-4">
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-400/40 flex items-center justify-center text-emerald-400 font-bold text-lg">
                {Math.round(snapshot.alignment_score)}%
              </div>
              <div>
                <div className="text-xs font-bold text-white uppercase tracking-wider">
                  Family Alignment
                </div>
                <div className="text-[11px] text-teal-200">
                  {snapshot.alignment_score > 80
                    ? "High consensus on goals"
                    : "Active constructive discussion"}
                </div>
              </div>
            </div>
          </div>

          {/* Decision State Stepper */}
          <div className="pt-4 border-t border-white/10 space-y-2">
            <div className="flex items-center justify-between text-xs text-stone-300 font-medium">
              <span>Decision Support Progression:</span>
              <span className="font-bold text-teal-300">
                Current: {DECISION_STATES.find((s) => s.id === snapshot.decision_status)?.label}
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
              {DECISION_STATES.map((st, idx) => {
                const isCompleted = idx < currentStateIdx;
                const isCurrent = idx === currentStateIdx;
                return (
                  <button
                    key={st.id}
                    type="button"
                    onClick={() => handleStateChange(st.id)}
                    className={`p-2.5 rounded-xl border text-left transition-all ${
                      isCurrent
                        ? "bg-teal-500 text-slate-950 font-bold border-teal-300 shadow-lg shadow-teal-500/30 scale-102"
                        : isCompleted
                        ? "bg-white/10 text-white border-white/20 hover:bg-white/15"
                        : "bg-white/5 text-stone-400 border-white/10 hover:bg-white/10"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] uppercase tracking-wider opacity-75">
                        Step 0{idx + 1}
                      </span>
                      {isCompleted ? (
                        <Check className="w-3.5 h-3.5 text-emerald-400" />
                      ) : null}
                    </div>
                    <div className="text-xs font-bold truncate mt-0.5">{st.label}</div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* 2. Active Counsellor Escalation Status (If Present) */}
      {snapshot.active_counsellor_case && (
        <div className="p-5 bg-gradient-to-r from-emerald-50 via-teal-50 to-emerald-50 rounded-2xl border border-emerald-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 animate-fade-in">
          <div className="flex items-start gap-3">
            <div className="p-2.5 bg-emerald-600 text-white rounded-xl shadow-xs">
              <Headphones className="w-5 h-5" />
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-200 text-emerald-900">
                  Case #{snapshot.active_counsellor_case.id}: {snapshot.active_counsellor_case.status}
                </span>
                <span className="text-xs font-semibold text-emerald-800">
                  Priority: {snapshot.active_counsellor_case.priority}
                </span>
              </div>
              <h4 className="text-sm font-bold text-stone-900">
                {snapshot.active_counsellor_case.assigned_counsellor_name
                  ? `Your counsellor (${snapshot.active_counsellor_case.assigned_counsellor_name}) has accepted your request.`
                  : "Your counsellor request has been received and is being assigned."}
              </h4>
              <p className="text-xs text-stone-600">
                Topic: {snapshot.active_counsellor_case.escalation_reason}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("counsellor")}
              className="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl transition-colors shadow-xs"
            >
              View Counsellor Guidance
            </button>
          </div>
        </div>
      )}

      {/* 3. FOUR-COLUMN PERSPECTIVE MATRIX (Learner | Parent | Evidence | Shared Decision) */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* COLUMN 1: LEARNER PERSPECTIVE */}
        <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-stone-100">
            <div className="p-2 bg-teal-50 text-teal-700 rounded-xl border border-teal-100">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-stone-900 text-sm">
                Learner Perspective
              </h3>
              <p className="text-[11px] text-stone-500">
                {snapshot.learner_perspective.name} ({snapshot.learner_perspective.education_level})
              </p>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 bg-teal-50/50 rounded-xl border border-teal-100 space-y-1">
              <div className="font-semibold text-teal-900 text-[11px] uppercase tracking-wider flex items-center gap-1">
                <Heart className="w-3.5 h-3.5 text-rose-500" />
                Interest Areas:
              </div>
              <div className="flex flex-wrap gap-1 pt-1">
                {snapshot.learner_perspective.interests.map((it, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 bg-white text-teal-800 font-medium rounded-md border border-teal-200 text-[11px]"
                  >
                    {it}
                  </span>
                ))}
              </div>
            </div>

            <div className="space-y-2 text-stone-700">
              <div className="flex justify-between py-1 border-b border-stone-100">
                <span className="text-stone-500">Work Environment:</span>
                <span className="font-semibold text-stone-900">{snapshot.learner_perspective.work_env}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-stone-100">
                <span className="text-stone-500">Salary Aspiration:</span>
                <span className="font-semibold text-stone-900">
                  ₹{snapshot.learner_perspective.expected_salary_monthly_inr.toLocaleString("en-IN")}/mo
                </span>
              </div>
              <div className="flex justify-between py-1">
                <span className="text-stone-500">Degree Goal:</span>
                <span className="font-semibold text-teal-700">Lateral B.Voc / B.Tech</span>
              </div>
            </div>
          </div>
        </div>

        {/* COLUMN 2: PARENT PERSPECTIVE */}
        <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-stone-100">
            <div className="p-2 bg-amber-50 text-amber-700 rounded-xl border border-amber-100">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-stone-900 text-sm">
                Parent Perspective
              </h3>
              <p className="text-[11px] text-stone-500">
                {snapshot.parent_perspective.name} ({snapshot.parent_perspective.relationship})
              </p>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200 space-y-1">
              <div className="font-semibold text-amber-900 text-[11px] uppercase tracking-wider">
                Top Family Priorities:
              </div>
              <div className="flex flex-wrap gap-1 pt-1">
                {snapshot.parent_perspective.top_priorities.map((p, i) => (
                  <span
                    key={i}
                    className="px-2 py-0.5 bg-white text-amber-900 font-medium rounded-md border border-amber-200 text-[11px]"
                  >
                    {p.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </div>

            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200 text-stone-700 italic leading-relaxed text-[11px]">
              "{snapshot.parent_perspective.raw_concerns_text}"
            </div>
          </div>
        </div>

        {/* COLUMN 3: AI VERIFIED EVIDENCE */}
        <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-stone-100">
            <div className="p-2 bg-emerald-50 text-emerald-700 rounded-xl border border-emerald-100">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-stone-900 text-sm">
                Verified AI Evidence
              </h3>
              <p className="text-[11px] text-stone-500">
                {snapshot.selected_trade?.title || "Trade Outcomes"}
              </p>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            {snapshot.evidence_citations.length > 0 ? (
              snapshot.evidence_citations.slice(0, 1).map((cite, idx) => (
                <div key={idx} className="p-3 bg-emerald-50/40 rounded-xl border border-emerald-200 space-y-2">
                  <div className="flex items-center justify-between text-[10px] font-bold text-emerald-800">
                    <span>{cite.publisher}</span>
                    <span>{cite.data_year ? `Year ${cite.data_year}` : "Verified"}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-1.5 text-[11px]">
                    <div className="p-2 bg-white rounded-lg border border-emerald-100">
                      <div className="text-[10px] text-stone-500">Starting Wage</div>
                      <div className="font-bold text-stone-900">
                        ₹{cite.starting_salary_min?.toLocaleString("en-IN")}/mo
                      </div>
                    </div>
                    <div className="p-2 bg-white rounded-lg border border-emerald-100">
                      <div className="text-[10px] text-stone-500">Placement</div>
                      <div className="font-bold text-emerald-700">{cite.placement_rate}%</div>
                    </div>
                  </div>
                  <div className="p-2 bg-white rounded-lg border border-emerald-100 text-[10px] text-teal-900 font-medium">
                    {cite.education_ladder}
                  </div>
                </div>
              ))
            ) : (
              <div className="p-4 bg-stone-50 rounded-xl text-center text-stone-500 text-xs">
                Select a trade to view verified outcome evidence.
              </div>
            )}

            <div className="text-[10px] text-stone-400 text-center">
              Zero-Hallucination: Grounded in NCVET & DGT registries.
            </div>
          </div>
        </div>

        {/* COLUMN 4: SHARED CONSENSUS & ACTIONS */}
        <div className="bg-white rounded-3xl border border-stone-200 p-5 shadow-sm space-y-4">
          <div className="flex items-center gap-2.5 pb-3 border-b border-stone-100">
            <div className="p-2 bg-slate-100 text-slate-800 rounded-xl border border-slate-200">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
            </div>
            <div>
              <h3 className="font-bold text-stone-900 text-sm">
                Shared Consensus
              </h3>
              <p className="text-[11px] text-stone-500">
                Bridging & next steps
              </p>
            </div>
          </div>

          <div className="space-y-3 text-xs">
            <div className="p-3 bg-stone-50 rounded-xl border border-stone-200 space-y-1.5">
              <div className="font-bold text-stone-800 text-[11px]">
                Agreed Alignment Areas:
              </div>
              <ul className="space-y-1 text-[11px] text-stone-700 list-disc list-inside">
                {snapshot.shared_priorities.map((sp, i) => (
                  <li key={i}>{sp}</li>
                ))}
              </ul>
            </div>

            <div className="pt-2 space-y-2">
              <button
                type="button"
                onClick={onExploreTrades}
                className="w-full py-2.5 px-3 bg-teal-700 hover:bg-teal-800 text-white rounded-xl text-xs font-bold transition-colors flex items-center justify-center gap-1.5 shadow-xs"
              >
                <Briefcase className="w-3.5 h-3.5" />
                <span>Explore Careers & Ladders</span>
              </button>

              <button
                type="button"
                onClick={onRequestCounselling}
                className="w-full py-2.5 px-3 bg-stone-100 hover:bg-stone-200 text-stone-800 rounded-xl text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
              >
                <Headphones className="w-3.5 h-3.5 text-stone-600" />
                <span>Request Human Counsellor</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 4. TABBED INTERACTIVE WORKSTATION */}
      <div className="bg-white rounded-3xl border border-stone-200 shadow-sm p-6 sm:p-8 space-y-6">
        {/* Navigation Bar */}
        <div className="flex border-b border-stone-200 gap-6 text-sm font-semibold text-stone-500 overflow-x-auto">
          {[
            { id: "perspectives", label: "Bridging Discussion Points", icon: MessageSquare },
            { id: "concerns", label: `Reported Concerns (${snapshot.reported_concerns.length})`, icon: AlertCircle },
            { id: "evidence", label: "Evidence & Options Ledger", icon: FileText },
            { id: "counsellor", label: "Counsellor Guidance Notes", icon: Headphones },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`pb-4 flex items-center gap-2 border-b-2 transition-all whitespace-nowrap ${
                  activeTab === tab.id
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

        {/* TAB 1: BRIDGING DISCUSSION POINTS */}
        {activeTab === "perspectives" && (
          <div className="space-y-4">
            <div className="p-4 bg-teal-50/60 rounded-2xl border border-teal-200 text-xs text-teal-950 flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-teal-700 shrink-0 mt-0.5" />
              <div>
                <h4 className="font-bold text-sm">"Let's explore the evidence together"</h4>
                <p className="mt-1 leading-relaxed text-stone-700">
                  SkillSathi does not take sides. We bring verified wage data and lateral education mobility options so your family can make a confident, consensus-driven choice.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              {snapshot.discussion_topics.map((dt, idx) => (
                <div
                  key={idx}
                  className="p-4 bg-stone-50 rounded-2xl border border-stone-200 space-y-2"
                >
                  <div className="text-[10px] font-bold text-teal-800 uppercase tracking-wider">
                    Discussion Point 0{idx + 1}
                  </div>
                  <p className="text-xs text-stone-800 leading-relaxed font-medium">
                    {dt}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 2: CONCERNS RESOLUTION CHECKLIST */}
        {activeTab === "concerns" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between text-xs text-stone-600 pb-2">
              <span>
                Resolved: <strong>{snapshot.resolved_concerns_count}</strong> | Open:{" "}
                <strong>{snapshot.open_concerns_count}</strong>
              </span>
              <span className="text-stone-400">Click to resolve when evidence is reviewed</span>
            </div>

            <div className="space-y-3">
              {snapshot.reported_concerns.map((c) => (
                <div
                  key={c.id}
                  className={`p-4 rounded-2xl border transition-all flex items-center justify-between gap-4 ${
                    c.is_addressed
                      ? "bg-emerald-50/50 border-emerald-200 text-stone-600 opacity-80"
                      : "bg-white border-stone-200 text-stone-900 shadow-xs"
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-stone-100 text-stone-700">
                        {c.category}
                      </span>
                      <span className="text-[10px] text-amber-700 font-semibold">
                        Severity: {c.severity_level}/10
                      </span>
                    </div>
                    <p className={`text-xs font-semibold ${c.is_addressed ? "line-through text-stone-500" : ""}`}>
                      {c.concern_text}
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() => handleResolveConcern(c.id)}
                    disabled={c.is_addressed}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                      c.is_addressed
                        ? "bg-emerald-100 text-emerald-800 cursor-default"
                        : "bg-teal-50 hover:bg-teal-100 text-teal-800 border border-teal-200"
                    }`}
                  >
                    <Check className="w-3.5 h-3.5" />
                    <span>{c.is_addressed ? "Resolved" : "Mark Resolved"}</span>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB 3: EVIDENCE & OPTIONS LEDGER */}
        {activeTab === "evidence" && (
          <div className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-stone-500">
              Saved Trades in Family Discussion Ledger
            </h4>
            {snapshot.saved_trades.length === 0 ? (
              <div className="p-6 text-center bg-stone-50 rounded-2xl border border-dashed border-stone-200 space-y-2">
                <Bookmark className="w-8 h-8 text-stone-300 mx-auto" />
                <p className="text-xs text-stone-500">
                  No trades bookmarked yet. Explore careers and save options for family review.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                {snapshot.saved_trades.map((st) => (
                  <div
                    key={st.id}
                    className="p-4 bg-stone-50 rounded-2xl border border-stone-200 space-y-2"
                  >
                    <div className="text-[10px] font-bold text-teal-800">{st.sector}</div>
                    <div className="text-xs font-bold text-stone-900">{st.title}</div>
                    <div className="text-[11px] text-stone-500">
                      NSQF L{st.nsqf_level} • {st.duration_months} Months
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 4: COUNSELLOR GUIDANCE NOTES */}
        {activeTab === "counsellor" && (
          <div className="space-y-4">
            {snapshot.shared_counsellor_notes.length === 0 ? (
              <div className="p-8 text-center bg-stone-50 rounded-2xl border border-dashed border-stone-200 space-y-2">
                <Headphones className="w-8 h-8 text-stone-300 mx-auto" />
                <p className="text-xs font-bold text-stone-700">No Shared Counsellor Notes Yet</p>
                <p className="text-[11px] text-stone-500">
                  When a certified counsellor provides tailored guidance or action items for your family, they will appear here.
                </p>
              </div>
            ) : (
              <div className="space-y-3">
                {snapshot.shared_counsellor_notes.map((note) => (
                  <div
                    key={note.id}
                    className="p-4 bg-emerald-50/50 rounded-2xl border border-emerald-200 space-y-1.5"
                  >
                    <div className="flex items-center justify-between text-[11px] font-semibold text-emerald-900">
                      <span>{note.author_name}</span>
                      <span>{new Date(note.created_at).toLocaleDateString()}</span>
                    </div>
                    <p className="text-xs text-stone-800 leading-relaxed">{note.note_text}</p>
                    {note.is_action_item && (
                      <span className="inline-block px-2 py-0.5 text-[10px] font-bold bg-emerald-200 text-emerald-900 rounded">
                        Action Item
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
