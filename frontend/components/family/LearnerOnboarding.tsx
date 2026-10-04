"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  GraduationCap,
  Wrench,
  Sun,
  Zap,
  Cpu,
  HeartPulse,
  Building,
  TreePine,
  Hospital,
  Award,
  Briefcase,
  MapPin,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Progress } from "@/components/ui/Progress";
import { translations, Language } from "@/lib/translations";
import { fadeUpVariant } from "@/animations/variants";

export interface LearnerOnboardingProps {
  lang: Language;
  onComplete: (data: any) => void;
  initialData?: any;
}

export const LearnerOnboarding: React.FC<LearnerOnboardingProps> = ({
  lang,
  onComplete,
  initialData,
}) => {
  const t = translations[lang];
  const [step, setStep] = useState<number>(initialData?.onboarding_step || 1);

  // Form State
  const [grade, setGrade] = useState<string>(initialData?.current_education_grade || "10th Standard");
  const [strengths, setStrengths] = useState<string[]>(initialData?.academic_strengths || ["PRACTICAL_HANDS_ON"]);
  const [interests, setInterests] = useState<string[]>(initialData?.interest_areas || ["SOLAR_ENERGY"]);
  const [workEnv, setWorkEnv] = useState<string>(initialData?.preferred_work_environment || "WORKSHOP");
  const [educationGoal, setEducationGoal] = useState<string>(initialData?.further_education_goals || "LATERAL_DEGREE");
  const [locationPref, setLocationPref] = useState<string>(initialData?.location_preference || "NEAR_HOME");
  const [salaryGoal, setSalaryGoal] = useState<number>(initialData?.expected_salary_monthly_inr || 22000);

  const totalSteps = 6;
  const progressPct = (step / totalSteps) * 100;

  const toggleItem = (list: string[], item: string, setter: (v: string[]) => void) => {
    if (list.includes(item)) {
      if (list.length > 1) setter(list.filter((x) => x !== item));
    } else {
      setter([...list, item]);
    }
  };

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      onComplete({
        current_education_grade: grade,
        academic_strengths: strengths,
        interest_areas: interests,
        preferred_work_environment: workEnv,
        further_education_goals: educationGoal,
        location_preference: locationPref,
        expected_salary_monthly_inr: salaryGoal,
        onboarding_step: totalSteps,
        is_complete: true,
      });
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Step Header */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs font-semibold text-[#64748B]">
          <Badge variant="teal">
            {t.learnerTitle} • {t.step} {step} {t.of} {totalSteps}
          </Badge>
          <span className="font-mono">{Math.round(progressPct)}% {t.completed}</span>
        </div>
        <Progress value={progressPct} variant="teal" />
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
          {/* STEP 1: Current Education Level */}
          {step === 1 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step1Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step1Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {[
                  { id: "10th Standard", label: t.grade10, icon: <GraduationCap className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "12th Standard", label: t.grade12, icon: <GraduationCap className="w-5 h-5 text-[#52B788]" /> },
                  { id: "ITI / Polytechnic", label: t.diplomaStudent, icon: <Wrench className="w-5 h-5 text-[#F6C85F]" /> },
                  { id: "Other", label: t.otherEducation, icon: <Briefcase className="w-5 h-5 text-[#F28482]" /> },
                ].map((item) => {
                  const isSelected = grade === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setGrade(item.id)}
                      className={`flex items-center gap-3.5 p-4 rounded-2xl border text-left transition-all min-h-[64px] ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] shadow-sm ring-2 ring-[#2A9D8F]/20"
                          : "bg-white/80 border-[#14213D]/8 hover:bg-white"
                      }`}
                    >
                      <div className="p-2.5 rounded-xl bg-white shadow-xs">{item.icon}</div>
                      <span className="text-sm font-bold text-[#14213D]">{item.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 2: Learning Strengths */}
          {step === 2 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step2Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step2Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {[
                  { id: "PRACTICAL_HANDS_ON", title: t.practicalHandsOn, desc: t.practicalHandsOnDesc, icon: <Wrench className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "SCIENCE_TECH", title: t.scienceTech, desc: t.scienceTechDesc, icon: <Zap className="w-5 h-5 text-[#52B788]" /> },
                  { id: "CREATIVE_DESIGN", title: t.creativeDesign, desc: t.creativeDesignDesc, icon: <Cpu className="w-5 h-5 text-[#F6C85F]" /> },
                  { id: "OPERATIONS", title: t.managementCoord, desc: t.managementCoordDesc, icon: <Building className="w-5 h-5 text-[#F28482]" /> },
                ].map((item) => {
                  const isSelected = strengths.includes(item.id);
                  return (
                    <button
                      key={item.id}
                      onClick={() => toggleItem(strengths, item.id, setStrengths)}
                      className={`p-4 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] shadow-sm ring-2 ring-[#2A9D8F]/20"
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

          {/* STEP 3: Core Technical Interests */}
          {step === 3 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step3Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step3Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {[
                  { id: "SOLAR_ENERGY", title: t.solarEnergy, desc: t.solarEnergyDesc, icon: <Sun className="w-5 h-5 text-[#F6C85F]" /> },
                  { id: "EV_TECH", title: t.evTech, desc: t.evTechDesc, icon: <Zap className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "CNC_MACHINING", title: t.cncPrecision, desc: t.cncPrecisionDesc, icon: <Cpu className="w-5 h-5 text-[#52B788]" /> },
                  { id: "MED_TECH", title: t.medTech, desc: t.medTechDesc, icon: <HeartPulse className="w-5 h-5 text-[#F28482]" /> },
                ].map((item) => {
                  const isSelected = interests.includes(item.id);
                  return (
                    <button
                      key={item.id}
                      onClick={() => toggleItem(interests, item.id, setInterests)}
                      className={`p-4 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] shadow-sm ring-2 ring-[#2A9D8F]/20"
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

          {/* STEP 4: Preferred Work Environment */}
          {step === 4 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step4Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step4Desc}</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                {[
                  { id: "WORKSHOP", title: t.workshopEnv, desc: t.workshopEnvDesc, icon: <Building className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "FIELD", title: t.fieldEnv, desc: t.fieldEnvDesc, icon: <TreePine className="w-5 h-5 text-[#52B788]" /> },
                  { id: "CLINICAL", title: t.clinicalEnv, desc: t.clinicalEnvDesc, icon: <Hospital className="w-5 h-5 text-[#F28482]" /> },
                ].map((item) => {
                  const isSelected = workEnv === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setWorkEnv(item.id)}
                      className={`p-4 rounded-2xl border text-left transition-all ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] shadow-sm ring-2 ring-[#2A9D8F]/20"
                          : "bg-white/80 border-[#14213D]/8 hover:bg-white"
                      }`}
                    >
                      <div className="p-2.5 rounded-xl bg-white shadow-xs w-fit mb-2.5">{item.icon}</div>
                      <h4 className="text-sm font-bold text-[#14213D] mb-1">{item.title}</h4>
                      <p className="text-xs text-[#64748B]">{item.desc}</p>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 5: Further Education Goals */}
          {step === 5 && (
            <div className="space-y-5">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step5Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step5Desc}</p>
              </div>

              <div className="space-y-3">
                {[
                  { id: "LATERAL_DEGREE", title: t.lateralDegree, desc: t.lateralDegreeDesc, icon: <Award className="w-5 h-5 text-[#2A9D8F]" /> },
                  { id: "DIRECT_JOB", title: t.directJob, desc: t.directJobDesc, icon: <Briefcase className="w-5 h-5 text-[#52B788]" /> },
                  { id: "APPRENTICESHIP_STUDY", title: t.apprenticeStudy, desc: t.apprenticeStudyDesc, icon: <Sparkles className="w-5 h-5 text-[#F6C85F]" /> },
                ].map((item) => {
                  const isSelected = educationGoal === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => setEducationGoal(item.id)}
                      className={`w-full p-4.5 rounded-2xl border text-left transition-all flex items-start gap-4 ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] shadow-sm ring-2 ring-[#2A9D8F]/20"
                          : "bg-white/80 border-[#14213D]/8 hover:bg-white"
                      }`}
                    >
                      <div className="p-2.5 rounded-xl bg-white shadow-xs shrink-0 mt-0.5">{item.icon}</div>
                      <div>
                        <h4 className="text-sm font-bold text-[#14213D]">{item.title}</h4>
                        <p className="text-xs text-[#64748B] mt-1 leading-relaxed">{item.desc}</p>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}

          {/* STEP 6: Location Preference & Salary Expectations */}
          {step === 6 && (
            <div className="space-y-6">
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-[#14213D]">{t.step6Title}</h3>
                <p className="text-xs sm:text-sm text-[#64748B] mt-1">{t.step6Desc}</p>
              </div>

              {/* Location Radios */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  { id: "NEAR_HOME", label: t.nearHome },
                  { id: "WITHIN_STATE", label: t.withinState },
                  { id: "METROS_ALLOWED", label: t.metrosAllowed },
                ].map((loc) => {
                  const isSelected = locationPref === loc.id;
                  return (
                    <button
                      key={loc.id}
                      onClick={() => setLocationPref(loc.id)}
                      className={`p-3.5 rounded-2xl border text-center font-bold text-xs transition-all ${
                        isSelected
                          ? "bg-[#E8F5F3] border-[#2A9D8F] text-[#14213D] ring-2 ring-[#2A9D8F]/20"
                          : "bg-white/80 border-[#14213D]/8 text-[#64748B]"
                      }`}
                    >
                      <MapPin className="w-4 h-4 mx-auto mb-1 text-[#2A9D8F]" />
                      <span>{loc.label}</span>
                    </button>
                  );
                })}
              </div>

              {/* Salary Expectation Slider */}
              <div className="p-5 rounded-2xl bg-white/90 border border-[#14213D]/8 space-y-3">
                <div className="flex items-center justify-between text-xs font-bold text-[#14213D]">
                  <span>{t.salaryGoalLabel}</span>
                  <span className="text-base text-[#2A9D8F]">₹{salaryGoal.toLocaleString("en-IN")}/mo</span>
                </div>
                <input
                  type="range"
                  min="12000"
                  max="45000"
                  step="1000"
                  value={salaryGoal}
                  onChange={(e) => setSalaryGoal(Number(e.target.value))}
                  className="w-full h-2.5 bg-neutral-200 rounded-lg appearance-none cursor-pointer accent-[#2A9D8F]"
                />
                <div className="flex justify-between text-[11px] text-neutral-400 font-mono">
                  <span>₹12,000 (ITI Base)</span>
                  <span>₹25,000 (EV/Solar Tech)</span>
                  <span>₹45,000+ (Advanced)</span>
                </div>
              </div>
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
              variant="primary"
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
