"use client";

import React from "react";
import { motion } from "framer-motion";
import {
  HeartHandshake,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  GraduationCap,
  Briefcase,
  Users,
  ShieldCheck,
  Compass,
  ArrowRight,
  TrendingUp,
  Award,
} from "lucide-react";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Progress } from "@/components/ui/Progress";
import { Button } from "@/components/ui/Button";
import { GlassSurface } from "@/components/ui/GlassSurface";
import { translations, Language } from "@/lib/translations";
import { fadeUpVariant, staggerContainerVariant } from "@/animations/variants";

export interface FamilySnapshotViewProps {
  lang: Language;
  snapshot: any;
  onEnterDecisionRoom?: () => void;
}

export const FamilySnapshotView: React.FC<FamilySnapshotViewProps> = ({
  lang,
  snapshot,
  onEnterDecisionRoom,
}) => {
  const t = translations[lang];

  return (
    <motion.div
      variants={staggerContainerVariant}
      initial="hidden"
      animate="visible"
      className="space-y-8"
    >
      {/* 1. Header & Alignment Meter Card */}
      <motion.div variants={fadeUpVariant}>
        <GlassSurface level="hero">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
            <div className="lg:col-span-8 space-y-3">
              <div className="flex items-center gap-2 flex-wrap">
                <Badge variant="teal">Family Room: {snapshot.family_code || "SK-8492"}</Badge>
                <Badge variant="emerald">{snapshot.onboarding_status || "COMPLETED"}</Badge>
                <span className="text-xs font-mono text-[#64748B]">
                  {snapshot.state || "Maharashtra"} • {snapshot.district || "Pune"}
                </span>
              </div>
              <h2 className="text-2xl sm:text-3xl font-black text-[#14213D]">
                {t.snapshotTitle}
              </h2>
              <p className="text-xs sm:text-sm text-[#64748B] max-w-2xl leading-relaxed">
                {t.snapshotSubtitle}
              </p>
            </div>

            {/* Alignment Score Meter */}
            <div className="lg:col-span-4 bg-white/90 p-5 rounded-2xl border border-[#14213D]/8 shadow-sm space-y-3 text-center">
              <div className="flex items-center justify-between text-xs font-bold text-[#14213D]">
                <span>{t.alignmentScoreTitle}</span>
                <span className="text-lg text-[#2A9D8F] font-black">{Math.round(snapshot.alignment_score || 82)}%</span>
              </div>
              <Progress value={snapshot.alignment_score || 82} variant="teal" />
              <p className="text-[11px] text-[#64748B]">
                High mutual respect with 2 specific topics flagged for factual discussion.
              </p>
            </div>
          </div>
        </GlassSurface>
      </motion.div>

      {/* 2. Side-by-Side Perspectives: Learner vs Parent */}
      <motion.div variants={fadeUpVariant} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Learner Perspective Card */}
        <Card variant="glass" className="space-y-4 border-t-4 border-t-[#2A9D8F]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-[#E8F5F3] text-[#2A9D8F] flex items-center justify-center font-bold">
                <GraduationCap className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-[#14213D]">{snapshot.learner?.name || "Learner"}</h3>
                <span className="text-[11px] text-[#64748B] font-medium">{snapshot.learner?.grade || "10th Standard"}</span>
              </div>
            </div>
            <Badge variant="teal" size="sm">Learner Unit</Badge>
          </div>

          <div className="space-y-2 text-xs">
            <div className="p-3 rounded-xl bg-white/80 border border-[#14213D]/5">
              <span className="text-[10px] uppercase font-bold text-[#64748B] block mb-1">Key Interest Fields</span>
              <div className="flex flex-wrap gap-1.5">
                {(snapshot.learner?.interests || ["Solar Energy", "Mechatronics"]).map((i: string) => (
                  <Badge key={i} variant="teal" size="sm">{i}</Badge>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="p-3 rounded-xl bg-white/80 border border-[#14213D]/5">
                <span className="text-[10px] uppercase font-bold text-[#64748B] block mb-0.5">Workplace Choice</span>
                <span className="font-semibold text-[#14213D]">{snapshot.learner?.work_env || "WORKSHOP"}</span>
              </div>
              <div className="p-3 rounded-xl bg-white/80 border border-[#14213D]/5">
                <span className="text-[10px] uppercase font-bold text-[#64748B] block mb-0.5">Salary Goal</span>
                <span className="font-semibold text-[#2A9D8F]">₹{(snapshot.learner?.salary_goal || 22000).toLocaleString("en-IN")}/mo</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Parent Perspective Card */}
        <Card variant="glass" className="space-y-4 border-t-4 border-t-[#F28482]">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-[#FDF0F0] text-[#F28482] flex items-center justify-center font-bold">
                <Users className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-[#14213D]">{snapshot.parent?.name || "Parent/Guardian"}</h3>
                <span className="text-[11px] text-[#64748B] font-medium">{snapshot.parent?.relationship || "MOTHER"}</span>
              </div>
            </div>
            <Badge variant="coral" size="sm">Guardian Unit</Badge>
          </div>

          <div className="space-y-2 text-xs">
            <div className="p-3 rounded-xl bg-white/80 border border-[#14213D]/5">
              <span className="text-[10px] uppercase font-bold text-[#64748B] block mb-1">Top Priorities for Decision</span>
              <div className="flex flex-wrap gap-1.5">
                {(snapshot.parent?.priorities || ["JOB_SECURITY", "INCOME", "FURTHER_EDUCATION", "SAFETY"]).map((p: string) => (
                  <Badge key={p} variant="coral" size="sm">{p.replace("_", " ")}</Badge>
                ))}
              </div>
            </div>

            {snapshot.parent?.raw_concerns && (
              <div className="p-3 rounded-xl bg-white/80 border border-[#14213D]/5">
                <span className="text-[10px] uppercase font-bold text-[#64748B] block mb-0.5">Stated Family Concerns</span>
                <p className="text-xs text-[#243047] italic">"{snapshot.parent.raw_concerns}"</p>
              </div>
            )}
          </div>
        </Card>
      </motion.div>

      {/* 3. Alignment Matrix: Shared vs Discussion Points */}
      <motion.div variants={fadeUpVariant} className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Shared Priorities */}
        <Card variant="solid" className="p-6 space-y-4 bg-white border-l-4 border-l-[#52B788]">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-[#52B788]" />
            <h3 className="text-base font-bold text-[#14213D]">{t.sharedPrioritiesTitle}</h3>
          </div>
          <div className="space-y-2.5">
            {snapshot.shared_priorities.map((item: string, idx: number) => (
              <div key={idx} className="flex items-start gap-2.5 p-3 rounded-xl bg-[#EBF8F2]/60 border border-[#52B788]/20 text-xs">
                <CheckCircle2 className="w-4 h-4 text-[#52B788] shrink-0 mt-0.5" />
                <span className="font-semibold text-[#14213D]">{item}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Discussion Points / Areas for Alignment */}
        <Card variant="solid" className="p-6 space-y-4 bg-white border-l-4 border-l-[#F6C85F]">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5 text-[#F6C85F]" />
            <h3 className="text-base font-bold text-[#14213D]">{t.differentPrioritiesTitle}</h3>
          </div>
          <div className="space-y-2.5">
            {snapshot.recommended_discussion_points.map((point: string, idx: number) => (
              <div key={idx} className="flex items-start gap-2.5 p-3 rounded-xl bg-[#FEF9EB] border border-[#F6C85F]/30 text-xs">
                <AlertCircle className="w-4 h-4 text-[#B8860B] shrink-0 mt-0.5" />
                <span className="font-medium text-[#243047]">{point}</span>
              </div>
            ))}
          </div>
        </Card>
      </motion.div>

      {/* 4. Action Banner */}
      <motion.div variants={fadeUpVariant} className="text-center pt-2">
        <Button
          variant="primary"
          size="lg"
          rightIcon={<ArrowRight className="w-4 h-4" />}
          onClick={onEnterDecisionRoom}
        >
          Open Joint Family Decision Room
        </Button>
      </motion.div>
    </motion.div>
  );
};
