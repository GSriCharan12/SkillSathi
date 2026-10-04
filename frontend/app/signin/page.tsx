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
  ArrowRight,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  ChevronLeft,
} from "lucide-react";
import { apiClient } from "@/lib/api-client";
import { Badge } from "@/components/ui/Badge";

type UserRole = "LEARNER" | "PARENT" | "COUNSELLOR" | "ADMIN";

interface RoleOption {
  id: UserRole;
  title: string;
  subtitle: string;
  icon: React.ReactNode;
  defaultEmail: string;
  color: string;
}

const ROLES: RoleOption[] = [
  {
    id: "PARENT",
    title: "Parent / Guardian",
    subtitle: "Family Decision Room & Security Radar",
    icon: <Users className="w-5 h-5 text-teal-700" />,
    defaultEmail: "parent.sharma@skillsathi.in",
    color: "border-teal-500 bg-teal-50/50 text-teal-900",
  },
  {
    id: "LEARNER",
    title: "Student / Learner",
    subtitle: "NSQF Career Explorer & AI Career Saathi",
    icon: <GraduationCap className="w-5 h-5 text-emerald-700" />,
    defaultEmail: "aarav.sharma@skillsathi.in",
    color: "border-emerald-500 bg-emerald-50/50 text-emerald-900",
  },
  {
    id: "COUNSELLOR",
    title: "Certified Counsellor",
    subtitle: "Escalated Cases & Guided Interventions",
    icon: <Briefcase className="w-5 h-5 text-amber-700" />,
    defaultEmail: "counsellor.rao@skillsathi.in",
    color: "border-amber-500 bg-amber-50/50 text-amber-900",
  },
  {
    id: "ADMIN",
    title: "Scheme Administrator",
    subtitle: "Macro Resistance Telemetry & Data Sync",
    icon: <Building className="w-5 h-5 text-slate-700" />,
    defaultEmail: "admin.directorate@skillsathi.in",
    color: "border-slate-500 bg-slate-50/50 text-slate-900",
  },
];

