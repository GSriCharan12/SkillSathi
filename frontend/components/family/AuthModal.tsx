"use client";

import React, { useState } from "react";
import { Dialog } from "@/components/ui/Dialog";
import { Input } from "@/components/ui/Input";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { apiClient } from "@/lib/api-client";
import { translations, Language } from "@/lib/translations";
import { Users, Lock, Mail, User as UserIcon, HeartHandshake } from "lucide-react";

export interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  lang: Language;
  onAuthSuccess: (data: any) => void;
  defaultRole?: "LEARNER" | "PARENT";
}

export const AuthModal: React.FC<AuthModalProps> = ({
  isOpen,
  onClose,
  lang,
  onAuthSuccess,
  defaultRole = "LEARNER",
}) => {
  const t = translations[lang];
  const [mode, setMode] = useState<"login" | "register">("register");
  const [role, setRole] = useState<"LEARNER" | "PARENT">(defaultRole);
  const [fullName, setFullName] = useState("");
  const [emailOrPhone, setEmailOrPhone] = useState("");
  const [password, setPassword] = useState("");
  const [familyCode, setFamilyCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (mode === "register") {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: fullName,
            email: emailOrPhone.includes("@") ? emailOrPhone : undefined,
            phone_number: !emailOrPhone.includes("@") ? emailOrPhone : undefined,
            password,
            role,
            preferred_language: lang,
            family_code: familyCode ? familyCode.trim().toUpperCase() : undefined,
          }),
        });
        const json = await res.json();
        if (!res.ok || !json.success) throw new Error(json.message || "Registration failed.");
        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_token", json.data.access_token);
        }
        onAuthSuccess(json.data);
        onClose();
      } else {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email_or_phone: emailOrPhone,
            password,
          }),
        });
        const json = await res.json();
        if (!res.ok || !json.success) throw new Error(json.message || "Login failed.");
        if (typeof window !== "undefined") {
          localStorage.setItem("skillsathi_token", json.data.access_token);
        }
        onAuthSuccess(json.data);
        onClose();
      }
    } catch (err: any) {
      setError(err.message || "Authentication error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title={mode === "register" ? "Create Family Account" : "Sign In to Family Room"}
      description="Connect learner aspirations with parental security."
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Tab switch */}
        <div className="flex p-1 rounded-xl bg-neutral-100 text-xs font-semibold">
          <button
            type="button"
            onClick={() => setMode("register")}
            className={`flex-1 py-1.5 rounded-lg transition-all ${
              mode === "register" ? "bg-white text-[#14213D] shadow-xs" : "text-neutral-500"
            }`}
          >
            Create Account
          </button>
          <button
            type="button"
            onClick={() => setMode("login")}
            className={`flex-1 py-1.5 rounded-lg transition-all ${
              mode === "login" ? "bg-white text-[#14213D] shadow-xs" : "text-neutral-500"
            }`}
          >
            Sign In
          </button>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-[#FDF0F0] border border-[#F28482]/30 text-xs text-[#D05353]">
            {error}
          </div>
        )}

        {mode === "register" && (
          <>
            {/* Role Switch */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-[#243047]">I am a:</label>
              <div className="grid grid-cols-2 gap-2">
                <button
                  type="button"
                  onClick={() => setRole("LEARNER")}
                  className={`p-2.5 rounded-xl border text-xs font-bold transition-all ${
                    role === "LEARNER"
                      ? "bg-[#E8F5F3] border-[#2A9D8F] text-[#14213D]"
                      : "bg-white border-[#14213D]/8 text-neutral-500"
                  }`}
                >
                  Student / Learner
                </button>
                <button
                  type="button"
                  onClick={() => setRole("PARENT")}
                  className={`p-2.5 rounded-xl border text-xs font-bold transition-all ${
                    role === "PARENT"
                      ? "bg-[#FDF0F0] border-[#F28482] text-[#14213D]"
                      : "bg-white border-[#14213D]/8 text-neutral-500"
                  }`}
                >
                  Parent / Guardian
                </button>
              </div>
            </div>

            <Input
              label="Full Name"
              placeholder="e.g. Aarav Sharma"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              required
              leftIcon={<UserIcon className="w-4 h-4" />}
            />
          </>
        )}

        <Input
          label="Email or Mobile Number"
          placeholder="e.g. aarav@gmail.com or 9876543210"
          value={emailOrPhone}
          onChange={(e) => setEmailOrPhone(e.target.value)}
          required
          leftIcon={<Mail className="w-4 h-4" />}
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          leftIcon={<Lock className="w-4 h-4" />}
        />

        {mode === "register" && (
          <Input
            label="Family Code (Optional)"
            placeholder="e.g. SK-4921 (Leave empty to create new room)"
            value={familyCode}
            onChange={(e) => setFamilyCode(e.target.value)}
            hint="Enter code if a family member already invited you."
            leftIcon={<HeartHandshake className="w-4 h-4" />}
          />
        )}

        <Button
          type="submit"
          variant="primary"
          size="md"
          className="w-full mt-2"
          isLoading={isLoading}
        >
          {mode === "register" ? "Continue to Onboarding" : "Sign In"}
        </Button>
      </form>
    </Dialog>
  );
};
