"use client";

import React from "react";
import { Trade } from "@/types";
import {
  Users,
  GraduationCap,
  Heart,
  ShieldCheck,
  MapPin,
  Briefcase,
  Sparkles,
  ChevronDown,
  Info,
} from "lucide-react";

interface FamilyContextPanelProps {
  activeTrade?: Trade | null;
  trades: Trade[];
  onSelectTrade: (trade: Trade) => void;
  speakerRole: "PARENT" | "LEARNER";
  onToggleSpeaker: (role: "PARENT" | "LEARNER") => void;
  alignmentScore?: number;
}

export function FamilyContextPanel({
  activeTrade,
  trades,
  onSelectTrade,
  speakerRole,
  onToggleSpeaker,
  alignmentScore = 82,
}: FamilyContextPanelProps) {
  return (
    <div className="bg-white rounded-2xl border border-stone-200 p-5 shadow-sm space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-stone-100 pb-4">
        <div className="flex items-center gap-2.5">
          <div className="p-2 rounded-xl bg-teal-50 text-teal-700 border border-teal-100">
            <Users className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-semibold text-stone-900 text-sm">Family Session Context</h3>
            <p className="text-xs text-stone-500">Shared perspective profile</p>
          </div>
        </div>
        <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">
          <Sparkles className="w-3.5 h-3.5 text-emerald-600" />
          {alignmentScore}% Family Alignment
        </span>
      </div>

      {/* Speaker Role Switcher */}
      <div className="space-y-2">
        <label className="text-xs font-semibold uppercase tracking-wider text-stone-500">
          Current Speaker
        </label>
        <div className="grid grid-cols-2 gap-2 p-1 bg-stone-100 rounded-xl border border-stone-200">
          <button
            type="button"
            onClick={() => onToggleSpeaker("PARENT")}
            className={`py-2 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
              speakerRole === "PARENT"
                ? "bg-white text-navy-900 shadow-sm border border-stone-200"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            <ShieldCheck className="w-4 h-4 text-amber-600" />
            Parent / Guardian
          </button>
          <button
            type="button"
            onClick={() => onToggleSpeaker("LEARNER")}
            className={`py-2 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-2 transition-all ${
              speakerRole === "LEARNER"
                ? "bg-white text-navy-900 shadow-sm border border-stone-200"
                : "text-stone-600 hover:text-stone-900"
            }`}
          >
            <GraduationCap className="w-4 h-4 text-teal-600" />
            Learner (Student)
          </button>
        </div>
      </div>

      {/* Active Trade Under Discussion */}
      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold uppercase tracking-wider text-stone-500 flex items-center gap-1.5">
            <Briefcase className="w-3.5 h-3.5 text-stone-400" />
            Trade Under Discussion
          </label>
        </div>
        <div className="relative">
          <select
            value={activeTrade?.id || ""}
            onChange={(e) => {
              const selected = trades.find((t) => t.id === Number(e.target.value));
              if (selected) onSelectTrade(selected);
            }}
            className="w-full appearance-none bg-stone-50 hover:bg-stone-100 border border-stone-200 rounded-xl px-3.5 py-2.5 text-sm font-medium text-stone-800 pr-9 focus:ring-2 focus:ring-teal-500 focus:outline-none transition-colors"
          >
            {trades.map((t) => (
              <option key={t.id} value={t.id}>
                {t.title} (NSQF L{t.nsqf_level} • {t.duration_months} mo)
              </option>
            ))}
          </select>
          <ChevronDown className="w-4 h-4 text-stone-400 absolute right-3 top-3 pointer-events-none" />
        </div>
      </div>

      {/* Learner Profile Card */}
      <div className="bg-teal-50/50 border border-teal-100 rounded-xl p-3.5 space-y-2.5">
        <div className="flex items-center gap-2 text-xs font-bold text-teal-900">
          <GraduationCap className="w-4 h-4 text-teal-700" />
          <span>Learner: Ramesh (10th Passed)</span>
        </div>
        <div className="space-y-1.5 text-xs text-stone-700">
          <div className="flex items-start gap-1.5">
            <Heart className="w-3.5 h-3.5 text-rose-500 mt-0.5 shrink-0" />
            <span>
              <strong>Interests:</strong> Hands-on wiring, motors, renewable energy
            </span>
          </div>
          <div className="flex items-start gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-teal-600 mt-0.5 shrink-0" />
            <span>
              <strong>Preference:</strong> Within Telangana (Medchal / Hyderabad)
            </span>
          </div>
        </div>
      </div>

      {/* Parent Priorities Card */}
      <div className="bg-amber-50/60 border border-amber-200 rounded-xl p-3.5 space-y-2.5">
        <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
          <ShieldCheck className="w-4 h-4 text-amber-700" />
          <span>Parent Priorities & Concerns</span>
        </div>
        <ul className="space-y-1.5 text-xs text-stone-700 list-disc list-inside">
          <li>Starting salary stability & formal contract safety</li>
          <li>Possibility of higher studies (Diploma / B.Tech lateral)</li>
          <li>Respectable social standing in the community</li>
        </ul>
      </div>

      {/* Family Principle Reminder */}
      <div className="bg-stone-50 rounded-xl p-3 border border-stone-200 text-xs text-stone-600 space-y-1">
        <div className="flex items-center gap-1.5 font-semibold text-stone-800">
          <Info className="w-3.5 h-3.5 text-teal-600" />
          Non-Coercive Guidance
        </div>
        <p className="text-[11px] leading-relaxed text-stone-500">
          SkillSathi provides verified evidence to empower family discussion. The final decision remains with your family.
        </p>
      </div>
    </div>
  );
}
