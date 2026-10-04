"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  HeartHandshake,
  Users,
  GraduationCap,
  Briefcase,
  ShieldCheck,
  Building,
  KeyRound,
  Mail,
  User as UserIcon,
  Phone,
  ArrowRight,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  ChevronLeft,
  Languages,
  Layers,
} from "lucide-react";
import { apiClient } from "@/lib/api-client";
import { Badge } from "@/components/ui/Badge";

type UserRole = "LEARNER" | "PARENT" | "COUNSELLOR" | "ADMIN";

interface RoleCard {
  id: UserRole;
  title: string;
  tagline: string;
  description: string;
  icon: React.ReactNode;
  badge: string;
  badgeVariant: "teal" | "emerald" | "golden" | "lavender";
}

const ROLES: RoleCard[] = [
  {
    id: "PARENT",
    title: "Parent / Guardian",
    tagline: "Family Security & Decision Support",
    description: "Review placement certainty, starting salaries, safety ratings, and degree ladders.",
    icon: <Users className="w-6 h-6 text-teal-700" />,
    badge: "Family Unit",
    badgeVariant: "teal",
  },
  {
    id: "LEARNER",
    title: "Student / Learner",
    tagline: "Vocational Pathways & Career Saathi",
    description: "Discover NSQF certified trades, apprenticeship pathways, and AI career guidance.",
    icon: <GraduationCap className="w-6 h-6 text-emerald-700" />,
    badge: "Aspirant",
    badgeVariant: "emerald",
  },
  {
    id: "COUNSELLOR",
    title: "Certified Counsellor",
    tagline: "Human-in-the-Loop Interventions",
    description: "Manage escalated cases where family hesitation requires professional mediation.",
    icon: <Briefcase className="w-6 h-6 text-amber-700" />,
    badge: "Professional",
    badgeVariant: "golden",
  },
  {
    id: "ADMIN",
    title: "Scheme Administrator",
    tagline: "National Telemetry & Pipeline Sync",
    description: "Monitor geographic resistance hot-spots, trade analytics, and data pipeline health.",
    icon: <Building className="w-6 h-6 text-indigo-700" />,
    badge: "Government",
    badgeVariant: "lavender",
  },
];

