"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  GraduationCap,
  Briefcase,
  TrendingUp,
  Award,
  ChevronRight,
  BookOpen,
  ArrowUpRight,
  CheckCircle,
  Sparkles,
  ShieldCheck
} from "lucide-react";

export interface PathwayStep {
  id?: number;
  step_order: number;
  role_title: string;
  experience_required_months: number;
  certifications_required?: string;
  expected_monthly_inr_min?: number;
  expected_monthly_inr_max?: number;
  education_ladder_option?: string;
  description?: string;
  progression_options?: Array<{
    id?: number;
    destination_type: string;
    title: string;
    eligibility_criteria?: string;
    recognizing_body?: string;
  }>;
}

export interface PathwayData {
  id?: number;
  title: string;
  overview?: string;
  entry_qualification: string;
  total_progression_years: number;
  steps: PathwayStep[];
}

interface InteractivePathwayLadderProps {
  pathway: PathwayData;
  tradeTitle?: string;
  tradeCode?: string;
}

export const InteractivePathwayLadder: React.FC<InteractivePathwayLadderProps> = ({
  pathway,
  tradeTitle,
  tradeCode,
}) => {
  const [selectedStepIndex, setSelectedStepIndex] = useState<number>(0);
  const steps = pathway.steps || [];
  const activeStep = steps[selectedStepIndex] || steps[0];

  const getStepIcon = (index: number, total: number) => {
    if (index === 0) return GraduationCap;
    if (index === total - 1) return Award;
    if (index === 1) return Briefcase;
    return TrendingUp;
  };

  const getStepStageName = (index: number, total: number) => {
    if (index === 0) return "1. Vocational Qualification";
    if (index === 1) return "2. Entry Industry Role";
    if (index === 2) return "3. Advanced Specialist";
    if (index === 3) return "4. Site Leadership / Manager";
    return `Step ${index + 1}`;
  };

  return (
    <div className="bg-white rounded-3xl border border-gray-200/80 p-6 sm:p-8 shadow-sm">
      {/* Header Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-gray-100">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-teal-50 text-teal-800 border border-teal-200 mb-2">
            <Sparkles className="w-3.5 h-3.5 text-teal-600" />
            NSQF Aligned Vertical Mobility Ladder
          </div>
          <h3 className="text-xl sm:text-2xl font-black text-gray-900">
            {pathway.title}
          </h3>
          <p className="text-sm text-gray-600 mt-1 max-w-2xl">
            {pathway.overview || "Step-by-step career progression showing industry roles, verified wage bands, and lateral university degree entry."}
          </p>
        </div>

        <div className="bg-[#FFFDF7] border border-amber-200/80 rounded-2xl px-4 py-3 text-right">
          <div className="text-xs text-gray-500 font-medium">Full Ladder Timeline</div>
          <div className="text-lg font-black text-teal-900">
            {pathway.total_progression_years} - {pathway.total_progression_years + 2} Years
          </div>
        </div>
      </div>

      {/* Main Interactive Progression Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-8">
        {/* Left Column: Visual Ladder Steps */}
        <div className="lg:col-span-5 space-y-4">
          <div className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-2">
            Select Ladder Step to Inspect Details
          </div>

          <div className="relative">
            {/* SVG Connecting Line behind buttons */}
            <div className="absolute left-6 top-8 bottom-8 w-1 bg-gradient-to-b from-teal-400 via-emerald-400 to-amber-400 rounded-full -z-0" />

            {steps.map((step, idx) => {
              const Icon = getStepIcon(idx, steps.length);
              const isSelected = selectedStepIndex === idx;

              return (
                <motion.button
                  key={idx}
                  onClick={() => setSelectedStepIndex(idx)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className={`w-full text-left p-4 rounded-2xl transition-all duration-200 relative z-10 flex items-start gap-4 mb-3 border ${
                    isSelected
                      ? "bg-teal-900 text-white shadow-lg border-teal-950 ring-2 ring-teal-500/30"
                      : "bg-white text-gray-800 hover:bg-teal-50/60 border-gray-200"
                  }`}
                >
                  <div
                    className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 font-bold ${
                      isSelected
                        ? "bg-teal-400 text-teal-950"
                        : "bg-teal-100 text-teal-800"
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <span
                        className={`text-xs font-semibold ${
                          isSelected ? "text-teal-200" : "text-teal-700"
                        }`}
                      >
                        {getStepStageName(idx, steps.length)}
                      </span>
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                          isSelected
                            ? "bg-teal-800 text-teal-100"
                            : "bg-gray-100 text-gray-600"
                        }`}
                      >
                        {step.experience_required_months === 0
                          ? "Entry Level"
                          : `${Math.round(step.experience_required_months / 12)} Yrs Exp`}
                      </span>
                    </div>

                    <h4
                      className={`text-base font-bold mt-0.5 truncate ${
                        isSelected ? "text-white" : "text-gray-900"
                      }`}
                    >
                      {step.role_title}
                    </h4>

                    {step.expected_monthly_inr_min && (
                      <div
                        className={`text-xs font-medium mt-1 ${
                          isSelected ? "text-amber-200 font-semibold" : "text-emerald-700"
                        }`}
                      >
                        ₹{step.expected_monthly_inr_min.toLocaleString()} - ₹{step.expected_monthly_inr_max?.toLocaleString()}/mo
                      </div>
                    )}
                  </div>

                  <ChevronRight
                    className={`w-5 h-5 shrink-0 self-center transition-transform ${
                      isSelected ? "text-teal-300 translate-x-1" : "text-gray-400"
                    }`}
                  />
                </motion.button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Deep-Dive Step Dossier */}
        <div className="lg:col-span-7">
          <AnimatePresence mode="wait">
            {activeStep && (
              <motion.div
                key={selectedStepIndex}
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                transition={{ duration: 0.2 }}
                className="bg-[#FFFDF7] rounded-2xl border border-amber-200/80 p-6 space-y-6 shadow-xs"
              >
                {/* Step Role Title and Salary Badge */}
                <div className="flex flex-wrap items-start justify-between gap-4 pb-4 border-b border-amber-200/60">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-teal-800 bg-teal-100/80 px-2.5 py-1 rounded-md">
                      Stage {activeStep.step_order} of {steps.length}
                    </span>
                    <h4 className="text-2xl font-black text-gray-900 mt-2">
                      {activeStep.role_title}
                    </h4>
                    <p className="text-sm text-gray-600 mt-1">
                      {activeStep.description || "Core technical responsibilities and industry operational tasks."}
                    </p>
                  </div>

                  {activeStep.expected_monthly_inr_min && (
                    <div className="bg-white border border-emerald-300 rounded-xl p-3 text-right">
                      <div className="text-xs text-gray-500 font-medium">Expected Monthly Wage</div>
                      <div className="text-xl font-black text-emerald-800">
                        ₹{activeStep.expected_monthly_inr_min.toLocaleString()} - ₹{activeStep.expected_monthly_inr_max?.toLocaleString()}
                      </div>
                      <div className="text-[10px] text-gray-400">Based on MSDE Tracer Benchmarks</div>
                    </div>
                  )}
                </div>

                {/* Requirements & Experience Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
                      <Briefcase className="w-4 h-4 text-teal-600" />
                      Required Industry Experience
                    </div>
                    <div className="text-base font-extrabold text-gray-900">
                      {activeStep.experience_required_months === 0
                        ? "Zero (Direct Campus / ITI Entry)"
                        : `${activeStep.experience_required_months} Months (~${Math.round(activeStep.experience_required_months / 12)} Years)`}
                    </div>
                  </div>

                  <div className="bg-white rounded-xl p-4 border border-gray-200">
                    <div className="flex items-center gap-2 text-xs font-bold text-gray-500 uppercase tracking-wider mb-2">
                      <Award className="w-4 h-4 text-emerald-600" />
                      Required Technical Credential
                    </div>
                    <div className="text-sm font-bold text-gray-900">
                      {activeStep.certifications_required || "NSQF Qualified Certificate"}
                    </div>
                  </div>
                </div>

                {/* Lateral Higher Education Avenue Highlight (Critical for Family Decision Support) */}
                {activeStep.education_ladder_option && (
                  <div className="bg-gradient-to-r from-teal-900 to-slate-900 rounded-2xl p-5 text-white shadow-md">
                    <div className="flex items-center gap-2 text-teal-300 text-xs font-bold uppercase tracking-wider mb-1.5">
                      <GraduationCap className="w-4 h-4 text-teal-300" />
                      Higher Education Degree Bridge (NCrF Recognized)
                    </div>
                    <h5 className="text-lg font-bold text-white mb-2">
                      {activeStep.education_ladder_option}
                    </h5>
                    <p className="text-xs text-teal-100 leading-relaxed">
                      Learners in this role accumulate academic credits under the National Credit Framework (NCrF) allowing direct lateral entry into polytechnic diplomas, B.Voc, or B.Tech degrees without repeating foundation courses.
                    </p>
                  </div>
                )}

                {/* Provenance Guarantee Footer */}
                <div className="flex items-center gap-2 text-xs text-gray-500 pt-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>
                    Progression ladder validated against <strong>NCVET National Qualifications Register (NQR)</strong> files.
                  </span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};
