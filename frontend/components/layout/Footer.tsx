import React from "react";
import { HeartHandshake, ShieldCheck, Database, Award, ExternalLink } from "lucide-react";
import { Badge } from "../ui/Badge";

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-[#14213D]/10 bg-white/70 backdrop-blur-md mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Col */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[#14213D] to-[#2A9D8F] flex items-center justify-center text-white">
                <HeartHandshake className="w-5 h-5 text-[#FFFDF7]" />
              </div>
              <span className="text-lg font-bold text-[#14213D]">SkillSathi</span>
            </div>
            <p className="text-sm text-[#64748B] max-w-md leading-relaxed">
              "Explore a future your whole family believes in."<br />
              An AI-enabled family decision-support and vocational career counselling platform connecting aspirations with verified government tracer data.
            </p>
            <div className="flex flex-wrap gap-2 pt-1">
              <Badge variant="emerald" size="sm">MSDE / NSDC Ground Truth</Badge>
              <Badge variant="teal" size="sm">Family-Centric Unit</Badge>
              <Badge variant="golden" size="sm">Regional Language Ready</Badge>
            </div>
          </div>

          {/* Pillars */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#14213D] mb-3">
              Core Ecosystem
            </h4>
            <ul className="space-y-2 text-xs font-medium text-[#64748B]">
              <li><a href="#family-room" className="hover:text-[#14213D] transition-colors">Family Decision Room</a></li>
              <li><a href="#pathways" className="hover:text-[#14213D] transition-colors">Vocational Pathways (NSQF)</a></li>
              <li><a href="#evidence" className="hover:text-[#14213D] transition-colors">Verified Outcome Tracer</a></li>
              <li><a href="#ai-counsellor" className="hover:text-[#14213D] transition-colors">AI Family Facilitator</a></li>
              <li><a href="#human-escalation" className="hover:text-[#14213D] transition-colors">Human Counsellor Desk</a></li>
            </ul>
          </div>

          {/* Standards & Compliance */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-[#14213D] mb-3">
              Government Alignment
            </h4>
            <ul className="space-y-2 text-xs font-medium text-[#64748B]">
              <li>National Skills Qualification Framework (NSQF)</li>
              <li>National Apprenticeship Promotion Scheme (NAPS)</li>
              <li>State Skill Development Missions (SSDM)</li>
              <li>B.Voc & Lateral Polytechnic Verticals</li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-neutral-200/60 flex flex-col sm:flex-row items-center justify-between text-xs text-[#64748B] gap-4">
          <p>© 2026 SkillSathi. All rights reserved. National Vocational Guidance Platform.</p>
          <div className="flex items-center gap-4">
            <span className="inline-flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-[#52B788]" /> Verified Government Data Link
            </span>
            <span className="font-mono">v0.1.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