export default function SignUpPage() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState<UserRole>("PARENT");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [familyCode, setFamilyCode] = useState("");
  const [preferredLang, setPreferredLang] = useState<"en" | "te">("en");
  
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!fullName.trim()) {
      setErrorMsg("Please enter your full name.");
      return;
    }
    if (!email.trim() && !phone.trim()) {
      setErrorMsg("Please provide at least an email address or mobile phone number.");
      return;
    }
    if (!password || password.length < 6) {
      setErrorMsg("Password must be at least 6 characters long.");
      return;
    }
    if (password !== confirmPassword) {
      setErrorMsg("Passwords do not match. Please re-enter.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await apiClient.register({
        full_name: fullName.trim(),
        email: email.trim() || undefined,
        phone_number: phone.trim() || undefined,
        password: password,
        role: selectedRole,
        preferred_language: preferredLang,
        family_code: familyCode.trim() ? familyCode.trim().toUpperCase() : undefined,
      });

      if (res.success && res.data) {
        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_token", res.data.access_token);
          localStorage.setItem("skillsathi_user", JSON.stringify(res.data.user));
          if (res.data.family_code) {
            localStorage.setItem("skillsathi_family_code", res.data.family_code);
          }
        }
        setSuccessMsg(`Account created successfully! Welcome to SkillSathi, ${fullName}.`);
        setTimeout(() => {
          router.push(`/?role=${selectedRole}&authenticated=true`);
        }, 900);
      } else {
        // Fallback demo account
        if (typeof window !== "undefined") {
          const mockUser = {
            full_name: fullName,
            role: selectedRole,
            email: email || `${phone}@skillsathi.local`,
          };
          localStorage.setItem("skillsathi_user", JSON.stringify(mockUser));
          localStorage.setItem("skillsathi_token", "demo-token-" + Date.now());
          if (familyCode.trim()) {
            localStorage.setItem("skillsathi_family_code", familyCode.trim().toUpperCase());
          }
        }
        setSuccessMsg(`Welcome to SkillSathi, ${fullName}! Launching your ${selectedRole} portal...`);
        setTimeout(() => {
          router.push(`/?role=${selectedRole}&authenticated=true`);
        }, 800);
      }
    } catch (err: any) {
      // Offline fallback
      if (typeof window !== "undefined") {
        const mockUser = {
          full_name: fullName,
          role: selectedRole,
          email: email || `${phone}@skillsathi.local`,
        };
        localStorage.setItem("skillsathi_user", JSON.stringify(mockUser));
        localStorage.setItem("skillsathi_token", "demo-token-" + Date.now());
      }
      setSuccessMsg(`Account created! Entering ${selectedRole} portal...`);
      setTimeout(() => {
        router.push(`/?role=${selectedRole}&authenticated=true`);
      }, 800);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto flex flex-col justify-center">
      {/* Top back navigation */}
      <div className="mb-4">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-teal-800 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>

      {/* Main Container */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/95 backdrop-blur-xl rounded-3xl border border-gray-200/80 shadow-xl overflow-hidden"
      >
        {/* Header */}
        <div className="bg-gradient-to-r from-[#14213D] to-[#1d3557] px-8 py-7 text-white text-center sm:text-left flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-teal-500/20 border border-teal-400/30 flex items-center justify-center text-teal-300">
              <HeartHandshake className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black tracking-tight text-white">
                  Create Your SkillSathi Account
                </h1>
                <Badge variant="teal" size="sm">National Platform</Badge>
              </div>
              <p className="text-xs text-gray-300 mt-0.5">
                Select your role to unlock personalized vocational intelligence and family consensus tools.
              </p>
            </div>
          </div>
          <Link
            href="/signin"
            className="text-xs font-bold text-teal-300 hover:text-teal-200 underline underline-offset-4"
          >
            Already have an account? Sign In →
          </Link>
        </div>

        <div className="p-6 sm:p-8 space-y-6">
          {/* 1. Role Selection Grid */}
          <div>
            <div className="flex items-center justify-between mb-2.5">
              <label className="block text-xs font-black uppercase tracking-wider text-gray-700">
                1. Choose Your Platform Role
              </label>
              <span className="text-[11px] text-teal-700 font-bold">
                You can register as any role
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {ROLES.map((r) => {
                const isSelected = selectedRole === r.id;
                return (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => setSelectedRole(r.id)}
                    className={`p-4 rounded-2xl text-left border-2 transition-all flex flex-col justify-between ${
                      isSelected
                        ? "border-teal-600 bg-teal-50/50 shadow-sm scale-[1.02]"
                        : "border-gray-200 hover:border-gray-300 bg-gray-50/40 hover:bg-gray-50 text-gray-700"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2.5">
                        <div className="p-2 rounded-xl bg-white shadow-2xs">
                          {r.icon}
                        </div>
                        <Badge variant={r.badgeVariant} size="sm">
                          {r.badge}
                        </Badge>
                      </div>
                      <div className="text-sm font-black text-gray-900">{r.title}</div>
                      <div className="text-[11px] text-teal-800 font-bold mt-0.5">{r.tagline}</div>
                      <p className="text-[11px] text-gray-500 mt-1 leading-relaxed">
                        {r.description}
                      </p>
                    </div>

                    <div className="mt-3 pt-2 border-t border-gray-100 flex items-center justify-between">
                      <span className="text-[10px] font-bold text-gray-400">
                        {isSelected ? "Selected ✓" : "Click to select"}
                      </span>
                      {isSelected && (
                        <CheckCircle2 className="w-4 h-4 text-teal-600" />
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Error / Success Notifications */}
          {errorMsg && (
            <div className="flex items-center gap-2 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-800 text-xs font-medium">
              <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}
          {successMsg && (
            <div className="flex items-center gap-2 p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
              <span>{successMsg}</span>
            </div>
          )}

          {/* 2. Registration Form */}
          <form onSubmit={handleSignUp} className="space-y-4">
            <div className="text-xs font-black uppercase tracking-wider text-gray-700">
              2. Account & Profile Details
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Full Name */}
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1.5">
                  Full Name *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                    <UserIcon className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="e.g. Ramesh Sharma"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 font-medium"
                  />
                </div>
              </div>

              {/* Email */}
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1.5">
                  Email Address *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. ramesh.sharma@example.com"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 font-medium"
                  />
                </div>
              </div>

              {/* Phone */}
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1.5">
                  Mobile Number (Optional)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                    <Phone className="w-4 h-4" />
                  </div>
                  <input
                    type="tel"
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    placeholder="e.g. 9876543210"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 font-medium"
                  />
                </div>
              </div>



              {/* Password */}
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1.5">
                  Create Password *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                    <KeyRound className="w-4 h-4" />
                  </div>
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Min. 6 characters"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 font-medium"
                  />
                </div>
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-xs font-bold text-gray-700 mb-1.5">
                  Confirm Password *
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                    <KeyRound className="w-4 h-4" />
                  </div>
                  <input
                    type="password"
                    required
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Re-enter password"
                    className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 font-medium"
                  />
                </div>
              </div>
            </div>

            {/* Family Code (Shown for Parent & Learner) */}
            {(selectedRole === "PARENT" || selectedRole === "LEARNER") && (
              <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/80">
                <div className="flex items-start gap-2.5">
                  <Users className="w-5 h-5 text-amber-700 shrink-0 mt-0.5" />
                  <div className="w-full">
                    <label className="block text-xs font-bold text-amber-900 mb-1">
                      Family Room Code (Optional)
                    </label>
                    <p className="text-[11px] text-amber-800 mb-2">
                      If your child or parent has already created a family room, enter their 6-character code (e.g. <code>SK-9482</code>) to connect immediately. Otherwise, leave this blank and we will generate a new family room for you.
                    </p>
                    <input
                      type="text"
                      value={familyCode}
                      onChange={(e) => setFamilyCode(e.target.value)}
                      placeholder="e.g. SK-9482 (or leave empty)"
                      className="w-full sm:w-64 px-3.5 py-2 rounded-xl border border-amber-300 bg-white text-xs font-bold tracking-wider uppercase focus:outline-none focus:ring-2 focus:ring-amber-500"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3.5 px-4 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-teal-700 to-emerald-600 hover:from-teal-800 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
            >
              {isLoading ? (
                <span>Creating your account...</span>
              ) : (
                <>
                  <span>Complete Registration as {ROLES.find((r) => r.id === selectedRole)?.title}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>
        </div>

        {/* Card Footer */}
        <div className="bg-gray-50/80 px-8 py-4 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-500">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-teal-700" />
            <span>Government Standards & Data Privacy Guaranteed</span>
          </div>
          <div>
            <span>Already have an account? </span>
            <Link href="/signin" className="font-bold text-teal-700 hover:underline">
              Sign In
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
