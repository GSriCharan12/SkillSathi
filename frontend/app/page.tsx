"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  Compass,
  Users,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  GraduationCap,
  Briefcase,
  Languages,
  Database,
  Search,
  Scale,
  Settings,
  Bot,
  Headphones,
  CheckCircle2,
  TrendingUp,
  Award,
  ChevronLeft,
  UserCheck,
  Building,
  HeartHandshake,
  Lock,
  AlertTriangle,
  LogOut,
} from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { GlassSurface } from "@/components/ui/GlassSurface";
import { Tabs } from "@/components/ui/Tabs";
import { CareerExplorer } from "@/components/intelligence/CareerExplorer";
import { EvidenceHub } from "@/components/intelligence/EvidenceHub";
import { CounsellingHub } from "@/components/counselling/CounsellingHub";
import { FamilyDecisionRoom } from "@/components/decision/FamilyDecisionRoom";
import { CounsellorPortal } from "@/components/counsellor/CounsellorPortal";
import { AdminProgrammeDashboard } from "@/components/admin/AdminProgrammeDashboard";
import { translations, Language } from "@/lib/translations";
import {
  fadeUpVariant,
  staggerContainerVariant,
} from "@/animations/variants";

type UserRole = "PARENT" | "LEARNER" | "COUNSELLOR" | "ADMIN" | null;

const ROLE_DISPLAY_NAMES: Record<string, string> = {
  PARENT: "Parent / Guardian",
  GUARDIAN: "Parent / Guardian",
  LEARNER: "Student / Learner",
  COUNSELLOR: "Certified Counsellor",
  ADMIN: "Scheme Administrator",
};