export default function SignInPage() {
  const router = useRouter();
  const [selectedRole, setSelectedRole] = useState<UserRole>("PARENT");
  const [emailOrPhone, setEmailOrPhone] = useState("parent.sharma@skillsathi.in");
  const [password, setPassword] = useState("SecurePass123!");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleRoleSelect = (role: UserRole) => {
    if (!role) return;
    setSelectedRole(role);
    const roleConfig = ROLES.find((r) => r.id === role);
    if (roleConfig) {
      setEmailOrPhone(roleConfig.defaultEmail);
      setPassword("SecurePass123!");
    }
  };

  const handleQuickDemoLogin = async (role: UserRole) => {
    if (!role) return;
    setSelectedRole(role);
    const roleConfig = ROLES.find((r) => r.id === role);
    if (!roleConfig) return;

    const targetEmail = roleConfig.defaultEmail;
    const targetPassword = "SecurePass123!";
    setEmailOrPhone(targetEmail);
    setPassword(targetPassword);
    setErrorMsg(null);
    setSuccessMsg(null);
    setIsLoading(true);

    try {
      const res = await apiClient.login({
        email_or_phone: targetEmail,
        password: targetPassword,
        role: role,
      });

      if (res.success && res.data) {
        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_token", res.data.access_token);
          localStorage.setItem("skillsathi_user", JSON.stringify(res.data.user));
          if (res.data.family_code) {
            localStorage.setItem("skillsathi_family_code", res.data.family_code);
          }
        }
        setSuccessMsg(`Welcome, ${res.data.user.full_name}! Launching ${roleConfig.title} Workspace...`);
        setTimeout(() => {
          window.location.href = `/?role=${role}&authenticated=true`;
        }, 500);
      } else {
        // Fallback for immediate demo access
        const mockUser = {
          full_name:
            role === "PARENT"
              ? "Ramesh Sharma"
              : role === "LEARNER"
              ? "Aarav Sharma"
              : role === "COUNSELLOR"
              ? "Dr. S. Rao"
              : "Directorate Admin",
          role: role,
          email: targetEmail,
        };
        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_user", JSON.stringify(mockUser));
          localStorage.setItem("skillsathi_token", "demo-token-" + Date.now());
          if (role === "PARENT" || role === "LEARNER") {
            localStorage.setItem("skillsathi_family_code", "SK-9482");
          }
        }
        setSuccessMsg(`Entering ${roleConfig.title} Workspace...`);
        setTimeout(() => {
          window.location.href = `/?role=${role}&authenticated=true`;
        }, 500);
      }
    } catch (err: any) {
      const mockUser = {
        full_name:
          role === "PARENT"
            ? "Ramesh Sharma"
            : role === "LEARNER"
            ? "Aarav Sharma"
            : role === "COUNSELLOR"
            ? "Dr. S. Rao"
            : "Directorate Admin",
        role: role,
        email: targetEmail,
      };
      if (typeof window !== "undefined") {
        localStorage.setItem("skillsathi_user", JSON.stringify(mockUser));
        localStorage.setItem("skillsathi_token", "demo-token-" + Date.now());
        if (role === "PARENT" || role === "LEARNER") {
          localStorage.setItem("skillsathi_family_code", "SK-9482");
        }
      }
      setSuccessMsg(`Entering ${roleConfig.title} Workspace...`);
      setTimeout(() => {
        window.location.href = `/?role=${role}&authenticated=true`;
      }, 500);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessMsg(null);

    if (!emailOrPhone.trim()) {
      setErrorMsg("Please enter your registered email address or mobile number.");
      return;
    }
    if (!password) {
      setErrorMsg("Please enter your password.");
      return;
    }

    setIsLoading(true);
    try {
      const res = await apiClient.login({
        email_or_phone: emailOrPhone.trim(),
        password: password,
        role: selectedRole,
      });

      if (res.success && res.data) {
        const userRole = (res.data.user.role || selectedRole).toUpperCase();
        
        // Strict Role Match Check
        const isCompatible =
          userRole === selectedRole ||
          (userRole in { PARENT: 1, GUARDIAN: 1 } && selectedRole in { PARENT: 1, GUARDIAN: 1 });

        if (!isCompatible) {
          setErrorMsg(
            `Access Denied: Your account is registered with the role '${userRole}'. You cannot log in through the '${selectedRole}' portal.`
          );
          setIsLoading(false);
          return;
        }

        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_token", res.data.access_token);
          localStorage.setItem("skillsathi_user", JSON.stringify(res.data.user));
          if (res.data.family_code) {
            localStorage.setItem("skillsathi_family_code", res.data.family_code);
          }
        }
        setSuccessMsg(`Welcome, ${res.data.user.full_name}! Launching your ${selectedRole} Portal...`);
        setTimeout(() => {
          window.location.href = `/?role=${userRole}&authenticated=true`;
        }, 500);
      } else {
        setErrorMsg(res.message || "Invalid credentials or unauthorized role access.");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to authenticate. Please check your credentials and portal role.");
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <div className="min-h-screen py-10 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto flex flex-col justify-center">
      {/* Top back navigation */}
      <div className="mb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-2 text-xs font-bold text-gray-600 hover:text-teal-800 transition-colors"
        >
          <ChevronLeft className="w-4 h-4" />
          <span>Back to Home</span>
        </Link>
      </div>

      {/* Main Card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white/95 backdrop-blur-xl rounded-3xl border border-gray-200/80 shadow-xl overflow-hidden"
      >
        {/* Card Header */}
        <div className="bg-gradient-to-r from-[#14213D] to-[#1d3557] px-8 py-8 text-white text-center sm:text-left flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-teal-500/20 border border-teal-400/30 flex items-center justify-center text-teal-300">
              <HeartHandshake className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-black tracking-tight text-white">
                  Sign In to SkillSathi
                </h1>
                <Badge variant="teal" size="sm">Secure Access</Badge>
              </div>
              <p className="text-xs text-gray-300 mt-0.5">
                Role-based access with verified government career intelligence & family collaboration.
              </p>
            </div>
          </div>
          <Link
            href="/signup"
            className="text-xs font-bold text-teal-300 hover:text-teal-200 underline underline-offset-4"
          >
            Need an account? Sign Up →
          </Link>
        </div>

        <div className="p-6 sm:p-8 space-y-6">
          {/* 1. Role Selector */}
          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-gray-700 mb-2.5">
              1. Select Your Role to Sign In
            </label>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {ROLES.map((r) => {
                const isSelected = selectedRole === r.id;
                return (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => handleRoleSelect(r.id)}
                    className={`p-3.5 rounded-2xl text-left border-2 transition-all flex flex-col justify-between ${
                      isSelected
                        ? `${r.color} shadow-sm scale-[1.02]`
                        : "border-gray-200 hover:border-gray-300 bg-gray-50/50 hover:bg-gray-50 text-gray-700"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="p-1.5 rounded-xl bg-white shadow-2xs">
                        {r.icon}
                      </div>
                      {isSelected && (
                        <CheckCircle2 className="w-4 h-4 text-teal-700" />
                      )}
                    </div>
                    <div>
                      <div className="text-xs font-black">{r.title}</div>
                      <div className="text-[10px] text-gray-500 line-clamp-1 mt-0.5">
                        {r.subtitle}
                      </div>
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

          {/* 2. Login Form */}
          <form onSubmit={handleSignIn} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-gray-700 mb-1.5">
                Email Address or Registered Mobile Number
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                  <Mail className="w-4 h-4" />
                </div>
                <input
                  type="text"
                  value={emailOrPhone}
                  onChange={(e) => setEmailOrPhone(e.target.value)}
                  placeholder="e.g. parent.sharma@skillsathi.in or 9876543210"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent font-medium"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1.5">
                <label className="block text-xs font-bold text-gray-700">
                  Password
                </label>
                <span className="text-[11px] text-gray-400 font-medium">
                  Default: <code className="bg-gray-100 px-1 py-0.5 rounded text-gray-600">SecurePass123!</code>
                </span>
              </div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
                  <KeyRound className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent font-medium"
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 px-4 rounded-xl text-sm font-bold text-white bg-gradient-to-r from-teal-700 to-emerald-600 hover:from-teal-800 hover:to-emerald-700 shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60"
            >
              {isLoading ? (
                <span>Signing in...</span>
              ) : (
                <>
                  <span>Sign In as {ROLES.find((r) => r.id === selectedRole)?.title}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo 1-Click Login Bar */}
          <div className="pt-4 border-t border-gray-100">
            <div className="flex items-center justify-between mb-2.5">
              <span className="text-[11px] font-black uppercase tracking-wider text-teal-800">
                ⚡ 1-Click Quick Demo Login (Instant Dashboard Entry)
              </span>
              <Sparkles className="w-4 h-4 text-amber-500" />
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {ROLES.map((r) => (
                <button
                  key={r.id}
                  type="button"
                  disabled={isLoading}
                  onClick={() => handleQuickDemoLogin(r.id)}
                  className="px-3 py-2.5 rounded-xl border border-teal-200/80 bg-teal-50/70 hover:bg-teal-100/80 text-xs font-bold text-teal-900 transition-all text-center flex flex-col items-center justify-center gap-0.5 shadow-2xs hover:shadow-xs cursor-pointer disabled:opacity-50"
                  title={`1-Click Login as ${r.title}`}
                >
                  <span className="font-extrabold">{r.title.split("/")[0].trim()}</span>
                  <span className="text-[10px] text-teal-700 font-semibold opacity-90">Login →</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Card Footer */}
        <div className="bg-gray-50/80 px-8 py-4 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-gray-500">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-teal-700" />
            <span>End-to-End Encrypted Session & Data Privacy</span>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/signup" className="font-bold text-teal-700 hover:underline">
              Create New Account
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
