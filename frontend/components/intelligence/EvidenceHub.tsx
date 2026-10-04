"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Search,
  ShieldCheck,
  MapPin,
  Sparkles,
  AlertTriangle,
  HelpCircle,
  ExternalLink,
  Layers,
  Building,
  CheckCircle2,
  RefreshCw
} from "lucide-react";
import { EvidenceCard, EvidenceItem } from "./EvidenceCard";

interface EvidenceHubProps {
  initialState?: string;
  initialDistrict?: string;
}

export const EvidenceHub: React.FC<EvidenceHubProps> = ({
  initialState = "Telangana",
  initialDistrict = "Warangal",
}) => {
  const [query, setQuery] = useState("");
  const [state, setState] = useState(initialState);
  const [district, setDistrict] = useState(initialDistrict);
  const [concernType, setConcernType] = useState<string>("INCOME");
  const [evidenceItems, setEvidenceItems] = useState<EvidenceItem[]>([]);
  const [isAvailable, setIsAvailable] = useState<boolean>(true);
  const [unavailabilityMsg, setUnavailabilityMsg] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const fetchEvidence = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      if (state) params.append("state", state);
      if (district) params.append("district", district);
      if (concernType) params.append("concern_type", concernType);
      if (query.trim()) params.append("query", query.trim());

      const res = await fetch(`/api/v1/evidence/retrieve?${params.toString()}`);
      const data = await res.json();

      if (data.success && data.data) {
        setIsAvailable(data.data.is_available);
        setUnavailabilityMsg(data.data.unavailability_message);
        setEvidenceItems(data.data.items || []);
      } else {
        setIsAvailable(false);
        setUnavailabilityMsg("Verified information for this question is currently unavailable.");
        setEvidenceItems([]);
      }
    } catch (err) {
      console.error("Error retrieving evidence:", err);
      setIsAvailable(false);
      setUnavailabilityMsg("Verified information for this question is currently unavailable.");
      setEvidenceItems([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEvidence();
  }, [state, district, concernType]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchEvidence();
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-teal-950 rounded-3xl p-8 text-white shadow-xl">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-teal-400/20 text-teal-300 border border-teal-400/30 mb-3">
          <ShieldCheck className="w-4 h-4 text-teal-300" />
          Strict Provenance & Anti-Hallucination Verification System
        </div>
        <h2 className="text-2xl sm:text-4xl font-black text-white">
          Verified Evidence & Provenance Registry
        </h2>
        <p className="text-sm sm:text-base text-teal-100/90 mt-2 max-w-3xl leading-relaxed">
          SkillSathi guarantees zero hallucination. Every placement percentage, salary band, and career progression claim is traceable to official MSDE, NCVET, and NAPS datasets.
        </p>

        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="mt-6 flex flex-wrap gap-3">
          <div className="flex-1 min-w-[280px] relative">
            <Search className="w-5 h-5 text-gray-400 absolute left-4 top-3.5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a verification query (e.g. 'Solar PV in Warangal', 'EV placement', 'CNC Machinist salary')..."
              className="w-full pl-12 pr-4 py-3.5 rounded-2xl bg-white text-gray-900 placeholder-gray-400 text-sm font-medium focus:outline-hidden focus:ring-2 focus:ring-teal-400 shadow-md"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="px-6 py-3.5 rounded-2xl bg-teal-500 hover:bg-teal-400 text-teal-950 font-bold text-sm transition-all shadow-md flex items-center gap-2 shrink-0"
          >
            {isLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Search className="w-4 h-4" />}
            Retrieve Evidence
          </button>
        </form>

        {/* Quick Filters */}
        <div className="flex flex-wrap items-center gap-4 mt-6 pt-4 border-t border-white/10 text-xs">
          <div className="flex items-center gap-2">
            <span className="text-teal-300 font-semibold">Location:</span>
            <select
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              className="bg-white/10 text-white rounded-lg px-2.5 py-1 text-xs font-semibold border border-white/20"
            >
              <option value="Warangal" className="text-gray-900">Warangal (Telangana)</option>
              <option value="Hyderabad" className="text-gray-900">Hyderabad (Telangana)</option>
              <option value="Pune" className="text-gray-900">Pune (Maharashtra)</option>
              <option value="Kanchipuram" className="text-gray-900">Kanchipuram (Tamil Nadu)</option>
              <option value="Bengaluru Urban" className="text-gray-900">Bengaluru Urban (Karnataka)</option>
              <option value="Ahmedabad" className="text-gray-900">Ahmedabad (Gujarat)</option>
            </select>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-teal-300 font-semibold">Concern Focus:</span>
            <select
              value={concernType}
              onChange={(e) => setConcernType(e.target.value)}
              className="bg-white/10 text-white rounded-lg px-2.5 py-1 text-xs font-semibold border border-white/20"
            >
              <option value="INCOME" className="text-gray-900">Income & Salary</option>
              <option value="PLACEMENT" className="text-gray-900">Job Security & Placement</option>
              <option value="LOCAL_AVAILABILITY" className="text-gray-900">Local Proximity</option>
              <option value="FURTHER_EDUCATION" className="text-gray-900">Degree Mobility</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-bold text-gray-900">
            Ranked Evidence Claims ({evidenceItems.length})
          </h3>
          <span className="text-xs text-gray-500">
            Ranked by Geographic Proximity, Trade Match & Data Freshness
          </span>
        </div>

        {/* Anti-Hallucination Safe Box if no evidence exists */}
        {!isAvailable || evidenceItems.length === 0 ? (
          <div className="bg-amber-50 rounded-3xl p-8 sm:p-12 text-center border border-amber-200 shadow-xs">
            <AlertTriangle className="w-12 h-12 text-amber-600 mx-auto mb-3" />
            <h4 className="text-xl font-black text-amber-950 mb-2">
              {unavailabilityMsg || "Verified information for this question is currently unavailable."}
            </h4>
            <p className="text-sm text-amber-800 max-w-xl mx-auto leading-relaxed">
              SkillSathi operates under a strict anti-hallucination mandate. When government survey or tracer data has not been officially published for a specific question, we never fabricate or guess statistics.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {evidenceItems.map((item) => (
              <EvidenceCard key={item.id} evidence={item} showScore={true} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
