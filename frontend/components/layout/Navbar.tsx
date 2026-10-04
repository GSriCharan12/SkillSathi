"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import {
  HeartHandshake,
  Users,
  Compass,
  ShieldCheck,
  Sparkles,
  Menu,
  X,
  Languages,
  LogOut,
  User as UserIcon,
} from "lucide-react";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";
import { HealthIndicator } from "../feedback/HealthIndicator";
import { translations, Language } from "@/lib/translations";

export interface NavbarProps {
  currentLang?: Language;
  onLanguageChange?: (lang: Language) => void;
  onOpenAuth?: (role: "LEARNER" | "PARENT") => void;
  currentUser?: any;
  onLogout?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentLang = "en",
  onLanguageChange,
  onOpenAuth,
  currentUser: propUser,
  onLogout: propLogout,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [lang, setLang] = useState<Language>(currentLang);
  const [localUser, setLocalUser] = useState<any>(null);
  const t = translations[lang];

  useEffect(() => {
    if (typeof window !== "undefined") {
      const stored = localStorage.getItem("skillsathi_user");
      const familyCode = localStorage.getItem("skillsathi_family_code");
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          setLocalUser({ ...parsed, family_code: familyCode || parsed.family_code });
        } catch {
          // ignore
        }
      }
    }
  }, []);

  const currentUser = propUser || localUser;

  const handleLogout = () => {
    if (propLogout) {
      propLogout();
    } else {
      if (typeof window !== "undefined") {
        localStorage.removeItem("skillsathi_token");
        localStorage.removeItem("skillsathi_user");
        localStorage.removeItem("skillsathi_family_code");
      }
      setLocalUser(null);
      window.location.href = "/";
    }
  };

  const handleLangToggle = () => {
    const nextLang: Language = lang === "en" ? "te" : "en";
    setLang(nextLang);
    if (onLanguageChange) onLanguageChange(nextLang);
  };

  const navLinks = [
    { label: t.familyRoom, href: "#family-snapshot", icon: <Users className="w-4 h-4 text-[#2A9D8F]" /> },
    { label: t.pathways, href: "#pathways", icon: <Compass className="w-4 h-4 text-[#52B788]" /> },
    { label: t.evidence, href: "#evidence", icon: <ShieldCheck className="w-4 h-4 text-[#F6C85F]" /> },
    { label: t.aiCounsellor, href: "#ai-counsellor", icon: <Sparkles className="w-4 h-4 text-[#F28482]" /> },
  ];


  return (
    <header className="sticky top-0 z-40 w-full glass-nav transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Logo & Brand Identity */}
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-[#14213D] to-[#2A9D8F] flex items-center justify-center text-white shadow-md group-hover:scale-105 transition-transform">
                <HeartHandshake className="w-6 h-6 text-[#FFFDF7]" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xl font-bold tracking-tight text-[#14213D]">
                    {t.brandName}
                  </span>
                  <Badge variant="teal" size="sm">National Platform</Badge>
                </div>
                <p className="text-[11px] text-[#64748B] hidden sm:block font-medium">
                  {t.tagline}
                </p>
              </div>
            </Link>
          </div>

          {/* Center Space / Brand Subtitle */}
          <div className="hidden md:flex items-center">
            {/* Center can remain clean for focused navigation */}
          </div>

          {/* Right Actions: Health Indicator & Sign In / Sign Up Buttons */}
          <div className="hidden md:flex items-center gap-3">
            {/* Live Backend Connection Indicator */}
            <HealthIndicator />

            {/* Profile State if Authenticated */}
            {currentUser ? (
              <div className="flex items-center gap-2">
                <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white border border-[#14213D]/8 text-xs font-semibold text-[#14213D]">
                  <UserIcon className="w-3.5 h-3.5 text-[#2A9D8F]" />
                  <span>{currentUser.user?.full_name || currentUser.full_name || "Family Member"}</span>
                  <Badge variant="teal" size="sm">
                    {currentUser.user?.role || currentUser.role || "USER"}
                  </Badge>
                  {currentUser.family_code && (
                    <Badge variant="emerald" size="sm">{currentUser.family_code}</Badge>
                  )}
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-xl text-neutral-400 hover:text-[#F28482] hover:bg-[#FDF0F0] transition-colors cursor-pointer"
                  title="Sign Out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  href="/signin"
                  className="inline-flex items-center justify-center px-4 py-2 rounded-xl text-xs font-bold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 shadow-2xs hover:shadow-xs transition-all"
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="inline-flex items-center justify-center px-4 py-2 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-teal-700 to-emerald-600 hover:from-teal-800 hover:to-emerald-700 shadow-xs hover:shadow-md transition-all"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu toggle */}
          <div className="flex items-center gap-2 lg:hidden">
            <Link
              href="/signin"
              className="px-2.5 py-1 rounded-lg border border-neutral-200 text-xs font-bold text-gray-700"
            >
              Sign In
            </Link>
            <Link
              href="/signup"
              className="px-2.5 py-1 rounded-lg bg-teal-700 text-white text-xs font-bold"
            >
              Sign Up
            </Link>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl text-[#14213D] hover:bg-[#14213D]/5 transition-colors"
              aria-label="Toggle Navigation"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-b border-[#14213D]/10 bg-white/95 backdrop-blur-md px-4 pt-2 pb-6 space-y-3">
          <div className="space-y-1">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold text-[#243047] hover:bg-[#14213D]/5"
              >
                {link.icon}
                <span>{link.label}</span>
              </a>
            ))}
          </div>
          <div className="pt-3 border-t border-neutral-100 flex flex-col gap-2">
            <Button
              variant="primary"
              size="md"
              className="w-full"
              onClick={() => {
                setMobileMenuOpen(false);
                if (onOpenAuth) onOpenAuth("LEARNER");
              }}
            >
              Enter Family Decision Room
            </Button>
          </div>
        </div>
      )}
    </header>
  );
};
