"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  Filter,
  MapPin,
  Clock,
  GraduationCap,
  TrendingUp,
  ArrowRight,
  ShieldCheck,
  Building,
  Sparkles,
  Layers,
  ChevronRight,
  CheckCircle2,
  AlertCircle,
  X
} from "lucide-react";
import { CareerDetailModal, TradeDetailData } from "./CareerDetailModal";
import { PathwayComparisonMatrix, ComparisonTradeItem } from "./PathwayComparisonMatrix";

interface CareerExplorerProps {
  initialState?: string;
  initialDistrict?: string;
  onOpenFamilyRoom?: () => void;
  onConsultCounsellor?: (tradeId: number) => void;
}

export const CareerExplorer: React.FC<CareerExplorerProps> = ({
  initialState = "Telangana",
  initialDistrict = "Warangal",
  onOpenFamilyRoom,
  onConsultCounsellor,
}) => {
  const [trades, setTrades] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedSector, setSelectedSector] = useState<string>("");
  const [selectedNsqf, setSelectedNsqf] = useState<string>("");
  const [maxDuration, setMaxDuration] = useState<string>("");
  const [state, setState] = useState<string>(initialState);
  const [district, setDistrict] = useState<string>(initialDistrict);
  const [localOnly, setLocalOnly] = useState<boolean>(false);

  // Modal and Comparison State
  const [selectedTradeForModal, setSelectedTradeForModal] = useState<TradeDetailData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [comparedTradeIds, setComparedTradeIds] = useState<number[]>([]);
  const [comparisonPayload, setComparisonPayload] = useState<ComparisonTradeItem[]>([]);
  const [showComparisonView, setShowComparisonView] = useState<boolean>(false);

  const fetchTrades = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams();
      if (searchQuery.trim()) params.append("search", searchQuery.trim());
      if (selectedSector) params.append("sector", selectedSector);
      if (selectedNsqf) params.append("nsqf_level", selectedNsqf);
      if (maxDuration) params.append("duration_months_max", maxDuration);
      if (state) params.append("state", state);
      if (district) params.append("district", district);

      const res = await fetch(`/api/v1/trades?${params.toString()}`);
      const data = await res.json();
      if (data.success && data.data) {
        setTrades(data.data);
      }
    } catch (err) {
      console.error("Error fetching trades:", err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchTrades();
  }, [searchQuery, selectedSector, selectedNsqf, maxDuration, state, district]);

  // Open trade dossier modal
  const handleOpenTradeDetail = async (tradeId: number) => {
    try {
      const res = await fetch(`/api/v1/trades/${tradeId}?state=${state}&district=${district}`);
      const data = await res.json();
      if (data.success && data.data) {
        setSelectedTradeForModal(data.data);
        setIsModalOpen(true);
      }
    } catch (err) {
      console.error("Error fetching trade detail:", err);
    }
  };

  // Toggle trade in comparison list
  const handleToggleCompare = (tradeId: number) => {
    if (comparedTradeIds.includes(tradeId)) {
      setComparedTradeIds(comparedTradeIds.filter((id) => id !== tradeId));
    } else {
      if (comparedTradeIds.length >= 3) {
        alert("You can compare up to 3 vocational pathways side-by-side.");
        return;
      }
      setComparedTradeIds([...comparedTradeIds, tradeId]);
    }
  };

  // Trigger side-by-side comparison fetch
  const handleRunComparison = async () => {
    if (comparedTradeIds.length === 0) return;
    try {
      const res = await fetch(
        `/api/v1/trades/compare?trade_ids=${comparedTradeIds.join(",")}&state=${state}&district=${district}`
      );
      const data = await res.json();
      if (data.success && data.data) {
        setComparisonPayload(data.data.trades);
        setShowComparisonView(true);
      }
    } catch (err) {
      console.error("Error fetching comparison:", err);
    }
  };

  const handleRemoveFromComparison = (tradeId: number) => {
    const updatedIds = comparedTradeIds.filter((id) => id !== tradeId);
    setComparedTradeIds(updatedIds);
    setComparisonPayload(comparisonPayload.filter((t) => t.trade_id !== tradeId));
    if (updatedIds.length === 0) {
      setShowComparisonView(false);
    }
  };

  const filteredTrades = localOnly
    ? trades.filter((t) => t.has_local_availability || t.local_provider_count > 0)
    : trades;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Comparison Matrix View if active */}
      {showComparisonView ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setShowComparisonView(false)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold transition-all"
            >
              ← Back to Career Explorer
            </button>
          </div>

          <PathwayComparisonMatrix
            trades={comparisonPayload}
            onRemoveTrade={handleRemoveFromComparison}
            onSelectTradeDetail={handleOpenTradeDetail}
          />
        </div>
      ) : (
        <>
          {/* Hero Discovery Banner */}
          <div className="bg-gradient-to-r from-teal-900 via-slate-900 to-teal-950 rounded-3xl p-8 sm:p-10 text-white shadow-xl relative overflow-hidden">
            <div className="relative z-10 max-w-3xl">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-teal-400/20 text-teal-300 border border-teal-400/30 mb-3">
                <Sparkles className="w-3.5 h-3.5 text-teal-300" />
                National Qualifications & Placement Intelligence
              </div>

              <h1 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                Vocational Career Intelligence Explorer
              </h1>
              <p className="text-sm sm:text-base text-teal-100/90 mt-3 leading-relaxed">
                Discover government-backed vocational qualifications with verified starting salaries, real employer placement rates, local ITI availability, and lateral university degree bridges.
              </p>
            </div>

            {/* Localized Priority Selector */}
            <div className="relative z-10 mt-8 bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/15 flex flex-wrap items-center justify-between gap-4">
              <div className="flex flex-wrap items-center gap-3 text-xs sm:text-sm">
                <div className="flex items-center gap-2 font-bold text-teal-300">
                  <MapPin className="w-4 h-4 text-teal-400" />
                  <span>Prioritizing For:</span>
                </div>

                <select
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="bg-teal-950 text-white border border-teal-400/40 rounded-xl px-3 py-1.5 font-semibold text-xs focus:ring-2 focus:ring-teal-400"
                >
                  <option value="Telangana">Telangana</option>
                  <option value="Maharashtra">Maharashtra</option>
                  <option value="Tamil Nadu">Tamil Nadu</option>
                  <option value="Karnataka">Karnataka</option>
                  <option value="Gujarat">Gujarat</option>
                </select>

                <select
                  value={district}
                  onChange={(e) => setDistrict(e.target.value)}
                  className="bg-teal-950 text-white border border-teal-400/40 rounded-xl px-3 py-1.5 font-semibold text-xs focus:ring-2 focus:ring-teal-400"
                >
                  {state === "Telangana" && (
                    <>
                      <option value="Warangal">Warangal District</option>
                      <option value="Hyderabad">Hyderabad District</option>
                    </>
                  )}
                  {state === "Maharashtra" && <option value="Pune">Pune District</option>}
                  {state === "Tamil Nadu" && <option value="Kanchipuram">Kanchipuram District</option>}
                  {state === "Karnataka" && <option value="Bengaluru Urban">Bengaluru Urban</option>}
                  {state === "Gujarat" && <option value="Ahmedabad">Ahmedabad District</option>}
                </select>
              </div>

              <div className="text-xs text-teal-200/90 font-medium">
                Prioritizing local training institutes and industrial clusters in <strong>{district}, {state}</strong>.
              </div>
            </div>
          </div>

          {/* Search & Filter Bar */}
          <div className="bg-white rounded-2xl p-5 border border-gray-200/80 shadow-xs space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3">
              {/* Search Bar */}
              <div className="lg:col-span-4 relative">
                <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search trade, sector, QP code, or skills..."
                  className="w-full pl-10 pr-3 py-2.5 rounded-xl bg-gray-50 border border-gray-200 text-xs font-medium focus:bg-white focus:outline-hidden focus:ring-2 focus:ring-teal-500"
                />
              </div>

              {/* Sector Filter */}
              <div className="lg:col-span-3">
                <select
                  value={selectedSector}
                  onChange={(e) => setSelectedSector(e.target.value)}
                  className="w-full py-2.5 px-3 rounded-xl bg-gray-50 border border-gray-200 text-xs font-semibold text-gray-700"
                >
                  <option value="">All Industry Sectors</option>
                  <option value="Green Jobs">Renewable & Green Energy</option>
                  <option value="Automotive">Automotive & Clean Mobility (EV)</option>
                  <option value="Advanced Manufacturing">Precision & Advanced Manufacturing</option>
                  <option value="Healthcare">Healthcare & Biomedical Tech</option>
                  <option value="Telecom">Telecom & 5G IoT Smart Networks</option>
                  <option value="Agriculture">Smart Agriculture & Drone Tech</option>
                </select>
              </div>

              {/* NSQF Level Filter */}
              <div className="lg:col-span-2">
                <select
                  value={selectedNsqf}
                  onChange={(e) => setSelectedNsqf(e.target.value)}
                  className="w-full py-2.5 px-3 rounded-xl bg-gray-50 border border-gray-200 text-xs font-semibold text-gray-700"
                >
                  <option value="">All NSQF Levels</option>
                  <option value="4">NSQF Level 4 (Technician)</option>
                  <option value="5">NSQF Level 5 (Specialist Lead)</option>
                </select>
              </div>

              {/* Duration Filter */}
              <div className="lg:col-span-3">
                <select
                  value={maxDuration}
                  onChange={(e) => setMaxDuration(e.target.value)}
                  className="w-full py-2.5 px-3 rounded-xl bg-gray-50 border border-gray-200 text-xs font-semibold text-gray-700"
                >
                  <option value="">Any Training Duration</option>
                  <option value="6">Up to 6 Months (Fast Track)</option>
                  <option value="12">Up to 12 Months (1 Year ITI)</option>
                  <option value="24">Up to 24 Months (2 Year Advanced)</option>
                </select>
              </div>
            </div>

            {/* Quick Filter Checkbox & Reset */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-gray-100 text-xs">
              <label className="flex items-center gap-2 font-medium text-gray-700 cursor-pointer">
                <input
                  type="checkbox"
                  checked={localOnly}
                  onChange={(e) => setLocalOnly(e.target.checked)}
                  className="w-4 h-4 rounded-sm text-teal-700 focus:ring-teal-500 border-gray-300"
                />
                <span>Show trades with local training institutes in <strong>{district}</strong> only</span>
              </label>

              {(searchQuery || selectedSector || selectedNsqf || maxDuration || localOnly) && (
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSelectedSector("");
                    setSelectedNsqf("");
                    setMaxDuration("");
                    setLocalOnly(false);
                  }}
                  className="text-teal-700 hover:text-teal-900 font-bold transition-colors"
                >
                  Reset All Filters
                </button>
              )}
            </div>
          </div>

          {/* Results Count and Heading */}
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900">
              Vocational Career Pathways ({filteredTrades.length})
            </h2>
            <div className="text-xs text-gray-500 font-medium">
              Zero Generic Jobs • 100% NSQF Verified
            </div>
          </div>

          {/* Grid of Career Cards */}
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <div key={n} className="bg-white rounded-3xl p-6 border border-gray-200 animate-pulse h-80" />
              ))}
            </div>
          ) : filteredTrades.length === 0 ? (
            <div className="bg-white rounded-3xl p-12 text-center border border-gray-200">
              <AlertCircle className="w-10 h-10 text-gray-400 mx-auto mb-2" />
              <h3 className="text-base font-bold text-gray-800">No vocational trades match your filters</h3>
              <p className="text-xs text-gray-500 mt-1">Try resetting the filters or broadening your search parameters.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredTrades.map((t) => {
                const isCompared = comparedTradeIds.includes(t.id);

                return (
                  <motion.div
                    key={t.id}
                    whileHover={{ y: -4 }}
                    className="bg-white rounded-3xl border border-gray-200/90 p-6 shadow-xs hover:shadow-xl transition-all duration-300 flex flex-col justify-between group"
                  >
                    <div>
                      {/* Card Badges */}
                      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <div className="flex items-center gap-1.5">
                          <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-50 text-teal-800 border border-teal-200">
                            NSQF L{t.nsqf_level}
                          </span>
                          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-gray-100 text-gray-600">
                            {t.duration_months} Mo
                          </span>
                          {t.is_demo ? (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">
                              DEMO DATA
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                              NCVET VERIFIED
                            </span>
                          )}
                        </div>

                        {t.local_provider_count > 0 && (
                          <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                            <MapPin className="w-3 h-3 text-emerald-600" />
                            {t.local_provider_count} Nearby
                          </span>
                        )}
                      </div>

                      {/* Trade Title & Sector */}
                      <h3 className="text-lg font-black text-gray-900 leading-snug group-hover:text-teal-700 transition-colors mb-1">
                        {t.title}
                      </h3>
                      <div className="text-xs font-semibold text-gray-500 mb-3">
                        {t.sector} • <span className="text-gray-400">QP: {t.code}</span>
                      </div>

                      <p className="text-xs text-gray-600 line-clamp-2 mb-4 leading-relaxed">
                        {t.description}
                      </p>

                      {/* Key Verified Stats Box */}
                      <div className="bg-[#FFFDF7] rounded-2xl p-3.5 border border-amber-200/70 grid grid-cols-2 gap-2 mb-4">
                        <div>
                          <div className="text-[11px] text-gray-500 font-medium">Placement Rate</div>
                          <div className="text-base font-extrabold text-emerald-700">
                            {t.verified_placement_rate ? `${t.verified_placement_rate}%` : "Verified data pending"}
                          </div>
                        </div>

                        <div>
                          <div className="text-[11px] text-gray-500 font-medium">Starting Wage</div>
                          <div className="text-base font-extrabold text-gray-900">
                            {t.median_starting_monthly_inr ? `₹${t.median_starting_monthly_inr.toLocaleString()}/mo` : "Benchmark"}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="space-y-2 pt-3 border-t border-gray-100">
                      <button
                        onClick={() => handleOpenTradeDetail(t.id)}
                        className="w-full py-2.5 px-4 rounded-xl bg-teal-900 hover:bg-teal-800 text-white font-bold text-xs transition-colors flex items-center justify-center gap-2 shadow-xs"
                      >
                        <span>View Full Trade Dossier</span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </button>

                      <button
                        onClick={() => handleToggleCompare(t.id)}
                        className={`w-full py-2 px-3 rounded-xl font-bold text-xs transition-all border ${
                          isCompared
                            ? "bg-amber-100 text-amber-900 border-amber-300"
                            : "bg-gray-50 hover:bg-gray-100 text-gray-700 border-gray-200"
                        }`}
                      >
                        {isCompared ? "✓ Selected for Comparison" : "+ Add to Pathway Comparison"}
                      </button>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          )}

          {/* Floating Comparison Bottom Drawer */}
          <AnimatePresence>
            {comparedTradeIds.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 50 }}
                className="fixed bottom-6 left-1/2 -translate-x-1/2 z-40 bg-slate-900 text-white rounded-2xl p-4 shadow-2xl border border-white/20 flex flex-wrap items-center gap-4 max-w-2xl w-[90%]"
              >
                <div className="flex-1">
                  <div className="text-xs font-bold text-teal-300">
                    Pathway Comparison ({comparedTradeIds.length} of 3 selected)
                  </div>
                  <div className="text-[11px] text-gray-300">
                    Evaluate starting wages, duration, and degree mobility side-by-side.
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => setComparedTradeIds([])}
                    className="p-2 text-gray-400 hover:text-white text-xs"
                  >
                    Clear
                  </button>

                  <button
                    onClick={handleRunComparison}
                    className="px-5 py-2.5 rounded-xl bg-teal-400 hover:bg-teal-300 text-teal-950 font-black text-xs transition-all shadow-md flex items-center gap-1.5"
                  >
                    <span>Compare Pathways</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}

      {/* Trade Detail Modal Popup */}
      <CareerDetailModal
        trade={selectedTradeForModal}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAddToCompare={(t) => handleToggleCompare(t.id)}
        isComparing={selectedTradeForModal ? comparedTradeIds.includes(selectedTradeForModal.id) : false}
        onConsultCounsellor={onConsultCounsellor}
      />
    </div>
  );
};