export default function Home() {
  const [lang, setLang] = useState<Language>("en");
  const t = translations[lang];

  // Current authenticated user (if any)
  const [currentUser, setCurrentUser] = useState<any>(null);

  // Selected Persona Portal (null = Hero / Role Selection Gate)
  const [selectedRole, setSelectedRole] = useState<UserRole>(null);

  // RBAC Access Restriction Alert Modal state
  const [accessDeniedNotice, setAccessDeniedNotice] = useState<{
    attemptedRole: UserRole;
    actualRole: string;
  } | null>(null);

  // Active view inside role-specific dashboards
  const [parentActiveTab, setParentActiveTab] = useState<string>("family_decision_room");
  const [learnerActiveTab, setLearnerActiveTab] = useState<string>("explorer");
  const [counsellingTradeId, setCounsellingTradeId] = useState<number | undefined>(undefined);

  // Simulated active family unit
  const [familyData, setFamilyData] = useState({
    family_id: 1,
    family_code: "SK-9482",
    family_name: "Sharma Family Room",
    state: "Telangana",
    district: "Warangal",
  });

  // Read user & role on mount
  useEffect(() => {
    if (typeof window !== "undefined") {
      let activeUser: any = null;
      const stored = localStorage.getItem("skillsathi_user");
      if (stored) {
        try {
          activeUser = JSON.parse(stored);
          setCurrentUser(activeUser);
        } catch {
          // ignore
        }
      }

      const params = new URLSearchParams(window.location.search);
      const roleParam = params.get("role")?.toUpperCase() as UserRole;

      if (
        roleParam === "PARENT" ||
        roleParam === "LEARNER" ||
        roleParam === "COUNSELLOR" ||
        roleParam === "ADMIN"
      ) {
        // Enforce RBAC: If user is logged in, their portal MUST match their role
        if (activeUser?.role) {
          const userRole = activeUser.role.toUpperCase();
          const isAllowed =
            userRole === roleParam ||
            ((userRole === "PARENT" || userRole === "GUARDIAN") && roleParam === "PARENT");

          if (isAllowed) {
            setSelectedRole(roleParam);
          } else {
            // Role mismatch detected -> set to their authorized role and warn
            setSelectedRole(userRole === "GUARDIAN" ? "PARENT" : (userRole as UserRole));
            setAccessDeniedNotice({
              attemptedRole: roleParam,
              actualRole: userRole,
            });
          }
        } else {
          setSelectedRole(roleParam);
        }
      } else if (activeUser?.role) {
        const userRole = activeUser.role.toUpperCase();
        setSelectedRole(userRole === "GUARDIAN" ? "PARENT" : (userRole as UserRole));
      }

      const familyCode = localStorage.getItem("skillsathi_family_code");
      if (familyCode) {
        setFamilyData((prev) => ({ ...prev, family_code: familyCode }));
      }
    }
  }, []);

  const handlePortalClick = (targetRole: UserRole) => {
    if (!targetRole) {
      setSelectedRole(null);
      return;
    }

    if (currentUser?.role) {
      const userRole = currentUser.role.toUpperCase();
      const isAllowed =
        userRole === targetRole ||
        ((userRole === "PARENT" || userRole === "GUARDIAN") && targetRole === "PARENT");

      if (!isAllowed) {
        setAccessDeniedNotice({
          attemptedRole: targetRole,
          actualRole: userRole,
        });
        return;
      }
    }

    setSelectedRole(targetRole);
    if (targetRole === "PARENT") setParentActiveTab("family_decision_room");
    if (targetRole === "LEARNER") setLearnerActiveTab("explorer");
  };

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("skillsathi_token");
      localStorage.removeItem("skillsathi_user");
      localStorage.removeItem("skillsathi_family_code");
    }
    setCurrentUser(null);
    setSelectedRole(null);
    setAccessDeniedNotice(null);
    window.location.href = "/";
  };

  // Check if current user is authorized for currently selected workspace
  const isWorkspaceAuthorized = () => {
    if (!selectedRole || !currentUser?.role) return true;
    const userRole = currentUser.role.toUpperCase();
    return (
      userRole === selectedRole ||
      ((userRole === "PARENT" || userRole === "GUARDIAN") && selectedRole === "PARENT")
    );
  };

  return (
    <div className="space-y-8">
      {/* ============================================================ */}
      {/* Access Denied Modal Notice (When Role Mismatch Occurs)        */}
      {/* ============================================================ */}
      {accessDeniedNotice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full border border-red-200 shadow-2xl space-y-4"
          >
            <div className="w-12 h-12 rounded-2xl bg-red-50 border border-red-200 flex items-center justify-center text-red-600">
              <Lock className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-black text-gray-900">
                Portal Access Restricted
              </h3>
              <p className="text-xs sm:text-sm text-gray-600 mt-2 leading-relaxed">
                You are currently signed in as a{" "}
                <strong className="text-teal-800">
                  {ROLE_DISPLAY_NAMES[accessDeniedNotice.actualRole] || accessDeniedNotice.actualRole}
                </strong>
                . SkillSathi enforces strict role isolation — each user can only enter their designated role portal.
              </p>
              <div className="mt-3 p-3 rounded-xl bg-amber-50 border border-amber-200 text-xs text-amber-900 font-medium">
                Attempted Portal: <strong>{ROLE_DISPLAY_NAMES[accessDeniedNotice.attemptedRole || ""] || accessDeniedNotice.attemptedRole}</strong>
              </div>
            </div>

            <div className="pt-2 flex flex-col sm:flex-row gap-2">
              <button
                onClick={() => {
                  setAccessDeniedNotice(null);
                  const authRole = (currentUser.role.toUpperCase() === "GUARDIAN" ? "PARENT" : currentUser.role.toUpperCase()) as UserRole;
                  setSelectedRole(authRole);
                }}
                className="flex-1 py-2.5 px-4 rounded-xl bg-teal-800 hover:bg-teal-900 text-white font-bold text-xs transition-all shadow-sm"
              >
                Go to My {ROLE_DISPLAY_NAMES[currentUser?.role || ""]?.split("/")[0]} Portal
              </button>
              <button
                onClick={handleLogout}
                className="py-2.5 px-4 rounded-xl border border-gray-300 hover:bg-gray-100 text-gray-700 font-bold text-xs transition-all flex items-center justify-center gap-1.5"
              >
                <LogOut className="w-3.5 h-3.5" />
                <span>Sign Out</span>
              </button>
            </div>
          </motion.div>
        </div>
      )}

      {/* ============================================================ */}
      {/* 1. HERO / PERSONA SELECTION GATE (When no role is selected)   */}
      {/* ============================================================ */}
      <AnimatePresence mode="wait">
        {selectedRole === null && (
          <motion.div
            key="hero-gate"
            variants={staggerContainerVariant}
            initial="hidden"
            animate="visible"
            exit={{ opacity: 0, y: -10 }}
            className="space-y-12"
          >
            {/* Hero Main Header */}
            <motion.div variants={fadeUpVariant} className="text-center space-y-4 max-w-4xl mx-auto pt-4">
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-bold shadow-2xs">
                <Sparkles className="w-3.5 h-3.5 text-teal-600" />
                <span>AI-Enabled Family Decision-Support for Vocational Education</span>
              </div>

              <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black text-gray-900 tracking-tight leading-tight">
                Explore a future your <br className="hidden sm:block" />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-700 via-emerald-600 to-navy-900">
                  whole family believes in.
                </span>
              </h1>

              <p className="text-sm sm:text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
                SkillSathi bridges generational perspectives with verified government outcome data, official placement statistics, salary certainty, and lateral university degree ladders.
              </p>
            </motion.div>

            {/* Persona Selection Gate Cards */}
            <motion.div variants={fadeUpVariant} className="space-y-4">
              <div className="text-center">
                <h2 className="text-xl sm:text-2xl font-black text-gray-900">
                  Select Your Portal to Enter
                </h2>
                <p className="text-xs sm:text-sm text-gray-500 mt-1">
                  Each user can log in exclusively to their dedicated role workspace.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 pt-2">
                {/* 1. Parent / Guardian Portal */}
                <motion.div
                  whileHover={{ y: -6 }}
                  className={`bg-white rounded-3xl p-6 border-2 transition-all duration-300 flex flex-col justify-between group relative overflow-hidden ${
                    currentUser?.role && (currentUser.role === "PARENT" || currentUser.role === "GUARDIAN")
                      ? "border-emerald-500 ring-4 ring-emerald-500/10 shadow-lg"
                      : "border-emerald-100 hover:border-emerald-400 shadow-sm hover:shadow-xl"
                  }`}
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 group-hover:scale-110 transition-transform">
                        <Users className="w-6 h-6" />
                      </div>
                      {currentUser?.role && (currentUser.role === "PARENT" || currentUser.role === "GUARDIAN") && (
                        <Badge variant="emerald" size="sm">Your Role ✓</Badge>
                      )}
                    </div>
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-emerald-700">Family Perspective</span>
                      <h3 className="text-lg font-bold text-gray-900 mt-0.5">Parent / Guardian Portal</h3>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Evaluate starting salary certainty, formal PF/ESI contracts, workplace safety, and lateral entry into 2nd-year Polytechnic & B.Tech degrees.
                    </p>
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-md">Job Security</span>
                      <span className="text-[10px] font-semibold bg-teal-50 text-teal-800 px-2 py-0.5 rounded-md">Salary Tracer</span>
                      <span className="text-[10px] font-semibold bg-amber-50 text-amber-800 px-2 py-0.5 rounded-md">College Degree</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePortalClick("PARENT")}
                    className="mt-6 w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-700 text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-95 shadow-md shadow-emerald-700/10 transition-all cursor-pointer"
                  >
                    <span>Enter Parent Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>

                {/* 2. Learner / Student Portal */}
                <motion.div
                  whileHover={{ y: -6 }}
                  className={`bg-white rounded-3xl p-6 border-2 transition-all duration-300 flex flex-col justify-between group relative overflow-hidden ${
                    currentUser?.role === "LEARNER"
                      ? "border-teal-500 ring-4 ring-teal-500/10 shadow-lg"
                      : "border-teal-100 hover:border-teal-400 shadow-sm hover:shadow-xl"
                  }`}
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="w-12 h-12 rounded-2xl bg-teal-50 border border-teal-200 flex items-center justify-center text-teal-700 group-hover:scale-110 transition-transform">
                        <GraduationCap className="w-6 h-6" />
                      </div>
                      {currentUser?.role === "LEARNER" && (
                        <Badge variant="teal" size="sm">Your Role ✓</Badge>
                      )}
                    </div>
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-teal-700">Career Aspirations</span>
                      <h3 className="text-lg font-bold text-gray-900 mt-0.5">Student / Learner Portal</h3>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Discover high-growth NSQF vocational trades, compare NAPS apprenticeship stipends, and get 1-on-1 advice from your AI Career Saathi.
                    </p>
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      <span className="text-[10px] font-semibold bg-teal-50 text-teal-800 px-2 py-0.5 rounded-md">NSQF Pathways</span>
                      <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-md">AI Guidance</span>
                      <span className="text-[10px] font-semibold bg-purple-50 text-purple-800 px-2 py-0.5 rounded-md">Apprenticeships</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePortalClick("LEARNER")}
                    className="mt-6 w-full py-3 px-4 rounded-xl bg-gradient-to-r from-teal-700 to-navy-900 text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-95 shadow-md shadow-teal-800/10 transition-all cursor-pointer"
                  >
                    <span>Enter Student Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>

                {/* 3. Certified Counsellor Workstation */}
                <motion.div
                  whileHover={{ y: -6 }}
                  className={`bg-white rounded-3xl p-6 border-2 transition-all duration-300 flex flex-col justify-between group relative overflow-hidden ${
                    currentUser?.role === "COUNSELLOR"
                      ? "border-amber-500 ring-4 ring-amber-500/10 shadow-lg"
                      : "border-amber-100 hover:border-amber-400 shadow-sm hover:shadow-xl"
                  }`}
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="w-12 h-12 rounded-2xl bg-amber-50 border border-amber-200 flex items-center justify-center text-amber-700 group-hover:scale-110 transition-transform">
                        <Headphones className="w-6 h-6" />
                      </div>
                      {currentUser?.role === "COUNSELLOR" && (
                        <Badge variant="golden" size="sm">Your Role ✓</Badge>
                      )}
                    </div>
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-amber-700">Expert Desk</span>
                      <h3 className="text-lg font-bold text-gray-900 mt-0.5">Counsellor Workstation</h3>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Manage escalated family cases, review specific parental priorities, attach official state hostel/fee subsidies, and guide families to consensus.
                    </p>
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      <span className="text-[10px] font-semibold bg-amber-50 text-amber-800 px-2 py-0.5 rounded-md">Case Queue</span>
                      <span className="text-[10px] font-semibold bg-blue-50 text-blue-800 px-2 py-0.5 rounded-md">Shared Notes</span>
                      <span className="text-[10px] font-semibold bg-teal-50 text-teal-800 px-2 py-0.5 rounded-md">State Subsidies</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePortalClick("COUNSELLOR")}
                    className="mt-6 w-full py-3 px-4 rounded-xl bg-gradient-to-r from-amber-600 to-orange-700 text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-95 shadow-md shadow-amber-700/10 transition-all cursor-pointer"
                  >
                    <span>Enter Counsellor Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>

                {/* 4. Scheme Administrator Analytics */}
                <motion.div
                  whileHover={{ y: -6 }}
                  className={`bg-white rounded-3xl p-6 border-2 transition-all duration-300 flex flex-col justify-between group relative overflow-hidden ${
                    currentUser?.role === "ADMIN"
                      ? "border-slate-600 ring-4 ring-slate-600/10 shadow-lg"
                      : "border-slate-200 hover:border-slate-500 shadow-sm hover:shadow-xl"
                  }`}
                >
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <div className="w-12 h-12 rounded-2xl bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-800 group-hover:scale-110 transition-transform">
                        <Building className="w-6 h-6" />
                      </div>
                      {currentUser?.role === "ADMIN" && (
                        <Badge variant="default" size="sm">Your Role ✓</Badge>
                      )}
                    </div>
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700">Governance & Data</span>
                      <h3 className="text-lg font-bold text-gray-900 mt-0.5">Scheme Admin Telemetry</h3>
                    </div>
                    <p className="text-xs text-gray-600 leading-relaxed">
                      Analyze district-level family resistance indices, break down root causes (income, stigma, mobility), audit data feeds, and export telemetry.
                    </p>
                    <div className="flex flex-wrap gap-1.5 pt-1">
                      <span className="text-[10px] font-semibold bg-slate-100 text-slate-800 px-2 py-0.5 rounded-md">Resistance Index</span>
                      <span className="text-[10px] font-semibold bg-teal-50 text-teal-800 px-2 py-0.5 rounded-md">Data Sync</span>
                      <span className="text-[10px] font-semibold bg-emerald-50 text-emerald-800 px-2 py-0.5 rounded-md">CSV Export</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handlePortalClick("ADMIN")}
                    className="mt-6 w-full py-3 px-4 rounded-xl bg-gradient-to-r from-slate-800 to-navy-950 text-white font-bold text-xs flex items-center justify-center gap-2 hover:opacity-95 shadow-md shadow-slate-900/10 transition-all cursor-pointer"
                  >
                    <span>Enter Admin Portal</span>
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </motion.div>
              </div>
            </motion.div>

            {/* Platform Trust & Provenance Bar */}
            <motion.div variants={fadeUpVariant} className="bg-white/80 rounded-3xl p-6 border border-gray-200/80 shadow-xs">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
                <div className="space-y-1">
                  <div className="text-2xl font-black text-emerald-700">86.5%</div>
                  <div className="text-xs font-bold text-gray-800">Verified Placement Benchmark</div>
                  <p className="text-[11px] text-gray-500">Official tracer data across 5 high-demand trades</p>
                </div>
                <div className="space-y-1 sm:border-x sm:border-gray-200 sm:px-4">
                  <div className="text-2xl font-black text-teal-700">₹18,500 - ₹24,000</div>
                  <div className="text-xs font-bold text-gray-800">Average Starting Monthly Wage</div>
                  <p className="text-[11px] text-gray-500">Guaranteed formal contracts with PF & ESI</p>
                </div>
                <div className="space-y-1">
                  <div className="text-2xl font-black text-indigo-700">100% Lateral Pathway</div>
                  <div className="text-xs font-bold text-gray-800">Degree & Polytechnic Progression</div>
                  <p className="text-[11px] text-gray-500">Direct admission to 2nd year engineering & B.Voc</p>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* ============================================================ */}
      {/* 2. DEDICATED ROLE WORKSPACES (When a role is selected)        */}
      {/* ============================================================ */}
      {selectedRole !== null && (
        <div className="space-y-8">
          {/* Top Role Header & Security Status */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-4 rounded-3xl bg-white/90 border border-gray-200 shadow-xs backdrop-blur-md">
            <div className="flex flex-wrap items-center gap-3">
              <button
                onClick={() => setSelectedRole(null)}
                className="inline-flex items-center gap-1 px-3 py-1.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-xs font-bold text-gray-700 transition-colors"
                title="Return to Portal Selection"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                <span>All Portals</span>
              </button>

              <div className="flex items-center gap-2">
                {selectedRole === "PARENT" && (
                  <Badge variant="emerald">👨‍👩‍👧 Parent / Guardian Workspace</Badge>
                )}
                {selectedRole === "LEARNER" && (
                  <Badge variant="teal">🎓 Student / Learner Workspace</Badge>
                )}
                {selectedRole === "COUNSELLOR" && (
                  <Badge variant="golden">🧑‍💼 Certified Counsellor Desk</Badge>
                )}
                {selectedRole === "ADMIN" && (
                  <Badge variant="default">🏛️ Scheme Administrator Telemetry</Badge>
                )}

                {currentUser ? (
                  <span className="inline-flex items-center gap-1 text-xs text-emerald-800 font-semibold bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-200">
                    <UserCheck className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Logged in as: <strong>{currentUser.full_name || currentUser.user?.full_name}</strong></span>
                  </span>
                ) : (
                  <Link
                    href={`/signin?role=${selectedRole}`}
                    className="inline-flex items-center gap-1 text-xs text-amber-800 font-semibold bg-amber-50 hover:bg-amber-100 px-2.5 py-1 rounded-lg border border-amber-200 transition-colors"
                  >
                    <span>Sign In to Save Progress →</span>
                  </Link>
                )}
              </div>
            </div>

            {/* Right Tools */}
            <div className="flex items-center gap-2">
              {currentUser && (
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1 px-3 py-1.5 rounded-xl border border-red-200 bg-red-50 hover:bg-red-100 text-xs font-bold text-red-700 transition-colors cursor-pointer"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Logout</span>
                </button>
              )}
            </div>
          </div>

          {/* Role Access Guard: Check if authorized */}
          {!isWorkspaceAuthorized() ? (
            <div className="bg-white rounded-3xl p-10 border border-red-200 text-center space-y-4 max-w-xl mx-auto shadow-lg">
              <div className="w-16 h-16 mx-auto rounded-3xl bg-red-50 border border-red-200 flex items-center justify-center text-red-600">
                <AlertTriangle className="w-8 h-8" />
              </div>
              <h2 className="text-xl font-black text-gray-900">
                Access Denied to This Portal
              </h2>
              <p className="text-sm text-gray-600 leading-relaxed">
                Your account is registered as a{" "}
                <strong className="text-teal-800">
                  {ROLE_DISPLAY_NAMES[currentUser?.role] || currentUser?.role}
                </strong>
                . You cannot access the{" "}
                <strong>{ROLE_DISPLAY_NAMES[selectedRole]}</strong>.
              </p>
              <div className="pt-4 flex justify-center gap-3">
                <button
                  onClick={() => {
                    const authRole = (currentUser.role.toUpperCase() === "GUARDIAN" ? "PARENT" : currentUser.role.toUpperCase()) as UserRole;
                    setSelectedRole(authRole);
                  }}
                  className="py-2.5 px-5 rounded-xl bg-teal-800 hover:bg-teal-900 text-white font-bold text-xs shadow-sm transition-all"
                >
                  Go to My {ROLE_DISPLAY_NAMES[currentUser?.role]?.split("/")[0]} Portal
                </button>
                <button
                  onClick={handleLogout}
                  className="py-2.5 px-5 rounded-xl border border-gray-300 hover:bg-gray-100 text-gray-700 font-bold text-xs transition-all"
                >
                  Sign Out
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* -------------------------------------------------------- */}
              {/* A. DEDICATED PARENT WORKSPACE                            */}
              {/* -------------------------------------------------------- */}
              {selectedRole === "PARENT" && (
                <div className="space-y-6">
                  {/* Parent Dashboard Navigation Tabs */}
                  <div className="flex items-center justify-center">
                    <Tabs
                      items={[
                        { id: "family_decision_room", label: "Family Decision & Security Room", icon: <Users className="w-3.5 h-3.5" /> },
                        { id: "ai_counsellor", label: "AI Family Reassurance & Questions", icon: <Bot className="w-3.5 h-3.5" /> },
                        { id: "evidence_hub", label: "Verified Outcome & Wage Evidence", icon: <ShieldCheck className="w-3.5 h-3.5" /> },
                        { id: "explorer", label: "Explore Vocational Pathways", icon: <Compass className="w-3.5 h-3.5" /> },
                      ]}
                      activeTab={parentActiveTab}
                      onChange={setParentActiveTab}
                    />
                  </div>

                  {/* View 1: Family Decision Room */}
                  {parentActiveTab === "family_decision_room" && (
                    <FamilyDecisionRoom
                      familyId={familyData.family_id}
                      onExploreTrades={() => setParentActiveTab("explorer")}
                      onRequestCounselling={() => setParentActiveTab("ai_counsellor")}
                    />
                  )}

                  {/* View 2: AI Counselling */}
                  {parentActiveTab === "ai_counsellor" && (
                    <CounsellingHub initialTradeId={counsellingTradeId} />
                  )}

                  {/* View 3: Evidence Hub */}
                  {parentActiveTab === "evidence_hub" && (
                    <EvidenceHub
                      initialState={familyData.state}
                      initialDistrict={familyData.district}
                    />
                  )}

                  {/* View 4: Explorer */}
                  {parentActiveTab === "explorer" && (
                    <CareerExplorer
                      initialState={familyData.state}
                      initialDistrict={familyData.district}
                      onOpenFamilyRoom={() => setParentActiveTab("family_decision_room")}
                      onConsultCounsellor={(tradeId) => {
                        setCounsellingTradeId(tradeId);
                        setParentActiveTab("ai_counsellor");
                      }}
                    />
                  )}
                </div>
              )}

              {/* -------------------------------------------------------- */}
              {/* B. DEDICATED LEARNER WORKSPACE                           */}
              {/* -------------------------------------------------------- */}
              {selectedRole === "LEARNER" && (
                <div className="space-y-6">
                  {/* Learner Dashboard Navigation Tabs */}
                  <div className="flex items-center justify-center">
                    <Tabs
                      items={[
                        { id: "explorer", label: "Vocational Career Explorer", icon: <Compass className="w-3.5 h-3.5" /> },
                        { id: "ai_counsellor", label: "AI Career Saathi Guide", icon: <Bot className="w-3.5 h-3.5" /> },
                        { id: "family_decision_room", label: "My Family Alignment Room", icon: <Users className="w-3.5 h-3.5" /> },
                        { id: "evidence_hub", label: "Verified Placement & Wages", icon: <ShieldCheck className="w-3.5 h-3.5" /> },
                      ]}
                      activeTab={learnerActiveTab}
                      onChange={setLearnerActiveTab}
                    />
                  </div>

                  {/* View 1: Career Explorer */}
                  {learnerActiveTab === "explorer" && (
                    <CareerExplorer
                      initialState={familyData.state}
                      initialDistrict={familyData.district}
                      onOpenFamilyRoom={() => setLearnerActiveTab("family_decision_room")}
                      onConsultCounsellor={(tradeId) => {
                        setCounsellingTradeId(tradeId);
                        setLearnerActiveTab("ai_counsellor");
                      }}
                    />
                  )}

                  {/* View 2: AI Counselling */}
                  {learnerActiveTab === "ai_counsellor" && (
                    <CounsellingHub initialTradeId={counsellingTradeId} />
                  )}

                  {/* View 3: Family Decision Room */}
                  {learnerActiveTab === "family_decision_room" && (
                    <FamilyDecisionRoom
                      familyId={familyData.family_id}
                      onExploreTrades={() => setLearnerActiveTab("explorer")}
                      onRequestCounselling={() => setLearnerActiveTab("ai_counsellor")}
                    />
                  )}

                  {/* View 4: Evidence */}
                  {learnerActiveTab === "evidence_hub" && (
                    <EvidenceHub
                      initialState={familyData.state}
                      initialDistrict={familyData.district}
                    />
                  )}
                </div>
              )}

              {/* -------------------------------------------------------- */}
              {/* C. DEDICATED COUNSELLOR WORKSPACE                        */}
              {/* -------------------------------------------------------- */}
              {selectedRole === "COUNSELLOR" && (
                <CounsellorPortal />
              )}

              {/* -------------------------------------------------------- */}
              {/* D. DEDICATED SCHEME ADMINISTRATOR WORKSPACE              */}
              {/* -------------------------------------------------------- */}
              {selectedRole === "ADMIN" && (
                <AdminProgrammeDashboard />
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
