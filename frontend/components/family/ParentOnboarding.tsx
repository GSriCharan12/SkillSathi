"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Shield,
  TrendingUp,
  Award,
  HeartHandshake,
  DollarSign,
  GraduationCap,
  MapPin,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  MessageSquareQuote,
  Mic,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Progress } from "@/components/ui/Progress";
import { translations, Language } from "@/lib/translations";
import { fadeUpVariant } from "@/animations/variants";

export interface ParentOnboardingProps {
  lang: Language;
  onComplete: (data: any) => void;
  initialData?: any;
}

export const ParentOnboarding: React.FC<ParentOnboardingProps> = ({
  lang,
  onComplete,
  initialData,
}) => {
  const t = translations[lang];
  const [step, setStep] = useState<number>(initialData?.onboarding_step || 1);

  // Form State
  const [relationship, setRelationship] = useState<string>(initialData?.relationship_type || "FATHER");
  const [priorities, setPriorities] = useState<string[]>(
    initialData?.top_priorities || ["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION"]
  );
  const [concernsText, setConcernsText] = useState<string>(
    initialData?.raw_concerns_text || "I am worried whether starting wages will be fair and if my child can later complete an official college degree."
  );

  const totalSteps = 3;
  const progressPct = (step / totalSteps) * 100;

  const togglePriority = (item: string) => {
    if (priorities.includes(item)) {
      if (priorities.length > 1) setPriorities(priorities.filter((x) => x !== item));
    } else {
      setPriorities([...priorities, item]);
    }
  };

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      onComplete({
        relationship_type: relationship,
        top_priorities: priorities,
        raw_concerns_text: concernsText,
        onboarding_step: totalSteps,
        is_complete: true,
      });
    }
  };

  // Preview extracted concerns dynamically
  const previewConcerns = [];
  const lower = concernsText.toLowerCase();
  if (lower.includes("salary") || lower.includes("wage") || lower.includes("money") || lower.includes("income") || lower.includes("జీతం")) {
    previewConcerns.push({ cat: "INCOME", title: "Starting Wage Parity", sev: 7 });
  }
  if (lower.includes("degree") || lower.includes("college") || lower.includes("study") || lower.includes("డిగ్రీ")) {
    previewConcerns.push({ cat: "FURTHER_EDUCATION", title: "Lateral College Degree Pathway", sev: 6 });
  }
  if (lower.includes("status") || lower.includes("respect") || lower.includes("society") || lower.includes("izzat") || lower.includes("గౌరవం")) {
    previewConcerns.push({ cat: "SOCIAL_STATUS", title: "Social Status & Peer Perception", sev: 8 });
  }
  if (lower.includes("safe") || lower.includes("girl") || lower.includes("travel") || lower.includes("భద్రత")) {
    previewConcerns.push({ cat: "SAFETY", title: "Workplace Safety & Commute", sev: 7 });
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Step Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-[#64748B]">
          <Badge variant="coral">
            {t.parentTitle} • {t.step} {step} {t.of} {totalSteps}
          </Badge>
          <span className="font-mono">{Math.round(progressPct)}% {t.completed}</span>
        </div>
        <Progress value={progressPct} variant="coral" />
      </div>

      {/* Interactive Question Card */}
      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          variants={fadeUpVariant}
          initial="hidden"
          animate="visible"
          exit="hidden"
          className="glass-panel p-6 sm:p-8 rounded-3xl space-y-6"
        >
          {/* STEP 1: Relationship */}
          {step === 1 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.parentStep1Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.parentStep1Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {[
                  { id: "FATHER", label: t.father },
                  { id: "MOTHER", label: t.mother },
                  { id: "GUARDIAN", label: t.guardian },
                  { id: "ELDER_SIBLING", label: t.elderSibling },
                ].map((item) => {
                  const isSelected = relationship === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setRelationship(item.id)}
                      className={`flex items-center gap-3.5 p-4.5 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? "bg-[#FDF0F0] border-[#F28482] shadow-sm ring-2 ring-[#F28482]/20"
                          : "bg-white/80 border-[#14213D]/8 hover:bg-white"
                      }`}
                    >
                      <div className="w-9 h-9 rounded-xl bg-white shadow-xs flex items-center justify-center font-bold text-[#F28482]">
                        {item.label[0]}
                      </div>
                      <span className="text-sm font-bold text-[#14213D]">{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 2: What matters most to the family? */}
          {step === 2 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.parentStep2Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.parentStep2Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {[
                  { id: "INCOME", title: t.priorityIncome, desc: t.priorityIncomeDesc, icon: <DollarSign className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "JOB_SECURITY", title: t.prioritySecurity, desc: t.prioritySecurityDesc, icon: <Shield className="w-5 h-5 text-[#52B788]" /> },
                  { id: "SOCIAL_STATUS", title: t.priorityStatus, desc: t.priorityStatusDesc, icon: <HeartHandshake className="w-5 h-5 text-[#F28482]" /> },
                  { id: "SAFETY", title: t.prioritySafety, desc: t.prioritySafetyDesc, icon: <Shield className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "CAREER_GROWTH", title: t.priorityGrowth, desc: t.priorityGrowthDesc, icon: <TrendingUp className="w-5 h-5 text-[#52B788]" /> },
                  { id: "FURTHER_EDUCATION", title: t.priorityDegree, desc: t.priorityDegreeDesc, icon: <GraduationCap className="w-5 h-5 text-[#F6C85F]" /> },
                  { id: "LOCATION", title: t.priorityLocation, desc: t.priorityLocationDesc, icon: <MapPin className="w-5 h-5 text-[#5E50A1]" /> },
                  { id: "AFFORDABILITY", title: t.priorityAffordable, desc: t.priorityAffordableDesc, icon: <Sparkles className="w-5 h-5 text-[#2A9D8F]" /> },
                ].map((item) => {
                  const isSelected = priorities.includes(item.id);
                  return (
                    <button
                      key={item.id}
                      onClick={() => togglePriority(item.id)}
                      className={`p-4 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? "bg-[#FDF0F0] border-[#F28482] shadow-sm ring-2 ring-[#F28482]/20"
                          : "bg-white/80 border-[#14213D]/8 hover:bg-white"
                      }`}
                    >
                      <div className="flex items-center gap-2.5 mb-1.5">
                        <div className="p-2 rounded-xl bg-white shadow-xs">{item.icon}</div>
                        <h4 className="text-sm font-bold text-[#14213D]">{item.title}</h4>
                      </div>
                      <p className="text-xs text-[#64748B] leading-relaxed">{item.desc}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 3: Natural Language Concerns Capture */}
          {step === 3 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.parentStep3Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.parentStep3Desc}</p>
              </div>

              <div className="relative">
                <textarea
                  rows={4}
                  value={concernsText}
                  onChange={(e) => setConcernsText(e.target.value)}
                  placeholder={t.parentTextPlaceholder}
                  className="w-full p-4 rounded-2xl border border-[#14213D]/12 bg-white/90 text-sm text-[#243047] placeholder:text-neutral-400 focus:outline-none focus:ring-2 focus:ring-[#F28482]/20 focus:border-[#F28482] transition-all"
                />
                <button
                  type="button"
                  className="absolute right-3 bottom-3 p-2 rounded-xl bg-neutral-100 hover:bg-[#FDF0F0] text-[#F28482] transition-colors"
                  title="Voice Input (Simulated)"
                >
                  <Mic className="w-4 h-4" />
                </button>
              </div>

              {/* Live Analyzed Concerns Feedback */}
              {previewConcerns.length > 0 && (
                <div className="p-4.5 rounded-2xl bg-[#FFFDF7] border border-[#14213D]/8 space-y-2.5">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-[#14213D]">
                    <Sparkles className="w-3.5 h-3.5 text-[#F28482]" />
                    <span>{t.detectedConcernsTitle}</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {previewConcerns.map((c) => (
                      <Badge key={c.cat} variant="coral" size="sm">
                        {c.title} (Severity: {c.sev}/10)
                      </Badge>
                    ))}
                  </div>
                  <p className="text-[11px] text-[#64748B] italic">
                    * Mapped as reported concerns. SkillSathi links each concern to official MSDE and NCVET outcome data in your family room.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* Navigation Controls */}
          <div className="flex items-center justify-between pt-4 border-t border-[#14213D]/8">
            <Button
              variant="outline"
              size="md"
              disabled={step === 1}
              onClick={() => setStep(step - 1)}
              leftIcon={<ArrowLeft className="w-4 h-4" />}
            >
              {t.back}
            </Button>

            <Button
              variant="coral"
              size="md"
              onClick={handleNext}
              rightIcon={<ArrowRight className="w-4 h-4" />}
            >
              {step === totalSteps ? t.saveAndContinue : t.next}
            </Button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
};
